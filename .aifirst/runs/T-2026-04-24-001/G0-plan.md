---
task_id: T-2026-04-24-001
parent_task: T-2026-04-23-001
parallel_task: T-2026-04-23-002
gate: G0
status: PASS
aifirst_protocol: aifirst/1.0
plan_document: "inline (authored from the 2026-04-24 Gemini review dispatch)"
schema_target: "cobol-md/1.2 (optional fields; backward-compatible with v1.1 and v1.0.2)"
branch: feat/schema-v1.2-hercules-parity
branch_base: main@245222a
opened: 2026-04-24T12:33Z
closed: 2026-04-24T12:55Z
author: "claude-sonnet-4.6 (Perplexity Computer autonomous COBOL modernization agent)"
human_ack_required: true
human_ack_trigger: "after G0 close, before any G1 scaffold or script creation"
llm_inference_allowed: false
---

# G0 — Plan: Schema v1.2 — Hercules Byte-Parity Foundation

## 1. Objective

Upgrade the COBOL-MD schema from v1.1 to **v1.2** so a future **T06 Hercules byte-parity tier** can SHA-256 compare DAG execution output against the original mainframe runtime running under [Hercules MVS 3.8J](http://www.hercules-390.org/). All v1.2 additions in this task are **DETERMINISTIC** — derivable from COBOL source plus the existing Cobol-REKT CFG JSON. **Zero LLM inference is required or permitted** in T-2026-04-24-001.

v1.2 is a **pure Pass-1 extension**. Pass 2 and Pass 3 (T-002 semantic layers) are untouched.

## 2. Why Now

External review ([Gemini, 2026-04-24](https://ai.google.dev/)) identified four gaps between the current v1.1 schema and what is needed for a 1:1 semantic translation verifiable against [IBM z/OS EBCDIC semantics](https://www.ibm.com/docs/en/cobol-zos/6.4.0?topic=clause-computational-items):

1. **PIC → byte layout not decomposed.** JSON state cannot be round-tripped to mainframe-compatible bytes without packed-decimal / zoned-decimal / binary offsets. Confirmed against [IBM Enterprise COBOL § Computational items](https://www.ibm.com/docs/en/cobol-zos/6.4.0?topic=clause-computational-items): 2/4/8-byte binary ladders, `ceil((n+1)/2)`-byte packed-decimal.
2. **Fall-through edges implicit.** The DAG router cannot choose the next paragraph after one that does not end in `GO TO / STOP RUN / GOBACK / EXIT PROGRAM / EXEC CICS RETURN`.
3. **EBCDIC codepage + sign-convention absent from `file_control[]`.** Dataset I/O is non-deterministic without explicit `input_codepage / record_format / record_length / sign_convention / endianness`. z/OS default is [IBM-1047](https://www.ibm.com/docs/en/zos/2.5.0?topic=statements-codepage-statement).
4. **Single global memory space not explicit.** `WORKING-STORAGE` is process-global, `LINKAGE` is parameter-passed, `FILE-SECTION` is I/O-bound. Scope metadata is a pre-requisite for the DAG router to reason about state persistence across paragraph boundaries.

## 3. Scope

- Apply the four schema additions (byte layout, fall-through, mutates/reads, codepage) to the **6 pilot files** in T-001 / T-002 priority order.
- Produce v1.2 MDs in a **new** directory `translations/baseline-v1.2/` — never overwriting T-001 `translations/baseline/*.md`, T-002 `translations/baseline-v1.1/*.md` (not yet on disk), or the gold candidates.
- Add **4 new deterministic validators** (`validate_byte_layout.py`, `validate_fallthrough.py`, `validate_mutations.py`, `validate_codepage.py`).
- Add **2 new deterministic extractors** (`extract_byte_layout.py`, `extract_fallthrough.py`). Paragraph-level `mutates[] / reads[]` extraction lives in either an extension of `pass1_annotate.py` or a companion `extract_paragraph_io.py` — decided at G1 (see §9 RF-07).
- Patch the existing T01/T02/T02-R/T03 validators only where **strictly necessary** to accept the optional v1.2 fields without breaking v1.0.2 / v1.1 files. Each patch must be atomic and reversible.

## 4. Out of Scope

- **T06 Hercules byte-parity tier** itself — no Hercules environment, no JCL execution, no SHA-256 comparison. Target task: T-2026-04-25-001.
- **JCL dataset layout.** The `CUSTFILE DD` codepage overrides (IBM-037 vs IBM-1047 vs IBM-273 etc.) live in JCL that is not in `app/cbl/`. Defaults to IBM-1047 with a `codepage_default_applied: true` flag.
- **Any LLM call.** If any phase of this task requires an LLM it is the wrong phase.
- **T-002 artefacts.** The merge scripts, Pass 2 / Pass 3 payloads, and `feat/t-002-llm-phase` branch are left alone. No write to `.aifirst/runs/T-2026-04-23-002/run.log`.
- **Modifying `app/cbl/`.** Sources are ground truth. Read-only.
- **`translations/baseline/`, `translations/baseline-v1.1/`, `translations/gold/`, `translations/gold-candidate/`.** All upstream artefacts untouched.

## 5. Decomposition (all chunks zero-LLM)

| # | Chunk | Blocks the next chunk if it fails? |
|---|-------|-----------------------------------|
| a | Pre-flight + G0 (this file) + G1 scaffold + directory creation | Yes |
| b | `extract_byte_layout.py` — PIC/USAGE byte-size engine with OCCURS, REDEFINES, group-sum, OCCURS DEPENDING ON min/max | Yes |
| c | Fall-through + terminator extractor (paragraph order, last-statement verb, mutates/reads over Pass 1 annotations) | Yes |
| d | File-control codepage extractor (SELECT + FD + record-descriptor sum → `file_control[]` additions) | Yes |
| e | v1.2 MD assembler — inherits T-001 baseline front-matter; bumps `schema_version` to `cobol-md/1.2`; appends all v1.2 fields | Yes |
| f | Four new validators (`validate_byte_layout.py`, `validate_fallthrough.py`, `validate_mutations.py`, `validate_codepage.py`) | Yes |
| g | Minimal v1.2-compat patches to `validate_t01.py`/`validate_t03.py` if required; backward-compat smoke on T-001 v1.0.2 files | Yes |
| h | Smoke test: full v1.2 pipeline on COBSWAIT; diff vs v1.0.2; only v1.2 fields should differ | Yes |
| i | Corpus run: CBCUS01C → COMEN01C → CBTRN01C → COSGN00C → CBACT01C | Yes |
| j | G3 validate + G4 commit + COMPLETION-REPORT.md + open PR to main | — |

## 6. Dependency DAG (abbreviated)

```
preflight → G0 → G1 → extract_byte_layout.py
                                    │
                                    ▼
                       extract_fallthrough.py / extract_paragraph_io.py
                                    │
                                    ▼
                       extract_file_control.py (new OR inline in assembler)
                                    │
                                    ▼
                       v1.2 MD assembler (deterministic) ── reads T-001 baseline front-matter
                                    │
                                    ▼
       ┌──── validate_byte_layout.py (T-PASS1-BYTES)
       ├──── validate_fallthrough.py (T-PASS1-FT)
       ├──── validate_mutations.py   (T-PASS1-MUT)
       └──── validate_codepage.py    (T-PASS1-CP)
                                    │
                                    ▼
                       v1.2 backward-compat check: T01/T02/T02-R/T03 on v1.0.2 files (must still PASS)
                                    │
                                    ▼
                       Smoke: COBSWAIT full run → diff v1.0.2 vs v1.2 (only new fields differ)
                                    │
                                    ▼
                       Corpus: CBCUS01C → COMEN01C → CBTRN01C → COSGN00C → CBACT01C
                                    │
                                    ▼
               G3-validate.md → G4-commit.md → COMPLETION-REPORT.md → PR
```

## 7. File Manifest (final shape — actually created at G1)

**New scripts** (under `scripts/`):

| Path | Purpose | LOC est. |
|------|---------|----------|
| `extract_byte_layout.py` | PIC/USAGE byte-layout engine; emits `validation/pass1/byte_layouts/<F>.json` | 400 |
| `extract_fallthrough.py` | Paragraph terminator + falls_through_to derivation from Pass-1 annotations | 180 |
| `extract_paragraph_io.py` | Paragraph `mutates[] / reads[]` derivation from Pass-1 verbs and operand_types | 220 |
| `extract_file_control.py` | SELECT + FD + record-descriptor sum → `file_control[]` v1.2 block | 200 |
| `assemble_v1_2.py` | Reads T-001 baseline front-matter + the four extractors → `translations/baseline-v1.2/<F>.md` | 280 |
| `validate_byte_layout.py` | T-PASS1-BYTES validator (threshold 100%, blocking) | 180 |
| `validate_fallthrough.py` | T-PASS1-FT validator (threshold 100%, blocking) | 140 |
| `validate_mutations.py` | T-PASS1-MUT validator (threshold 100%, blocking) | 180 |
| `validate_codepage.py` | T-PASS1-CP validator (threshold 100%, blocking) | 130 |

**New outputs**:

- `translations/baseline-v1.2/<F>.md` × 6
- `validation/pass1/byte_layouts/<F>.json` × 6
- `validation/pass1/fallthrough/<F>.json` × 6
- `validation/pass1/paragraph_io/<F>.json` × 6
- `validation/pass1/file_control/<F>.json` × 6
- `validation/reports/<F>_T-PASS1-BYTES.json` × 6
- `validation/reports/<F>_T-PASS1-FT.json` × 6
- `validation/reports/<F>_T-PASS1-MUT.json` × 6
- `validation/reports/<F>_T-PASS1-CP.json` × 6

**New task artefacts**:

- `.aifirst/runs/T-2026-04-24-001/{G0-plan.md, G1-scaffold.md, G3-validate.md, G4-commit.md, COMPLETION-REPORT.md, run.log}`
- `.aifirst/runs/T-2026-04-24-001/review-checklists/<F>.md` (per-file, only if a blocker is raised)

**Modified** (atomic, reversible patches only):

- `scripts/validate_t01.py` — accept `"cobol-md/1.2"` as a valid `schema_version`; ignore unknown optional fields. If the existing validator already ignores unknown keys, this is a **no-op patch**.
- `scripts/validate_t03.py` — no change expected (v1.2 fields are outside T03 scope).
- `docs/COBOL-MD-SCHEMA.md` — append v1.2 section; do not modify existing field tables.

## 8. Deterministic Extraction Rules (authoritative — quoted from the dispatch)

### 8.1 PIC / USAGE → byte-layout derivation table

| PIC pattern | USAGE | encoding | total_bytes formula |
|-------------|-------|----------|---------------------|
| `PIC X(n)` | (default/DISPLAY) | display | n |
| `PIC 9(n)` | (default/DISPLAY) | zoned-decimal | n |
| `PIC 9(n)` | COMP-3 / PACKED-DECIMAL | packed-decimal | `ceil((n+1)/2)` |
| `PIC 9(n)` | COMP / BINARY / COMP-4 | binary | 2 if n≤4 else 4 if n≤9 else 8 |
| `PIC 9(n)` | COMP-5 | binary (native) | 2 if n≤4 else 4 if n≤9 else 8 |
| `PIC 9(n)` | COMP-1 | float | 4 |
| `PIC 9(n)` | COMP-2 | float | 8 |
| `PIC S9(n)V9(m)` | COMP-3 | packed-decimal | `ceil((n+m+1)/2)` |
| `POINTER` | — | pointer | 8 (default; configurable) |

`S` prefix ⇒ signed. `V` ⇒ implied decimal point (zero bytes on disk). Group items (01, 05, etc. with sub-items) have `total_bytes = sum(children.total_bytes)`. `OCCURS n` ⇒ `total_bytes *= n`. `OCCURS DEPENDING ON` ⇒ emit `total_bytes_min` + `total_bytes_max` and flag for human override. `REDEFINES` ⇒ `total_bytes = same as redefined target` (zero new storage).

Confirmed against IBM Enterprise COBOL 6.4 § [Computational items](https://www.ibm.com/docs/en/cobol-zos/6.4.0?topic=clause-computational-items) and § [Formats for numeric data](https://www.ibm.com/docs/en/cobol-zos/6.3.0?topic=arithmetic-formats-numeric-data).

### 8.2 Fall-through detection rules

Walk Pass 1 annotations per paragraph (ordered by `seq`, which is source order). The last statement's `verb`:

- `GO TO` ⇒ `falls_through_to = null`, `terminator = goto`
- `STOP RUN` ⇒ `falls_through_to = null`, `terminator = stop-run`
- `GOBACK` ⇒ `falls_through_to = null`, `terminator = goback`
- `EXIT PROGRAM` ⇒ `falls_through_to = null`, `terminator = explicit-exit`
- `EXEC CICS RETURN` ⇒ `falls_through_to = null`, `terminator = cics-return`
- `EXEC CICS XCTL` ⇒ `falls_through_to = null`, `terminator = cics-xctl`
- Otherwise, and paragraph is **not** last in source order ⇒ `falls_through_to = <next paragraph name>`, `terminator = implicit`
- Otherwise, and paragraph is last in source order ⇒ `falls_through_to = null`, `terminator = implicit-end-of-program`

### 8.3 Paragraph `mutates[] / reads[]` derivation

Rules per Pass-1 annotation (one pass over each paragraph's annotations):

- **Writers (add to `mutates[]`):** receiver operand of `MOVE`, `INITIALIZE`, `SET`, `ADD … TO`, `SUBTRACT … FROM`, `MULTIPLY … BY`, `COMPUTE` (LHS), `STRING … INTO`, `UNSTRING … INTO`.
- **Readers (add to `reads[]`):** sender operand of the same verbs; all operands of `IF`, `EVALUATE`, `DISPLAY`; RHS of `COMPUTE`; source of `ADD`/`SUBTRACT`; `FROM` clauses of `STRING`; source of `UNSTRING`.
- Deduplicate. All names must be **fully qualified** (Rule 9 compliance). Bare tokens that match multiple scopes are a T-PASS1-MUT failure.

### 8.4 `file_control[]` v1.2 additions

For every `SELECT` entry in `ENVIRONMENT DIVISION → FILE-CONTROL`:

- `input_codepage: IBM-1047` (default; see RF-02)
- `record_format`: derived from `FD RECORDING MODE IS {F|FB|V|VB|U}` if present; else `FB` default (flag `codepage_default_applied: true` analog → `record_format_default_applied: true`).
- `record_length`: sum of `byte_layout.total_bytes` over all fields of the FD's record descriptor. For OCCURS DEPENDING ON, emit `record_length_min` + `record_length_max`.
- `sign_convention: mainframe-ebcdic` for any record containing numeric fields with USAGE DISPLAY; else `none`.
- `endianness: big` (fixed for mainframe).

### 8.5 Top-level `memory_model` additions

- `memory_model.working_storage_bytes`: sum of byte-layout totals for all 01-level items in WORKING-STORAGE SECTION.
- `memory_model.linkage_bytes`: same for LINKAGE SECTION.
- `memory_model.global_memory: true` (fixed).
- `memory_model.persistence: process` (CICS-Online programs could eventually differ, but no current pilot file warrants a deviation; documented below).

### 8.6 `hercules_parity` block

Emitted with all fields null/false. Populated only at T06 execution:

- `hercules_parity.ready: false`
- `hercules_parity.jcl_reference: null`
- `hercules_parity.input_dataset_sha256: null`
- `hercules_parity.expected_output_sha256: null`

## 9. Risk Flags (non-empty — human ACK required before G1 opens)

| ID | Risk | First-principles check result | Mitigation |
|----|------|-------------------------------|------------|
| RF-01 | **COMP-5 byte size is platform-specific.** Dispatch table shows "binary (native)"; IBM docs confirm 2/4/8 by PIC digits on z/OS. | IBM Enterprise COBOL 6.4 uses the same 2/4/8 ladder as COMP on z/OS (see §8.1 citation). No additional ambiguity on our target (z/OS 64-bit). | Document z/OS 64-bit target in `extract_byte_layout.py` docstring. Treat COMP-5 identically to COMP for byte count. Flag any PIC that triggers the edge case in a future Intel-native Hercules re-target. |
| RF-02 | **IBM-037 vs IBM-1047 codepage selection requires JCL DD statements not in `app/cbl/`.** | JCL is not in-scope for T-002/T-004. Our CFG JSON also has no codepage data. | Default every `file_control[]` entry to `IBM-1047` and set a boolean `codepage_default_applied: true`. `validate_codepage.py` records the default, does not fail on it. Surface every file with defaults in the review checklist for human override once JCL lands. |
| RF-03 | **OCCURS DEPENDING ON creates variable-length records.** `byte_layout.total_bytes` cannot be statically computed. | Confirmed in [IBM Enterprise COBOL OCCURS DEPENDING](https://learn.microsoft.com/da-dk/host-integration-server/core/defining-a-variable-length-table-with-the-occurs-depending-clause). Most likely on CBTRN01C (transaction processing). | Emit `total_bytes_min` + `total_bytes_max`. Add `occurs_depending_on: <length-specifier-name>` metadata. Validator flags the field for human annotation but does not block (OCCURS DEPENDING ON is an expected v1.2 edge case, not a v1.2 failure). |
| RF-04 | **Cobol-REKT may report paragraph order differently from source order.** | T-001 already saw phantom paragraphs (END-IF, END-EVALUATE) ordered unpredictably in CFG. | `extract_fallthrough.py` derives `falls_through_to` from **Pass 1 annotation `line` numbers** (source-order lines), never from CFG edge order. Document this explicitly. |
| RF-05 | **REDEFINES with different group structures** (CBACT01C's `WS-REISSUE-DATE`). | `byte_layout.total_bytes` uses the base target's size (zero new storage). Sub-items of the redefining group still emit their own byte layouts. | Covered by §8.1 last row. Validator cross-checks that `sum(redefiner children) == base target total_bytes`. |
| RF-06 | **Paragraphs ending mid-statement via continuation lines** (long EXEC CICS blocks). | Pass 1 already handles multi-line statements by continuing to the period. | Re-use Pass 1 tokenization. Validator requires `last statement seq` to be the annotation with the highest `seq` in the paragraph. |
| RF-07 | **`mutates[]` / `reads[]` extractor placement.** Could extend `pass1_annotate.py` (already written) or stand alone. | `pass1_annotate.py` is deployed under T-002 and modifying it could destabilize the T-002 branch during its LLM-merge phase. | **Isolate.** Create a standalone `scripts/extract_paragraph_io.py` that consumes existing `validation/pass1/<F>_annotations.json`. Zero changes to `pass1_annotate.py`. |
| RF-08 | **Pass 1 annotations list is the sole source of truth for the six pilot files on main.** If T-002 re-emits annotations after a merge it could shift `seq`/`line` pairings. | Annotations on `main` at `245222a` are fixed. Our extractors read from `main` at the branch point. | Pin extractor inputs to `validation/pass1/*.json` at branch base. Document the commit hash in `COMPLETION-REPORT.md §2`. |
| RF-09 | **Backward-compatibility of `validate_t01.py` with `schema_version: "cobol-md/1.2"`.** | Must verify the existing validator does not reject the new version string. The T-001 validator hard-codes `schema_version: "cobol-md/1.0"` as a check. | Inspect `validate_t01.py` at G1; if it hard-codes v1.0, patch to accept `{v1.0, v1.0.2, v1.1, v1.2}`. Commit as its own atomic commit. |
| RF-10 | **`input_codepage` + `sign_convention` are `file_control[]` additions on an existing field, not a new block.** | Must not break T01/T02-R on existing baseline/ files (they don't use v1.2 fields). | Because v1.2 fields are **optional** and exist only under `translations/baseline-v1.2/<F>.md`, T01 on T-001 `translations/baseline/` files is unaffected. Explicit regression smoke at chunk g. |

## 10. Success Criteria

1. 6 v1.2 MD files exist in `translations/baseline-v1.2/` (one per pilot).
2. All 6 files pass **existing** `T01 / T02 / T02-R / T03` validators (backward-compat proof).
3. All 6 files pass **new** `T-PASS1-BYTES / T-PASS1-FT / T-PASS1-MUT / T-PASS1-CP`.
4. No file in `translations/baseline/`, `translations/baseline-v1.1/`, or `translations/gold/` / `gold-candidate/` has been modified.
5. No v1.2 file contains raw COBOL source (T01 source-leak check).
6. Zero LLM inference calls made during this task (budget §12).
7. `run.log` is append-only, ISO-8601 timestamped, one event per real gate transition.
8. `COMPLETION-REPORT.md` contains all 8 sections listed in the dispatch.
9. PR opened against `main` with explicit backward-compatibility proof in the description.

## 11. Rollback Plan

- Every T-004 artefact lives under three paths only: `.aifirst/runs/T-2026-04-24-001/`, `validation/pass1/{byte_layouts,fallthrough,paragraph_io,file_control}/`, `validation/reports/<F>_T-PASS1-{BYTES,FT,MUT,CP}.json`, and `translations/baseline-v1.2/`.
- Deleting those paths + reverting the 9 new scripts reverts the repo cleanly.
- The 9 new scripts go in individual commits (one extractor per commit, validators in one grouped commit, assembler last) so any single script can be reverted atomically.
- If `validate_t01.py` is patched for v1.2 acceptance, that patch is its own commit.

## 12. LLM Budget

| Step | Expected LLM calls | Rationale |
|------|-------------------:|-----------|
| Every step in this task | **0** | All extraction is deterministic per §8. Validators are pattern-matchers. Assembler is a YAML/Markdown concatenation. No prompt template exists in the T-004 surface area. |

Any dispatch that produces a non-zero LLM call during T-2026-04-24-001 is an immediate G3 FAIL per Hard Constraint #1.

## 13. Hard Rules (restated from dispatch)

1. No LLM inference. All additions derivable from COBOL source + existing CFG JSON.
2. v1.2 MUST be backward-compatible with v1.1. All new fields are optional.
3. Do not modify `translations/baseline/`, `translations/gold-candidate/`, or `translations/baseline-v1.1/`.
4. Do not modify `validate_t01.py`/`validate_t02.py`/`validate_t02r.py`/`validate_t03.py` beyond optional-field acceptance.
5. Do not dispatch LLM calls. Do not modify T-002 payload files. Do not alter T-002 run.log.
6. `app/cbl/` is read-only.
7. All run.log events go to `.aifirst/runs/T-2026-04-24-001/run.log` only.

## 14. Inputs

- COBOL sources: `app/cbl/{COBSWAIT,CBCUS01C,COSGN00C,COMEN01C,CBACT01C,CBTRN01C}.cbl` — 6 files, line counts 41 / 178 / 260 / 308 / 430 / 494.
- Pass 1 annotations (from `main@245222a`): `validation/pass1/<F>_annotations.json` × 6.
- CFG JSON (from `main@245222a`): `validation/structure/<F>_cfg.json` × 6.
- T-001 baseline front-matter: `translations/baseline/<F>.md` × 6 (read-only; source of inherited `schema_version` / `program_id` / `source_sha` / `translation_date` / `cfg_source` etc.).
- Schema spec: `docs/COBOL-MD-SCHEMA.md` v1.0.2 (to be appended with v1.2 section).

## 15. Gate Decision

Risk flags are **non-empty** (10 of them). Per the AiFirst Protocol design principle that **"a human must acknowledge G0 when `risk_flags` is non-empty before G1 opens"**, this G0 closes with status PASS and **waits for human ACK** before any G1 scaffold, script creation, directory write (beyond `.aifirst/runs/T-2026-04-24-001/`), or gate-to-gate transition.

STATUS: **PASS**. Awaiting human ACK of §9 risk flags before G1.

## 16. Version History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 0.1 | 2026-04-24 | claude-sonnet-4.6 | Initial G0 plan for v1.2 schema upgrade — Hercules byte-parity foundation |
