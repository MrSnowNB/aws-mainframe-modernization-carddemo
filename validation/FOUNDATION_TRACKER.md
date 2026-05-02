# Validation Foundation Tracker

> **Living document** — update this file whenever a pipeline stage completes for any program.
> Last updated: 2026-05-02 | Gate baseline: 8/8 PASS (all programs with `.md` pass gate)

---

## Pipeline Layers

```
Layer 1  Source           app/cbl/*.cbl + app/cpy/*.cpy   (authoritative — never changes)
Layer 2  Static Analysis  Cobol-REKT CFG  →  validation/structure/<PROG>_cfg.json
                          GnuCOBOL compile check  (syntax gate, local metal only)
Layer 3  Ground Truth     extract_cfg_summary.py  →  validation/structure/<PROG>_cfg.json
                          extract_ground_truth.py →  validation/logs/gt_*.log
Layer 4  LLM Claims       translations/gold-candidate/<PROG>.md
Layer 5  Gate             extract_md_claims.py + gate_compare.py
```

**Trust rule:** a program is only "fully trusted" when Layers 2 → 5 are all metal-derived and committed.
A gate PASS achieved via suppression (0-paragraph CICS programs) or with no REKT report is flagged ⚠️.

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Complete and committed |
| ❌ | Not done |
| ⚠️ | Partial / caveat — see Notes |
| — | Not applicable |

---

## Full Program Inventory (28 source files)

### Batch Programs — CB prefix

| Program | Type | REKT ran | CFG JSON | `.md` exists | Gate PASS | Fully Trusted | Notes |
|---------|------|:--------:|:--------:|:------------:|:---------:|:-------------:|-------|
| CBACT01C | Batch/VSAM | ✅ | ✅ | ✅ | ✅ | ✅ | 16 paragraphs, 21 L01 items |
| CBACT02C | Batch/VSAM | ✅ | ✅ | ✅ | ✅ | ✅ | 5 paragraphs, 10 L01 items |
| CBACT03C | Batch/VSAM | ✅ | ✅ | ✅ | ✅ | ✅ | 5 paragraphs, 10 L01 items |
| CBACT04C | Batch/VSAM | ✅ | ✅ | ❌ | — | ⚠️ | 22 paragraphs, 24 L01 items — CFG ready, no `.md` yet |
| CBCUS01C | Batch/VSAM | ✅ | ✅ | ✅ | ✅ | ✅ | 5 paragraphs, 10 L01 items |
| CBEXPORT | Batch | ❌ | ❌ | ❌ | — | ❌ | Not started |
| CBIMPORT | Batch | ❌ | ❌ | ❌ | — | ❌ | Not started |
| CBSTM03A | Batch | ❌ | ❌ | ❌ | — | ❌ | Not started |
| CBSTM03B | Batch | ❌ | ❌ | ❌ | — | ❌ | Not started |
| CBTRN01C | Batch/VSAM | ✅ | ✅ | ✅ | ✅ | ✅ | 18 paragraphs, 21 L01 items |
| CBTRN02C | Batch/VSAM | ❌ | ❌ | ❌ | — | ❌ | Not started — large file (58 KB) |
| CBTRN03C | Batch/VSAM | ❌ | ❌ | ❌ | — | 
❌ | Not started — large file (52 KB) |

### CICS Online Programs — CO prefix

| Program | Type | REKT ran | CFG JSON | `.md` exists | Gate PASS | Fully Trusted | Notes |
|---------|------|:--------:|:--------:|:------------:|:---------:|:-------------:|-------|
| COACTUPC | CICS | ❌ | ❌ | ❌ | — | ❌ | Not started — very large (182 KB) |
| COACTVWC | CICS | ❌ | ❌ | ❌ | — | ❌ | Not started — large (74 KB) |
| COADM01C | CICS | ❌ | ❌ | ❌ | — | ❌ | Not started |
| COBIL00C | CICS | ❌ | ❌ | ❌ | — | ❌ | Not started |
| COBSWAIT | Batch (inline) | ✅ | ✅ (0 para) | ✅ | ✅ | ⚠️ | Trivial — 0 real paragraphs, 1 synthetic (MAIN-INLINE), 2 L01 items |
| COCRDLIC | CICS | ❌ | ❌ | ❌ | — | ❌ | Not started — large (117 KB) |
| COCRDSLC | CICS | ❌ | ❌ | ❌ | — | ❌ | Not started — large (71 KB) |
| COCRDUPC | CICS | ❌ | ❌ | ⚠️ | — | ❌ | `.md` stub exists (0 paragraphs in GT); no REKT report |
| COMEN01C | CICS/Menu | ✅ | ✅ | ✅ | ✅ (suppressed) | ⚠️ | REKT ran — 7 reachable paragraphs, 3 scope terminators suppressed (RC8). Gate PASS confirmed. Full paragraph validation pending. |
| CORPT00C | CICS | ❌ | ❌ | ❌ | — | ❌ | Not started |
| COSGN00C | CICS/Signon | ✅ | ✅ | ✅ | ✅ (suppressed) | ⚠️ | REKT ran — 6 reachable paragraphs, 3 scope terminators suppressed (RC8). Gate PASS confirmed. Full paragraph validation pending. |
| COTRN00C | CICS | ❌ | ❌ | ❌ | — | ❌ | Not started |
| COTRN01C | CICS | ❌ | ❌ | ❌ | — | ❌ | Not started |
| COTRN02C | CICS | ❌ | ❌ | ❌ | — | ❌ | Not started |
| COUSR00C | CICS | ❌ | ❌ | ❌ | — | ❌ | Not started |
| COUSR01C | CICS | ❌ | ❌ | ❌ | — | ❌ | Not started |
| COUSR02C | CICS | ❌ | ❌ | ❌ | — | ❌ | Not started |
| COUSR03C | CICS | ❌ | ❌ | ❌ | — | ❌ | Not started |

