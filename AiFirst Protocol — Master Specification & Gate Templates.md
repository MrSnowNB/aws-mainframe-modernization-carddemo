# AiFirst Protocol — Master Specification & Gate Templates

> **Repository:** [MrSnowNB/Morty](https://github.com/MrSnowNB/Morty)
> **Protocol Version:** `aifirst/1.0`
> **Date Authored:** 2026-04-23
> **Status:** DRAFT → ready for commit to `main`

***

## Overview

The `/aifirst` protocol is a **slash-command-driven, gate-validated execution standard** for all AI-assisted tasks in the Morty harness and downstream projects. Every task that invokes `/aifirst` must pass through five sequential gates before it is considered complete. Each gate has a corresponding Markdown file with a YAML front-matter header that the AI agent must populate in full before progression is allowed.

This protocol formalizes the existing patterns in the Morty repo — `AI-FIRST-IMPROVEMENT-PLAN.md`, `CHECKPOINT.md`, `POST-MORTEM.md`, and the `.claude/` command directory — into a single, repeatable, auditable system. It directly extends the `feat/ai-first-playbooks-and-validation-gates` branch work and the `task_id` propagation design.[^1]

***

## Design Principles

- **Gate-first execution** — no code runs before the plan is documented and optionally ACK'd
- **No simulated data** — validation tiers must use real outputs; mocked/synthetic data auto-fails G3
- **Append-only logging** — `run.log` is JSON-L; never overwrite, only append
- **Halt-on-failure** — any gate failure writes `BLOCKED` and stops; agents do not self-correct without re-entering G0
- **Traceability** — every file carries a `task_id`, every sub-step carries a `step_id`; both propagate into logs and PR titles[^1]
- **Human ACK on risk** — if `risk_flags` is non-empty in G0, a human must acknowledge before G1 opens

***

## Gate Flow

```
PLAN → SCAFFOLD → EXECUTE → VALIDATE → COMMIT
 G0       G1         G2         G3        G4
```

Each gate writes a `.md` file with a YAML header. The AI populates it. If the gate passes, status flips to `PASS` and the next gate opens. If it fails, status flips to `FAIL` → `BLOCKED` and the run halts.

***

## File Layout

All protocol files live inside `.claude/` in the Morty repo:

```
.claude/
  commands/
    aifirst.md                  ← slash command definition
  protocol/
    AIFIRST-SPEC.md             ← this document
    gates/
      G0-plan.template.md
      G1-scaffold.template.md
      G2-execute.template.md
      G3-validate.template.md
      G4-commit.template.md
  runs/
    <task_id>/
      G0-plan.md
      G1-scaffold.md
      G2-execute.md
      G3-validate.md
      G4-commit.md
      run.log                   ← append-only JSON-L
```

***

## YAML Header Schema

Every gate file uses this front-matter schema. All fields are required unless marked optional.

```yaml
---
schema_version: "aifirst/1.0"
task_id: "T-YYYY-MM-DD-NNN"       # e.g. T-2026-04-23-001
gate: G0                           # G0 | G1 | G2 | G3 | G4
gate_name: "PLAN"                  # PLAN | SCAFFOLD | EXECUTE | VALIDATE | COMMIT
status: PENDING                    # PENDING | PASS | FAIL | BLOCKED | OVERRIDE
agent: "model-name-here"           # exact model identifier used at this gate
timestamp_open: "ISO-8601"
timestamp_close: null              # filled on gate close
parent_task_id: null               # optional: for sub-tasks / escalations
depends_on: []                     # optional: task_ids that must PASS first
override_reason: null              # REQUIRED if status = OVERRIDE; null otherwise
---
```

**Rules:**
- `task_id` format is strictly `T-YYYY-MM-DD-NNN` with zero-padded three-digit sequence
- `status` must be one of the five enum values; any other string is a schema violation (T01 fail)
- `override_reason` must be a non-null string if and only if `status = OVERRIDE`
- `timestamp_close` must be populated before the gate can be marked `PASS`

***

## The Slash Command

**File:** `.claude/commands/aifirst.md`

```yaml
---
schema_version: "aifirst/1.0"
command: "/aifirst"
version: "1.0.0"
description: >
  Invoke the AiFirst gated validation protocol for a task.
  Creates a runs/<task_id>/ directory and opens G0-plan.md
  for population before any execution begins.
parameters:
  - name: task_name
    required: true
    type: string
    description: "Short human-readable label for the task"
  - name: tier_ceiling
    required: false
    default: T05
    type: "enum[T01,T02,T03,T04,T05]"
    description: "Highest validation tier to run in G3"
  - name: skip_human_ack
    required: false
    default: false
    type: boolean
    description: "Only valid when G0 risk_flags is empty"
behavior:
  on_invoke:
    - "Generate task_id using format T-YYYY-MM-DD-NNN"
    - "Create runs/<task_id>/ directory"
    - "Copy gate templates into runs/<task_id>/"
    - "Populate G0-plan.md YAML header and body"
    - "If risk_flags non-empty AND skip_human_ack=false: pause, surface to user, await ACK"
    - "On ACK: open G1"
  on_gate_fail:
    - "Write BLOCKED entry to run.log"
    - "Set gate status to FAIL"
    - "Surface error and blocked gate to user"
    - "Halt — do not proceed to next gate"
    - "Do not self-correct without re-entering G0"
  on_complete:
    - "Verify all five gates status = PASS"
    - "Write final POST-MORTEM block to G4-commit.md"
    - "Tag PR title with [AIFIRST-VERIFIED]"
    - "Append completion event to run.log"
---

## Usage

```
/aifirst task_name="COBOL-to-MD batch 01" tier_ceiling=T04
/aifirst task_name="NemoClaw tool-router refactor"
/aifirst task_name="Hotfix: introspect anchor bug" skip_human_ack=true
```
```

***

## Gate Templates

***

### G0 — PLAN

**File:** `.claude/protocol/gates/G0-plan.template.md`

```yaml
---
schema_version: "aifirst/1.0"
task_id: "{{TASK_ID}}"
gate: G0
gate_name: "PLAN"
status: PENDING
agent: "{{AGENT}}"
timestamp_open: "{{NOW}}"
timestamp_close: null
parent_task_id: null
depends_on: []
override_reason: null
---
```

```markdown
## Objective

<!-- One clear sentence: what will be true when this task is done? -->

## Scope

<!-- Bullet list of what IS included -->

## Out of Scope

<!-- Bullet list of what is explicitly excluded -->

## Success Criteria

<!-- Measurable, testable conditions. Each item maps to a G3 validation tier. -->
- [ ] SC-01:
- [ ] SC-02:
- [ ] SC-03:

## Risk Flags

<!-- List anything that could block, corrupt, or cause unexpected side effects.
     If non-empty, human ACK is required before G1 opens. Leave empty [] if none. -->
risk_flags:
  - flag: ""
    mitigation: ""

## Inputs

<!-- Files, APIs, models, or data the task depends on. Include SHA or version where known. -->

## Outputs

<!-- Files, artifacts, or state changes the task will produce. -->

## Rollback Plan

<!-- How to undo if G2 or G3 fails. -->
```

**Gate pass condition:** All sections populated; `risk_flags` either empty or human-ACK'd; `timestamp_close` set.

***

### G1 — SCAFFOLD

**File:** `.claude/protocol/gates/G1-scaffold.template.md`

```yaml
---
schema_version: "aifirst/1.0"
task_id: "{{TASK_ID}}"
gate: G1
gate_name: "SCAFFOLD"
status: PENDING
agent: "{{AGENT}}"
timestamp_open: "{{NOW}}"
timestamp_close: null
parent_task_id: null
depends_on: ["{{TASK_ID}}/G0"]
override_reason: null
---
```

```markdown
## File Manifest

<!-- Every file that will be created, modified, or deleted.
     Record current SHA for all modified/deleted files (for rollback).
     New files: sha = null -->

| Action   | Path                          | Current SHA  | Notes           |
|----------|-------------------------------|--------------|-----------------|
| CREATE   | path/to/new-file.md           | null         |                 |
| MODIFY   | path/to/existing-file.md      | abc1234      |                 |
| DELETE   | path/to/old-file.md           | def5678      | confirm backup  |

## Branch

<!-- Feature branch to be used for this task -->
branch: "feat/{{TASK_ID}}"

## Stub Verification

<!-- After scaffold commit, confirm each file exists with correct structure -->
- [ ] All CREATE files exist with correct YAML headers
- [ ] All MODIFY files backed up to rollback branch
- [ ] Scaffold commit pushed to branch

## Dry-Run Notes

<!-- Anything observed during scaffolding that changes the G0 plan -->
```

**Gate pass condition:** All files in manifest exist; stub verification checklist complete; no implementation code yet committed; `timestamp_close` set.

***

### G2 — EXECUTE

**File:** `.claude/protocol/gates/G2-execute.template.md`

```yaml
---
schema_version: "aifirst/1.0"
task_id: "{{TASK_ID}}"
gate: G2
gate_name: "EXECUTE"
status: PENDING
agent: "{{AGENT}}"
timestamp_open: "{{NOW}}"
timestamp_close: null
parent_task_id: null
depends_on: ["{{TASK_ID}}/G1"]
override_reason: null
---
```

```markdown
## Step Log

<!-- Each sub-step is appended here AND to run.log as a JSON-L event.
     step_id format: {{TASK_ID}}-S-NNN -->

| step_id              | description                    | status  | timestamp            | notes |
|----------------------|-------------------------------|---------|----------------------|-------|
| {{TASK_ID}}-S-001    |                               | PENDING |                      |       |
| {{TASK_ID}}-S-002    |                               | PENDING |                      |       |

## Error Log

<!-- Any errors encountered during execution.
     If ANY error is logged here, gate status = FAIL → BLOCKED immediately. -->

| step_id | error_type | message | action_taken |
|---------|-----------|---------|--------------|

## Drift Notes

<!-- Any deviation from G0 Scope or G1 File Manifest. Document here AND re-open G0 if scope changes. -->

## Completion Checklist

- [ ] All steps PASS
- [ ] Error log empty (or OVERRIDE with reason)
- [ ] run.log append-only integrity confirmed
- [ ] No scope drift (or G0 re-opened)
```

**Gate pass condition:** All steps `PASS`; error log empty (or `OVERRIDE` with reason documented); `timestamp_close` set.

***

### G3 — VALIDATE

**File:** `.claude/protocol/gates/G3-validate.template.md`

```yaml
---
schema_version: "aifirst/1.0"
task_id: "{{TASK_ID}}"
gate: G3
gate_name: "VALIDATE"
status: PENDING
agent: "{{AGENT}}"
timestamp_open: "{{NOW}}"
timestamp_close: null
parent_task_id: null
depends_on: ["{{TASK_ID}}/G2"]
tier_ceiling: T05
override_reason: null
---
```

```markdown
## Validation Tier Results

<!-- Run tiers sequentially. Any FAIL halts further tiers and sets gate to BLOCKED.
     Do NOT use mocked, synthetic, or simulated data at any tier. -->

### T01 — Schema Validity
**Threshold:** 100% pass
**Test:** YAML front-matter parseable; all required fields present; status enum valid; override_reason rules enforced.

| file | yaml_valid | fields_complete | status_enum_valid | result |
|------|-----------|-----------------|-------------------|--------|
|      |           |                 |                   |        |

**T01 Result:** PENDING

---

### T02 — Structural Correctness
**Threshold:** 100% pass
**Test:** All scaffold files exist; no empty stub bodies; no placeholder text remaining ({{TASK_ID}}, {{AGENT}}, {{NOW}} all resolved).

| file | exists | no_empty_stubs | placeholders_resolved | result |
|------|--------|----------------|----------------------|--------|
|      |        |                |                      |        |

**T02 Result:** PENDING

---

### T03 — Functional Output
**Threshold:** ≥95% pass
**Test:** Task-specific functional correctness (e.g., COBOL→MD translation parseable; tool-router routes correct tool; introspect returns valid anchor).

| test_case_id | description | expected | actual | pass |
|-------------|-------------|----------|--------|------|
|             |             |          |        |      |

**T03 Score:** 0/0 (0%)
**T03 Result:** PENDING

---

### T04 — Semantic Accuracy
**Threshold:** ≥85% pass
**Test:** Human rubric or LLM-as-judge evaluation. Rubric defined per task in G0 Success Criteria.

| item_id | criterion | score_0_to_5 | notes |
|---------|-----------|--------------|-------|
|         |           |              |       |

**T04 Score:** 0/0 (0%)
**T04 Result:** PENDING

---

### T05 — Regression
**Threshold:** ≥ prior baseline (no regression)
**Test:** SWE-bench Lite/Verified, or prior task baseline, run with identical harness and submission tooling.

| benchmark | baseline_score | current_score | delta | pass |
|-----------|---------------|---------------|-------|------|
|           |               |               |       |      |

**T05 Result:** PENDING

---

## Gate Summary

| Tier | Threshold | Result  |
|------|-----------|---------|
| T01  | 100%      | PENDING |
| T02  | 100%      | PENDING |
| T03  | ≥95%      | PENDING |
| T04  | ≥85%      | PENDING |
| T05  | ≥baseline | PENDING |

**G3 Overall:** PENDING
```

**Gate pass condition:** All tiers up to `tier_ceiling` return `PASS`; no synthetic data used; `timestamp_close` set.

***

### G4 — COMMIT

**File:** `.claude/protocol/gates/G4-commit.template.md`

```yaml
---
schema_version: "aifirst/1.0"
task_id: "{{TASK_ID}}"
gate: G4
gate_name: "COMMIT"
status: PENDING
agent: "{{AGENT}}"
timestamp_open: "{{NOW}}"
timestamp_close: null
parent_task_id: null
depends_on: ["{{TASK_ID}}/G3"]
override_reason: null
---
```

```markdown
## Pre-Commit Verification

- [ ] All five gates (G0–G3) status = PASS
- [ ] run.log integrity verified (no overwritten lines)
- [ ] Branch is `feat/{{TASK_ID}}`
- [ ] No uncommitted changes outside the task scope

## Post-Mortem

### What was planned (G0) vs. what was built (G2)
<!-- Describe any drift. "No drift" is a valid and good answer. -->

### Metrics Delta
<!-- Compare G3 results to G0 Success Criteria -->

| success_criterion | target | achieved | delta |
|-------------------|--------|----------|-------|
| SC-01             |        |          |       |
| SC-02             |        |          |       |
| SC-03             |        |          |       |

### Lessons Learned
<!-- What would you change in G0 next time? Any surprises? -->

### Open Issues
<!-- Anything NOT resolved that should become a new /aifirst task -->
- [ ]

## PR

- **Title:** `[AIFIRST-VERIFIED] {{task_name}} ({{TASK_ID}})`
- **Branch:** `feat/{{TASK_ID}}` → `main`
- **Linked run:** `.claude/runs/{{TASK_ID}}/`
- **Validation summary:** T01✅ T02✅ T03✅ T04✅ T05✅
```

**Gate pass condition:** Pre-commit checklist complete; post-mortem all sections populated; PR opened with `[AIFIRST-VERIFIED]` tag; `timestamp_close` set.[^2]

***

## run.log Schema

`run.log` is **append-only JSON-L** (one JSON object per line). Never truncate or overwrite.

```jsonc
// Gate open event
{"event":"gate_open","task_id":"T-2026-04-23-001","gate":"G0","agent":"qwen3","ts":"2026-04-23T08:02:00Z"}

// Step event (G2)
{"event":"step","task_id":"T-2026-04-23-001","gate":"G2","step_id":"T-2026-04-23-001-S-001","desc":"translate CICS001.cbl","status":"PASS","ts":"2026-04-23T08:15:22Z"}

// Validation tier event (G3)
{"event":"tier","task_id":"T-2026-04-23-001","gate":"G3","tier":"T03","score":0.97,"threshold":0.95,"status":"PASS","ts":"2026-04-23T08:20:10Z"}

// Gate close event
{"event":"gate_close","task_id":"T-2026-04-23-001","gate":"G3","status":"PASS","ts":"2026-04-23T08:20:11Z"}

// Blocked event
{"event":"blocked","task_id":"T-2026-04-23-001","gate":"G3","tier":"T04","reason":"score 0.81 below threshold 0.85","ts":"2026-04-23T08:21:00Z"}

// Completion event
{"event":"complete","task_id":"T-2026-04-23-001","pr":"https://github.com/MrSnowNB/Morty/pull/N","tag":"[AIFIRST-VERIFIED]","ts":"2026-04-23T08:30:00Z"}
```

The JSON-L format allows the fine-tuning pipeline to consume `run.log` directly as training signal — each `step` and `tier` event becomes a labeled example.

***

## Integration Points

### COBOL → MD Pipeline (`aws-mainframe-modernization-carddemo`)

Wire `/aifirst` as the outer envelope for each translation batch:[^3]

- **G0:** Define batch scope (file list, complexity tier, schema_version contract)
- **G3/T03:** YAML validity + field-level match against gold set
- **G3/T04:** LLM-as-judge faithfulness rubric (semantic accuracy)
- **G3/T05:** Before/after SWE-bench Lite comparison

### NemoClaw / OpenClaw Harness

Each harness refactor or new tool integration becomes a `/aifirst` task. The `AI-First Architecture v2.0` 16-file structure maps cleanly to G1 scaffolding.

### Fine-Tuning Pipeline

`run.log` events feed directly into the training data collector. Passing T03/T04 examples become positive training samples; `BLOCKED` events with their preceding steps become negative examples.

***

## Example: First Run

A fully worked example lives at `.claude/runs/T-2026-04-23-001/` — one batch of COBOL→MD translation with all five gate files and a complete `run.log`.

```
/aifirst task_name="COBOL-to-MD pilot batch" tier_ceiling=T04
```

| Gate | File | Populated By | Status |
|------|------|-------------|--------|
| G0 | G0-plan.md | Agent | PASS |
| G1 | G1-scaffold.md | Agent | PASS |
| G2 | G2-execute.md | Agent | PASS |
| G3 | G3-validate.md | Agent + T03 scorer | PASS |
| G4 | G4-commit.md | Agent | PASS |

PR title: `[AIFIRST-VERIFIED] COBOL-to-MD pilot batch (T-2026-04-23-001)`

***

## Version History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-04-23 | Mark Snow / Perplexity | Initial draft from Morty repo patterns |

---

## References

1. [Create new PR [https://github.com/MrSnowNB/Morty](https://github.com/MrSnowNB/Morty) I reset the Github credentials](https://www.perplexity.ai/search/f1161639-a1af-4e47-8b59-a93a99fa6ae4) - You can’t create a PR from that branch right now because there are no differences between main and f...

2. [I merged but I do not see any actual changes. Check the repo](https://www.perplexity.ai/search/574f27d5-ed5d-4e74-a6a2-9d4df58f97db) - Everything is confirmed on main.  The changes are there — you may just need to do a git pull in your...

3. [[https://github.com/MrSnowNB/aws-mainframe-modernization-carddemo](https://github.com/MrSnowNB/aws-mainframe-modernization-carddemo) I need to convert COBOL to Markdown files with YAML headers. I have it sitting in VScode with Cline and Qwen3.635B A3...

... check the accuracy, then fine tune the Qwen model for this task, then re-run the experiment and check accuracy. I will also need to compare the before and after models on SWE Bench. I need all data logged and Captured  /AiFirst. Research and discuss](https://www.perplexity.ai/search/4fe06255-fc60-4cfb-8159-b184ef9e9fe7) - Finding  [GPT-5.4 Thinking](pplx://action/model_info?id=gpt54_thinking&provider=openai)  [Claude Opu...
