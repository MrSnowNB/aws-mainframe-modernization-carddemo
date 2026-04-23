# G4 Gate — Addendum (human sign-off received 2026-04-23T15:36Z)

- **task_id**: T-2026-04-23-001
- **gate**: G4 (re-opened)
- **reopened**: 2026-04-23T15:36Z
- **closed**: 2026-04-23T15:50Z
- **status**: PASS — Phase 3 curation authorised and executed for READY files; CBACT01C held back.

## Human authorisation on record

The human reviewer signed off on:
1. **Option A validator fix** — filter `cfg.data_items[]` to level-01 only in `validate_t03.py`; broaden the T02-R condition-referent check to accept any CFG-known field name at any level.
2. **Phase 3 gold-candidate staging** for files passing the re-run.
3. **T04 dispatch manifest** in the specified priority order.
4. **CBACT01C hold** until the re-baseline vs validator-relaxation vs escalate decision is taken.

## Actions taken under this authorisation

- Patched `scripts/validate_t02r.py` and `scripts/validate_t03.py` to validator version `v1.0.1-option-a`. All changes are self-documented inline.
- Re-ran T02-R and T03 on all 6 files. Results recorded in `validation/reports/*_T02R.json` and `*_T03.json` (files overwritten, every event appended to `run.log` with `"iteration":2`).
- Staged Phase 3 gold candidates at `translations/gold-candidate/{COBSWAIT,COMEN01C,CBCUS01C,CBTRN01C,COSGN00C}.md` — unmodified copies of the corresponding baselines.
- Did NOT stage `translations/gold-candidate/CBACT01C.md` — see §CBACT01C below.
- Wrote per-file review checklists to `.aifirst/runs/T-2026-04-23-001/review-checklists/{FILE}.md` (6 files; CBACT01C's checklist is a block notice rather than a review checklist).
- Wrote T04 dispatch manifest to `validation/reports/T04_dispatch_manifest.json` in the priority order the reviewer specified (COMEN01C → COBSWAIT → CBCUS01C → CBTRN01C → COSGN00C; CBACT01C at #6 = HOLD).

## Re-run matrix after Option A fix

| File | T02-R | T03 score | 01-level items | Total CFG items | Verdict |
|------|-------|-----------|---------------:|----------------:|---------|
| COBSWAIT | PASS | 1.0000 | 2 | 2 | READY |
| COMEN01C | PASS | 1.0000 | 2 | 16 | READY |
| CBCUS01C | PASS | 1.0000 | 10 | 22 | READY |
| CBTRN01C | PASS | 1.0000 | 21 | 55 | READY |
| COSGN00C | PASS | 1.0000 | 2 | 14 | READY |
| CBACT01C | **FAIL** | 1.0000 | 21 | 66 | BLOCKED |

## CBACT01C disposition

T02-R remained FAIL after the Option A fix because the defect is on the translation side, not the validator/schema side:

- `WS-REISSUE-DATE.redefines_interpretations[0].condition` uses the bare token `ACCT-REISSUE-DATE`. The CFG contains `OUT-ACCT-REISSUE-DATE`, `WS-ACCT-REISSUE-DATE`, `WS-ACCT-REISSUE-YYYY`, and `VB2-ACCT-REISSUE-YYYY`, but no bare `ACCT-REISSUE-DATE`.
- `interpretation[1]` uses `WS-ACCT-REISSUE-YYYY` and passes. The problem is isolated to the first entry.

Per Hard Rule 5 the agent has NOT edited the translation. CBACT01C is documented in `review-checklists/CBACT01C.md` with three reviewer options (re-baseline, relax the check further, or escalate). Recommended path: re-baseline.

## Hard Rules re-audit (post-sign-off)

1. No raw COBOL source in any `.md` — 5 gold candidates inherit from baselines already passing T01 source-leak; re-spot-checked.
2. `validation` blocks in every MD remain all `PENDING`.
3. Phase-3 output files (gold-candidate MDs + review checklists + T04 manifest) exist on disk before this gate was closed.
4. Phase 3 gold promotion still awaits human verification per the checklists — the agent has prepared candidates, not promoted them.
5. No synthetic judgments, no fabricated scores. The Option A patch changed the denominator of T03, not the scoring math; the re-run numbers are genuine.
6. Every tier, step, and gate event under this addendum is appended to `run.log` as it occurred.

## Next gate

G5 — Phase 3 human review — opens on receipt of any reviewer-signed checklist. Phase 4 readiness is re-stated in the updated `COMPLETION-REPORT.md`.
