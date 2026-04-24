#!/usr/bin/env python3
# LLM-FREE — Deterministic paragraph fall-through derivation from COBOL source
# LLM-FREE — and Pass 1 annotations. No LLM inference.
"""
extract_fallthrough.py — Derive paragraph-level fall-through[] for v1.2.

Task: T-2026-04-24-001 (Schema v1.2 — Hercules Byte-Parity Foundation)
Gate: G1 (scaffold stub, per RF-07 standalone) → implemented in chunk (c).

Authoritative rule (verbatim from G1-scaffold.md §6.2 / §8.2):

    For each paragraph P, inspect the LAST verb emitted in P:
      GO TO ...                 → terminator = goto
      STOP RUN                  → terminator = stop-run
      GOBACK                    → terminator = goback
      EXIT PROGRAM              → terminator = explicit-exit
      EXEC CICS RETURN END-EXEC → terminator = cics-return
      EXEC CICS XCTL    END-EXEC→ terminator = cics-xctl
      (none of above)           → terminator = implicit,
                                  falls_through_to = next-paragraph-in-source-order
      Last paragraph in program with no explicit terminator
                                → terminator = implicit-end-of-program

C-5 (RF-04) mandatory assertion:
    For every consecutive paragraph pair (P_n, P_{n+1}) in source order:
        P_{n+1}.line > P_n.line
    If this guard fails anywhere, emit BLOCKED and halt. This prevents
    mis-ordering caused by stale CFG or reordered source.

Inputs  (planned):
  --source app/cbl/<PROGRAM>.cbl   read-only COBOL source (RF-06)
  --cfg    validation/pass1/<PROGRAM>_annotations.json (RF-07 read-only)
  --out    validation/pass1/fallthrough/<PROGRAM>.json

Output (planned): JSON list with elements:
    {"paragraph": str, "line": int, "terminator": str,
     "falls_through_to": str|None, "last_verb": str}

This script is STANDALONE — it does NOT modify scripts/pass1_annotate.py
(T-002 is still in-flight on feat/t-002-llm-phase). RF-07 enforced.

Status: STUB — implementation opens under chunk (c) after G1 close.
"""
from __future__ import annotations

import argparse
import sys

__LLM_FREE__ = True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="extract_fallthrough.py",
        description=(
            "Derive v1.2 fall_through[] (LLM-FREE). STUB — see chunk (c)."
        ),
    )
    parser.add_argument("--source", required=False, help="COBOL source file (read-only)")
    parser.add_argument(
        "--cfg",
        required=False,
        help="Pass 1 annotations JSON (read-only, RF-07)",
    )
    parser.add_argument("--out", required=False, help="Output JSON path")
    parser.parse_args(argv)
    raise NotImplementedError(
        "extract_fallthrough.py — scaffold stub. Implementation lands in "
        "T-2026-04-24-001 chunk (c). See .aifirst/runs/T-2026-04-24-001/G1-scaffold.md "
        "§6.2 / §8.2 for authoritative fall-through rules and C-5 source-order assertion."
    )


if __name__ == "__main__":
    sys.exit(main())
