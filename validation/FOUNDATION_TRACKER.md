# Validation Foundation Tracker

> **Living document** — update this file whenever a pipeline stage completes for any program.
> Last updated: 2026-05-02 | Gate baseline: 8/8 PASS on `recovery/restore-green-baseline`

---

## Pipeline Layers

```
Layer 1  Source           app/cbl/*.cbl + app/cpy/*.cpy   (authoritative — never changes)
Layer 2  Static Analysis  Cobol-REKT CFG  →  validation/rekt/<PROG>.cbl.report/
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
| CBTRN03C | Batch/VSAM | ❌ | ❌ | ❌ | — | ❌ | Not started — large file (52 KB) |

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
| COMEN01C | CICS/Menu | ❌ | ❌ | ✅ | ✅ (suppressed) | ❌ | REKT never run — gate PASS via RC8 scope-terminator suppression only |
| CORPT00C | CICS | ❌ | ❌ | ❌ | — | ❌ | Not started |
| COSGN00C | CICS/Signon | ❌ | ❌ | ✅ | ✅ (suppressed) | ❌ | REKT never run — gate PASS via RC8 scope-terminator suppression only |
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
| REKT ran | 7 | 25% |
| CFG JSON committed | 7 | 25% |
| `.md` translation exists | 9 | 32% |
| Gate PASS | 8 | — (of 9 with `.md`) |
| **Fully trusted (metal-backed)** | **5** | **18%** |

> ⚠️ CBACT04C has REKT + CFG but no `.md` — next easiest win.
> ⚠️ COMEN01C and COSGN00C pass the gate but have no REKT backing — run REKT before treating them as trusted.

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
[ ] 1. Run REKT on COMEN01C and COSGN00C — convert suppressed PASSes to metal-backed
[ ] 2. Write CBACT04C.md — CFG already exists, easiest translation win
[ ] 3. Decide GnuCOBOL role — document formally in this tracker
[ ] 4. Run REKT on remaining batch programs (CBTRN02C, CBTRN03C, CBEXPORT, CBIMPORT, CBSTM03A/B)
[ ] 5. Run REKT on CICS programs (COADM01C, COBIL00C, COTRN*, COUSR*, COCRD*, CORPT00C)
[ ] 6. Run REKT on CSUTLDTC utility
[ ] 7. Begin inference pipeline smoke test — pick 2 untranslated programs, run LLM → gate
```

---

## How to Update This File

After completing any pipeline stage for a program:
1. Change the relevant cell from ❌ to ✅ (or ⚠️ with a note)
2. Update the Summary Scorecard counts
3. Move completed items off the Next Actions list
4. Commit with message: `docs(tracker): <PROGRAM> — <stage> complete`
