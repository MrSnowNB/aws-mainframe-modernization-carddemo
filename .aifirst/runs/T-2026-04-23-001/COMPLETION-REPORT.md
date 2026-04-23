# COMPLETION REPORT — AI-First COBOL→English Middle Layer

- **task_id**: T-2026-04-23-001
- **corpus**: CardDemo 6-file pilot
- **spec version**: MASTER-ARCHITECTURE.md v1.0.0 · COBOL-MD-SCHEMA.md v1.0.2 · COBOL-MD-PIPELINE.md v1.1.0
- **branch**: `feat/cobol-md-schema-v1`
- **phases executed**: 0 (CFG) · 1 (baseline translation) · 2 (validation T01–T05) · 3-prep (candidate staging + checklists; no self-promotion)
- **phase 3 status**: CANDIDATES STAGED; awaiting human reviewer sign-off per MASTER-ARCHITECTURE §4 and §7 Rule 6
- **phase 4 readiness**: NO-GO
- **report time**: 2026-04-23T15:50Z
- **iteration**: 2 (post-Option-A validator fix; human sign-off 2026-04-23T15:36Z)

---

## 1. Files Translated (Phase 1)

All 6 pilot files have baseline translations in `translations/baseline/`. No raw COBOL source is embedded in any MD (T01 source-leak check 6/6 PASS). `HOLD` files per MASTER-ARCHITECTURE §3: `CBTRN02C.cbl`, `COACTUPC.cbl`.

| File | Size | Subtype | Domain | Paragraphs | Business Rules | REDEFINES | GOTOs | Translator |
|------|-----:|---------|--------|-----------:|---------------:|----------:|------:|------------|
| COBSWAIT.cbl | 2 KB | Utility | Utility | 1 | 2 | 0 | 0 | claude-sonnet-4.6 (autonomous) |
| CBCUS01C.cbl | 7 KB | Batch | Customer Management | 7 | 7 | 1 | 0 | claude-opus-4-5 (subagent) |
| COSGN00C.cbl | 10 KB | CICS-Online | Administration | 9 | 12 | 0 | 0 | claude-opus-4-5 (subagent) |
| COMEN01C.cbl | 12 KB | Menu | Administration | 10 | 10 | 0 | 0 | claude-opus-4-5 (subagent) |
| CBACT01C.cbl | 17 KB | Batch | Account Management | 21 | 15 | 2 | 0 | claude-opus-4-5 (subagent) |
| CBTRN01C.cbl | 18 KB | Transaction Processing | Batch | 21 | 13 | 1 | 0 | claude-opus-4-5 (subagent) |

---

## 2. Tier Validation Matrix

**Two runs recorded.** Iteration 1 ran with validator v1.0.0 and produced four BLOCKs traceable to a schema-vs-validator ambiguity on sub-level items. After human sign-off, Option A (`v1.0.1-option-a`) filtered `cfg.data_items[]` to level-01 in T03 and broadened the T02-R condition-referent check to accept any CFG-known field; this is the iteration-2 state now on disk.

### 2.1 Iteration 1 (pre-fix, for the record)

| File | T01 | T02 | T02-R | T03 | T04 | T05 | Verdict |
|------|-----|-----|-------|-----|-----|-----|---------|
| COBSWAIT | PASS | PASS | PASS | PASS 1.0000 | DEFERRED | DEFERRED | READY |
| CBCUS01C | PASS | PASS | PASS | FAIL 0.7692 | DEFERRED | DEFERRED | BLOCKED |
| COSGN00C | PASS | PASS | PASS | FAIL 0.4000 | DEFERRED | DEFERRED | BLOCKED |
| COMEN01C | PASS | PASS | PASS | PASS 1.0000 | DEFERRED | DEFERRED | READY |
| CBACT01C | PASS | PASS | FAIL | FAIL 0.6512 | DEFERRED | DEFERRED | BLOCKED |
| CBTRN01C | PASS | PASS | PASS | FAIL 0.7241 | DEFERRED | DEFERRED | BLOCKED |

