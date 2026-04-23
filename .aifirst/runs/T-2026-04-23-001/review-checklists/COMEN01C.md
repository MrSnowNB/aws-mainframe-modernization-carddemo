# Phase 3 Review Checklist — COMEN01C.cbl

- **Candidate path**: `translations/gold-candidate/COMEN01C.md`
- **Source path**: `app/cbl/COMEN01C.cbl`
- **Source SHA**: `a404313748b0715a306336ac599b3e585697c05c`
- **Size**: 12 KB · **Subtype**: Menu · **Domain**: Administration
- **Est. review time**: 45 min
- **T01 PASS · T02 PASS · T02-R PASS (0 REDEFINES) · T03 PASS (1.0000, validator v1.0.1-option-a) · T04 DEFERRED · T05 DEFERRED**

## 1. Factual accuracy (against source)
- [ ] All 10 paragraphs (0000-MAIN, 1000-SEND-MENU-SCREEN, 1100-RECEIVE-MAP, 2000-PROCESS-ENTER-KEY, 9000-SEND-MAP, 9100-WRITE-PROCESSING-MESSAGE, 9200-SEND-MENU-WITH-ERRORS, 9999-RETURN-XCTL, etc.) match source.
- [ ] EIBCALEN / DFHEIBLK handling described at `0000-MAIN` level.
- [ ] Transaction ID `CM00` recorded.

## 2. REDEFINES coverage
- [ ] N/A — 0 REDEFINES.

## 3. CICS control flow
- [ ] Table-driven dispatch via `CDEMO-MENU-OPT-PGMNAME(WS-OPTION)` is represented as TWO `calls_to[]` entries (NORMAL-returning INQUIRE branch and non-DUMMY/non-COPAUS0C branch).
- [ ] `EXEC CICS XCTL` to `COSGN00C` on (a) `EIBCALEN = 0` and (b) `PF3` pressed is captured.
- [ ] The `EXEC CICS INQUIRE PROGRAM` guard in front of each XCTL is described in `business_rules[]`.
- [ ] PF-key handling (ENTER, PF3, invalid keys) is complete.

## 4. Business rules completeness
- [ ] 10 rules cover: first-time initialization, admin-vs-user menu variants, option validity, disabled options, program-inquiry error, COPAUS0C special path, XCTL vs RETURN, error-message rendering, pseudo-conversational RETURN with COMMAREA, and EIBCALEN bootstrap.
- [ ] No rule fabricated (e.g., no claim of DB2 access — this is a pure menu driver).

## 5. Dead-code / CFG artefact audit
- [ ] Any paragraph flagged `dead_code_flag: true` in the MD corresponds to a true dead-code path in the source — NOT a Cobol-REKT scope-terminator artefact (`END-IF`, `END-EXEC`, `END-EVALUATE`).
- [ ] If the baseline retained scope-terminator phantoms from the CFG, confirm they are annotated as such in the paragraph's `semantic` field.

## 6. Semantic density
- [ ] Paragraph semantics read as menu-navigation intent, not BMS map mechanics.
- [ ] `COMMAREA` and `CDEMO-FROM-PROGRAM` / `CDEMO-FROM-TRANID` context is present at the right abstraction.

## 7. Hallucination check
- [ ] No invented paragraphs, fields, or callees.
- [ ] `calls_to[]` matches source; note that two entries use the literal `CDEMO-MENU-OPT-PGMNAME(WS-OPTION)` as the program expression — confirm this is intentional and documented.
- [ ] Anomaly reminder (from subagent self-check): Cobol-REKT's `performs` lists are global-within-program, not per-paragraph — verify the baseline doesn't naively propagate that.

## 8. Hard-rule audit
- [ ] No raw COBOL source embedded in the MD.
- [ ] `validation` block is all `PENDING`.

## Sign-off
- Reviewer: _________________________ · Date: __________
- Decision: [ ] Promote to `translations/gold/COMEN01C.md` · [ ] Send back for revision
- T04 judge result attached: [ ] yes (10 paragraphs) · [ ] no
