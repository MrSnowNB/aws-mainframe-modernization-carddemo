#!/usr/bin/env python3
"""
pass2_merge.py — Merge Pass 2 LLM responses back into propositions.

Task: T-2026-04-23-002
Plan: AIFIRST-PLAN-3PASS.md §5
Contract: .aifirst/runs/T-2026-04-23-002/translation-prompt-contract-v2.md Rule 8

Inputs:
  - validation/pass2/<F>_propositions.json         (original, needs_llm flagged)
  - validation/pass2/<F>_llm_responses.jsonl       (one JSON per line OR
                                                    one dispatch-wrapper per line
                                                    with response.content)
  - validation/pass1/<F>_annotations.json          (for operand inventory used
                                                    by the T-PASS2-OPS re-check)

Output:
  - validation/pass2/<F>_propositions_merged.json  (TEMPLATE records pass
                                                    through unchanged; LLM +
                                                    PARTIAL records have
                                                    proposition populated
                                                    from the response)
  - validation/reports/<F>_T-PASS2-MERGED.json     (merge-phase gate result)

Merge logic (per user instruction):
  1. Index responses by `seq` (extracted from response JSON or from the
     dispatcher's _routing envelope).
  2. For each proposition with needs_llm=True:
       a. If response missing         \u2192 log llm_response_missing,
                                         keep proposition_stub as fallback,
                                         flag for human review.
       b. If response JSON unparseable \u2192 log llm_response_unparseable,
                                         keep proposition_stub, flag.
       c. If response schema invalid   \u2192 log llm_schema_violation,
                                         keep proposition_stub, flag.
       d. Otherwise: replace proposition=null with response text, set
          proposition_source=\"LLM\" (both LLM and refined-PARTIAL merge
          to the same final source marker; proposition_stub retained
          for audit).
  3. Re-run T-PASS2-OPS (operand bounds check) on the merged output.
     Any data name in `modifies` or `reads` that is not in the Pass-1
     data_items_inventory is a T-PASS2-OPS failure for that record and
     the response is rejected (proposition reverts to null + flag).

Failure modes addressed per review feedback:
  - llm_response_unparseable (keep stub)
  - llm_response_missing     (keep stub)
  - llm_schema_violation     (keep stub)
  - T-PASS2-OPS rejection    (revert to null)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SEMANTIC_PATTERN_ENUM = {
    "guard-with-override", "accumulation", "state-machine", "delegation",
    "sequential", "conditional-branch", "cics-interaction", "file-io", "unknown",
}

REQUIRED_RESPONSE_KEYS = {"seq", "proposition", "modifies", "reads",
                          "semantic_pattern", "confidence"}


def _extract_response_object(line: str) -> tuple[dict | None, dict | None, str | None]:
    """Accept either a raw response JSON or a dispatch-wrapper of the form:
        {"_routing": {...}, "response": {...}}   (wrapper)
        {...response fields...}                   (bare)
    Returns (response_dict, routing_dict_or_None, error_or_None).
    """
    try:
        outer = json.loads(line)
    except json.JSONDecodeError as e:
        return None, None, f"outer json parse error: {e}"
    if not isinstance(outer, dict):
        return None, None, "outer not an object"
    routing = outer.get("_routing")
    # Three possible shapes:
    #   (a) outer IS the response       \u2192 keys like "seq", "proposition"
    #   (b) outer has .response (dict)  \u2192 parsed already
    #   (c) outer has .response_content (string) \u2192 need to parse
    if "response" in outer and isinstance(outer["response"], dict):
        return outer["response"], routing, None
    if "response_content" in outer and isinstance(outer["response_content"], str):
        try:
            inner = json.loads(outer["response_content"])
        except json.JSONDecodeError as e:
            return None, routing, f"response_content json parse error: {e}"
        return inner, routing, None
    # Bare form — outer has the response fields directly.
    if REQUIRED_RESPONSE_KEYS & set(outer.keys()):
        return outer, routing, None
    return None, routing, "no recognized response shape"


def _validate_response_schema(resp: dict) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_RESPONSE_KEYS - set(resp.keys())
    if missing:
        errors.append(f"missing keys: {sorted(missing)}")
    if "seq" in resp and not isinstance(resp["seq"], int):
        errors.append(f"seq must be int, got {type(resp['seq']).__name__}")
    if "proposition" in resp and not isinstance(resp["proposition"], str):
        errors.append("proposition must be string")
    if "proposition" in resp and isinstance(resp["proposition"], str) \
            and len(resp["proposition"].strip()) < 3:
        errors.append("proposition too short (<3 chars)")
    if "modifies" in resp and resp["modifies"] is not None \
            and not isinstance(resp["modifies"], str):
        errors.append("modifies must be string or null")
    if "reads" in resp:
        if not isinstance(resp["reads"], list):
            errors.append("reads must be list")
        elif any(not isinstance(x, str) for x in resp["reads"]):
            errors.append("reads[] entries must be strings")
    if "semantic_pattern" in resp:
        if resp["semantic_pattern"] not in SEMANTIC_PATTERN_ENUM:
            errors.append(f"semantic_pattern not in enum: {resp['semantic_pattern']!r}")
    if "confidence" in resp and resp["confidence"] is not None:
        if not isinstance(resp["confidence"], (int, float)):
            errors.append("confidence must be number")
        elif not (0.0 <= float(resp["confidence"]) <= 1.0):
            errors.append(f"confidence out of range [0,1]: {resp['confidence']}")
    return errors


def _load_data_items(annotations: list[dict]) -> set[str]:
    """Derive data_items_inventory from the annotations' operand lists.
    This is a conservative proxy for the CFG data_items \u2014 an operand that
    appears as 'working-storage' in any annotation is a known name."""
    inv: set[str] = set()
    for a in annotations:
        for o, t in zip(a.get("operands", []), a.get("operand_types", [])):
            if t == "working-storage":
                inv.add(o.upper())
                # Also accept qualified forms; split on ' OF '.
                for part in o.upper().split(" OF "):
                    inv.add(part.strip())
    return inv


def _check_ops_bounds(resp: dict, inventory: set[str]) -> list[str]:
    """T-PASS2-OPS: every non-null data name in modifies/reads must resolve.
    Qualified names pass if any component is in inventory."""
    errors: list[str] = []
    names: list[tuple[str, str]] = []
    if resp.get("modifies"):
        names.append(("modifies", resp["modifies"]))
    for n in resp.get("reads", []) or []:
        names.append(("reads", n))
    for field, name in names:
        if not name:
            continue
        # Accept if any component (split on ' OF ') is in inventory.
        parts = [p.strip().upper() for p in name.split(" OF ")]
        if not any(p in inventory for p in parts):
            errors.append(f"{field}: {name!r} not in data_items_inventory")
    return errors


def merge(propositions: list[dict], responses: list[dict],
          inventory: set[str]) -> tuple[list[dict], dict]:
    # Index responses by seq (from response or _routing).
    by_seq: dict[int, dict] = {}
    parse_events: list[dict] = []
    for i, raw_line in enumerate(responses):
        # `responses` is the list of raw lines from the .jsonl file.
        resp, routing, parse_err = _extract_response_object(raw_line)
        if parse_err:
            parse_events.append({"line": i, "event": "llm_response_unparseable",
                                  "error": parse_err})
            continue
        seq = resp.get("seq") if isinstance(resp, dict) else None
        if seq is None and routing:
            seq = routing.get("seq")
        if seq is None:
            parse_events.append({"line": i, "event": "llm_response_unparseable",
                                  "error": "no seq in response or routing"})
            continue
        by_seq[int(seq)] = resp

    merged: list[dict] = []
    events: list[dict] = list(parse_events)
    stats = {"total": 0, "template_unchanged": 0, "llm_merged": 0,
             "partial_merged": 0, "missing": 0, "unparseable": 0,
             "schema_violation": 0, "ops_rejected": 0}

    for p in propositions:
        stats["total"] += 1
        out = dict(p)
        if not p.get("needs_llm"):
            stats["template_unchanged"] += 1
            merged.append(out)
            continue

        seq = p["seq"]
        resp = by_seq.get(seq)
        if resp is None:
            stats["missing"] += 1
            events.append({"seq": seq, "event": "llm_response_missing",
                           "fallback": "stub" if p.get("proposition_stub") else "null"})
            # Keep proposition=null (or stub for PARTIAL) and mark for review.
            if p.get("proposition_source") == "PARTIAL":
                out["proposition"] = p.get("proposition_stub")
                out["merge_flag"] = "human_review_required_stub_retained"
            else:
                out["merge_flag"] = "human_review_required_no_response"
            merged.append(out)
            continue

        schema_errs = _validate_response_schema(resp)
        if schema_errs:
            stats["schema_violation"] += 1
            events.append({"seq": seq, "event": "llm_schema_violation",
                           "errors": schema_errs})
            if p.get("proposition_source") == "PARTIAL":
                out["proposition"] = p.get("proposition_stub")
                out["merge_flag"] = "schema_violation_stub_retained"
            else:
                out["merge_flag"] = "schema_violation_no_fallback"
            merged.append(out)
            continue

        ops_errs = _check_ops_bounds(resp, inventory)
        if ops_errs:
            stats["ops_rejected"] += 1
            events.append({"seq": seq, "event": "t_pass2_ops_rejection",
                           "errors": ops_errs})
            out["proposition"] = None
            out["merge_flag"] = "ops_rejected_revert_to_null"
            merged.append(out)
            continue

        # Success: apply merged fields.
        was_partial = (p.get("proposition_source") == "PARTIAL")
        out["proposition"] = resp["proposition"].strip()
        out["proposition_source"] = "LLM"
        out["modifies"] = resp.get("modifies")
        out["reads"] = resp.get("reads", [])
        out["semantic_pattern"] = resp["semantic_pattern"]
        out["confidence"] = float(resp["confidence"]) if resp.get("confidence") is not None else None
        out["needs_llm"] = False
        if was_partial:
            stats["partial_merged"] += 1
            # proposition_stub already preserved on the record for audit.
        else:
            stats["llm_merged"] += 1
        merged.append(out)

    return merged, {"stats": stats, "events": events}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--propositions", type=Path, required=True)
    ap.add_argument("--responses", type=Path, required=True,
                    help="JSONL file of LLM responses (one per line)")
    ap.add_argument("--annotations", type=Path, required=True,
                    help="Pass-1 annotations JSON (for data_items_inventory)")
    ap.add_argument("--out", type=Path, required=True,
                    help="Output merged propositions JSON")
    ap.add_argument("--report", type=Path, required=True,
                    help="Output merge report JSON")
    args = ap.parse_args()

    props = json.loads(args.propositions.read_text())
    anns = json.loads(args.annotations.read_text())
    inv = _load_data_items(anns)

    # Read responses as raw lines for lenient parsing.
    if args.responses.exists():
        lines = [ln for ln in args.responses.read_text().splitlines() if ln.strip()]
    else:
        lines = []

    merged, report = merge(props, lines, inv)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(merged, indent=2))

    report_out = {
        "tier": "T-PASS2-MERGED",
        "propositions_file": str(args.propositions),
        "responses_file": str(args.responses),
        "out": str(args.out),
        "inventory_size": len(inv),
        "responses_found": len(lines),
        "stats": report["stats"],
        "events": report["events"],
        "pass": (report["stats"]["missing"] == 0
                 and report["stats"]["unparseable"] == 0
                 and report["stats"]["schema_violation"] == 0
                 and report["stats"]["ops_rejected"] == 0),
        "merger_version": "v1.0.0",
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report_out, indent=2))
    print(json.dumps({"tier": "T-PASS2-MERGED",
                      "file": str(args.out),
                      "pass": report_out["pass"],
                      "stats": report_out["stats"]}))
    return 0 if report_out["pass"] else 2


if __name__ == "__main__":
    sys.exit(main())
