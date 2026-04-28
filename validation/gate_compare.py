#!/usr/bin/env python3
"""
gate_compare.py -- diff ground truth vs MD claims, emit gate report.

Reads:  validation/ground_truth/{PROGRAM}_gt.json
        validation/claims/{PROGRAM}_claims.json
Writes: validation/reports/{PROGRAM}_gate.json

No LLM. Purely set-difference logic.
Runnable on any machine with Python 3.8+ stdlib only.

Exit codes:
    0 = all tested programs PASS
    1 = one or more programs FAIL

Usage:
    python validation/gate_compare.py              # all 6 programs
    python validation/gate_compare.py CBACT01C     # single program

Run AFTER extract_ground_truth.py and extract_md_claims.py.
"""
import io
import json
import sys
import datetime
from pathlib import Path

# Force UTF-8 stdout so box/check chars survive Windows cp1252 terminals.
# Falls back silently on platforms that don't support reconfigure.
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
except AttributeError:
    pass

PROGRAMS = ["CBACT01C", "CBCUS01C", "CBTRN01C", "COBSWAIT", "COMEN01C", "COSGN00C"]


def compare(program_id: str) -> bool:
    gt_path = Path(f"validation/ground_truth/{program_id}_gt.json")
    cl_path = Path(f"validation/claims/{program_id}_claims.json")

    if not gt_path.exists():
        print(f"[GATE] {program_id}: SKIP -- ground truth not found (run extract_ground_truth.py first)")
        return False
    if not cl_path.exists():
        print(f"[GATE] {program_id}: SKIP -- claims not found (run extract_md_claims.py first)")
        return False

    gt = json.loads(gt_path.read_text(encoding="utf-8"))
    cl = json.loads(cl_path.read_text(encoding="utf-8"))

    failures = []
    warnings = []

    # -- Check 1: No reachable paragraph missing from MD ----------------------
    gt_reachable = set(gt["paragraphs_reachable"])
    cl_paragraphs = set(cl["paragraphs_claimed"])
    # synthetic_paragraphs: MD-declared labels for inline-only programs
    # (programs with zero named paragraphs in source, e.g. COBSWAIT).
    # These are explicitly exempt from the hallucination check.
    cl_synthetic = set(cl.get("synthetic_paragraphs", []))

    missing_paras = sorted(gt_reachable - cl_paragraphs)
    if missing_paras:
        failures.append({
            "check": "paragraphs_missing_from_md",
            "detail": "Reachable paragraphs in source not found in MD",
            "items": missing_paras
        })

    # -- Check 2: Extra paragraphs in MD must be CFG dead-code OR synthetic ---
    extra_paras = cl_paragraphs - gt_reachable
    gt_dead = set(gt["paragraphs_dead"])
    cl_dead = set(cl["dead_declared_in_md"])
    # Unexplained = extra AND not dead AND not synthetic
    unexplained = sorted(extra_paras - gt_dead - cl_synthetic)
    if unexplained:
        failures.append({
            "check": "hallucinated_paragraphs",
            "detail": "MD claims paragraphs not in source, not dead-code, and not synthetic",
            "items": unexplained
        })

    # Synthetic paragraphs trigger an INFO note, not a failure
    if cl_synthetic and gt_reachable == set():  # inline-only source confirmed
        warnings.append({
            "check": "synthetic_paragraphs_accepted",
            "detail": "Source has no named paragraphs; MD synthetic labels accepted",
            "items": sorted(cl_synthetic)
        })

    # -- Check 2b: Dead code in GT not declared in MD (warning only) ----------
    undeclared_dead = sorted(gt_dead - cl_dead)
    if undeclared_dead:
        warnings.append({
            "check": "dead_code_not_declared_in_md",
            "detail": "CFG dead paragraphs not explicitly marked reachable:false in MD",
            "items": undeclared_dead
        })

    # -- Check 3: Level-01 data items -----------------------------------------
    gt_items = set(gt["data_items_level01"])
    cl_items = set(cl["data_items_level01"])
    missing_items = sorted(gt_items - cl_items)
    extra_items = sorted(cl_items - gt_items)
    if missing_items:
        failures.append({
            "check": "data_items_missing",
            "detail": "Level-01 data items in source not found in MD",
            "items": missing_items
        })
    if extra_items:
        failures.append({
            "check": "data_items_hallucinated",
            "detail": "Level-01 data items in MD not found in source",
            "items": extra_items
        })

    # -- Check 4: REDEFINES pairs ---------------------------------------------
    gt_red = set(map(tuple, gt["redefines_pairs"]))
    cl_red = set(map(tuple, cl["redefines_pairs"]))
    missing_red = [list(r) for r in sorted(gt_red - cl_red)]
    if missing_red:
        failures.append({
            "check": "redefines_missing",
            "detail": "REDEFINES clauses in source not declared in MD",
            "items": missing_red
        })

    # -- Check 5: Calls -------------------------------------------------------
    missing_calls = sorted(set(gt["calls_to"]) - set(cl["calls_to"]))
    if missing_calls:
        failures.append({
            "check": "calls_missing",
            "detail": "CALL targets in source not listed in MD calls_to",
            "items": missing_calls
        })

    # -- Check 6: Copybooks ---------------------------------------------------
    missing_cpyb = sorted(set(gt["copybooks"]) - set(cl["copybooks"]))
    if missing_cpyb:
        failures.append({
            "check": "copybooks_missing",
            "detail": "COPY statements in source not listed in MD copybooks_used",
            "items": missing_cpyb
        })

    # -- Check 7: No fabricated T04 score -------------------------------------
    if not cl["t04_score_is_null"]:
        failures.append({
            "check": "fabricated_t04_score",
            "detail": "t04_semantic_score is non-null with no judge report present",
            "value": cl["t04_score_in_md"]
        })

    # -- Emit report ----------------------------------------------------------
    gate_pass = len(failures) == 0
    report = {
        "program_id": program_id,
        "gate_run_at": datetime.datetime.utcnow().isoformat() + "Z",
        "source_sha": gt["source_sha"],
        "md_sha": cl["md_sha"],
        "gate_pass": gate_pass,
        "failure_count": len(failures),
        "warning_count": len(warnings),
        "failures": failures,
        "warnings": warnings,
    }

    out_path = Path(f"validation/reports/{program_id}_gate.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    status = "PASS [OK]" if gate_pass else f"FAIL [{len(failures)} failures, {len(warnings)} warnings]"
    print(f"[GATE] {program_id}: {status}")
    for f in failures:
        items_str = str(f.get("items", f.get("value", "")))
        print(f"  X {f['check']}: {items_str}")
    for w in warnings:
        print(f"  ~ {w['check']}: {w.get('items', '')}")

    return gate_pass


if __name__ == "__main__":
    targets = sys.argv[1:] if sys.argv[1:] else PROGRAMS
    unknown = [p for p in targets if p not in PROGRAMS]
    if unknown:
        print(f"[GATE] WARNING: unknown program(s): {unknown}")
    results = {p: compare(p) for p in targets if p in PROGRAMS}

    print("")
    print("-- Gate Summary ------------------------------------------------")
    for prog, passed in results.items():
        print(f"  {'PASS' if passed else 'FAIL'}  {prog}")
    total = len(results)
    passed_count = sum(results.values())
    print(f"  {passed_count}/{total} programs passed")
    print("----------------------------------------------------------------")

    sys.exit(0 if all(results.values()) else 1)
