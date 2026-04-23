---
schema_version: "cobol-md/1.0"
document: "COBOL-MD-PIPELINE"
version: "1.0.0"
status: "ACTIVE"
authored: "2026-04-23"
author: "Mark Snow"
aifirst_protocol: "aifirst/1.0"
---

# COBOL→English Middle Layer Pipeline

## Mission

Prove that every semantic element in a COBOL program can be losslessly expressed in structured English inside a YAML-headered MD file. This creates an **English middle layer** — a human-readable, machine-parseable, knowledge-graph-ready representation that replaces COBOL as the source of truth for business logic.

This is **not** a code documentation tool. The MD file is an independent semantic artifact. Raw COBOL source stays in `app/cbl/` and is never embedded in the output.

---

## Pipeline Overview

```
[COBOL Source]
      │
      ▼
 Phase 1: Baseline Translation (pre-fine-tune)
      │  Model: Qwen3.635B A3B
      │  Output: translations/baseline/*.md
      │
      ▼
 Phase 2: Gated Validation (T01–T05)
      │  Protocol: /aifirst G3
      │  Halt-on-fail per tier
      │
      ▼
 Phase 3: Gold Set Construction
      │  Human review + correction
      │  Output: translations/gold/*.md
      │  Size: 8–10 verified pairs
      │
      ▼
 Phase 4: QLoRA Fine-Tuning
      │  Hardware: HP Z8 Fury G5 / Zbook (ROCm, AMD)
      │  Input: gold/*.md training pairs
      │  run.log T03/T04 PASS events → positive training signal
      │
      ▼
 Phase 5: Post-Fine-Tune Validation + SWE-bench
      │  Same T01–T05 suite, same files
      │  SWE-bench Lite before/after delta = proof document
      │
      ▼
[English Middle Layer — Knowledge Graph Ready]
```

---

## Phase 1 — Baseline Translation

**Model:** Qwen3.635B A3B (via Lemonade Server / Ollama on Z8)
**Input:** COBOL source files from `app/cbl/` (pilot corpus, 8 files)
**Output:** `translations/baseline/<PROGRAM_ID>.md`
**Schema:** `docs/COBOL-MD-SCHEMA.md` v1.0.1

### Pilot Corpus Run Order

| # | File | `business_domain` | `subtype` | Size |
|---|------|------------------|-----------|------|
| 1 | COBSWAIT.cbl | Utility | Utility | 2KB |
| 2 | CBCUS01C.cbl | Customer Management | Batch | 7KB |
| 3 | COSGN00C.cbl | Administration | CICS-Online | 10KB |
| 4 | COMEN01C.cbl | Administration | Menu | 12KB |
| 5 | CBACT01C.cbl | Account Management | Batch | 17KB |
| 6 | CBTRN01C.cbl | Transaction Processing | Batch | 18KB |
| 7 | CBTRN02C.cbl | Transaction Processing | Batch | 59KB — post-FT |
| 8 | COACTUPC.cbl | Account Management | CICS-Online | 182KB — post-FT |

Files 7–8 are held out for post-fine-tune generalization testing.

### Prompt Contract

Every translation prompt MUST:
- Include the full COBOL source as context
- Reference `docs/COBOL-MD-SCHEMA.md` as the schema contract
- Specify `business_domain` and `subtype` for the file being translated
- Instruct the model to populate ALL schema fields — no omissions
- Explicitly prohibit embedding raw COBOL in the output

---

## Phase 2 — Gated Validation

All validation runs under `/aifirst` protocol (see `Morty:.claude/protocol/AIFIRST-SPEC.md`).

### Tier Definitions for COBOL→MD

| Tier | Test | Tool | Threshold |
|------|------|------|-----------|
| T01 | YAML front-matter parses; all required schema fields present; `business_domain` and `subtype` are valid enum values | `pyyaml` + JSON Schema | 100% |
| T02 | Every COBOL SECTION, PARAGRAPH, and 01-level DATA item appears in MD | GnuCOBOL parse diff (`scripts/validate_t02.py`) | 100% |
| T03 | All `data_items[]` entries field-match against COBOL DATA DIVISION parse | Field-level comparator | ≥95% |
| T04 | Business logic is semantically faithful; no business rule present in COBOL is absent from MD | LLM-as-judge rubric (5-point scale per paragraph) | ≥85% |
| T05 | Model hasn't degraded on general code tasks | SWE-bench Lite before/after | ≥ baseline |

### T02 Technical Detail

T02 is the deterministic gate for "1:1" accuracy. The test:
1. Run `cobc -fsyntax-only` on the source `.cbl` file
2. Extract all paragraphs, sections, data items, and COPY references into a JSON structure list
3. Parse the translated `.md` file's Procedure Logic and Data Layer sections
4. Diff: any element in the structure list absent from the MD = T02 FAIL

T02 FAIL is absolute — no threshold, no partial credit. A missing paragraph means the translation is incomplete.

### T04 Rubric

