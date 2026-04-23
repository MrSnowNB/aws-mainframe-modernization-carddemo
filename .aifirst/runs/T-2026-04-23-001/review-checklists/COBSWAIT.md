# Phase 3 Review Checklist — COBSWAIT.cbl

- **Candidate path**: `translations/gold-candidate/COBSWAIT.md`
- **Source path**: `app/cbl/COBSWAIT.cbl`
- **Source SHA**: `7957347717cf04be2dc4f5be24aa94668cf780ab`
- **Size**: 2 KB · **Subtype**: Utility · **Domain**: Utility
- **Est. review time**: 10 min
- **T01 PASS · T02 PASS · T02-R PASS (0 REDEFINES) · T03 PASS (1.0000) · T04 DEFERRED · T05 DEFERRED**

## 1. Factual accuracy (against source)
- [ ] Single paragraph `MAIN-PARA` behaviour faithfully described (10-sec wait then GOBACK).
- [ ] `STATIC` call to `MVSWAIT` with length `WS-TIME-OUT` = `00000000010` captured.
- [ ] No behaviour invented or omitted.

## 2. REDEFINES coverage
- [ ] N/A — file has zero REDEFINES clauses (CFG confirms).

## 3. Business rules completeness
- [ ] The 2 rules in `business_rules[]` cover (a) the fixed 10-second wait duration and (b) the use of `MVSWAIT` as the wait primitive.
- [ ] No additional implicit rule is missing (e.g., unconditional success return code).

## 4. Semantic density
- [ ] `semantic` paragraphs read as intent, not mechanics (e.g., "pause batch job for 10 seconds" rather than "call MVSWAIT with X(11) parameter").
- [ ] No line-by-line narration of COBOL verbs.

## 5. Hallucination check
- [ ] No paragraph exists in the MD that is absent from the source.
- [ ] No field exists in `data_items[]` that is absent from the source.
- [ ] `calls_to[]` contains only `MVSWAIT` (no fabricated callees).

## 6. Hard-rule audit
- [ ] No raw COBOL source embedded in the MD.
- [ ] `validation` block is all `PENDING`.

## Sign-off
- Reviewer: _________________________ · Date: __________
- Decision: [ ] Promote to `translations/gold/COBSWAIT.md` · [ ] Send back for revision
- T04 judge result attached: [ ] yes (0 paragraphs required — single-block file) · [ ] n/a
