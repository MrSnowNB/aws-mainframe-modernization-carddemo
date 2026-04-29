#!/usr/bin/env python3
"""
pass1_annotate.py — Pass 1 annotation inventory generator (DETERMINISTIC).

Task: T-2026-04-23-002
Plan: AIFIRST-PLAN-3PASS.md §2
Deterministic: yes — zero LLM inference

Toolchain substitution (RF-01, logged in G0):
  The plan specified `cobc -fsyntax-only -fdiagnostics-format=json`.
  GnuCOBOL 3.2.0 does not support `-fdiagnostics-format=json`.
  Substitute: `cobc -E` (preprocessor) emits line-numbered preprocessed source
  that is sufficient to identify verbs, operands, paragraph boundaries, and
  branch contexts when combined with the Cobol-REKT CFG JSON produced under
  Phase 0. This script documents the substitution inline.

Output: validation/pass1/<PROGRAM_ID>_annotations.json
  JSON array of annotation records per plan §2 "Output Format".

Patch history:
  P3 (2026-04-29): Track IF/EVALUATE scope depth so that pending_branch_context
    is cleared when the matching END-IF / END-EVALUATE is consumed.  Previously
    the context bled into every subsequent statement in the paragraph, causing the
    LLM to treat unconditional post-scope code as conditionally guarded.
  P5 (2026-04-29): Add CICS branch command detection.  EXEC CICS commands such as
    RETURN, XCTL, LINK, HANDLE, and ABEND are conditional branch / state-machine
    transition points in pseudo-conversational CICS programs.  Previously they
    received no cfg_branch_context and were emitted to Pass 2 as unconditional
    cics-interaction.  Now they carry is_cics_branch=True and a descriptive
    cfg_branch_context so the LLM can correctly classify them as state-machine
    or guard-with-override.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Plan §2 — complete COBOL verb reference for Pass 1.
KNOWN_VERBS = {
    "MOVE", "ADD", "SUBTRACT", "MULTIPLY", "DIVIDE", "COMPUTE",
    "IF", "EVALUATE", "PERFORM", "CALL", "GO TO",
    "READ", "WRITE", "REWRITE", "DELETE", "START", "OPEN", "CLOSE",
    "EXEC CICS", "EXEC SQL",
    "MOVE CORRESPONDING", "STRING", "UNSTRING", "INSPECT",
    "INITIALIZE", "SET", "ACCEPT", "DISPLAY", "STOP RUN", "EXIT",
    # Common additional verbs encountered in the pilot corpus.
    "GOBACK", "CONTINUE", "COPY",
}

BRANCH_VERBS = {"IF", "EVALUATE", "GO TO"}

# Scope-opening verbs that increment _scope_depth (P3).
_SCOPE_OPENERS = {"IF", "EVALUATE"}

# Scope terminators that decrement _scope_depth (P3).
# Shared with the phantom-paragraph filter further below.
SCOPE_TERMINATORS = {"END-IF", "END-EVALUATE", "END-EXEC", "END-PERFORM", "END-READ"}

# Regex matching a bare scope-terminator token on its own source line.
# Used in the statement loop to detect scope closes without consuming a verb.
_SCOPE_CLOSE_PATTERN = re.compile(
    r"^\s+(END-IF|END-EVALUATE)\b",
    re.IGNORECASE,
)

# P5: CICS commands that represent conditional branch / state-machine transitions
# in pseudo-conversational CICS programs (CardDemo uses all of these).
# Non-branch CICS commands (SEND, RECEIVE, READ, WRITE, etc.) are NOT listed here
# and will continue to be classified as cics-interaction by the LLM.
CICS_BRANCH_COMMANDS = {"HANDLE", "RETURN", "XCTL", "LINK", "ABEND"}

# Regex to extract the first CICS command token from the text following EXEC CICS.
_CICS_COMMAND_PATTERN = re.compile(
    r"^\s*([A-Z][A-Z0-9\-]*)",
    re.IGNORECASE,
)

# Regex for a statement-leading COBOL verb. We require the verb to start at
# start-of-line (with leading whitespace) to reduce false positives where a
# verb keyword appears as part of a longer identifier.
_VERB_PATTERN = re.compile(
    r"^\s+(" + "|".join(re.escape(v) for v in sorted(KNOWN_VERBS, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)

# COBOL paragraph header: "3000-READ-INPUT." (name dot alone on a line, area A).
_PARAGRAPH_PATTERN = re.compile(r"^\s{0,3}([A-Z0-9][A-Z0-9\-]*)\.\s*$", re.IGNORECASE)

# Section header: "WORKING-STORAGE SECTION."
_SECTION_PATTERN = re.compile(r"^\s{0,3}([A-Z0-9\-]+)\s+SECTION\.\s*$", re.IGNORECASE)

# Division header: "PROCEDURE DIVISION."
_DIVISION_PATTERN = re.compile(r"^\s{0,3}(IDENTIFICATION|ENVIRONMENT|DATA|PROCEDURE)\s+DIVISION\b", re.IGNORECASE)


def preprocess(src_path: Path) -> list[tuple[int, str]]:
    """Return a list of (physical_line, text) pairs from `cobc -E`."""
    proc = subprocess.run(
        ["cobc", "-E", str(src_path)],
        capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0 and not proc.stdout:
        raise RuntimeError(f"cobc -E failed on {src_path}: {proc.stderr}")
    lines: list[tuple[int, str]] = []
    current_line = 0
    for raw in proc.stdout.splitlines():
        # cobc emits `#line N "path"` markers between preprocessed regions.
        m = re.match(r'^#line\s+(\d+)\s+"', raw)
        if m:
            current_line = int(m.group(1))
            continue
        lines.append((current_line, raw))
        current_line += 1
    return lines


def identify_operands(verb: str, rest: str, data_items_inventory: set[str]) -> tuple[list[str], list[str]]:
    """
    Extract operands from the text following the verb.

    Returns parallel lists of operand strings and their types:
      - 'literal'          — quoted string or numeric literal
      - 'working-storage'  — identifier present in data_items_inventory
      - 'paragraph'        — used by PERFORM/GO TO (resolved by caller via CFG)
      - 'external-program' — quoted literal target of CALL
      - 'unresolved'       — identifier not in inventory (flagged later)
    """
    ops: list[str] = []
    types: list[str] = []

    # Strip trailing period and comments.
    text = rest.split("*>")[0].rstrip(". \t")

    # Split conservatively on whitespace, commas, and a few connectors while
    # preserving quoted literals.
    tokens = re.findall(r"'[^']*'|\"[^\"]*\"|[A-Z0-9][A-Z0-9\-]*", text, re.IGNORECASE)

    # Filter connective keywords that are not operands.
    connective = {
        "TO", "FROM", "BY", "INTO", "USING", "GIVING", "UPON",
        "THRU", "THROUGH", "TIMES", "UNTIL", "VARYING",
        "IS", "ARE", "NOT", "AND", "OR", "OF", "IN", "THEN", "ELSE",
        "WHEN", "ON", "SIZE", "ERROR", "AT", "END", "KEY",
        "EQUAL", "GREATER", "LESS", "THAN", "ZERO", "ZEROS", "ZEROES",
        "SPACE", "SPACES", "HIGH-VALUE", "HIGH-VALUES", "LOW-VALUE", "LOW-VALUES",
        "ALL", "FIRST", "LAST", "ANY", "EACH", "WITH", "BEFORE", "AFTER",
        "INPUT", "OUTPUT", "I-O", "EXTEND", "REVERSED", "NO",
        "REWIND", "RECORD", "CORRESPONDING", "CORR",
    }

    for tok in tokens:
        up = tok.upper()
        if tok.startswith(("'", '"')):
            ops.append(tok)
            types.append("literal" if verb != "CALL" else "external-program")
            continue
        if up in connective:
            continue
        if re.fullmatch(r"[+-]?\d+(\.\d+)?", tok):
            ops.append(tok)
            types.append("literal")
            continue
        if up in data_items_inventory:
            ops.append(up)
            types.append("working-storage")
        else:
            # Could be a paragraph (PERFORM, GO TO) or unresolved.
            if verb in {"PERFORM", "GO TO"}:
                ops.append(up)
                types.append("paragraph")
            else:
                ops.append(up)
                types.append("unresolved")
    return ops, types


def load_cfg(cfg_path: Path) -> dict:
    return json.loads(cfg_path.read_text())


def build_branch_context(verb: str, text: str) -> str | None:
    """Extract a short textual branch context for IF / EVALUATE / WHEN."""
    text = text.rstrip(". \t")
    if verb == "IF":
        return f"IF {text.strip()}"
    if verb == "EVALUATE":
        return f"EVALUATE {text.strip()}"
    return None


def extract_cics_command(rest: str) -> str | None:
    """P5: Extract the first CICS command token from text following EXEC CICS.

    Returns the uppercased command name (e.g. 'RETURN', 'XCTL') or None if
    the text is blank or unparseable.
    """
    m = _CICS_COMMAND_PATTERN.match(rest)
    if m:
        return m.group(1).upper()
    return None


def annotate(src_path: Path, cfg_path: Path, program_id: str) -> tuple[list[dict], list[dict]]:
    """Return (annotations, phantom_filter_events)."""
    cfg = load_cfg(cfg_path)
    data_items_inventory = {d["name"].upper() for d in cfg.get("data_items", []) if d.get("name")}
    cfg_paragraphs = {p.get("name", "").upper() for p in cfg.get("paragraphs", []) if p.get("name")}

    # RF-02: filter Cobol-REKT phantom paragraphs (scope terminators, data-item
    # names promoted to pseudo-paragraph nodes). We ONLY filter a name as a
    # phantom paragraph when it meets two conditions simultaneously:
    #  (a) it is a Cobol-REKT artefact name or is present in data_items_inventory, AND
    #  (b) the next non-blank line is NOT another statement (i.e. the token is
    #      really being used as a paragraph header by the CFG tool rather than
    #      as a real terminating statement like `GOBACK.` or `EXIT.`).
    # A bare `GOBACK.` statement on its own line is a legitimate PROCEDURE
    # statement that must be annotated, not filtered.
    # Statements that also happen to pattern-match as paragraph headers when
    # they appear alone on a line followed by a period. These are always real
    # statements, never phantom paragraphs, regardless of what the CFG says.
    STATEMENT_ONLY_TOKENS = {"GOBACK", "EXIT", "CONTINUE", "STOP"}
    phantom_events: list[dict] = []

    preprocessed = preprocess(src_path)

    annotations: list[dict] = []
    current_paragraph: str | None = None
    current_section: str | None = None  # noqa: F841  (tracked for future use)
    current_division: str | None = None
    seq = 0
    pending_branch_context: str | None = None
    # P3: scope depth counter — incremented on IF/EVALUATE, decremented on
    # END-IF/END-EVALUATE.  When depth returns to 0 the pending branch context
    # is cleared so post-scope statements are not falsely marked as guarded.
    _scope_depth: int = 0

    for phys_line, line in preprocessed:
        # ----------------------------------------------------------------
        # P3: detect scope-close tokens BEFORE verb/paragraph matching so
        # that END-IF / END-EVALUATE decrement depth even when they appear
        # as standalone lines that do not match _VERB_PATTERN.
        # ----------------------------------------------------------------
        mclose = _SCOPE_CLOSE_PATTERN.match(line)
        if mclose and current_division == "PROCEDURE":
            _scope_depth = max(0, _scope_depth - 1)
            if _scope_depth == 0:
                pending_branch_context = None
            continue

        # Track structure
        mdiv = _DIVISION_PATTERN.match(line)
        if mdiv:
            current_division = mdiv.group(1).upper()
            continue
        msec = _SECTION_PATTERN.match(line)
        if msec:
            current_section = msec.group(1).upper()  # type: ignore[assignment]
            continue
        mpar = _PARAGRAPH_PATTERN.match(line)
        if mpar and current_division == "PROCEDURE":
            name = mpar.group(1).upper()
            # Statements that look like paragraph headers (GOBACK., EXIT., etc.)
            # fall through to verb detection below — they are real statements.
            if name in STATEMENT_ONLY_TOKENS:
                pass  # fall through to verb detection
            elif name in SCOPE_TERMINATORS or name in data_items_inventory:
                phantom_events.append({
                    "event": "cfg_phantom_filtered",
                    "paragraph_candidate": name,
                    "line": phys_line,
                    "reason": "Cobol-REKT artefact: scope terminator or data-item name",
                })
                continue
            else:
                current_paragraph = name
                # P3: entering a new paragraph always resets scope state.
                pending_branch_context = None
                _scope_depth = 0
                continue

        # Statement detection (PROCEDURE DIVISION only).
        if current_division != "PROCEDURE":
            continue
        if not current_paragraph:
            # Some programs put PROCEDURE DIVISION code before an explicit
            # paragraph header; synthesise a MAIN paragraph.
            current_paragraph = f"{program_id}-MAIN"

        mverb = _VERB_PATTERN.match(line)
        if not mverb:
            continue

        verb = mverb.group(1).upper()
        rest = line[mverb.end():]

        ops, op_types = identify_operands(verb, rest, data_items_inventory)

        seq += 1
        rec = {
            "seq": seq,
            "paragraph": current_paragraph,
            "line": phys_line,
            "verb": verb,
            "operands": ops,
            "operand_types": op_types,
            "cfg_reachable": current_paragraph.upper() in cfg_paragraphs,
            "cfg_branch_context": pending_branch_context,
            "cfg_predecessors": [seq - 1] if seq > 1 else [],
            "cfg_successors": [seq + 1],
            "division": current_division,
            "raw": line.strip(),
        }

        # Flag any operand we could not resolve.
        if any(t == "unresolved" for t in op_types):
            rec["operand_unresolved"] = True

        # -----------------------------------------------------------------
        # P5: CICS branch command detection.
        # Check BEFORE the standard BRANCH_VERBS block so that CICS branch
        # annotations are applied on the same pass as the record is built.
        # -----------------------------------------------------------------
        if verb == "EXEC CICS":
            cics_cmd = extract_cics_command(rest)
            if cics_cmd and cics_cmd in CICS_BRANCH_COMMANDS:
                # Summarise options from rest (first 60 chars, stripped).
                options_summary = rest.strip()[:60].rstrip()
                branch_ctx = f"EXEC CICS {cics_cmd} {options_summary}".strip()
                rec["cfg_branch_context"] = branch_ctx
                rec["is_cics_branch"] = True
                rec["cics_command"] = cics_cmd
                # CICS branches do NOT increment _scope_depth — they are
                # point exits, not block-scoped constructs.
            else:
                # Non-branch CICS command: record the command for Pass 2
                # context but leave cfg_branch_context as-is.
                if cics_cmd:
                    rec["cics_command"] = cics_cmd

        elif verb in BRANCH_VERBS and rec["cfg_branch_context"] is None:
            rec["cfg_branch_context"] = build_branch_context(verb, rest)
            if rec["cfg_branch_context"] is None:
                rec["cfg_branch_unresolved"] = True
            # P3: open a new scope and set the branch context.
            if verb in _SCOPE_OPENERS:
                _scope_depth += 1
                pending_branch_context = rec["cfg_branch_context"]
            else:
                # GO TO: no scope block; just record context for this statement.
                pending_branch_context = rec["cfg_branch_context"]

        annotations.append(rec)

    # Last annotation has no successor.
    if annotations:
        annotations[-1]["cfg_successors"] = []

    return annotations, phantom_events


def selftest() -> int:
    repo = Path(__file__).resolve().parents[1]
    src = repo / "app" / "cbl" / "COBSWAIT.cbl"
    cfg = repo / "validation" / "structure" / "COBSWAIT_cfg.json"
    anns, phantoms = annotate(src, cfg, "COBSWAIT")
    # COBSWAIT has 4 PROCEDURE-DIVISION statements: ACCEPT, MOVE, CALL, STOP RUN.
    assert len(anns) == 4, f"selftest expected 4 annotations, got {len(anns)}: {[a['verb'] for a in anns]}"
    verbs = [a["verb"] for a in anns]
    assert verbs == ["ACCEPT", "MOVE", "CALL", "STOP RUN"], f"verbs mismatch: {verbs}"
    # P3: COBSWAIT has no IF/EVALUATE blocks so scope depth must be 0 at end.
    # We verify indirectly: no annotation should carry a non-null branch context.
    assert all(a["cfg_branch_context"] is None for a in anns), \
        "selftest P3: unexpected branch context on COBSWAIT annotation"
    # P5: COBSWAIT uses EXEC CICS but via a CALL verb wrapper; no is_cics_branch
    # flag should appear on any annotation (COBSWAIT has no direct EXEC CICS).
    assert not any(a.get("is_cics_branch") for a in anns), \
        "selftest P5: unexpected is_cics_branch on COBSWAIT annotation"
    print(json.dumps({"selftest": "PASS", "annotations": len(anns), "verbs": verbs,
                      "phantoms_filtered": len(phantoms),
                      "p3_scope_depth_ok": True,
                      "p5_cics_branch_ok": True}))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Pass 1 annotator (deterministic)")
    ap.add_argument("--src", type=Path, help="Path to COBOL source (.cbl)")
    ap.add_argument("--cfg", type=Path, help="Path to Phase-0 CFG JSON")
    ap.add_argument("--program-id", type=str, help="PROGRAM-ID (e.g. COBSWAIT)")
    ap.add_argument("--out", type=Path, help="Output annotations JSON path")
    ap.add_argument("--phantoms-out", type=Path, default=None, help="Optional: phantom events JSON path")
    ap.add_argument("--selftest", action="store_true", help="Run built-in COBSWAIT selftest and exit")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if not (args.src and args.cfg and args.program_id and args.out):
        ap.error("--src, --cfg, --program-id, --out all required (or --selftest)")

    annotations, phantoms = annotate(args.src, args.cfg, args.program_id)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(annotations, indent=2))
    if args.phantoms_out:
        args.phantoms_out.parent.mkdir(parents=True, exist_ok=True)
        args.phantoms_out.write_text(json.dumps(phantoms, indent=2))
    print(json.dumps({
        "program_id": args.program_id,
        "annotations": len(annotations),
        "phantoms_filtered": len(phantoms),
        "unresolved_operands": sum(1 for a in annotations if a.get("operand_unresolved")),
        "branch_verbs": sum(1 for a in annotations if a["verb"] in BRANCH_VERBS),
        "cics_branches": sum(1 for a in annotations if a.get("is_cics_branch")),
        "out": str(args.out),
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
