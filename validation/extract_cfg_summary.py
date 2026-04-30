#!/usr/bin/env python3
"""
extract_cfg_summary.py
Converts Cobol-REKT cfg-{PROG}.cbl.json -> validation/structure/{PROG}_cfg.json

Usage:
    py validation/extract_cfg_summary.py CBACT04C
    py validation/extract_cfg_summary.py --all
"""

import json
import hashlib
import re
import sys
from pathlib import Path

ROOT       = Path(__file__).parent.parent
REKT_DIR   = ROOT / "validation" / "rekt"
STRUCT_DIR = ROOT / "validation" / "structure"
SRC_DIR    = ROOT / "app" / "cbl"
CFG_TOOL   = "Cobol-REKT smojol-cli + extract_cfg_summary.py"

# Real COBOL paragraph names: uppercase letters, digits, hyphens; no slashes or spaces.
_PARA_RE = re.compile(r'^[A-Z0-9][A-Z0-9\-]{1,}$')

# Exact labels that Cobol-REKT emits as synthetic graph nodes — never paragraph names.
_SKIP_LABELS = {
    "YES", "NO", "ELSE", "EXIT", "CONTINUE", "UNTIL",
    "END-PERFORM", "END-IF", "END-READ", "END-EVALUATE",
    "END-STRING", "END-COMPUTE", "END-EXEC", "END-CALL",
    "END-SEARCH", "END-UNSTRING", "END-MULTIPLY", "END-DIVIDE",
    "END-ADD", "END-SUBTRACT", "END-RETURN",
}

# COBOL statement verbs.  Cobol-REKT builds inline-code node labels by
# concatenating the verb with the first operand, e.g.:
#   MOVECARDFILE-ST   CLOSECARDFILE-F   PERFORMUNTILEND   GOBACK
# None of these can ever be a user-defined paragraph name, so reject
# ANY label that starts with one of these verbs — no digit-guard needed.
_STMT_PREFIXES = (
    "ACCEPT",
    "ADD",
    "CALL",
    "CLOSE",
    "COMPUTE",
    "CONTINUE",
    "DISPLAY",
    "DIVIDE",
    "EVALUATE",
    "EXIT",
    "GO",
    "GOBACK",
    "IF",
    "INITIALIZE",
    "INSPECT",
    "MERGE",
    "MOVE",
    "MULTIPLY",
    "NEXT",
    "OPEN",
    "PERFORM",
    "READ",
    "RELEASE",
    "RETURN",
    "REWRITE",
    "SEARCH",
    "SET",
    "SORT",
    "STOP",
    "STRING",
    "SUBTRACT",
    "UNSTRING",
    "WRITE",
)


def is_paragraph_node(label: str) -> bool:
    """True only if label is a user-defined COBOL paragraph name."""
    if '/' in label or ' ' in label:
        return False
    if label in _SKIP_LABELS:
        return False
    if not _PARA_RE.match(label):
        return False
    # Reject every label that begins with a COBOL statement verb.
    # Real paragraph names never start with a verb (they start with
    # a sequence number like 0000- or a unique alphabetic prefix).
    for prefix in _STMT_PREFIXES:
        if label.startswith(prefix):
            return False
    return True


def sha1_file(path: Path) -> str:
    h = hashlib.sha1()
    h.update(path.read_bytes())
    return h.hexdigest()


def extract(prog_name: str):
    cfg_file = REKT_DIR / f"{prog_name}.cbl.report" / "cfg" / f"cfg-{prog_name}.cbl.json"
    if not cfg_file.exists():
        print(f"[SKIP] No Cobol-REKT output found: {cfg_file}")
        return False

    data = json.loads(cfg_file.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in data.get("nodes", [])}
    edges = data.get("edges", [])

    # Build outgoing-edge adjacency map.
    out_edges: dict[str, list[tuple[str, str]]] = {}
    for e in edges:
        out_edges.setdefault(e["fromNodeID"], []).append((e["toNodeID"], e["edgeType"]))

    # Identify paragraph nodes using the tightened filter.
    para_nodes = {n["id"]: n for n in nodes.values()
                  if is_paragraph_node(n.get("label", ""))}

    def collect_performs(start_id: str, visited: set | None = None) -> list[str]:
        if visited is None:
            visited = set()
        if start_id in visited:
            return []
        visited.add(start_id)
        result: list[str] = []
        for (to_id, _etype) in out_edges.get(start_id, []):
            if to_id in para_nodes:
                lbl = para_nodes[to_id]["label"]
                if lbl not in result:
                    result.append(lbl)
            else:
                for lbl in collect_performs(to_id, visited):
                    if lbl not in result:
                        result.append(lbl)
        return result

    def collect_gotos(start_id: str, visited: set | None = None) -> list[str]:
        if visited is None:
            visited = set()
        if start_id in visited:
            return []
        visited.add(start_id)
        result: list[str] = []
        node = nodes.get(start_id, {})
        orig = node.get("originalText", "").upper()
        if "GO TO" in orig:
            for (to_id, _) in out_edges.get(start_id, []):
                if to_id in para_nodes:
                    t = para_nodes[to_id]["label"]
                    if t not in result:
                        result.append(t)
        for (to_id, _) in out_edges.get(start_id, []):
            if to_id not in para_nodes:
                for t in collect_gotos(to_id, visited):
                    if t not in result:
                        result.append(t)
        return result

    # BFS from ProcedureDivisionBodyContext root to find reachable nodes.
    root_id = next(
        (nid for nid, n in nodes.items()
         if "ProcedureDivisionBodyContext" in n.get("label", "")),
        None,
    )
    reachable_ids: set[str] = set()
    if root_id:
        stack = [root_id]
        while stack:
            cur = stack.pop()
            if cur in reachable_ids:
                continue
            reachable_ids.add(cur)
            for (to_id, _) in out_edges.get(cur, []):
                stack.append(to_id)

    reachable_paras = {nid for nid in para_nodes if nid in reachable_ids}

    # Assemble paragraph records.
    paragraphs = []
    for nid, n in para_nodes.items():
        performs = collect_performs(nid)
        gotos    = collect_gotos(nid)
        paragraphs.append({
            "name":         n["label"],
            "reachable":    nid in reachable_paras,
            "performs":     performs,
            "goto_targets": gotos,
            "goto_flag":    len(gotos) > 0,
        })

    paragraphs.sort(key=lambda p: (not p["reachable"], p["name"]))

    src_file = SRC_DIR / f"{prog_name}.cbl"
    output = {
        "program_id":  prog_name,
        "source_file": f"app/cbl/{prog_name}.cbl",
        "source_sha":  sha1_file(src_file) if src_file.exists() else "",
        "cfg_tool":    CFG_TOOL,
        "paragraphs":  paragraphs,
    }

    out_file = STRUCT_DIR / f"{prog_name}_cfg.json"
    out_file.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"[OK] {prog_name}: {len(paragraphs)} paragraphs -> {out_file}")
    return True


def main():
    if "--all" in sys.argv:
        for report_dir in sorted(REKT_DIR.glob("*.cbl.report")):
            prog = report_dir.name.replace(".cbl.report", "")
            extract(prog)
    else:
        for prog in sys.argv[1:]:
            extract(prog.replace(".cbl", ""))


if __name__ == "__main__":
    main()
