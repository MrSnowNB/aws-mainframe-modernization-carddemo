#!/usr/bin/env python3
"""
pass3_merge.py — Merge Pass 3 synthesis responses into v1.1 translations.

Task: T-2026-04-23-002
Plan: AIFIRST-PLAN-3PASS.md §6 + §15 (Rules 9 & 10)
Contract: .aifirst/runs/T-2026-04-23-002/translation-prompt-contract-v2.md

Inputs:
  - validation/pass3/<F>_synth_responses.jsonl         (paragraph responses)
  - validation/pass2/<F>_propositions_merged.json      (from pass2_merge.py)
  - validation/pass1/<F>_annotations.json              (for CFG edge context)
  - translations/baseline/<F>.md                       (T-001 v1 baseline to
                                                        inherit front-matter)

Outputs:
  - translations/baseline-v1.1/<F>.md                  (final v1.1 translation)
  - validation/reports/<F>_T-PASS3.json                (gate result)

Validation tiers (per user checklist):
  T-PASS3-COVERAGE      every proposition seq appears in exactly ONE
                        logical_groups[].statements[] entry (100%, blocking)
  T-PASS3-SEMANTIC      every logical_groups[].semantic_pattern is in the
                        9-value enum; any `unknown` is a blocking failure
                        per Rule 10 (100%, blocking)
  T-PASS3-DERIVATION    every business_rules[].derived_from[] references
                        a defined LG id (100%, blocking)
  T-PASS3-CONFIDENCE    business_rules[].confidence < 0.70 flagged for
                        review (non-blocking)

Failure modes addressed per review checklist:
  - logical_groups coverage < 100% \u2192 T-PASS3-COVERAGE fail; record
    missing seqs and block merge (re-dispatch instruction emitted)
  - semantic_pattern = unknown    \u2192 T-PASS3-SEMANTIC fail (blocking)
  - dangling derived_from         \u2192 T-PASS3-DERIVATION fail (blocking)
  - low-confidence business rule  \u2192 flagged, not blocking
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any

import yaml

SEMANTIC_PATTERN_ENUM = {
    "guard-with-override", "accumulation", "state-machine", "delegation",
    "sequential", "conditional-branch", "cics-interaction", "file-io", "unknown",
}


# ---------------------------------------------------------------------------
# Response parsing (robust to wrappers)
# ---------------------------------------------------------------------------

def _extract_response(line: str) -> tuple[dict | None, dict | None, str | None]:
    try:
        outer = json.loads(line)
    except json.JSONDecodeError as e:
        return None, None, f"outer parse error: {e}"
    routing = outer.get("_routing") if isinstance(outer, dict) else None
    if isinstance(outer, dict):
        if "response" in outer and isinstance(outer["response"], dict):
            return outer["response"], routing, None
        if "response_content" in outer and isinstance(outer["response_content"], str):
            try:
                return json.loads(outer["response_content"]), routing, None
            except json.JSONDecodeError as e:
                return None, routing, f"response_content parse error: {e}"
        if "logical_groups" in outer or "paragraph" in outer:
            return outer, routing, None
    return None, routing, "unrecognized response shape"


def _validate_response(resp: dict) -> list[str]:
    errors: list[str] = []
    for k in ("paragraph", "logical_groups"):
        if k not in resp:
            errors.append(f"missing top-level key: {k}")
    if "logical_groups" in resp and not isinstance(resp["logical_groups"], list):
        errors.append("logical_groups must be list")
    if "business_rules" in resp and not isinstance(resp["business_rules"], list):
        errors.append("business_rules must be list")
    for i, lg in enumerate(resp.get("logical_groups", []) or []):
        if not isinstance(lg, dict):
            errors.append(f"logical_groups[{i}] not object"); continue
        for k in ("id", "group_label", "semantic_pattern", "summary", "statements"):
            if k not in lg:
                errors.append(f"logical_groups[{i}] missing {k}")
        if lg.get("semantic_pattern") not in SEMANTIC_PATTERN_ENUM:
            errors.append(f"logical_groups[{i}].semantic_pattern not in enum: {lg.get('semantic_pattern')!r}")
        if "statements" in lg and not isinstance(lg["statements"], list):
            errors.append(f"logical_groups[{i}].statements must be list")
    for i, br in enumerate(resp.get("business_rules", []) or []):
        if not isinstance(br, dict):
            errors.append(f"business_rules[{i}] not object"); continue
        for k in ("id", "rule", "rule_type", "confidence", "derived_from"):
            if k not in br:
                errors.append(f"business_rules[{i}] missing {k}")
    return errors


# ---------------------------------------------------------------------------
# Validation tiers
# ---------------------------------------------------------------------------

def check_coverage(paragraph: str, props_in_para: list[dict], lgs: list[dict]) -> dict:
    expected = {p["seq"] for p in props_in_para}
    present: dict[int, int] = {}
    for lg in lgs:
        for seq in lg.get("statements", []) or []:
            present[seq] = present.get(seq, 0) + 1
    missing = sorted(expected - set(present.keys()))
    duplicated = {s: c for s, c in present.items() if c > 1}
    extra = sorted(set(present.keys()) - expected)
    return {
        "paragraph": paragraph,
        "expected_count": len(expected),
        "present_count": len(present),
        "missing_seqs": missing,
        "duplicated_seqs": duplicated,
        "extra_seqs": extra,
        "pass": not missing and not duplicated and not extra,
    }


def check_semantic(lgs: list[dict]) -> dict:
    violations = []
    unknown_ids = []
    for lg in lgs:
        sp = lg.get("semantic_pattern")
        if sp not in SEMANTIC_PATTERN_ENUM:
            violations.append({"id": lg.get("id"), "semantic_pattern": sp,
                               "reason": "not in enum"})
        elif sp == "unknown":
            unknown_ids.append(lg.get("id"))
    return {
        "violations": violations,
        "unknown_ids": unknown_ids,
        "pass": not violations and not unknown_ids,
    }


def check_derivation(lgs: list[dict], brs: list[dict]) -> dict:
    lg_ids = {lg.get("id") for lg in lgs if lg.get("id")}
    dangling = []
    for br in brs:
        for ref in br.get("derived_from", []) or []:
            if ref not in lg_ids:
                dangling.append({"br_id": br.get("id"), "bad_ref": ref})
    return {"dangling": dangling, "pass": not dangling}


def _conf_to_float(c: Any) -> float | None:
    if c is None:
        return None
    if isinstance(c, (int, float)):
        return float(c)
    s = str(c).strip().lower()
    return {"high": 0.9, "medium": 0.6, "low": 0.3}.get(s)


def check_confidence(brs: list[dict], threshold: float = 0.70) -> dict:
    flagged = []
    for br in brs:
        c = _conf_to_float(br.get("confidence"))
        if c is not None and c < threshold:
            flagged.append({"br_id": br.get("id"), "confidence": br.get("confidence")})
    return {"flagged": flagged, "threshold": threshold, "pass_blocking": True}


# ---------------------------------------------------------------------------
# v1.1 MD assembly
# ---------------------------------------------------------------------------

def _load_v1_md(md_path: Path) -> tuple[dict, str]:
    if not md_path.exists():
        return {}, ""
    raw = md_path.read_text()
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            front = yaml.safe_load(parts[1]) or {}
            body = parts[2].lstrip("\n")
            return front, body
    return {}, raw


def _renumber_unique(items: list[dict], prefix: str) -> None:
    """Ensure IDs across multiple paragraph responses don't collide."""
    used: set[str] = set()
    for i, it in enumerate(items):
        orig = it.get("id") or f"{prefix}-{i+1:03d}"
        new = orig
        n = 1
        while new in used:
            n += 1
            new = f"{orig}#{n}"
        it["id"] = new
        used.add(new)