### 2.2 Iteration 2 (post-Option-A, current)

| File | T01 | T02 | T02-R | T03 | T04 | T05 | Verdict |
|------|-----|-----|-------|-----|-----|-----|---------|
| COBSWAIT | PASS | PASS | PASS | PASS 1.0000 | DEFERRED | DEFERRED | **READY** |
| CBCUS01C | PASS | PASS | PASS | PASS 1.0000 | DEFERRED | DEFERRED | **READY** |
| COSGN00C | PASS | PASS | PASS | PASS 1.0000 | DEFERRED | DEFERRED | **READY** |
| COMEN01C | PASS | PASS | PASS | PASS 1.0000 | DEFERRED | DEFERRED | **READY** |
| CBACT01C | PASS | PASS | **FAIL** | PASS 1.0000 | DEFERRED | DEFERRED | BLOCKED |
| CBTRN01C | PASS | PASS | PASS | PASS 1.0000 | DEFERRED | DEFERRED | **READY** |

**READY (Phase 3 candidates): 5 / 6** · **BLOCKED (translation defect): 1 / 6**.

### 2.3 Why T03 scores all report 1.0000

After filtering CFG `data_items[]` to level-01, the denominator drops to the items the MD schema actually covers. For the five 01-surface-complete translations, every 01-level CFG item maps cleanly to an MD item with matching `level`/`picture`/`usage`/dead-code status, producing a genuine perfect match. The diagnostic columns `cfg_items_01` vs `cfg_items_total` are preserved in every T03 JSON so the denominator change is auditable.

---

## 3. Remaining Block — CBACT01C

After Option A, CBACT01C's T03 flipped to PASS (84/84, 21/21 01-level items), but T02-R remained FAIL. The surviving failure is a **translation-side imprecision**:

- `WS-REISSUE-DATE.redefines_interpretations[0].condition` references a bare token `ACCT-REISSUE-DATE`.
- The CFG contains `OUT-ACCT-REISSUE-DATE`, `WS-ACCT-REISSUE-DATE`, `WS-ACCT-REISSUE-YYYY`, `VB2-ACCT-REISSUE-YYYY` — but no bare `ACCT-REISSUE-DATE`.
- `interpretation[1]` uses `WS-ACCT-REISSUE-YYYY` correctly and passes the referent check.

Per Hard Rule 5 the agent has NOT edited the translation. Reviewer options are documented in `review-checklists/CBACT01C.md` (recommended: re-baseline with explicit qualified-name instruction).

---

## 4. Phase 3 Candidate Inventory

All five READY files are staged at `translations/gold-candidate/` with per-file review checklists at `.aifirst/runs/T-2026-04-23-001/review-checklists/`. No file has been promoted to `translations/gold/`.

| Rank | Candidate MD | Checklist | Size | Est. review | Key review item |
|-----:|--------------|-----------|-----:|------------:|------------------|
| 1 | `translations/gold-candidate/COMEN01C.md` | `review-checklists/COMEN01C.md` | 12 KB | 45 min | Table-driven CICS XCTL dispatch |
| 2 | `translations/gold-candidate/COBSWAIT.md` | `review-checklists/COBSWAIT.md` | 2 KB | 10 min | Single-paragraph utility; establish T04 cadence |
| 3 | `translations/gold-candidate/CBCUS01C.md` | `review-checklists/CBCUS01C.md` | 7 KB | 40 min | TWO-BYTES-ALPHA REDEFINES; source-bug flag |
| 4 | `translations/gold-candidate/CBTRN01C.md` | `review-checklists/CBTRN01C.md` | 18 KB | 90 min | Transaction validation + abend path + REDEFINES |
| 5 | `translations/gold-candidate/COSGN00C.md` | `review-checklists/COSGN00C.md` | 10 KB | 50 min | **Capability-boundary sentinel** (see §5) |

Total first-pass review effort: ≈ 4 hours (10 + 45 + 40 + 90 + 50 = 235 min). CBACT01C adds ≈ 90 min once unblocked.

