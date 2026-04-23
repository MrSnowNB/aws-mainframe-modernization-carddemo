# AiFirst Protocol — Master Specification

> **Protocol Version:** `aifirst/1.0`
> **Status:** ACTIVE

## Overview

The `/aifirst` protocol is a **gate-validated execution standard** for all AI-assisted tasks. Every task must pass through five sequential gates before it is considered complete. Each gate has a corresponding Markdown file with a YAML front-matter header that the AI agent must populate in full before progression is allowed.

This protocol implements a **first principles problem solving protocol** with gated validation testing to prove 100% accurate translation.

## Design Principles

- **Gate-first execution** — no code runs before the plan is documented.
- **No simulated data** — validation tiers must use real outputs; mocked/synthetic data auto-fails G3.
- **Append-only logging** — logs are append-only.
- **Halt-on-failure** — any gate failure writes `BLOCKED` and stops; agents do not self-correct without re-entering G0.
- **Traceability** — every file carries a `task_id`, every sub-step carries a `step_id`; both propagate into PR titles.

## Gate Flow

```
PLAN → SCAFFOLD → EXECUTE → VALIDATE → COMMIT
 G0       G1         G2         G3        G4
```

Each gate writes a `.md` file with a YAML header. The AI populates it. If the gate passes, status flips to `PASS` and the next gate opens. If it fails, status flips to `FAIL` → `BLOCKED` and the run halts.

## File Layout

All protocol files live inside `.clinerules/`:

```
.clinerules/
  00-aifirst-protocol.md          ← this document
  01-cobol-to-md.md               ← translation rules
  protocol/
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

## run.log Schema

`run.log` is **append-only JSON-L** (one JSON object per line). Never truncate or overwrite.

```jsonc
// Gate open event
{"event":"gate_open","task_id":"T-2026-04-23-001","gate":"G0","agent":"qwen3.6","ts":"2026-04-23T08:02:00Z"}

// Step event (G2)
{"event":"step","task_id":"T-2026-04-23-001","gate":"G2","step_id":"T-2026-04-23-001-S-001","desc":"translate CICS001.cbl","status":"PASS","ts":"2026-04-23T08:15:22Z"}

// Validation tier event (G3)
{"event":"tier","task_id":"T-2026-04-23-001","gate":"G3","tier":"T03","score":0.97,"threshold":0.95,"status":"PASS","ts":"2026-04-23T08:20:10Z"}

// Gate close event
{"event":"gate_close","task_id":"T-2026-04-23-001","gate":"G3","status":"PASS","ts":"2026-04-23T08:20:11Z"}

// Blocked event
{"event":"blocked","task_id":"T-2026-04-23-001","gate":"G3","tier":"T04","reason":"score 0.81 below threshold 0.85","ts":"2026-04-23T08:21:00Z"}

// Completion event
{"event":"complete","task_id":"T-2026-04-23-001","pr":"PR_URL","tag":"[AIFIRST-VERIFIED]","ts":"2026-04-23T08:30:00Z"}
```
