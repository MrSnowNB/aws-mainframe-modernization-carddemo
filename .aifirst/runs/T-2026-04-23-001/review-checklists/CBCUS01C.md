# Phase 3 Review Checklist — CBCUS01C.cbl

- **Candidate path**: `translations/gold-candidate/CBCUS01C.md`
- **Source path**: `app/cbl/CBCUS01C.cbl`
- **Source SHA**: `88a99d7fc534579e538c438a4860e72ec068730c`
- **Size**: 7 KB · **Subtype**: Batch · **Domain**: Customer Management
- **Est. review time**: 40 min
- **T01 PASS · T02 PASS · T02-R PASS (1 REDEFINES: TWO-BYTES-ALPHA) · T03 PASS (1.0000, validator v1.0.1-option-a) · T04 DEFERRED · T05 DEFERRED**

## 1. Factual accuracy (against source)
- [ ] All 7 paragraphs (0000-CUSTFILE-OPEN, 1000-CUSTFILE-GET-NEXT, 9000-CUSTFILE-CLOSE, 9999-ABEND-OF-JOB, plus display/error handlers) match source.
- [ ] File definition (FD CUSTFILE with customer record layout) is described at the semantic level.
- [ ] DD names and ACCESS MODE captured at an appropriate abstraction.

## 2. REDEFINES coverage (HIGHEST EXPERTISE BAR)
- [ ] `TWO-BYTES-ALPHA` redefines `TWO-BYTES-BINARY`; 2 `redefines_interpretations[]` entries present.
- [ ] Each interpretation has non-empty `condition`, `interpreted_as`, `encoding`.
- [ ] Condition strings reference real CFG-known field names.
- [ ] Interpretations semantically distinguish the binary I/O-status view from the alpha RC-decoding view.

## 3. Business rules completeness
- [ ] 7 rules cover: sequential read loop, EOF detection, file-open verification, file-close verification, I/O status handling via TWO-BYTES split, abend path via `CEE3ABD`, and the `ADD 8 TO ZERO GIVING APPL-RESULT` idiom.
- [ ] The `ADD 8 TO ZERO GIVING APPL-RESULT` idiom (9000-CUSTFILE-CLOSE) is surfaced as a rule **and** flagged as a COBOL idiom rather than a bug.

## 4. Known source defect acknowledgement
- [ ] The duplicate `DISPLAY` inside `1000-CUSTFILE-GET-NEXT` (flagged during Phase 1) is documented in a `business_rules[]` entry or semantic note as a source-side defect; the MD should NOT silently "fix" it.

## 5. CFG / dead-code audit
- [ ] The CFG-marked-unreachable `GOBACK` (known tool artefact) is represented correctly — i.e. NOT marked `dead_code_flag: true` if the paragraph is in fact reachable from the main loop.
- [ ] Any paragraph flagged dead corresponds to true dead code in the source.

## 6. Semantic density
- [ ] Paragraphs read as "read next customer record / handle EOF / close cleanly" intent, not COBOL verb narration.
- [ ] `semantic` fields avoid restating picture clauses or numeric literals unless they encode business meaning.

## 7. Hallucination check
- [ ] `calls_to[]` contains only `CEE3ABD` with the correct guard condition (APPL-RESULT neither 0 nor 16).
- [ ] No invented fields, paragraphs, or I/O operations.
- [ ] Cobol-REKT `performs` lists not propagated verbatim if they are global-within-program artefacts.

## 8. Hard-rule audit
- [ ] No raw COBOL source embedded.
- [ ] `validation` block is all `PENDING`.

## Sign-off
- Reviewer: _________________________ · Date: __________
- Decision: [ ] Promote to `translations/gold/CBCUS01C.md` · [ ] Send back for revision
- T04 judge result attached: [ ] yes (7 paragraphs) · [ ] no