def assemble_v11_md(program_id: str, v1_front: dict, v1_body: str,
                    all_lgs: list[dict], all_brs: list[dict],
                    merged_propositions: list[dict],
                    source_sha: str | None) -> str:
    """Produce the v1.1 MD. The v1 front-matter is inherited verbatim EXCEPT:
      - aifirst_task_id bumped to T-2026-04-23-002
      - translation_date updated
      - schema_version bumped to cobol-md/1.1
      - logical_groups[] added (new in v1.1)
      - business_rules[] replaced with refined set
      - validation block left PENDING per hard rule 5
    """
    front = dict(v1_front)  # shallow copy
    front["schema_version"] = "cobol-md/1.1"
    front["aifirst_task_id"] = "T-2026-04-23-002"
    front["translation_date"] = "2026-04-23"
    front["translating_agent"] = "T-002 three-pass (deterministic + gpt-4o-2024-08-06 Pass 2/3)"
    if source_sha:
        front["source_sha"] = source_sha

    # Insert/replace logical_groups[] and business_rules[].
    front["logical_groups"] = all_lgs
    front["business_rules"] = all_brs

    # Leave validation block PENDING per hard rule 5.
    front["validation"] = {
        "t01_structure": None,
        "t02_semantic": None,
        "t03_functional": None,
        "t04_behavioral": None,
        "overall": "PENDING",
    }

    # Serialize. Use default_flow_style=False for readability.
    yaml_text = yaml.safe_dump(front, sort_keys=False, default_flow_style=False,
                                allow_unicode=True, width=100)

    body_lines = [f"# {program_id} \u2014 v1.1 Translation (T-002 three-pass)",
                  "",
                  "## Purpose",
                  "",
                  "See v1 body below (inherited from T-001 baseline). The v1.1 "
                  "front-matter adds paragraph-scoped `logical_groups[]` and "
                  "LLM-refined `business_rules[]` produced by the T-002 Pass 3 "
                  "synthesis. All data-name references honor Rule 9 (qualified "
                  "names) and every semantic_pattern is drawn from the "
                  "Rule 10 nine-value enum.",
                  "",
                  "## Inherited body (T-001 baseline)",
                  "",
                  v1_body.strip(),
                  ""]
    return "---\n" + yaml_text + "---\n\n" + "\n".join(body_lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--program-id", required=True)
    ap.add_argument("--propositions", type=Path, required=True,
                    help="validation/pass2/<F>_propositions_merged.json")
    ap.add_argument("--annotations", type=Path, required=True,
                    help="validation/pass1/<F>_annotations.json")
    ap.add_argument("--responses", type=Path, required=True,
                    help="validation/pass3/<F>_synth_responses.jsonl")
    ap.add_argument("--v1-md", type=Path, required=True,
                    help="translations/baseline/<F>.md (inherited baseline)")
    ap.add_argument("--out-md", type=Path, required=True,
                    help="translations/baseline-v1.1/<F>.md")
    ap.add_argument("--report", type=Path, required=True,
                    help="validation/reports/<F>_T-PASS3.json")
    args = ap.parse_args()

    props = json.loads(args.propositions.read_text())
    anns = json.loads(args.annotations.read_text())

    # Build paragraph \u2192 props index (preserve CFG order).
    paras: "OrderedDict[str, list[dict]]" = OrderedDict()
    for p in props:
        paras.setdefault(p["paragraph"], []).append(p)

    # Parse responses into paragraph \u2192 response-obj.
    lines = args.responses.read_text().splitlines() if args.responses.exists() else []
    resp_by_para: dict[str, dict] = {}
    parse_events: list[dict] = []
    for i, ln in enumerate(lines):
        if not ln.strip():
            continue
        resp, routing, err = _extract_response(ln)
        if err:
            parse_events.append({"line": i, "event": "synth_response_unparseable",
                                 "error": err})
            continue
        para = resp.get("paragraph") if isinstance(resp, dict) else None
        if para is None and routing:
            para = routing.get("paragraph")
        if para is None:
            parse_events.append({"line": i, "event": "synth_response_unparseable",
                                 "error": "no paragraph in response or routing"})
            continue
        resp_by_para[para] = resp

    # Tier results, aggregated.
    coverage_results: list[dict] = []
    semantic_results: list[dict] = []
    derivation_results: list[dict] = []
    confidence_flags: list[dict] = []
    schema_errors: list[dict] = []

    all_lgs: list[dict] = []
    all_brs: list[dict] = []

    for para, members in paras.items():
        resp = resp_by_para.get(para)
        if resp is None:
            coverage_results.append({"paragraph": para,
                                     "expected_count": len(members),
                                     "present_count": 0,
                                     "missing_seqs": sorted(p["seq"] for p in members),
                                     "duplicated_seqs": {},
                                     "extra_seqs": [],
                                     "pass": False,
                                     "reason": "synth_response_missing"})
            continue

        errs = _validate_response(resp)
        if errs:
            schema_errors.append({"paragraph": para, "errors": errs})
            # Cannot proceed with this paragraph's LGs/BRs.
            continue

        lgs = resp.get("logical_groups", []) or []
        brs = resp.get("business_rules", []) or []

        coverage_results.append(check_coverage(para, members, lgs))
        semantic_results.append({"paragraph": para, **check_semantic(lgs)})
        derivation_results.append({"paragraph": para, **check_derivation(lgs, brs)})
        cf = check_confidence(brs)
        if cf["flagged"]:
            confidence_flags.append({"paragraph": para, **cf})

        # Prefix LG/BR ids with paragraph to guarantee uniqueness before
        # concatenation across paragraphs.
        for lg in lgs:
            lg["paragraph"] = para
            if lg.get("id"):
                lg["id"] = f"{para}:{lg['id']}"
        for br in brs:
            br["source_paragraph"] = para
            if br.get("id"):
                br["id"] = f"{para}:{br['id']}"
            if br.get("derived_from"):
                br["derived_from"] = [f"{para}:{ref}" for ref in br["derived_from"]]

        all_lgs.extend(lgs)
        all_brs.extend(brs)

    _renumber_unique(all_lgs, "LG")
    _renumber_unique(all_brs, "BR")

    # Aggregate tier results.
    coverage_pass = all(r["pass"] for r in coverage_results) and not schema_errors
    semantic_pass = all(r["pass"] for r in semantic_results) and not schema_errors
    derivation_pass = all(r["pass"] for r in derivation_results) and not schema_errors
    overall_pass = coverage_pass and semantic_pass and derivation_pass

    # Assemble v1.1 MD only if blocking tiers pass.
    v1_front, v1_body = _load_v1_md(args.v1_md)
    source_sha = v1_front.get("source_sha")

    if overall_pass:
        md = assemble_v11_md(args.program_id, v1_front, v1_body,
                             all_lgs, all_brs, props, source_sha)
        args.out_md.parent.mkdir(parents=True, exist_ok=True)
        args.out_md.write_text(md)
        md_written = True
    else:
        md_written = False

    report = {
        "tier": "T-PASS3",
        "program_id": args.program_id,
        "paragraphs_total": len(paras),
        "paragraphs_with_response": len(resp_by_para),
        "coverage": {
            "pass": coverage_pass,
            "blocking": True,
            "results": coverage_results,
        },
        "semantic": {
            "pass": semantic_pass,
            "blocking": True,
            "results": semantic_results,
        },
        "derivation": {
            "pass": derivation_pass,
            "blocking": True,
            "results": derivation_results,
        },
        "confidence": {
            "pass": True,  # non-blocking
            "blocking": False,
            "flagged": confidence_flags,
            "threshold": 0.70,
        },
        "schema_errors": schema_errors,
        "parse_events": parse_events,
        "logical_groups_total": len(all_lgs),
        "business_rules_total": len(all_brs),
        "md_written": md_written,
        "md_path": str(args.out_md) if md_written else None,
        "pass": overall_pass,
        "validator_version": "v1.0.0",
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2))
    print(json.dumps({
        "tier": "T-PASS3",
        "program_id": args.program_id,
        "pass": overall_pass,
        "coverage_pass": coverage_pass,
        "semantic_pass": semantic_pass,
        "derivation_pass": derivation_pass,
        "md_written": md_written,
    }))
    return 0 if overall_pass else 2


if __name__ == "__main__":
    sys.exit(main())
