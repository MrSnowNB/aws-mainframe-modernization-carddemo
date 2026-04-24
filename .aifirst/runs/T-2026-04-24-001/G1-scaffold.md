---
task_id: T-2026-04-24-001
parent_task: T-2026-04-23-001
parallel_task: T-2026-04-23-002
gate: G1
status: OPEN
aifirst_protocol: aifirst/1.0
branch: feat/schema-v1.2-hercules-parity
opened: 2026-04-24T12:57Z
closed: null
human_ack_g0: 2026-04-24T12:55Z (risk_flags RF-01..RF-10 acknowledged with 6 additional G1 constraints)
g0_plan: .aifirst/runs/T-2026-04-24-001/G0-plan.md
author: "claude-sonnet-4.6 (Perplexity Computer autonomous COBOL modernization agent)"
llm_inference_allowed: false
---

# G1 — Scaffold: Schema v1.2 — Hercules Byte-Parity Foundation

## 1. Gate Status

- **G0 ACK received** 2026-04-24T12:55Z. Human acknowledged all 10 risk flags and authorized G1 subject to 6 additional constraints (enumerated in §2 below).
- G1 opens at 2026-04-24T12:57Z.
- This document is the single source of truth for what G1 must produce before any extractor or validator is authored.
- **G1 will not close** until every §2 constraint is met and the validator-compatibility audit (§3) has been human-reviewed.

## 2. G1 Additional Constraints (from G0 ACK)

| # | Constraint | Target | Status |
|---|-----------|--------|--------|
| C-1 | First G1 commit = `validate_t01.py` compatibility audit. If patching required, the patch is the **second** commit on the branch, before any extractor is written. | This document §3 + possible `scripts/validate_t01.py` patch commit | §3 complete — patch required — queued as commit #2 |
| C-2 | §8.1 addition — `SYNC` / `SYNCHRONIZED` clause forces alignment; emit `slack_bytes_before: N` where required. | `extract_byte_layout.py` derivation logic | Rule captured in §5 of this file |
| C-3 | §8.3 addition — `SEARCH` / `SEARCH ALL` / `SET index` verb rules for `mutates[]`/`reads[]`. | `extract_paragraph_io.py` derivation logic | Rule captured in §5 of this file |
| C-4 | §8.6 addition — `hercules_parity` gains `actual_output_sha256` and `byte_diff_report` placeholders. | `assemble_v1_2.py` YAML emitter | Rule captured in §5 of this file |
| C-5 | RF-04 assertion — `line[n+1] > line[n]` for every consecutive paragraph pair (hard assert). | `extract_fallthrough.py` | Rule captured in §5 of this file |
| C-6 | RF-08 — SHA-256 of each pinned `validation/pass1/<F>_annotations.json` recorded in COMPLETION-REPORT.md §2. | COMPLETION-REPORT assembly step | Deferred to G4; SHA-256s captured at chunk h (smoke) |

## 3. Validator Compatibility Audit (C-1)

### Method

Read-only inspection of the four existing validators on `main@245222a`. Grep for `schema_version` and any hardcoded version literal. No code executed.

### Findings

| Script | Line(s) | Finding | Action |
|--------|---------|---------|--------|
| `scripts/validate_t01.py` | 39–40 | Hard equality: `if data.get("schema_version") != "cobol-md/1.0": errors.append(...)`. Every v1.2 file would FAIL T01. | **Patch required.** Accept the explicit set `{"cobol-md/1.0", "cobol-md/1.0.2", "cobol-md/1.1", "cobol-md/1.2"}`. |
| `scripts/validate_t02.py` | — | No `schema_version` reference. Version-agnostic. Diffs CFG paragraph/data-item names against MD YAML. | No change required. |
| `scripts/validate_t02r.py` | — | No `schema_version` reference. Validates `redefines_interpretations[]` structure regardless of schema version. | No change required. |
| `scripts/validate_t03.py` | — | No `schema_version` reference. Compares MD `data_items[]` vs CFG at 01-level. | No change required. |