The rank column mirrors the T04 dispatch order at `validation/reports/T04_dispatch_manifest.json` — ranks are for convenience, not prescriptive review order.

---

## 5. T04 Dispatch Manifest (DEFERRED — human-operated)

`validation/reports/T04_dispatch_manifest.json` defines the 68-paragraph judging batch in reviewer-specified priority:

| Rank | File | Para requests | Note |
|-----:|------|--------------:|------|
| 1 | COMEN01C | 10 | Already READY; fast gold path |
| 2 | COBSWAIT | 0 | Single-block; smoke test |
| 3 | CBCUS01C | 7 | READY post-Option A |
| 4 | CBTRN01C | 21 | Largest READY file; most trajectory-pair yield |
| 5 | COSGN00C | 9 | **Capability-boundary sentinel** — a low T04 here is the first signal of a model limit on CICS-Online programs |
| 6 | CBACT01C | 21 | **HOLD** — not dispatched until re-baseline decision |
| **Σ** | — | **68** | — |

- Threshold: ≥ 0.85 weighted mean (dead-code paragraphs weighted 0.1×).
- Trajectory-pair yield produced by this run: **0** (T04 deferred → no Stream-3 pairs yet).

---

## 6. Anomaly Inventory (unchanged from iteration 1)

| File | Anomaly | Category |
|------|---------|----------|
| CBCUS01C | GOBACK marked unreachable in CFG (actually reachable) | CFG tool artefact |
| CBCUS01C | Source bug: duplicate DISPLAY in `1000-CUSTFILE-GET-NEXT` | Source defect, flagged not fixed |
| CBCUS01C | `ADD 8 TO ZERO GIVING APPL-RESULT` idiom in `9000-CUSTFILE-CLOSE` | COBOL idiom, documented |
| COSGN00C | Empty `calls_to[]` in CFG; XCTL targets filled from source review | CFG tool artefact |
| COSGN00C | 3 "dead" paragraphs are scope terminators (END-IF/END-EXEC/END-EVALUATE) | CFG tool artefact |
| COMEN01C | Same 3 scope-terminator phantoms | CFG tool artefact |
| COMEN01C | Table-driven `EXEC CICS XCTL` surfaced in `business_rules[]` | Design note |
| CBACT01C | `WS-REISSUE-DATE.interpretation[0]` uses bare `ACCT-REISSUE-DATE` — see §3 | Translation defect |
| CBACT01C | 4 "dead" paragraphs: GOBACK, WS-REISSUE-DATE, END-IF, VB2-ACCT-ID | CFG tool artefact |
| CBTRN01C | `Z-ABEND-PROGRAM` terminal via `CEE3ABD` | Design note |
| All files | Cobol-REKT `performs` lists appear global, not local | CFG tool artefact |

---

## 7. Novel Failure Modes Observed (to be appended to `failure_modes.log`)

1. **Paragraph-as-data-item leakage from Cobol-REKT.** The CFG emits 01-level names (`WS-REISSUE-DATE`, `VB2-ACCT-ID`), scope terminators (`END-IF`, `END-EVALUATE`, `END-EXEC`), and statement terminators (`GOBACK`) as pseudo-paragraph nodes. Pre-filter in `extract_cfg_summary.py` recommended.
2. **Schema/validator ambiguity on `data_items[]` enumeration breadth.** Resolved this iteration via Option A. Recommend a v1.1 schema upgrade that adds a `sub_items[]` structure so 05/10/88-level items can be captured formally.
3. **Schema/validator ambiguity on REDEFINES condition referents.** Resolved this iteration via T02-R's broadened referent set.
4. **Unqualified COBOL name collisions in REDEFINES conditions.** CBACT01C demonstrates that when multiple qualified variants of a name exist in the CFG, the translator may emit the shortest ambiguous form. Mitigation: add a translation-prompt clause requiring fully-qualified CFG field names in `redefines_interpretations[].condition`.
5. **Global vs local `performs` lists.** Cobol-REKT renders one whole-program PERFORMS set on every paragraph. Corpus-scale runs should extract per-paragraph PERFORMS from CFG node bodies.
6. **Missing LLM-as-judge endpoint.** Operational gap, not a defect. Converts T04 from automated gate to human-dispatched batch.

