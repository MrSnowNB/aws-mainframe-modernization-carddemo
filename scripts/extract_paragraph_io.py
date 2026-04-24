#!/usr/bin/env python3
# LLM-FREE — Deterministic mutates[]/reads[] derivation from COBOL verbs
# LLM-FREE — and operand classification. No LLM inference.
"""
extract_paragraph_io.py — Derive paragraph-level mutates[] and reads[] for v1.2.

Task: T-2026-04-24-001 (Schema v1.2 — Hercules Byte-Parity Foundation)
Gate: G1 (scaffold stub, per RF-07 standalone) → implemented in chunk (d).

Authoritative rules (verbatim from G1-scaffold.md §6.3 / §8.3):

    Writers (append to mutates[]):
      receiver of MOVE, INITIALIZE, SET, ADD ... TO,
        SUBTRACT ... FROM, MULTIPLY ... BY, COMPUTE (LHS),
        STRING ... INTO, UNSTRING ... INTO
    Readers (append to reads[]):
      sender of MOVE/ADD/SUBTRACT/MULTIPLY, RHS of COMPUTE,
        all operands of IF, EVALUATE, DISPLAY,
        STRING source operands, UNSTRING source operand

    C-3 SEARCH / SET table rules (mandatory):
      SET <index> TO <value>           → mutates += [<index>]
      SEARCH <table> ... AT END ...    → mutates += [<index-of-table>]
                                          reads   += [<table>]
      SEARCH ALL <table> ... WHEN ...  → mutates += [<index-of-table>]
                                          reads   += [<table>, <WHEN-operands>]
      SEARCH ... WHEN <condition>      → reads   += [<condition operands>]

    Identifier rule (Rule 9):
      All data-name operands MUST be emitted fully qualified
      (e.g. CUST-REC.CUST-ID, not bare CUST-ID). Deduplicate per paragraph
      before emission; preserve first-occurrence source order.

Inputs  (planned):
  --source app/cbl/<PROGRAM>.cbl   read-only COBOL source (RF-06)
  --cfg    validation/pass1/<PROGRAM>_annotations.json (RF-07 read-only)
  --out    validation/pass1/paragraph_io/<PROGRAM>.json

Output (planned): JSON list with elements:
    {"paragraph": str, "line": int, "mutates": [str], "reads": [str]}

This script is STANDALONE — it does NOT modify scripts/pass1_annotate.py
(T-002 is still in-flight on feat/t-002-llm-phase). RF-07 enforced.

Status: STUB — implementation opens under chunk (d) after G1 close.
"""
from __future__ import annotations

import argparse
import sys

__LLM_FREE__ = True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="extract_paragraph_io.py",
        description=(
            "Derive v1.2 mutates[]/reads[] per paragraph (LLM-FREE). "
            "STUB — see chunk (d)."
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
        "extract_paragraph_io.py — scaffold stub. Implementation lands in "
        "T-2026-04-24-001 chunk (d). See .aifirst/runs/T-2026-04-24-001/G1-scaffold.md "
        "§6.3 / §8.3 for authoritative writer/reader and C-3 SEARCH/SET rules."
    )


if __name__ == "__main__":
    sys.exit(main())
