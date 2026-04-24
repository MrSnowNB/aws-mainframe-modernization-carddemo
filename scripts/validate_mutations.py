#!/usr/bin/env python3
# LLM-FREE — Deterministic validator (T-PASS1-MUT). No LLM inference.
"""
validate_mutations.py — T-PASS1-MUT (100% blocking).

Task: T-2026-04-24-001 (Schema v1.2 — Hercules Byte-Parity Foundation)
Gate: G2 (implementation in chunk (g)). G1 status: STUB.

Authoritative checks (verbatim from G1-scaffold.md §6.3 / §8.3 / C-3):

  1. Every paragraph present in the CFG annotations MUST have a
     paragraph_io record (may be empty mutates/reads, not missing).
  2. Every name in mutates[] and reads[] MUST be fully qualified
     (Rule 9). Bare names → pass=false.
  3. mutates[] ∩ reads[] may be non-empty (e.g. COMPUTE X = X + 1),
     but each list individually MUST be deduplicated.
  4. Writer-verb receivers present in mutates[]:
       MOVE .. TO <r>, INITIALIZE <r>, SET <r> TO ...,
       ADD .. TO <r>, SUBTRACT .. FROM <r>, MULTIPLY .. BY <r>,
       COMPUTE <r> = ..., STRING .. INTO <r>, UNSTRING .. INTO <r>.
  5. Reader operands present in reads[]:
       senders of the above; all operands of IF, EVALUATE, DISPLAY;
       RHS operands of COMPUTE.
  6. C-3 SEARCH / SET table rules:
       SET <i> TO .....................→ <i> ∈ mutates
       SEARCH <t> AT END/WHEN .........→ <index-of-t> ∈ mutates,
                                         <t> ∈ reads,
                                         WHEN operands ∈ reads
       SEARCH ALL <t> WHEN ............→ same as above

  Any miss → tier=T-PASS1-MUT, pass=false. 100% blocking.

Inputs  (planned):
  --paragraph-io validation/pass1/paragraph_io/<PROGRAM>.json (extractor output)
  --cfg          validation/pass1/<PROGRAM>_annotations.json (read-only, RF-07)
  --out          validation/pass1/paragraph_io/<PROGRAM>.report.json

Status: STUB — implementation opens under chunk (g) after chunk (f) close.
"""
from __future__ import annotations

import argparse
import sys

__LLM_FREE__ = True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="validate_mutations.py",
        description="T-PASS1-MUT 100%-blocking validator (LLM-FREE). STUB — see chunk (g).",
    )
    parser.add_argument("--paragraph-io", required=False, help="paragraph_io JSON (input)")
    parser.add_argument("--cfg", required=False, help="Pass 1 annotations (read-only)")
    parser.add_argument("--out", required=False, help="Report JSON path")
    parser.parse_args(argv)
    raise NotImplementedError(
        "validate_mutations.py — scaffold stub. Implementation lands in "
        "T-2026-04-24-001 chunk (g). T-PASS1-MUT is 100% blocking. "
        "C-3 SEARCH/SET rules apply."
    )


if __name__ == "__main__":
    sys.exit(main())
