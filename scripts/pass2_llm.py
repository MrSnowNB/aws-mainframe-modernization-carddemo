#!/usr/bin/env python3
"""
pass2_llm.py — Pass 2 LLM request payload emitter (bounded inference).

Task: T-2026-04-23-002
Plan: AIFIRST-PLAN-3PASS.md §5 + §15 (Rule 8)
Contract: .aifirst/runs/T-2026-04-23-002/translation-prompt-contract-v2.md Rule 8

Purpose: for every proposition whose `needs_llm == True` (i.e.
`proposition_source` is `LLM` or `PARTIAL`), build a fully specified LLM
request payload and write the payload set to:

    validation/pass2/<PROGRAM_ID>_llm_requests.jsonl

Each line is a single self-contained JSON payload ready to POST to a
chat-completions endpoint. No endpoint is called in this sandbox — the
payload file is the audit trail (Risk Flag RF-03, same pattern as T-001
`scripts/score_t04.py`). A human operator dispatches the payloads
out-of-band, collects responses into:

    validation/pass2/<PROGRAM_ID>_llm_responses.jsonl

… and re-runs `scripts/pass2_merge.py` (separate tool) to merge refined
propositions back into `<PROGRAM_ID>_propositions.json`.

Rule 8 envelope enforced on every payload:
  - temperature = 0
  - seed = 42
  - response_format = {"type": "json_object"}
  - max_tokens bounded
  - structured system prompt declaring the required JSON response schema
  - user prompt contains ONLY annotation context (no raw COBOL is
    forwarded except the single statement `raw` string, per prompt
    contract rule "the raw COBOL source must never appear as fenced
    blocks"; a single-statement operand listing is not a program dump)

Review issues addressed:
  #1  PARTIAL entries are routed through this emitter (needs_llm=True)
      so weak template stubs don't ship to Pass 3.
  #2  Every payload includes the annotation `raw` field so the LLM has
      the original statement text.
  #3  Payload files (`*_llm_requests.jsonl`) are emitted to disk here.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SEMANTIC_PATTERN_ENUM = [
    "guard-with-override",
    "accumulation",
    "state-machine",
    "delegation",
    "sequential",
    "conditional-branch",
    "cics-interaction",
    "file-io",
    "unknown",
]

SYSTEM_PROMPT = (
    "You are a COBOL-to-English semantic annotator. "
    "Given a single COBOL statement and its surrounding annotation context, "
    "produce a single JSON object that matches the schema below. "
    "Respond with ONLY the JSON object, no prose, no code fence, no commentary. "
    "If any required field cannot be determined, use null (for `modifies`) or "
    "`\"unknown\"` (for `semantic_pattern`); do not fabricate. "
    "\n\nRequired response JSON schema (Rule 8 in translation-prompt-contract-v2.md):\n"
    "{\n"
    '  "seq": <int, copy from request>,\n'
    '  "proposition": "<one-sentence English description, imperative voice>",\n'
    '  "modifies": "<fully-qualified data name OR null>",\n'
    '  "reads": ["<fully-qualified data name>", ...],\n'
    '  "semantic_pattern": "<one of: ' + ", ".join(SEMANTIC_PATTERN_ENUM) + '>",\n'
    '  "confidence": <float in [0.0, 1.0]>\n'
    "}\n"
    "\nRule 9: all data names in `modifies` and `reads` must be fully "
    "qualified (e.g., `WS-REISSUE-DATE OF OUT-REISSUE-DATE-BLOCK`). "
    "Bare unqualified tokens are rejected."
)


def build_user_prompt(prop: dict, program_id: str) -> str:
    lines = [
        f"Program ID: {program_id}",
        f"Paragraph: {prop['paragraph']}",
        f"Source line: {prop['line']}",
        f"Seq (copy this into your response): {prop['seq']}",
        f"Verb: {prop['verb']}",
        f"CFG branch context: {prop.get('cfg_branch_context') or '(none)'}",
        f"Raw statement: {prop.get('raw') or '(unavailable)'}",
    ]
    ops = prop.get("operands") or []
    types = prop.get("operand_types") or []
    if ops:
        lines.append("Operands:")
        for o, t in zip(ops, types):
            lines.append(f"  - {o}  (type={t})")
    if prop.get("proposition_source") == "PARTIAL":
        lines.append(
            f"Template produced a PROVISIONAL stub: {prop.get('proposition_stub')!r}. "
            "Produce the final refined proposition \u2014 do not simply repeat the stub."
        )
    if prop.get("operand_unresolved"):
        lines.append(
            "NOTE: at least one operand could not be resolved against the data-items "
            "inventory during Pass 1. Prefer qualified names per Rule 9; if you "
            "cannot qualify a name, include it verbatim and lower confidence."
        )
    return "\n".join(lines)


def build_payload(prop: dict, program_id: str, model: str,
                  max_tokens: int) -> dict[str, Any]:
    """Build a Rule-8-conformant chat-completions payload."""
    return {
        # Routing keys (not part of the wire payload; stripped by dispatcher).
        "_routing": {
            "task_id": "T-2026-04-23-002",
            "program_id": program_id,
            "seq": prop["seq"],
            "paragraph": prop["paragraph"],
            "line": prop["line"],
            "verb": prop["verb"],
            "proposition_source": prop["proposition_source"],
        },
        # Wire payload (Rule 8 envelope).
        "model": model,
        "temperature": 0,
        "seed": 42,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(prop, program_id)},
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Pass 2 LLM request payload emitter")
    ap.add_argument("--propositions", type=Path, required=True,
                    help="Pass 2 propositions JSON (from pass2_template.py)")
    ap.add_argument("--program-id", required=True)
    ap.add_argument("--out", type=Path, required=True,
                    help="Output JSONL file of request payloads")
    ap.add_argument("--model", default="gpt-4o-2024-08-06",
                    help="Model ID to set in the payload. Does not call the endpoint.")
    ap.add_argument("--max-tokens", type=int, default=400)
    args = ap.parse_args()

    propositions = json.loads(args.propositions.read_text())
    targets = [p for p in propositions if p.get("needs_llm")]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as f:
        for p in targets:
            payload = build_payload(p, args.program_id, args.model, args.max_tokens)
            f.write(json.dumps(payload) + "\n")

    # Per-bucket counts for the audit manifest.
    buckets: dict[str, int] = {}
    for p in targets:
        buckets[p["proposition_source"]] = buckets.get(p["proposition_source"], 0) + 1

    stats = {
        "program_id": args.program_id,
        "total_propositions": len(propositions),
        "llm_requests_emitted": len(targets),
        "buckets": buckets,
        "out": str(args.out),
        "envelope": {
            "temperature": 0,
            "seed": 42,
            "response_format": "json_object",
            "max_tokens": args.max_tokens,
            "model": args.model,
        },
    }
    print(json.dumps(stats))
    return 0


if __name__ == "__main__":
    sys.exit(main())
