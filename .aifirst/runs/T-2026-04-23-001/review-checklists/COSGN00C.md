# Phase 3 Review Checklist — COSGN00C.cbl

- **Candidate path**: `translations/gold-candidate/COSGN00C.md`
- **Source path**: `app/cbl/COSGN00C.cbl`
- **Source SHA**: `c3e7f8e4fb96466d3822ad82ceda8a96fb555d78`
- **Size**: 10 KB · **Subtype**: CICS-Online · **Domain**: Administration
- **Est. review time**: 50 min
- **T01 PASS · T02 PASS · T02-R PASS (0 REDEFINES) · T03 PASS (1.0000, validator v1.0.1-option-a) · T04 DEFERRED · T05 DEFERRED**
- **⚠ CAPABILITY-BOUNDARY SENTINEL**: COSGN00C is the file to watch in the T04 batch. Its pre-fix T03 score of 0.40 was validator-induced (only 2 of 14 CFG items were 01-level; after filter, score flipped to 1.0). A low T04 result here would be the first real signal that the model struggles on CICS-Online programs, independent of the schema ambiguity. Reviewer should give extra weight to semantic fidelity on the sign-on flow and VSAM user-record handling.

## 1. Factual accuracy (against source)
- [ ] All 9 paragraphs accounted for (0000-MAIN, 1000-SEND-MAP, 1100-RECEIVE-MAP, 1200-PROCESS-ENTER-KEY, 1210-READ-USER-SEC-FILE, 2000-SEND-ERROR-MAP, 9000-RETURN-XCTL, etc.).
- [ ] Sign-on screen send/receive via BMS map (`COSGN0A`) is described.
- [ ] VSAM READ of `USRSEC01` keyed on `USER-ID` with matching on `USER-PWD` correctly represented.

## 2. REDEFINES coverage
- [ ] N/A — 0 REDEFINES.

## 3. CICS control flow
- [ ] `calls_to[]` contains exactly two XCTL targets: `COADM01C` (admin branch) and `COMEN01C` (regular-user branch), each with the correct `CDEMO-USRTYP-*` condition.
- [ ] Transaction ID `CC00` recorded.
- [ ] PF3 / Clear key handling and retry-on-error flow captured.

## 4. Business rules completeness (12 rules)
- [ ] Rules cover: empty-field validation (USER-ID and PASSWORD), password mismatch handling, user-not-found handling (VSAM NOTFND), admin vs regular branching, retry loop after error, first-entry (EIBCALEN = 0) behaviour, CICS RETURN semantics, error-message display, and screen-initialisation on entry.
- [ ] No rule fabricated about audit-logging, lockout, or session-timeout that doesn't exist in source.

## 5. CFG / dead-code audit
- [ ] The 3 "dead-code" paragraphs flagged during Phase 1 as Cobol-REKT scope-terminator artefacts (`END-IF`, `END-EXEC`, `END-EVALUATE`) are either (a) absent from the MD, or (b) retained with `dead_code_flag: true` and a `semantic` note stating they are CFG-tool artefacts.
- [ ] Any other paragraph flagged dead corresponds to true dead code in source.

## 6. XCTL completeness (Phase 1 anomaly)
- [ ] The original CFG emitted an empty `calls_to[]`; XCTL targets were filled in by manual source review during Phase 1. Reviewer must independently verify these two XCTL entries against source.
- [ ] The source uses `DFHCOMMAREA`; baseline must describe COMMAREA length semantics without inventing fields.

## 7. Semantic density
- [ ] Paragraphs read as authentication intent ("validate user and route to admin or regular menu"), not BMS map mechanics.
- [ ] VSAM response-code handling described by business meaning, not literal RESP values.

## 8. Hallucination check
- [ ] No invented callees beyond `COADM01C` and `COMEN01C`.
- [ ] No invented database/DB2 operations (program is VSAM-only).
- [ ] Cobol-REKT global `performs` list not propagated verbatim.

## 9. Hard-rule audit
- [ ] No raw COBOL source embedded.
- [ ] `validation` block is all `PENDING`.

## Sign-off
- Reviewer: _________________________ · Date: __________
- Decision: [ ] Promote to `translations/gold/COSGN00C.md` · [ ] Send back for revision
- T04 judge result attached: [ ] yes (9 paragraphs) · [ ] no
- **Capability-boundary note recorded if T04 < 0.85**: [ ] yes · [ ] n/a
