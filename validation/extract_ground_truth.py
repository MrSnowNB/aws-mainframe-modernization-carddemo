#!/usr/bin/env python3
"""
extract_ground_truth.py — normalize CFG JSON into gate-comparable ground truth.

Reads:  validation/structure/{PROGRAM}_cfg.json  (produced by Cobol-REKT)
Writes: validation/ground_truth/{PROGRAM}_gt.json

No LLM. No external dependencies beyond stdlib + json/pathlib.
Runnable on any machine with Python 3.8+.

Usage:
    python validation/extract_ground_truth.py              # all 6 programs
    python validation/extract_ground_truth.py CBACT01C     # single program
    python validation/extract_ground_truth.py CBACT01C COBSWAIT  # subset
"""
import json
import sys
import hashlib
import datetime
from pathlib import Path

PROGRAMS = ["CBACT01C", "CBCUS01C", "CBTRN01C", "COBSWAIT", "COMEN01C", "COSGN00C"]


def extract(program_id: str) -> dict:
    cfg_path = Path(f"validation/structure/{program_id}_cfg.json")
    if not cfg_path.exists():
        print(f"[GT] ERROR: {cfg_path} not found — skipping {program_id}")
        return {}

    raw = cfg_path.read_bytes()
    cfg = json.loads(raw)

    gt = {
        "program_id": program_id,
        "source_sha": cfg.get("source_sha", "unknown"),
        "cfg_sha": hashlib.sha256(raw).hexdigest()[:12],
        "extracted_at": datetime.datetime.utcnow().isoformat() + "Z",
        # Paragraphs the CFG tool confirmed reachable
        "paragraphs_reachable": sorted({
            p["name"] for p in cfg.get("paragraphs", []) if p.get("reachable", False)
        }),
        # Paragraphs CFG tool marked as dead / unreachable
        "paragraphs_dead": sorted(cfg.get("dead_code_paragraphs", [])),
        # Level-01 data items only (group + elementary FD/WS roots)
        "data_items_level01": sorted({
            d["name"] for d in cfg.get("data_items", []) if d.get("level") == 1
        }),
        # [[redefining_name, target_name], ...]
        "redefines_pairs": sorted([
            [r["name"], r["redefines"]]
            for r in cfg.get("redefines_clauses", [])
        ]),
        "calls_to": sorted(cfg.get("calls_to", [])),
        "copybooks": sorted(cfg.get("copybooks_used", [])),
        "cics_commands": cfg.get("cics_commands", []),
    }

    out_path = Path(f"validation/ground_truth/{program_id}_gt.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(gt, indent=2))

    print(
        f"[GT] {program_id}: "
        f"{len(gt['paragraphs_reachable'])} reachable, "
        f"{len(gt['paragraphs_dead'])} dead, "
        f"{len(gt['data_items_level01'])} L01 items, "
        f"{len(gt['redefines_pairs'])} redefines"
    )
    return gt


if __name__ == "__main__":
    targets = sys.argv[1:] if sys.argv[1:] else PROGRAMS
    unknown = [p for p in targets if p not in PROGRAMS]
    if unknown:
        print(f"[GT] WARNING: unknown program(s): {unknown}")
    for p in targets:
        extract(p)
