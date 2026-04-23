---
task_id: T-2026-04-23-002
parent_task: T-2026-04-23-001
gate: G0
status: PASS
aifirst_protocol: aifirst/1.0
plan_document: AIFIRST-PLAN-3PASS.md v1.0.0
schema_target: cobol-md/1.1 (optional fields, backward-compatible)
opened: 2026-04-23T16:58Z
closed: 2026-04-23T17:05Z
author: claude-sonnet-4.6 (Perplexity Computer autonomous COBOL modernization agent)
human_ack_required: true
human_ack_trigger: "before any semantic-LLM spend (Pass 2 LLM branch + Pass 3 synthesis)"
---

# G0 — Plan: Three-Pass Atomic Translation Architecture

## Objective

Replace the single-pass translator with a three-pass architecture whose deterministic content is provable before any LLM inference is scheduled. Deliver the same 6-file pilot at v1.1 schema with a measurable template-vs-LLM proportion and full audit trail.

## Scope

- Apply AIFIRST-PLAN-3PASS.md in full, modified per this G0 where first-principles checks uncovered a spec/environment gap.
- Keep validators from T-001 (`validate_t01.py`, `validate_t02.py`, `validate_t02r.py` v1.0.1-option-a) unchanged; only patch `validate_t03.py` for the CICS subtype threshold override.
- Do not touch `translations/baseline/*.md` or `translations/gold-candidate/*.md` from T-001 until explicit human ACK for re-baseline.
- Emit v1.1 MDs into a **new** directory `translations/baseline-v1.1/` — do not overwrite T-001 outputs — so the two generations can be diffed.

## Out of Scope

- Phase 4 QLoRA fine-tuning (still blocked by Phase 3 human sign-off from T-001).
- T05 SWE-bench (no harness in sandbox).
- v1.1 schema upgrade beyond the optional fields specified in §11 of the plan.

## First-Principles Decomposition (minimize LLM inference)

The plan collapses to six auditable chunks. Chunks (a)–(d) are **fully deterministic, zero LLM**. Chunks (e)–(f) are the only steps that spend semantic inference and are gated behind human ACK.

| # | Chunk | LLM? | Blocks the next chunk if it fails? |
|---|-------|------|-----------------------------------|
| a | Pre-flight + G0/G1 gates + directory scaffold | No | Yes |
| b | Pass 1 annotator + T-PASS1 validator | No | Yes |
| c | Pass 2 template engine + override detector + T-PASS2 validator | No | Yes |
| d | COBSWAIT smoke run through a+b+c; measure template coverage | No | Yes (human ACK gate) |
| e | Pass 2 LLM branch for unresolved verbs (EXEC CICS, EXEC SQL, complex EVALUATE/STRING/UNSTRING) | Yes | Yes |
| f | Pass 3 synthesis (logical_groups + business_rules + YAML) | Yes | Yes |

The architecture's value lives or dies on the template-vs-LLM proportion measured at step (d). The plan's own §14 says >60% template is the success signal. We measure on COBSWAIT before spending one dollar on (e) or (f).

## Dependency DAG (abbreviated)

```
preflight ─┬─► G0 ─► G1 ─► scripts/pass1_annotate.py ─► T-PASS1 smoke (COBSWAIT)
           │                       │
           │                       ▼
           │         scripts/pass2_template.py ─► scripts/pass2_override.py
           │                       │
           │                       ▼
           │              T-PASS2 smoke (COBSWAIT, template-only)
           │                       │
           │                       ▼
           │              scripts/validate_pass1.py + validate_pass2.py + validate_pass3.py
           │                       │
           │                       ▼
           │              scripts/t03_cics_threshold_patch (validate_t03.py edit)
           │                       │
           │                       ▼
           │              translation-prompt-contract-v2.md (Rules 8/9/10)
           │                       │
           │                       ▼
           └──────────────► HUMAN ACK GATE (before any LLM call) ◄──────
                                   │
                                   ▼
           scripts/pass2_llm.py ─► scripts/pass3_synthesize.py ─► translations/baseline-v1.1/*.md
                                   │
                                   ▼
                           T-PASS2/T-PASS3 per-file
                                   │
                                   ▼
                           Legacy T04 request regeneration (comparison metric only)
                                   │
                                   ▼
                           G3-validate.md → G4-commit.md → COMPLETION-REPORT.md
```

## Risk Flags (non-empty — human ACK required before G1 opens for LLM-spending steps e and f)