Verified command (read-only):

```
grep -n "cobol-md\|schema_version" scripts/validate_t0{1,2,2r,3}.py
# → only validate_t01.py:39 matches
```

### Required Patch

```python
# scripts/validate_t01.py — diff (preview only, not yet applied)
- if data.get("schema_version") != "cobol-md/1.0":
-     errors.append(f"schema_version must be 'cobol-md/1.0' (got {data.get('schema_version')!r})")
+ ACCEPTED_SCHEMA_VERSIONS = frozenset({
+     "cobol-md/1.0",      # T-001 baseline
+     "cobol-md/1.0.2",    # (tolerated; not emitted by any generator today but legal per docs v1.0.2)
+     "cobol-md/1.1",      # T-002 baseline-v1.1 (reserved even if payloads not yet merged)
+     "cobol-md/1.2",      # T-2026-04-24-001 baseline-v1.2
+ })
+ if data.get("schema_version") not in ACCEPTED_SCHEMA_VERSIONS:
+     errors.append(
+         f"schema_version must be one of {sorted(ACCEPTED_SCHEMA_VERSIONS)} "
+         f"(got {data.get('schema_version')!r})"
+     )
```

Design constraints for the patch:

- **Atomic.** Single commit, title exactly: `fix(validate_t01): accept schema_version cobol-md/1.2`.
- **Reversible.** Single-function edit; no behaviour change for `cobol-md/1.0`.
- **Regression-proof.** Run `validate_t01.py` against all 6 T-001 baseline files after the patch; every one must PASS (backward-compat smoke). Event logged to `run.log` as `validator_compat_smoke`.
- **No semantic change.** Patch only broadens the accepted set; every other check in the file is untouched.
- **No new imports / no signature changes / no new CLI flags.**

### Commit Order on `feat/schema-v1.2-hercules-parity`

1. `be01a7b` — G0 plan + run.log (already pushed)
2. **NEXT** — `fix(validate_t01): accept schema_version cobol-md/1.2` (isolated commit; applies the patch above)
3. Then — `scripts/validate_t01_compat_smoke.log` event appended to run.log (as part of same commit OR separate if the smoke runs later)
4. Then — Chunk (a) directory scaffold + empty stubs for the 9 new scripts
5. Then — Chunks (b)…(j) per G0 DAG

## 4. Directory Scaffold (to be created after C-1 complete)

```
translations/baseline-v1.2/                            # NEW  — output target
validation/pass1/byte_layouts/                         # NEW  — extractor artefacts
validation/pass1/fallthrough/                          # NEW
validation/pass1/paragraph_io/                         # NEW
validation/pass1/file_control/                         # NEW
.aifirst/runs/T-2026-04-24-001/                        # EXISTS
.aifirst/runs/T-2026-04-24-001/review-checklists/      # NEW (populated at G3 only if a blocker is raised)
```

No existing directory is modified.

## 5. Script Stubs (to be created after C-1 complete)

Each stub is a deterministic Python 3 module with:
- A docstring that quotes the relevant §8 rule(s) it implements.
- A `main()` with `--help` that documents CLI contract.
- A `NotImplementedError` raised from the core function body (no logic yet).
- An `if __name__ == "__main__":` guard.
- `# LLM-FREE: this script performs zero LLM inference.` banner at top.

### 5.1 Extractors (4)

