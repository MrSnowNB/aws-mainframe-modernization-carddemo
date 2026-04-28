#!/usr/bin/env python3
"""
extract_ground_truth.py -- normalize CFG JSON into gate-comparable ground truth.

Reads:  validation/structure/{PROGRAM}_cfg.json  (produced by Cobol-REKT)
Writes: validation/ground_truth/{PROGRAM}_gt.json
        validation/logs/gt_{TIMESTAMP}.log        (append-only run log)

No LLM. No external dependencies beyond stdlib + json/pathlib.
Runnable on any machine with Python 3.8+.

Cobol-REKT RC8 known issue: scope terminators (END-IF, END-EXEC,
END-PERFORM, END-EVALUATE, END-READ, END-WRITE, END-STRING,
END-UNSTRING, END-MULTIPLY, END-DIVIDE, END-ADD, END-SUBTRACT,
END-COMPUTE, END-SEARCH) are misidentified as paragraph names and
reported as dead code. These are filtered out before gate comparison.

Usage:
    python validation/extract_ground_truth.py              # all 6 programs
    python validation/extract_ground_truth.py CBACT01C     # single program
    python validation/extract_ground_truth.py CBACT01C COBSWAIT  # subset
"""
import io
import json
import sys
import hashlib
import datetime
from pathlib import Path

try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
except AttributeError:
    pass

PROGRAMS = ["CBACT01C", "CBCUS01C", "CBTRN01C", "COBSWAIT", "COMEN01C", "COSGN00C"]

# Cobol-REKT RC8 false positives: structured statement scope terminators
# misidentified as paragraph labels. Filter these from dead_code_paragraphs.
COBOL_SCOPE_TERMINATORS = {
    "END-EXEC", "END-IF", "END-PERFORM", "END-EVALUATE",
    "END-READ", "END-WRITE", "END-STRING", "END-UNSTRING",
    "END-MULTIPLY", "END-DIVIDE", "END-ADD", "END-SUBTRACT",
    "END-COMPUTE", "END-SEARCH",
}


def log(run_id: str, lines: list, log_dir: Path):
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"gt_{run_id}.log"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return log_path


def extract(program_id: str) -> dict:
    cfg_path = Path(f"validation/structure/{program_id}_cfg.json")
    if not cfg_path.exists():
        print(f"[GT] ERROR: {cfg_path} not found -- skipping {program_id}")
        return {}

    raw = cfg_path.read_bytes()
    cfg = json.loads(raw)

    # Filter Cobol-REKT RC8 false-positive scope terminators from dead list
    raw_dead = cfg.get("dead_code_paragraphs", [])
    filtered_dead = [p for p in raw_dead if p not in COBOL_SCOPE_TERMINATORS]
    suppressed = [p for p in raw_dead if p in COBOL_SCOPE_TERMINATORS]

    gt = {
        "program_id": program_id,
        "source_sha": cfg.get("source_sha", "unknown"),
        "cfg_sha": hashlib.sha256(raw).hexdigest()[:12],
        "extracted_at": datetime.datetime.utcnow().isoformat() + "Z",
        "paragraphs_reachable": sorted({
            p["name"] for p in cfg.get("paragraphs", []) if p.get("reachable", False)
        }),
        "paragraphs_dead": sorted(filtered_dead),
        "scope_terminators_suppressed": sorted(suppressed),
        "data_items_level01": sorted({
            d["name"] for d in cfg.get("data_items", []) if d.get("level") == 1
        }),
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
    out_path.write_text(json.dumps(gt, indent=2), encoding="utf-8")

    suppressed_note = f", {len(suppressed)} terminators suppressed" if suppressed else ""
    line = (
        f"[GT] {program_id}: "
        f"{len(gt['paragraphs_reachable'])} reachable, "
        f"{len(gt['paragraphs_dead'])} dead{suppressed_note}, "
        f"{len(gt['data_items_level01'])} L01 items, "
        f"{len(gt['redefines_pairs'])} redefines"
    )
    print(line)
    return gt, line


if __name__ == "__main__":
    run_id = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    log_dir = Path("validation/logs")
    targets = sys.argv[1:] if sys.argv[1:] else PROGRAMS
    unknown = [p for p in targets if p not in PROGRAMS]
    run_lines = [f"# extract_ground_truth run {run_id}", f"# targets: {targets}"]
    if unknown:
        warn = f"[GT] WARNING: unknown program(s): {unknown}"
        print(warn)
        run_lines.append(warn)
    for p in targets:
        if p in PROGRAMS:
            result = extract(p)
            if result:
                _, line = result
                run_lines.append(line)
    log(run_id, run_lines, log_dir)
    print(f"[GT] log written: validation/logs/gt_{run_id}.log")