---

## 8. Per-File Phase-3 Review Effort Estimate (post-fix)

| File | Est. review | Notes |
|------|------------:|-------|
| COBSWAIT.cbl | 10 min | Trivial utility; baseline for review cadence. |
| COMEN01C.cbl | 45 min | 10 paragraphs + table-driven XCTL dispatch. |
| CBCUS01C.cbl | 40 min | 7 paragraphs + 1 REDEFINES + source-bug flag. |
| COSGN00C.cbl | 50 min | 9 paragraphs; XCTL targets manually reconciled; capability sentinel. |
| CBTRN01C.cbl | 90 min | 21 paragraphs + 13 rules + abend + REDEFINES. |
| **Subtotal (5 READY)** | **235 min ≈ 4 h** | — |
| CBACT01C.cbl | +90 min | Blocked; re-baseline + review once unblocked. |

---

## 9. Phase 4 Readiness

**GO / NO-GO: NO-GO.** Conditions gating Phase 4:

- At least one file in `translations/gold/` — **0 at present**.
- T04 judgments returned for every promoted file — **DEFERRED**.
- CBACT01C resolved (re-baseline, further validator relaxation, or escalation) — **pending**.
- Stream-3 trajectory pairs extractable from T04 scores < 3 — **0 until T04 runs**.

---

## 10. Artefact Manifest

```
.aifirst/runs/T-2026-04-23-001/
├── G0-plan.md                         (PASS)
├── G1-scaffold.md                     (PASS)
├── G3-validate.md                     (PASS-WITH-BLOCKS, iteration 1)
├── G4-commit.md                       (iteration-1 STOP record)
├── G4-commit-addendum.md              (iteration-2 PASS after human sign-off)
├── G5-phase3.md                       (candidates staged, awaiting human review)
├── translation-prompt-contract.md
├── run.log                            (append-only JSON-L, 84 events)
├── COMPLETION-REPORT.md               (this file)
└── review-checklists/
    ├── COBSWAIT.md
    ├── COMEN01C.md
    ├── CBCUS01C.md
    ├── CBTRN01C.md
    ├── COSGN00C.md
    └── CBACT01C.md                    (block notice, not a checklist)

translations/
├── baseline/     (6 files; unchanged; `validation` block PENDING)
└── gold-candidate/
    ├── COBSWAIT.md
    ├── COMEN01C.md
    ├── CBCUS01C.md
    ├── CBTRN01C.md
    └── COSGN00C.md                    (5 staged; no CBACT01C; no gold/)

validation/
├── structure/    (6 *_cfg.json; source_sha verified)
└── reports/
    ├── *_T01.json            (6)
    ├── *_T02.json            (6)
    ├── *_T02R.json           (6 · validator_version v1.0.1-option-a)
    ├── *_T03.json            (6 · validator_version v1.0.1-option-a)
    ├── *_T04.json            (6 DEFERRED stubs)
    ├── *_T04_requests.json   (6 paragraph-level judging payloads)
    ├── T04_dispatch_manifest.json
    └── T05_global.json       (DEFERRED)

scripts/
├── extract_cfg_summary.py
├── validate_t01.py
├── validate_t02.py
├── validate_t02r.py          (v1.0.1-option-a, inline-documented)
├── validate_t03.py           (v1.0.1-option-a, inline-documented)
├── score_t04.py
└── run_sweBench.sh
```

---

## 11. Stop Declaration (iteration 2)

The agent stops here at gate G5 with:

- 5 gold candidates staged but NOT promoted;
- 6 reviewer checklists ready;
- 1 file held out for a re-baseline decision;
- 68-paragraph T04 judging batch manifested but not dispatched.

Gold promotion, T04 dispatch, and Phase 4 go/no-go are human actions per MASTER-ARCHITECTURE §4 and §7 Rule 6.