| Script | CLI | Output |
|--------|-----|--------|
| `scripts/extract_byte_layout.py` | `--source app/cbl/<F>.cbl --out validation/pass1/byte_layouts/<F>.json` | JSON: list of data item entries with `byte_layout` sub-object per §8.1 + §C-2 SYNC/SYNCHRONIZED rule |
| `scripts/extract_fallthrough.py` | `--annotations validation/pass1/<F>_annotations.json --out validation/pass1/fallthrough/<F>.json` | JSON: paragraph entries with `falls_through_to` + `terminator` per §8.2 + C-5 assertion |
| `scripts/extract_paragraph_io.py` | `--annotations validation/pass1/<F>_annotations.json --out validation/pass1/paragraph_io/<F>.json` | JSON: paragraph entries with `mutates[]` + `reads[]` per §8.3 + §C-3 SEARCH rules |
| `scripts/extract_file_control.py` | `--source app/cbl/<F>.cbl --byte-layouts validation/pass1/byte_layouts/<F>.json --out validation/pass1/file_control/<F>.json` | JSON: one entry per SELECT with v1.2 codepage/record_format/record_length/sign_convention/endianness |

### 5.2 Assembler (1)

| Script | CLI | Output |
|--------|-----|--------|
| `scripts/assemble_v1_2.py` | `--baseline translations/baseline/<F>.md --byte-layouts ... --fallthrough ... --paragraph-io ... --file-control ... --out translations/baseline-v1.2/<F>.md` | v1.2 MD: inherits T-001 YAML front-matter; bumps `schema_version: "cobol-md/1.2"`; appends `memory_model` + `hercules_parity` (with C-4 placeholders); enriches `data_items[]` / `procedure_paragraphs[]` / `file_control[]`; leaves `validation` block PENDING per hard rule. |

### 5.3 Validators (4)

| Script | CLI | Threshold |
|--------|-----|-----------|
| `scripts/validate_byte_layout.py` | `--md ... --annotations ... --out validation/reports/<F>_T-PASS1-BYTES.json` | 100% blocking |
| `scripts/validate_fallthrough.py` | `--md ... --annotations ... --out validation/reports/<F>_T-PASS1-FT.json` | 100% blocking |
| `scripts/validate_mutations.py` | `--md ... --propositions validation/pass2/<F>_propositions.json --out validation/reports/<F>_T-PASS1-MUT.json` | 100% blocking |
| `scripts/validate_codepage.py` | `--md ... --out validation/reports/<F>_T-PASS1-CP.json` | 100% blocking |

**Note on `validate_mutations.py`:** the T-001/T-002 propositions files live at `validation/pass2/<F>_propositions.json`. Per RF-07 / RF-08 we do NOT edit pass1_annotate.py or any pass2_* scripts; we read the existing files from `main@245222a`.

## 6. Derivation Rules — Final (v1.2)

All rules below are the **authoritative implementation contract** for the extractors. Rules from the dispatch are unchanged; additions C-2, C-3, C-4, C-5 are inlined.

### 6.1 PIC / USAGE byte layout (dispatch §8.1 + C-2)

Base table unchanged. Add:

- **SYNC / SYNCHRONIZED clause:**
  - On COMP / COMP-4 / COMP-5 / COMP-1 / COMP-2 items, aligns to halfword (2B), word (4B), or doubleword (8B) per USAGE: COMP-1 and 4-byte COMP/COMP-4/COMP-5 → word; COMP-2 and 8-byte COMP/COMP-4/COMP-5 → doubleword; 2-byte COMP/COMP-4/COMP-5 → halfword.
  - When an item is SYNC and its natural offset within the enclosing group is not already aligned, emit `slack_bytes_before: N` where `N` = bytes needed to reach the aligned offset.
  - Write `alignment: "halfword" | "word" | "doubleword"` on the item's `byte_layout`; default `alignment: "byte"` otherwise.
  - Group `total_bytes` recomputation: sum of `slack_bytes_before + total_bytes` per child (slack bytes are counted once at the child's position, not added to the child's own `total_bytes`).

