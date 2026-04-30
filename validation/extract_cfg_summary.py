#!/usr/bin/env python3
"""
extract_cfg_summary.py
Converts Cobol-REKT cfg-{PROG}.cbl.json -> validation/structure/{PROG}_cfg.json

Usage:
    python validation/extract_cfg_summary.py CBACT04C
    python validation/extract_cfg_summary.py --all
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

# Paragraph name pattern: COBOL paragraph names are all-caps with hyphens/digits
# Excludes internal Cobol-REKT labels like "ProcedureDivisionBodyContext/..."
_PARA_RE = re.compile(r'^[A-Z0-9][A-Z0-9\-]{1,}$')
_SKIP_LABELS = {
    "YES", "NO", "ELSE", "EXIT", "CONTINUE", "UNTIL", "END-PERFORM",
    "END-IF", "END-READ", "END-EVALUATE", "END-STRING", "END-COMPUTE",
}

# Statement-type prefixes emitted by Cobol-REKT as truncated node labels
_STMT_PREFIXES = (
    "PERFORM", "DISPLAY", "MOVE", "ADD", "SUBTRACT",
    "MULTIPLY", "DIVIDE", "COMPUTE", "READ", "WRITE",
    "REWRITE", "OPEN", "CLOSE", "IF", "EVALUATE", "STRING",
    "CALL", "GOBACK", "STOP", "GO", "INITIALIZE",
    "INSPECT", "UNSTRING", "SET",
)


def is_paragraph_node(label: str) -> bool:
    """True if this label looks like a user-defined COBOL paragraph name."""
    if '/' in label or ' ' in label:
        return False
    if label in _SKIP_LABELS:
        return False
    if not _PARA_RE.match(label):
        return False
    for prefix in _STMT_PREFIXES:
        if label.startswith(prefix) and len(label) > len(prefix):
            remainder = label[len(prefix):]
            # Statement nodes like "PERFORM0300-ACC" have a digit right after prefix
            if remainder and remainder[0].isdigit():
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

    # Adjacency maps
    out_edges: dict[str, list[tuple[str, str]]] = {}
    for e in edges:
        out_edges.setdefault(e["fromNodeID"], []).append((e["toNodeID"], e["edgeType"]))

    # Identify paragraph nodes
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
        lbl  = node.get("label", "").upper()
        if "GO TO" in orig or "GOTO" in lbl:
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

    # Reachability BFS from ProcedureDivisionBodyContext root
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

    # Build paragraph list
    paragraphs = []
    for nid, n in para_nodes.items():
        performs  = collect_performs(nid)
        gotos     = collect_gotos(nid)
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
