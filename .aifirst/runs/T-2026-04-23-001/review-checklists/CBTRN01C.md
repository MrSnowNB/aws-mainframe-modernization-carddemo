# Phase 3 Review Checklist — CBTRN01C.cbl

- **Candidate path**: `translations/gold-candidate/CBTRN01C.md`
- **Source path**: `app/cbl/CBTRN01C.cbl`
- **Source SHA**: `6494be3b695bd33f27b39f8d13dc5b510f92b7ed`
- **Size**: 18 KB · **Subtype**: Batch · **Domain**: Transaction Processing
- **Est. review time**: 90 min
- **T01 PASS · T02 PASS · T02-R PASS (1 REDEFINES: TWO-BYTES-ALPHA) · T03 PASS (1.0000, validator v1.0.1-option-a) · T04 DEFERRED · T05 DEFERRED**

## 1. Factual accuracy (against source)
- [ ] All 21 paragraphs accounted for (open/read/validate/write/close, daily-transaction processing, abend handler `Z-ABEND-PROGRAM`, etc.).
- [ ] Three file sets (DALYTRAN-FILE, TRANSACT-FILE, reject flow) correctly identified with distinct FD sections.
- [ ] Reject-file writing, counters (`WS-RECORDS-PROCESSED`, `WS-RECORDS-REJECTED`), and end-of-job DISPLAY totals all represented.

## 2. REDEFINES coverage (HIGHEST EXPERTISE BAR)
- [ ] `TWO-BYTES-ALPHA` redefines `TWO-BYTES-BINARY`; 2 `redefines_interpretations[]` entries present.
- [ ] Each interpretation has non-empty `condition`, `interpreted_as`, `encoding`.
- [ ] Conditions reference real CFG-known fields (e.g., `WS-IO-STATUS`, `TWO-BYTES-LEFT`, `TWO-BYTES-RIGHT`).
- [ ] Interpretations semantically differentiate the binary/RC view from the alpha/status-byte view.

## 3. Business rules completeness
- [ ] 13 rules cover: file-open verification for all 3 files, per-record read/validate loop, reject criteria, counter bookkeeping, end-of-job summary, abend path (`Z-ABEND-PROGRAM` → `CEE3ABD`), and the date/amount/format validations surfaced in Phase 1.
- [ ] No validation rule is described that is not actually enforced by the source.

## 4. Abend path integrity
- [ ] `Z-ABEND-PROGRAM` is correctly marked terminal (no PERFORM return) and wires `CEE3ABD` with the correct ABEND-CODE and REASON-CODE fields.
- [ ] `calls_to[]` contains `CEE3ABD` with the correct guard condition.

## 5. CFG / dead-code audit
- [ ] Any paragraph flagged `dead_code_flag: true` is actually unreachable in source.
- [ ] If Cobol-REKT scope-terminator phantoms survived into the MD, each is annotated as such in its `semantic` field.
- [ ] No GOTOs present (CFG confirmed); any `goto_flag: true` on a paragraph is a real GOTO, not a tool artefact.

## 6. Semantic density
- [ ] Paragraph semantics read as transaction-validation intent ("reject stale transactions", "accumulate daily totals"), not verb-by-verb narration.
- [ ] `WS-RECORDS-*` counters are described in terms of their business role, not just their PICs.

## 7. Hallucination check
- [ ] No invented paragraphs, FD sections, or callees.
- [ ] No inferred DB2 / VSAM features that are not in the source.
- [ ] Cobol-REKT `performs` globality not propagated verbatim.

## 8. Hard-rule audit
- [ ] No raw COBOL source embedded.
- [ ] `validation` block is all `PENDING`.

## Sign-off
- Reviewer: _________________________ · Date: __________
- Decision: [ ] Promote to `translations/gold/CBTRN01C.md` · [ ] Send back for revision
- T04 judge result attached: [ ] yes (21 paragraphs) · [ ] no