### Utility Programs — CS prefix

| Program | Type | REKT ran | CFG JSON | `.md` exists | Gate PASS | Fully Trusted | Notes |
|---------|------|:--------:|:--------:|:------------:|:---------:|:-------------:|-------|
| CSUTLDTC | Utility | ❌ | ❌ | ❌ | — | ❌ | Date/time utility — called by other programs |

---

## Summary Scorecard

| Metric | Count | of 28 |
|--------|------:|------:|
| REKT ran | 9 | 32% |
| CFG JSON committed | 9 | 32% |
| `.md` translation exists | 9 | 32% |
| Gate PASS | 8 | — (of 9 with `.md`) |
| **Fully trusted (metal-backed)** | **5** | **18%** |

> ⚠️ CBACT04C has REKT + CFG but no `.md` — next easiest translation win.
> ⚠️ COMEN01C and COSGN00C: REKT ran and gate passes, but scope-terminator suppression means paragraph-level completeness has not been positively asserted. Run a full paragraph diff before marking Fully Trusted.
> ⚠️ COBSWAIT is trivial (0 real paragraphs) — Fully Trusted carries an asterisk.

---

## GnuCOBOL Status

GnuCOBOL was installed and exercised in a previous session for compile-check purposes.
Its role in the pipeline is **not yet formally defined**.

| Question | Status |
|----------|--------|
| GnuCOBOL installed locally? | ✅ confirmed in prior session |
| Used for syntax-only compile check? | ⚠️ used interactively — not committed to pipeline |
| Used for execution / output comparison? | ⚠️ explored — role undefined |
| Output committed to validation/? | ❌ |

**Decision needed:** Define GnuCOBOL's formal role before expanding to new programs:
- Option A: Syntax gate only (compile each `.cbl` — fail fast on parse errors)
- Option B: Runtime comparison oracle (compile + run with test data, compare output)
- Option C: Both, in separate pipeline stages

---

## Next Actions

Priority order for expanding the trusted foundation:

```
[✅] 1. Run REKT on COMEN01C and COSGN00C — REKT confirmed ran, gate passes with suppression
[ ] 2. Write CBACT04C.md — CFG already exists, easiest translation win
[ ] 3. Decide GnuCOBOL role — document formally in this tracker
[ ] 4. Fully validate COMEN01C and COSGN00C paragraphs — clear suppressed-PASS caveat
[ ] 5. Run REKT on remaining batch programs (CBTRN02C, CBTRN03C, CBEXPORT, CBIMPORT, CBSTM03A/B)
[ ] 6. Run REKT on CICS programs (COADM01C, COBIL00C, COTRN*, COUSR*, COCRD*, CORPT00C)
[ ] 7. Run REKT on CSUTLDTC utility
[ ] 8. Begin inference pipeline smoke test — pick 2 untranslated programs, run LLM → gate
```

---

## Session Changelog

| Date | Change |
|------|--------|
| 2026-05-01 | Gate failures diagnosed: CBACT01C/02C/03C all FAILing due to (1) missing `data_items` in `_cfg.json` — L01 parser added to `extract_cfg_summary.py`; (2) synthetic Cobol-REKT CFG labels leaking through `is_paragraph_node()` — filter tightened. MD content fixed: CBACT01C removed 5 hallucinated names; CBACT02C fixed missing frontmatter + removed 1 paragraph + 1 data item; CBACT03C removed 1 data item. |
| 2026-05-02 | Gate confirmed **8/8 PASS** locally after fixes. Branch `fix/gate-failures-cbact01c-02c-03c` merged to main. COMEN01C and COSGN00C REKT status corrected to ✅ — `extract_cfg_summary.py --all` and `extract_ground_truth.py` confirmed both programs processed (7 and 6 reachable paragraphs respectively). Tracker scorecard updated: REKT ran 7→9, CFG committed 7→9. |

---

## How to Update This File

After completing any pipeline stage for a program:
1. Change the relevant cell from ❌ to ✅ (or ⚠️ with a note)
2. Update the Summary Scorecard counts
3. Move completed items off the Next Actions list
4. Commit with message: `docs(tracker): <PROGRAM> — <stage> complete`
