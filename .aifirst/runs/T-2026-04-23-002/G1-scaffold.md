---
task_id: T-2026-04-23-002
gate: G1
status: PASS
opened: 2026-04-23T17:05Z
closed: 2026-04-23T17:12Z
depends_on: G0
---

# G1 — Scaffold

## File Manifest

### New scripts (to be created under G2 — chunks b+c)

| Path | Purpose | Deterministic? | Depends on |
|------|---------|----------------|------------|
| `scripts/pass1_annotate.py` | Emit one annotation record per COBOL statement | YES | `cobc -E` (substitute for `-fdiagnostics-format=json` per RF-01), `validation/structure/<F>_cfg.json` |
| `scripts/pass2_template.py` | Fill propositions from verb taxonomy templates | YES | `validation/pass1/<F>_annotations.json` |
| `scripts/pass2_override.py` | Detect `overrides_seq` by CFG-reachable same-field writes | YES | `validation/pass2/<F>_propositions.json` (intermediate) |
| `scripts/pass2_llm.py` | Bounded-context LLM call for unresolved verbs (EXEC CICS/SQL, complex EVALUATE/STRING/UNSTRING) | BOUNDED — emits request payloads when endpoint absent | `validation/pass2/<F>_llm_requests.json` |
| `scripts/pass3_synthesize.py` | LLM synthesis into `logical_groups[]` + `business_rules[]` + YAML | BOUNDED — emits payloads when endpoint absent | verified `validation/pass2/<F>_propositions.json` |
| `scripts/validate_pass1.py` | T-PASS1 / T-PASS1-CFG / T-PASS1-OPS tiers | YES | Pass 1 outputs |
| `scripts/validate_pass2.py` | T-PASS2 / T-PASS2-OPS / T-PASS2-OVR tiers | YES | Pass 2 outputs |
| `scripts/validate_pass3.py` | T-PASS3 / T-PASS3-D / T-PASS3-P / T-PASS3-CONFIDENCE | YES | Pass 3 outputs |

### Scripts modified under G2

| Path | Change | Reason |
|------|--------|--------|
| `scripts/validate_t03.py` | Add CICS-subtype threshold override: `≥0.80` when `subtype == 'CICS-Online'` AND `cfg_confidence == 'MEDIUM'`; default stays `≥0.95`. Bump to `validator_version: v1.0.2-cics-threshold`. | Plan §11 |

### Scripts untouched

`validate_t01.py`, `validate_t02.py`, `validate_t02r.py`, `score_t04.py`, `run_sweBench.sh`, `extract_cfg_summary.py` — per plan §9 "Existing scripts are unchanged."

### Schema/contract updates

| Path | Change |
|------|--------|
| `.aifirst/runs/T-2026-04-23-002/translation-prompt-contract-v2.md` | Append Rule 8 (temperature=0 + structured JSON), Rule 9 (qualified CFG names in REDEFINES), Rule 10 (semantic_pattern enum required from plan §6) |

### New directories

- `validation/pass1/`
- `validation/pass2/`
- `validation/pass3/` (created on first Pass 3 output)
- `translations/baseline-v1.1/` (created on first v1.1 MD output)

## Branch

Continue on `feat/cobol-md-schema-v1` (unchanged from T-001); T-002 artefacts are additive under new paths. No rebase required.

## Stub Verification Plan

Each new script declares a `--selftest` mode that runs on COBSWAIT and reports pass/fail without modifying files outside `/tmp/`. The selftest runs at G2 open and is logged to run.log. A selftest failure blocks the chunk it belongs to.

## Dry-Run Notes

- Pass 1: the substitute toolchain (`cobc -E` + regex tokenizer) will be tested on COBSWAIT first. COBSWAIT's PROCEDURE DIVISION has 4 statements (ACCEPT, MOVE, CALL, STOP RUN). Expected annotation count: 4.
- Pass 2: all 4 COBSWAIT statements should be fully template-covered (no EXEC CICS, no EXEC SQL, no complex EVALUATE). Expected LLM calls on COBSWAIT: 0.
- Pass 3: COBSWAIT has a single paragraph; synthesis can produce a single `logical_group` mechanically — this may qualify as template-level too and require zero LLM. Will be confirmed at smoke.

## Gate Decision

All scaffold items documented; no code written yet; no risk-flag mitigations require further human input before G2 opens for deterministic chunks. PASS. Proceed to G2.
