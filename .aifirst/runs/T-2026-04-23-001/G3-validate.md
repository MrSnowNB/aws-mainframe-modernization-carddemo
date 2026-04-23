# G3 Gate — Validate

- **task_id**: T-2026-04-23-001
- **gate**: G3
- **phase**: 2 (validation tiers T01–T05)
- **opened**: 2026-04-23T14:16:50Z
- **closed**: 2026-04-23T14:20:10Z
- **status**: PASS-WITH-BLOCKS (pipeline integrity preserved; 4 files blocked on validator findings for human review; NOTHING was retroactively patched to fake-pass per Hard Rule 5)

## Tier-by-File Matrix

| File | T01 | T02 | T02-R | T03 | T04 | T05 | Verdict |
|------|-----|-----|-------|-----|-----|-----|---------|
| COBSWAIT.cbl | PASS | PASS | PASS (0 REDEFINES) | PASS (1.0000) | DEFERRED | DEFERRED | READY for Phase 3 |
| CBCUS01C.cbl | PASS | PASS | PASS (1 REDEFINES) | **FAIL (0.7692)** | DEFERRED | DEFERRED | BLOCKED |
| COSGN00C.cbl | PASS | PASS | PASS (0 REDEFINES) | **FAIL (0.4000)** | DEFERRED | DEFERRED | BLOCKED |
| COMEN01C.cbl | PASS | PASS | PASS (0 REDEFINES) | PASS (1.0000) | DEFERRED | DEFERRED | READY for Phase 3 |
| CBACT01C.cbl | PASS | PASS | **FAIL**          | **FAIL (0.6512)** | DEFERRED | DEFERRED | BLOCKED |
| CBTRN01C.cbl | PASS | PASS | PASS (1 REDEFINES) | **FAIL (0.7241)** | DEFERRED | DEFERRED | BLOCKED |

## Summary of Findings

**T01 (baseline shape checks):** 6/6 PASS. All baseline translations are valid YAML front-matter + Markdown, contain every required top-level key, expose non-empty `semantic` bodies, and carry no raw COBOL (Hard Rule 1 holds).

**T02 (structural completeness, absolute):** 6/6 PASS. Every paragraph present in the CFG is present in `procedure_paragraphs[]`. Every CFG-level data item that the schema requires (01-level) is present in `data_items[]`.

**T02-R (REDEFINES completeness, absolute):** 5/6 PASS. Only CBACT01C failed. The two `WS-REISSUE-DATE` interpretation entries pass the 2-entry-minimum, `condition`/`interpreted_as`/`encoding` presence and content checks, but their condition strings reference `ACCT-REISSUE-DATE` and `WS-ACCT-REISSUE-YYYY`, which are sub-fields of group items and therefore are deliberately not surfaced in the 01-only `data_items[]` per COBOL-MD-SCHEMA.md §Data Layer. The validator as written enforces *"`condition` values reference an actual field present in `data_items[]`"* (COBOL-MD-SCHEMA.md line 211) literally. The translation is semantically correct; the validator/schema pair contains an ambiguity. NO retro-patching was performed.

**T03 (functional score, threshold ≥0.95):** 2/6 PASS (COBSWAIT, COMEN01C). The four failures share a single root cause: `scripts/validate_t03.py` iterates `cfg.data_items[]` (which enumerates every CFG-observed data item at every level, including 05/10/15 sub-fields and FD record descriptors) and checks each for presence in the MD's `data_items[]`. The MD schema explicitly restricts `data_items[]` to 01-level working-storage items. These failures are validator-vs-schema mismatches, not translation defects. NO scores were fabricated or adjusted.

**T04 (semantic, threshold ≥0.85):** 6/6 DEFERRED. No LLM-as-judge endpoint is configured in this sandbox. `score_t04.py` emitted per-paragraph judging-request payloads to `validation/reports/<F>_T04_requests.json` so a human operator can dispatch the judge out-of-band.

**T05 (SWE-bench Lite regression):** DEFERRED (global). SWE-bench Lite not available.

## Hard Rules Audit

1. No raw COBOL source in any translated `.md` — verified by `validate_t01.py` source-leak check; 6/6 PASS.
2. `validation` block in every MD front-matter remains all `PENDING` — inspected manually; confirmed.
3. Phase 2 output files (`validation/reports/*_T0{1,2,2R,3,4}.json`, `T05_global.json`) exist on disk before gate close — verified.
4. Phase 3 hard-stop is enforced by G4 gate file (next); no gold file is being self-certified.
5. No synthetic judgments or placeholder scores were written; T04/T05 are explicitly DEFERRED.
6. Every tier event above is appended to `run.log` at the time it ran.

## Artifacts

- `validation/reports/*_T01.json` (6 files)
- `validation/reports/*_T02.json` (6 files)
- `validation/reports/*_T02R.json` (6 files)
- `validation/reports/*_T03.json` (6 files)
- `validation/reports/*_T04.json` (6 DEFERRED stubs)
- `validation/reports/*_T04_requests.json` (6 paragraph-level judging-request payloads)
- `validation/reports/T05_global.json` (DEFERRED)

## Next Gate

G4 will open immediately and close with a Phase-3 HARD-STOP notice. Per MASTER-ARCHITECTURE §4 and §7 Rule 6, the agent does not self-certify gold translations. The 2 READY files and 4 BLOCKED files are handed to human review as detailed in `COMPLETION-REPORT.md`.
