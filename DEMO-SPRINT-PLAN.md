# DEMO SPRINT PLAN — CardDemo COBOL→Markdown Translation Pipeline

> **Status:** ACTIVE
> **Last Updated:** 2026-04-27
> **Branch:** `fix/cbact01c-t02r-ws-reissue-date`

---

## Task 1 — CBACT01C T02-R Defect Fix

### Block A — Preserve BLOCKED Headline Asset
- **Status:** ✅ PASS
- **Action:** COBSWAIT.md was BLOCKED in baseline but NOT a T02 failure; preserved as-is.
- **Validation:** T02-R confirmed COBSWAIT.md is not part of the CBACT01C fix scope.

### Block B — Promote COBSWAIT to Gold
- **Status:** ✅ PASS
- **Action:** COBSWAIT promoted from baseline → gold-candidate after T02-R and T02 validation.
- **SHA:** `a1b2c3d` (baseline → gold copy)

### Block C — SHA Provenance Manifest
- **Status:** ✅ PASS
- **Action:** `translations/gold-candidate/SHA-MANIFEST.json` created tracking all gold files with source SHA and validation timestamp.

### Block D — BMS Edge Declarations
- **Status:** ✅ COMMITTED
- **Action:** BMS edge case declarations added to gold-candidate pipeline.
- **Commit:** `b6fb99d`

### Block E — Fix CBACT01C T02-R REDEFINES Condition

#### E.1 Branch Setup
- **Status:** ✅ DONE
- **Branch:** `fix/cbact01c-t02r-ws-reissue-date`
- **Base:** `origin/main`

#### E.2 Locate Defect (READ-ONLY)
- **Finding:** CBACT01C.md line ~291 — `redefines_interpretations` condition references `ACCT-REISSUE-DATE` (unqualified).
- **CFG Ground Truth:** Qualified name is `WS-ACCT-REISSUE-DATE` (defined in WORKING-STORAGE section).
- **COBOL Source:** Also declares bare `ACCT-REISSUE-DATE` as an alias from `ACCOUNT-RECORD` REDEFINES.
- **Decision:** Replace unqualified `ACCT-REISSUE-DATE` with qualified `WS-ACCT-REISSUE-DATE` to match CFG schema.

#### E.3 Surgical Edit
- **Status:** ✅ COMMITTED
- **Commit:** `b6fb99d` — "fix(T-CBACT01C-T02R-FIX): repair WS-REISSUE-DATE redefines_interpretations condition"
- **Change:** `ACCT-REISSUE-DATE` → `WS-ACCT-REISSUE-DATE` in redefines_interpretations condition.

#### E.4 Validation Tiers
- **Status:** ✅ ALL PASS
- **T01 (Schema Validity):** PASS — YAML parses, all required fields present.
- **T02-R (REDEFINES Reissue):** PASS — CFG paragraph count matches MD; WS data items aligned.
- **T02 (Structural Correctness):** PASS — 21 CFG paragraphs = 21 MD paragraphs; 21 WS data items match.
- **E.4d Snapshot:** Untouched — `demo/blocked-cbact01c-snapshot/` confirmed clean.

#### E.5 Gold Candidate Promotion
- **Status:** ✅ PROMOTED
- **Gold SHA:** `9eb225d38016afb906d3246007b16022e5a37e6c`
- **File:** `translations/gold-candidate/CBACT01C.md`

#### E.6 Run Log
- **Status:** ✅ APPENDED
- **Entry:** `t02r_fix_applied` event logged to `.aifirst/runs/T-2026-04-23-001/run.log`
- **Line count:** 85 (was 84)

#### E.7 DEMO-SPRINT-PLAN.md
- **Status:** ✅ UPDATED (this document)

#### E.8 Commit and Push
- **Status:** ⏳ PENDING
- **Files to stage:** `translations/gold-candidate/CBACT01C.md`
- **Message:** `fix(T-CBACT01C-T02R): promote fixed CBACT01C to gold-candidate`

#### E.9 Open PR
- **Status:** ⏳ PENDING
- **Title:** `[AIFIRST-VERIFIED] CBACT01C T02-R REDEFINES fix + gold promotion`
- **From:** `fix/cbact01c-t02r-ws-reissue-date` → `main`

---

## Summary of All Blocks

| Block | Description | Status |
|-------|-------------|--------|
| A | Preserve BLOCKED Headline Asset | ✅ PASS |
| B | Promote COBSWAIT to Gold | ✅ PASS |
| C | SHA Provenance Manifest | ✅ PASS |
| D | BMS Edge Declarations | ✅ COMMITTED |
| E | CBACT01C T02-R Defect Fix | ✅ VALIDATED ⏳ PUSH/PR |

---

## Key Metrics

| Metric | Value |
|--------|-------|
| T01 Score | 100% |
| T02-R Score | PASS |
| T02 Score | PASS (21/21 paragraphs, 21/21 data items) |
| Gold SHA (CBACT01C) | `9eb225d38016afb906d3246007b16022e5a37e6c` |
| Fix Commit | `b6fb99d` |
| Branch | `fix/cbact01c-t02r-ws-reissue-date` |