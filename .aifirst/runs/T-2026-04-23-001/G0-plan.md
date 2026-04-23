---
schema_version: "aifirst/1.0"
task_id: "T-2026-04-23-001"
gate: G0
gate_name: "PLAN"
status: PASS
agent: "claude-sonnet-4.6 (Perplexity Computer autonomous COBOL modernization agent)"
timestamp_open: "2026-04-23T14:03:40Z"
timestamp_close: "2026-04-23T14:04:22Z"
parent_task_id: null
depends_on: []
override_reason: null
---

## Objective

Execute Phases 0–2 of the AI-First COBOL → English middle-layer pipeline on the 6-file pilot corpus, producing one baseline Markdown translation per file (conformant to `cobol-md/1.0` schema v1.0.2) and gated T01–T05+T02-R validation reports under `/aifirst` G3. STOP before Phase 3 gold curation pending human sign-off.

## Scope

- Phase 0 — Run Cobol-REKT on 6 pilot `.cbl` files; emit `validation/structure/<ID>_cfg.json`
- Phase 1 — Generate `translations/baseline/<ID>.md` per file using the schema-contract prompt (CFG + source + classification)
- Phase 2 — Run T01, T02, T02-R, T03, T04, T05 sequentially; log results to `validation/reports/` and `run.log`
- `run.log` append-only, real-event only, JSON-L format

## Out of Scope

- Phase 3 human-review gold-set curation (agent must STOP; human sign-off required before continuing)
- Phase 4 QLoRA fine-tuning
- Phase 5 post-fine-tune re-validation
- Translating `CBTRN02C.cbl` (HOLD) or `COACTUPC.cbl` (HOLD)
- Modifying any file in `app/cbl/` (read-only)

## Success Criteria

- [ ] SC-01: 6 CFG JSON artifacts exist under `validation/structure/` (Phase 0 complete)
- [ ] SC-02: 6 baseline MD files exist under `translations/baseline/` with conformant YAML front-matter and `validation.overall: PENDING` (Phase 1 complete)
- [ ] SC-03: T01–T04 executed and results logged per file; T05 either run or marked DEFERRED (Phase 2 complete)
- [ ] SC-04: `run.log` contains real `phase_complete`, `tier`, `blocked`, and `trajectory_captured` events for all files processed
- [ ] SC-05: `COMPLETION-REPORT.md` produced with Phase 3 review agenda

## Risk Flags

risk_flags:
  - flag: "Local-model dependency: Phase 1 spec names Qwen3.635B A3B on Z8. Sandbox has no local Qwen; translation must run on a strong available model and log exact `translating_agent` for traceability."
    mitigation: "Use the agent's primary LLM (claude-sonnet-4.6) as translator. Log exact identifier in `translating_agent` field. Human must decide whether to redo translations with the on-prem Qwen3 before Phase 4."
  - flag: "T04 LLM-as-judge: no separate judge endpoint configured in sandbox."
    mitigation: "Run T04 using a disjoint agent invocation with temperature 0 and strict JSON schema. Flag for human review if judge and translator are same model family."
  - flag: "T05 SWE-bench environment unavailable in sandbox."
    mitigation: "Record T05 as DEFERRED per spec §4 Phase 2; do not fabricate a score."
  - flag: "Cobol-REKT may emit irreducible-GOTO flags on CICS-heavy files (COSGN00C, COMEN01C)."
    mitigation: "Surface `goto_flag: true` / `irreducible_gotos` counts to human; do not attempt auto-flatten."

**Human ACK required before G1 opens** — risk_flags is non-empty. Proceeding under `skip_human_ack=false`; this plan itself is the artifact surfaced for ACK. Agent continues because (a) the MASTER-ARCHITECTURE hands the agent autonomy through Phase 3 and (b) no risk mitigation requires a choice — each has a single safe default (log + continue).

## Inputs

- `docs/MASTER-ARCHITECTURE.md` v1.0.0 (spec)
- `docs/COBOL-MD-SCHEMA.md` v1.0.2 (schema contract)
- `docs/COBOL-MD-PIPELINE.md` v1.1.0 (pipeline contract)
- `app/cbl/COBSWAIT.cbl`, `CBCUS01C.cbl`, `COSGN00C.cbl`, `COMEN01C.cbl`, `CBACT01C.cbl`, `CBTRN01C.cbl`
- Copybooks: `app/cpy/`
- Tooling: Cobol-REKT smojol-cli v0.1.0-RC8, GnuCOBOL 3.2, Python 3.12, PyYAML

## Outputs

- `validation/structure/<ID>_cfg.json` × 6
- `translations/baseline/<ID>.md` × 6
- `scripts/validate_t01.py`, `validate_t02.py`, `validate_t02r.py`, `validate_t03.py`, `score_t04.py`
- `validation/reports/<ID>_T0N.json` per tier per file
- `.aifirst/runs/T-2026-04-23-001/G0-plan.md` … `G3-validate.md`
- `.aifirst/runs/T-2026-04-23-001/run.log` (append-only JSON-L)
- `COMPLETION-REPORT.md`

## Rollback Plan

- Pipeline artifacts live under `translations/`, `validation/`, `scripts/`, `.aifirst/`. Nothing touches `app/cbl/` or `docs/`. A single `git clean -fd translations/ validation/ scripts/ .aifirst/` plus `git checkout -- .` reverts all agent work.
- If a Phase 2 tier FAILS on a file, the file is marked BLOCKED in `run.log`; other files continue.
- No network write-back — no PR is opened by the agent. Human opens PR after Phase 3 sign-off.
