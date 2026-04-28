#!/usr/bin/env python3
"""
extract_md_claims.py -- extract structural claims from a gold-candidate MD file.

Reads:  translations/gold-candidate/{PROGRAM}.md
Writes: validation/claims/{PROGRAM}_claims.json

No LLM. Parses YAML frontmatter only -- no interpretation of prose body.
Runnable on any machine with Python 3.8+ and PyYAML.

Install deps:  pip install pyyaml

Usage:
    python validation/extract_md_claims.py              # all 6 programs
    python validation/extract_md_claims.py CBACT01C     # single program
"""
import io
import json
import sys
import hashlib
import datetime
from pathlib import Path

# Force UTF-8 stdout for Windows cp1252 safety
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
except AttributeError:
    pass

try:
    import yaml
except ImportError:
    sys.exit("[CLAIMS] ERROR: PyYAML not installed. Run: pip install pyyaml")

PROGRAMS = ["CBACT01C", "CBCUS01C", "CBTRN01C", "COBSWAIT", "COMEN01C", "COSGN00C"]


def parse_frontmatter(md_path: Path) -> dict:
    """Extract the YAML block between the first pair of --- delimiters."""
    text = md_path.read_text(encoding="utf-8")
    parts = text.split("---")
    if len(parts) < 3:
        raise ValueError(f"No valid --- frontmatter in {md_path}")
    return yaml.safe_load(parts[1]) or {}


def extract(program_id: str) -> dict:
    md_path = Path(f"translations/gold-candidate/{program_id}.md")
    if not md_path.exists():
        print(f"[CLAIMS] ERROR: {md_path} not found -- skipping {program_id}")
        return {}

    md_bytes = md_path.read_bytes()
    fm = parse_frontmatter(md_path)

    # -- Paragraphs -----------------------------------------------------------
    proc = fm.get("procedure_paragraphs", [])
    if not isinstance(proc, list):
        proc = []

    para_names = sorted(
        p["name"] if isinstance(p, dict) else str(p)
        for p in proc
    )

    # Dead-code paragraphs the MD explicitly marks reachable:false
    dead_declared = sorted(
        p["name"]
        for p in proc
        if isinstance(p, dict) and p.get("reachable") is False
    )

    # Synthetic paragraphs: MD-invented labels for inline-only sources
    # (programs with no named paragraphs). Declared via synthetic: true.
    synthetic_paragraphs = sorted(
        p["name"]
        for p in proc
        if isinstance(p, dict) and p.get("synthetic") is True
    )

    # -- Data items (level-01 only) -------------------------------------------
    items = fm.get("data_items", [])
    if not isinstance(items, list):
        items = []

    l01_names = sorted(
        d["name"]
        for d in items
        if isinstance(d, dict) and d.get("level") == 1
    )

    redefines = sorted(
        [d["name"], d["redefines"]]
        for d in items
        if isinstance(d, dict) and d.get("redefines")
    )

    # -- Calls, copybooks, CICS -----------------------------------------------
    calls_raw = fm.get("calls_to", [])
    calls = sorted(
        c["program"] if isinstance(c, dict) else str(c)
        for c in (calls_raw if isinstance(calls_raw, list) else [])
    )

    cpyb_raw = fm.get("copybooks_used", [])
    copybooks = sorted(
        c["name"] if isinstance(c, dict) else str(c)
        for c in (cpyb_raw if isinstance(cpyb_raw, list) else [])
    )

    cics = fm.get("cics_commands", [])

    # -- Validation block: detect fabricated T04 score ------------------------
    val = fm.get("validation", {})
    if not isinstance(val, dict):
        val = {}
    t04_score = val.get("t04_semantic_score", None)

    claims = {
        "program_id": program_id,
        "md_sha": hashlib.sha256(md_bytes).hexdigest()[:12],
        "extracted_at": datetime.datetime.utcnow().isoformat() + "Z",
        "paragraphs_claimed": para_names,
        "dead_declared_in_md": dead_declared,
        "synthetic_paragraphs": synthetic_paragraphs,
        "data_items_level01": l01_names,
        "redefines_pairs": redefines,
        "calls_to": calls,
        "copybooks": copybooks,
        "cics_commands": cics if isinstance(cics, list) else [],
        "t04_score_in_md": t04_score,
        "t04_score_is_null": t04_score is None,
    }

    out_path = Path(f"validation/claims/{program_id}_claims.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(claims, indent=2), encoding="utf-8")

    score_flag = "NULL [OK]" if t04_score is None else f"{t04_score} [!!] FABRICATED SCORE"
    synth_note = f", {len(synthetic_paragraphs)} synthetic" if synthetic_paragraphs else ""
    print(
        f"[CLAIMS] {program_id}: "
        f"{len(para_names)} paragraphs{synth_note}, "
        f"{len(dead_declared)} dead declared, "
        f"{len(l01_names)} L01 items | "
        f"t04={score_flag}"
    )
    return claims


if __name__ == "__main__":
    targets = sys.argv[1:] if sys.argv[1:] else PROGRAMS
    unknown = [p for p in targets if p not in PROGRAMS]
    if unknown:
        print(f"[CLAIMS] WARNING: unknown program(s): {unknown}")
    for p in targets:
        extract(p)
