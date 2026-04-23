# G5 Gate — Phase 3 Review (agent-prepared, awaiting human sign-off)

- **task_id**: T-2026-04-23-001
- **gate**: G5
- **opened**: 2026-04-23T15:50Z
- **status**: STAGED-FOR-HUMAN (no gold file has been promoted; no reviewer has signed)
- **phase_3_candidates**: 5 · **phase_3_blocked**: 1 · **phase_3_promoted**: 0

## Candidate inventory

| Rank (T04) | Candidate | Checklist | T-gate state | Paragraphs for T04 |
|-----------:|-----------|-----------|-------------|-------------------:|
| 1 | `translations/gold-candidate/COMEN01C.md` | `review-checklists/COMEN01C.md` | T01–T03 PASS · T04/T05 DEFERRED | 10 |
| 2 | `translations/gold-candidate/COBSWAIT.md` | `review-checklists/COBSWAIT.md` | T01–T03 PASS · T04/T05 DEFERRED | 0 (single-block) |
| 3 | `translations/gold-candidate/CBCUS01C.md` | `review-checklists/CBCUS01C.md` | T01–T03 PASS · T04/T05 DEFERRED | 7 |
| 4 | `translations/gold-candidate/CBTRN01C.md` | `review-checklists/CBTRN01C.md` | T01–T03 PASS · T04/T05 DEFERRED | 21 |
| 5 | `translations/gold-candidate/COSGN00C.md` | `review-checklists/COSGN00C.md` · **capability-boundary sentinel** | T01–T03 PASS · T04/T05 DEFERRED | 9 |
| — | (not staged) | `review-checklists/CBACT01C.md` | T02-R FAIL on translation-side | 21 (HOLD) |

Total T04 requests covering the staged 5: 47 paragraphs. CBACT01C adds 21 more once it is unblocked.

## Promotion procedure (reviewer executes)

For each candidate:

1. Work through the per-file review checklist against `app/cbl/<FILE>.cbl`.
2. If the candidate clears every item **and** T04 ≥ 0.85 (once the judge batch runs), copy it with `cp translations/gold-candidate/<FILE>.md translations/gold/<FILE>.md` and sign the checklist.
3. If any item fails, tick the "send back for revision" box and open a Phase-1 re-baseline ticket with a pointer to the specific checklist failure.
4. Append a `{"event":"gold_promote","file":"<FILE>.cbl","reviewer":"<handle>","ts":...}` line to `.aifirst/runs/T-2026-04-23-001/run.log` and close this gate in a `G5-phase3-signoff.md` once all 6 files (including CBACT01C once unblocked) are resolved.

## Stop rule

No Phase 4 work (Stream 1/2/3 training-set build, QLoRA fine-tune) begins until:
- at least one file exists under `translations/gold/`, and
- T04 has returned real scores for every promoted file.

## Phase 4 readiness (as of this gate)

| Criterion | Status |
|-----------|--------|
| Any file in `translations/gold/` | ❌ 0 |
| T04 judgments returned | ❌ DEFERRED |
| CBACT01C resolved | ❌ BLOCKED |
| Trajectory pairs extractable | ❌ 0 (depends on T04) |
| **Phase 4 go/no-go** | **NO-GO** |