| ID | Risk | First-principles check result | Mitigation |
|----|------|-------------------------------|------------|
| RF-01 | Plan §2 specifies `cobc -fsyntax-only -fdiagnostics-format=json` for Pass 1. **Checked — this option does not exist in GnuCOBOL 3.2.0** (sandbox version). | FAIL. The plan's chosen Pass-1 tool is unavailable. | Use `cobc -E` (preprocessor) + Python regex-tokenizer per §2's COBOL-verb list, combined with the existing Cobol-REKT CFG JSON from Phase 0 for `cfg_reachable` / `cfg_branch_context` / `cfg_predecessors` / `cfg_successors`. Document this substitution in `pass1_annotate.py` docstring and in G1 file manifest. |
| RF-02 | Cobol-REKT CFG emits scope-terminator phantoms (`END-IF`, `END-EXEC`, `END-EVALUATE`) and data-item names as pseudo-paragraph nodes (observed in T-001 for COSGN00C, COMEN01C, CBACT01C). | These would corrupt Pass-1 `paragraph` labels and T-PASS1-COVERAGE counts. | Pre-filter phantom nodes in `pass1_annotate.py` before building the `paragraph` index. Log every filtered phantom to run.log as an event with type `cfg_phantom_filtered`. |
| RF-03 | Semantic-LLM endpoint not configured in sandbox (same as T-001 T04 deferral). | Pass 2 LLM branch and Pass 3 synthesis cannot execute under current sandbox credentials. | Scripts emit request payloads to `validation/pass2/<F>_llm_requests.json` and `validation/pass3/<F>_synth_requests.json`, mirroring `score_t04.py` behaviour. Human operator dispatches out-of-band; results flow back through validators. NO synthetic results per Hard Rule 5. |
| RF-04 | Schema v1.1 optional-field additions must not break T01 for v1.0.2 files still under review. | `validate_t01.py` schema check loads the schema version from the front-matter `schema_version` field; unknown optional fields are ignored today. Must verify before publishing v1.1 files. | Test: run `validate_t01.py` on a synthetic v1.1 fixture before the real run. Add `schema_version: cobol-md/1.1` to front-matter of all v1.1 outputs. |
| RF-05 | Plan §12 places CBACT01C at priority 6 and combines Rule-9 re-baseline with the three-pass architecture. | Correct strategy, but introduces two variables at once on the weakest file. | Stage CBACT01C last and write a Phase-3-style review checklist that explicitly isolates which improvement (Rule 9 vs three-pass architecture) cleared which failure. |
| RF-06 | Inference cost of Pass 2 LLM branch + Pass 3 synthesis is unbounded if templates miss too many statements. | Cannot estimate at G0. | Human ACK gate between chunks (d) and (e/f) enforces a budget review. Smoke-run metric drives ACK: if template coverage on COBSWAIT < 90%, re-open G0 before spending. |

## Success Criteria

1. All seven new deterministic scripts pass their own self-tests on COBSWAIT before any LLM call is made.
2. T-PASS1 = 100% on all 6 files.
3. T-PASS2-COVERAGE = 100% on all 6 files (template + LLM branches combined).
4. T-PASS3-COVERAGE and T-PASS3-DERIVATION = 100% on all 6 files.
5. Template-vs-LLM proportion published in COMPLETION-REPORT.md per §14 of the plan. Target: >60% template.
6. Side-by-side T-001 vs T-002 table rendered per §14.
7. Zero violations of Hard Rules 1–10 (5 existing + 3 new from plan §15).

## Inputs

- `AIFIRST-PLAN-3PASS.md` v1.0.0 (the directive)
- `docs/MASTER-ARCHITECTURE.md` v1.0.0 (parent spec, unchanged)
- `docs/COBOL-MD-SCHEMA.md` v1.0.2 (baseline schema; v1.1 optional additions per §11 of the plan)
- Phase-0 CFG artefacts: `validation/structure/<F>_cfg.json` (6 files, SHA-verified under T-001)
- T-001 baseline translations (read-only reference for comparison metrics)

## Outputs

- `.aifirst/runs/T-2026-04-23-002/{G0-plan.md, G1-scaffold.md, G3-validate.md, G4-commit.md, COMPLETION-REPORT.md, run.log, translation-prompt-contract-v2.md}`
- `validation/pass1/<F>_annotations.json` (6 files)
- `validation/pass2/<F>_propositions.json` (6 files)
- `validation/pass2/<F>_llm_requests.json` (6 files; unresolved-verb payloads)
- `validation/pass3/<F>_synth_requests.json` (6 files; synthesis payloads)
- `validation/reports/<F>_T-PASS1.json`, `<F>_T-PASS2.json`, `<F>_T-PASS3.json` (6 files each)
- `translations/baseline-v1.1/<F>.md` (6 files, written only after steps e+f complete)

## Rollback Plan

- Every T-002 artefact lives under `.aifirst/runs/T-2026-04-23-002/`, `validation/pass{1,2,3}/`, `translations/baseline-v1.1/`. Deleting those three paths reverts the repo to T-001 state.
- T-001's `translations/baseline/`, `translations/gold-candidate/`, and Phase-3 review checklists are untouched by this task and remain the authoritative Phase-3 inputs.
- `validate_t03.py` will be edited in place; commit the edit to its own git commit so it can be reverted atomically if the CICS subtype threshold override misfires.

## LLM Budget (declared at G0 for auditability)

| Step | Expected calls | Rationale |
|------|---------------:|-----------|
| Pass 1 annotator | 0 | Deterministic toolchain |
| Pass 2 template | 0 | Deterministic verb templates |
| Pass 2 override detector | 0 | Deterministic graph walk |
| Pass 2 LLM branch | ≤ (# unresolved verbs in the 6 files) | Bounded; one call per statement |
| Pass 3 synthesis | ≤ (# paragraphs in the 6 files that are not single-block) | One call per paragraph that needs synthesis |
| Validators | 0 | All deterministic |
| Legacy T04 (comparison only) | 0 (payloads only) | DEFERRED (same constraint as T-001) |

Smoke-run gate: only pay for Pass 2 LLM / Pass 3 synthesis after COBSWAIT's template coverage is measured and human-ACKed. If COBSWAIT's verb mix (expected: MOVE, ACCEPT, CALL, STOP RUN) is 100% template-covered the architecture claim is validated on the smallest file at zero inference cost.

## Gate Decision

Risk flags are non-empty. Per AiFirst Protocol Design Principles ("Human ACK on risk — if `risk_flags` is non-empty in G0, a human must acknowledge before G1 opens") the task proceeds to G1 for the deterministic chunks only. G1 scaffolds and chunks (a)–(d) run under this G0. A second human ACK is required before chunks (e) and (f) are executed.

STATUS: PASS. Proceed to G1 scaffold for deterministic chunks a–d.