For each paragraph in the Procedure Logic section, score 0–5:
- **5** — Complete, accurate, no information lost
- **4** — Minor phrasing imprecision, all information present
- **3** — Some implicit logic missing, but main flow captured
- **2** — Significant business rule absent or wrong
- **1** — Paragraph present but semantically incorrect
- **0** — Paragraph missing or gibberish

Overall T04 score = mean across all scored paragraphs. Threshold: ≥0.85 (≥85%).

---

## Phase 3 — Gold Set Construction

For each baseline translation that reaches G3:
- Human review against original COBOL source
- Correct any T04 deficiencies
- Ensure all `business_rules[]` entries are captured
- Verify `calls_to` / `called_by` graph edges are accurate
- Save corrected file to `translations/gold/<PROGRAM_ID>.md`

Gold set size: minimum 6 files (Tiers S and M from pilot corpus). Gold files are the fine-tuning training pairs.

---

## Phase 4 — QLoRA Fine-Tuning

**Hardware:** HP Z8 Fury G5 + RTX 6000 Ada (ROCm/AMD — not CUDA)
**Base model:** Qwen3.635B A3B
**Method:** QLoRA (4-bit NF4 quantization)

### Recommended Config

```yaml
method: qlora
quantization: nf4
rank_r: 16
alpha: 32
learning_rate: 2.0e-4
epochs: 3
batch_size: 4
gradient_checkpointing: true
warmup_steps: 50
target_modules: [q_proj, v_proj, k_proj, o_proj]
```

### Training Signal from run.log

Each JSON-L event from `/aifirst` `run.log` contributes:
- `"status": "PASS"` tier events (T03/T04) → **positive examples**
- `"event": "blocked"` events with preceding steps → **negative examples**
- The (COBOL source → YAML+MD output) pair from each gold file → **primary supervised pairs**

---

## Phase 5 — Post-Fine-Tune Validation

Re-run the identical T01–T05 suite on the same 8 pilot files using the fine-tuned model.

### Proof Document Metrics

| Metric | Pre-FT | Post-FT | Delta | Pass? |
|--------|--------|---------|-------|-------|
| T01 schema validity | — | — | — | 100% required |
| T02 structural completeness | — | — | — | 100% required |
| T03 functional score (mean) | — | — | — | ≥0.95 required |
| T04 semantic score (mean) | — | — | — | ≥0.85 required |
| SWE-bench Lite | — | — | — | ≥ baseline |

Populated after each run. Delta = proof of fine-tuning value. SWE-bench delta = proof of no regression.

---

## Directory Structure

```
aws-mainframe-modernization-carddemo/
  app/cbl/                    ← original COBOL source (untouched)
  docs/
    COBOL-MD-SCHEMA.md        ← schema spec v1.0.1 (this defines the contract)
    COBOL-MD-PIPELINE.md      ← this file
  translations/
    baseline/                 ← Phase 1 output
    gold/                     ← Phase 3 human-verified training pairs
    post-finetune/            ← Phase 5 output
  validation/
    structure/                ← GnuCOBOL parse outputs (*.json)
    reports/                  ← T01–T05 results per run (JSON-L)
  scripts/
    validate_t01.py           ← YAML schema validator
    validate_t02.py           ← GnuCOBOL parse diff
    validate_t03.py           ← field-level data item comparator
    score_t04.py              ← LLM-as-judge rubric runner
    run_sweBench.sh           ← SWE-bench Lite wrapper
  .aifirst/
    runs/                     ← /aifirst run logs (JSON-L)
```

---

## Toward the Knowledge Graph

Once ≥10 files pass T04, each MD file is a validated graph node:

| Schema Field | Graph Element |
|-------------|---------------|
| `program_id` | Node identity |
| `business_domain` | Cluster / community label |
| `subtype` | Subgraph partition |
| `calls_to[]` | Directed edge: Program→Program |
| `called_by[]` | Reverse index edge |
| `copybooks_used[]` | Edge: Program→Copybook (shared type) |
| `file_control[]` | Edge: Program→VsamFile |
| `business_rules[]` | Property node: BusinessRule |
| `data_items[]` | Property node: DataItem |

The `business_domain` + `subtype` combination defines graph topology:
- `business_domain` → community detection clusters (Louvain algorithm)
- `subtype` → bipartite partition for CICS vs. Batch analysis

---

## Related Documents

- Schema spec: `docs/COBOL-MD-SCHEMA.md`
- AiFirst protocol: [Morty/.claude/protocol/AIFIRST-SPEC.md](https://github.com/MrSnowNB/Morty/blob/main/.claude/protocol/AIFIRST-SPEC.md)
- AiFirst slash command: [Morty/.claude/commands/aifirst.md](https://github.com/MrSnowNB/Morty/blob/main/.claude/commands/aifirst.md)

---

## Version History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-04-23 | Mark Snow | Initial pipeline doc — 5 phases, T01–T05 definitions, knowledge graph node model |