Reference: IBM Enterprise COBOL 6.4 — [SYNCHRONIZED clause](https://www.ibm.com/docs/en/cobol-zos/6.4.0?topic=clauses-synchronized-clause).

### 6.2 Fall-through + terminator (dispatch §8.2 + C-5)

Rules unchanged. Add:

- **Hard source-order assertion (C-5):** before emitting any fall-through edge, assert that for every consecutive paragraph pair `P_n, P_{n+1}` as sorted by source line, `first_line(P_{n+1}) > last_line(P_n)`. If the assertion fails on any file, `extract_fallthrough.py` raises with exit code 2 and writes an event `cfg_paragraph_order_anomaly` to run.log. No fall-through output is produced for that file; the file is BLOCKED at chunk c and a review checklist entry is generated.

### 6.3 Paragraph `mutates[]` / `reads[]` (dispatch §8.3 + C-3)

Base rules unchanged. Add:

- **Writers:** `SET index-name TO ...` → `mutates += [index-name]`. `SEARCH ... AT END …` and `SEARCH ALL` → `mutates += [index-name-of-TABLE]` (the SEARCH itself updates the associated INDEXED BY index as it iterates).
- **Readers:** `SEARCH ... WHEN <condition>` — every operand in `<condition>` → `reads += [operand]`. The SEARCH/SEARCH ALL verb also reads the table being searched → `reads += [table-name]`.

Reference: IBM Enterprise COBOL 6.4 — [SEARCH statement](https://www.ibm.com/docs/en/cobol-zos/6.4.0?topic=statements-search-statement) and [SET statement](https://www.ibm.com/docs/en/cobol-zos/6.4.0?topic=statements-set-statement).

### 6.4 `file_control[]` (dispatch §8.4)

Unchanged. Default `input_codepage: IBM-1047` flagged `codepage_default_applied: true`.

### 6.5 `memory_model{}` (dispatch §8.5)

Unchanged.

### 6.6 `hercules_parity{}` (dispatch §8.6 + C-4)

```yaml
hercules_parity:
  ready: false
  jcl_reference: null
  input_dataset_sha256: null
  expected_output_sha256: null
  actual_output_sha256: null          # NEW (C-4) — written by T06 run
  byte_diff_report: null              # NEW (C-4) — path to detailed diff on mismatch
```

## 7. Pinning (RF-08 + C-6)

The extractors must pin to `validation/pass1/<F>_annotations.json` as they exist on `feat/schema-v1.2-hercules-parity` at branch-point `main@245222a`. At chunk (h) smoke, compute `sha256sum` of each of the 6 pinned annotation files and save to `.aifirst/runs/T-2026-04-24-001/pinned-inputs.sha256`. COMPLETION-REPORT.md §2 (G4) embeds this table verbatim.

## 8. Non-Negotiables (restated from G0, repeated here so G1 builders cannot miss them)

1. Zero LLM calls. Every extractor, assembler, and validator is pure Python regex + string manipulation.
2. `app/cbl/` read-only.
3. `translations/baseline/`, `translations/baseline-v1.1/`, `translations/gold/`, `translations/gold-candidate/` read-only.
4. T-002 artefacts (`scripts/pass2_*.py`, `scripts/pass3_*.py`, `validation/pass2/*`, `validation/pass3/*`, `.aifirst/runs/T-2026-04-23-002/**`) read-only.
5. All run.log writes go to `.aifirst/runs/T-2026-04-24-001/run.log` only. Append-only.
6. `validation` block in every v1.2 MD left as `overall: PENDING` with every tier field `null` — populated only by the new validators at G3, not by the assembler.
7. No raw COBOL source embedded anywhere in the v1.2 MD.

## 9. Gate Decision

G1 status: **OPEN — CHECKPOINT**.

Per the G0 ACK directive, G1 pauses here for human confirmation of §3 findings (patch design) before the `validate_t01.py` patch commit is made. Once confirmed, the commit sequence in §3 proceeds. G1 closes after §4 directories exist, §5 stubs are in place, §3 patch is committed, and `validator_compat_smoke` has been logged to run.log against all 6 T-001 baseline files.

Expected G1 close: within 30 minutes of patch authorization.

## 10. Version History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 0.1 | 2026-04-24T12:57Z | claude-sonnet-4.6 | G1 opens — validator compat audit embedded; 6 G0-ACK constraints captured. |
