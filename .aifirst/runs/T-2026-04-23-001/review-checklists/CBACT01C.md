# Phase 3 Review Checklist — CBACT01C.cbl (BLOCKED, not a gold candidate)

- **Baseline path**: `translations/baseline/CBACT01C.md` (no gold candidate staged)
- **Source path**: `app/cbl/CBACT01C.cbl`
- **Source SHA**: `a9a14e021e6fe1c14caa544213d938abd15b6681`
- **Size**: 17 KB · **Subtype**: Batch · **Domain**: Account Management
- **T01 PASS · T02 PASS · T02-R FAIL · T03 PASS (1.0000 after Option A fix) · T04 DEFERRED · T05 DEFERRED**
- **Status**: BLOCKED pending translation-side correction — NOT a Phase 3 review candidate yet.

## Why blocked after validator fix

After Option A validator alignment, CBACT01C's T03 flipped to PASS (84/84 checks, 21/21 01-level items matched). The T02-R failure, however, persisted:

> `Item WS-REISSUE-DATE interpretation[0]: condition does not reference any CFG-known field`

Root cause: the interpretation's `condition` string uses the bare token `ACCT-REISSUE-DATE`, which does not appear in the CFG field inventory (the CFG has `OUT-ACCT-REISSUE-DATE`, `WS-ACCT-REISSUE-DATE`, `WS-ACCT-REISSUE-YYYY`, `VB2-ACCT-REISSUE-YYYY`, but no bare `ACCT-REISSUE-DATE`). The second interpretation uses `WS-ACCT-REISSUE-YYYY` correctly and passes.

This is a **translation-side imprecision**, not a schema ambiguity. Per Hard Rule 5 the agent has NOT edited the translation.

## Human decision required

Choose one path before CBACT01C can enter Phase 3 review:

1. **Re-baseline CBACT01C** — re-run the Phase 1 translator with an explicit instruction to use fully-qualified CFG field names in REDEFINES conditions. Expected change: the first interpretation's condition string refers to `WS-ACCT-REISSUE-DATE` (or `OUT-ACCT-REISSUE-DATE`, whichever is semantically correct at the POPUL-ACCT-RECORD line) instead of the bare form.
2. **Relax T02-R condition-referent check further** — accept partial-token matches (e.g. `ACCT-REISSUE-DATE` substring-matches `WS-ACCT-REISSUE-DATE`). This weakens semantic precision and is not recommended without documenting the trade-off in `COBOL-MD-SCHEMA.md`.
3. **Escalate as a novel failure mode** — log "REDEFINES condition referent unqualified against multiple qualified candidates" to `failure_modes.log` and continue the pipeline without CBACT01C in the first gold batch.

Recommended: path (1). The two-interpretation REDEFINES with one qualified and one unqualified referent suggests the translator defaulted to the shortest available name when multiple qualified variants existed.

## Do not proceed until resolved

- [ ] No file copied from `translations/baseline/CBACT01C.md` to `translations/gold-candidate/` or `translations/gold/`.
- [ ] No T04 judging dispatched for CBACT01C (kept at priority 6 / HOLD in `T04_dispatch_manifest.json`).
- [ ] No entry added to `training/` streams for this file.

## Reviewer sign-off (when path chosen)

- Reviewer: _________________________ · Date: __________
- Path selected: [ ] 1 — re-baseline · [ ] 2 — relax T02-R · [ ] 3 — escalate
- Action ticket filed: _________________________________
