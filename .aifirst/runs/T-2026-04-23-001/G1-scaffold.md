---
schema_version: "aifirst/1.0"
task_id: "T-2026-04-23-001"
gate: G1
gate_name: "SCAFFOLD"
status: PASS
agent: "claude-sonnet-4.6"
timestamp_open: "2026-04-23T14:04:22Z"
timestamp_close: "2026-04-23T14:05:00Z"
parent_task_id: null
depends_on: ["T-2026-04-23-001/G0"]
override_reason: null
---

## File Manifest

| Action | Path | Current SHA | Notes |
|--------|------|-------------|-------|
| CREATE | validation/structure/ | null | Phase 0 CFG JSON artifacts per file |
| CREATE | validation/reports/ | null | T01–T05 JSON reports per file per tier |
| CREATE | translations/baseline/ | null | Phase 1 MD outputs |
| CREATE | translations/gold/ | null | Phase 3 human-verified (empty at G1) |
| CREATE | translations/post-finetune/ | null | Phase 5 (empty) |
| CREATE | scripts/extract_cfg_summary.py | null | Phase 0 CFG summariser |
| CREATE | scripts/validate_t01.py | null | T01 schema validator |
| CREATE | scripts/validate_t02.py | null | T02 structural diff |
| CREATE | scripts/validate_t02r.py | null | T02-R REDEFINES subcheck |
| CREATE | scripts/validate_t03.py | null | T03 field-level comparator |
| CREATE | scripts/score_t04.py | null | T04 judge-request scaffold |
| CREATE | scripts/run_sweBench.sh | null | T05 DEFERRED harness |
| CREATE | .aifirst/runs/T-2026-04-23-001/* | null | gate files + run.log |

## Branch

branch: "feat/cobol-md-schema-v1" (existing branch — task T-2026-04-23-001 adds artifacts only; no rename)

## Stub Verification

- [x] All CREATE directories exist (`validation/structure/`, `validation/reports/`, `translations/baseline/`, etc.)
- [x] All seven Python/Bash validator scripts exist and are executable
- [x] `.aifirst/runs/T-2026-04-23-001/` exists with `run.log` and `G0-plan.md`
- [x] No implementation code committed yet — this gate only scaffolds
- [x] PyYAML installed in Python 3.12

## Tooling Confirmed

- GnuCOBOL `cobc` 3.2.0 — T02 fallback parser available
- Java 21.0.10 + Cobol-REKT smojol-cli.jar v0.1.0-RC8 — tested: COBSWAIT.cbl emits CFG JSON ✅
- PyYAML 6.0.3 — available

## Dry-Run Notes

- Cobol-REKT CLI requires the filename WITH `.cbl` extension as the program argument; permissive search alone is insufficient without the extension. `extract_cfg_summary.py` invokes it this way.
- Cobol-REKT emits CFG under `<report>/cfg/cfg-<FILE>.cbl.json` with UUID-keyed nodes (SENTENCE / PARAGRAPH / SECTION / PROCEDURE_DIVISION_BODY). Reachability is not directly tagged per paragraph, so the summariser cross-references source-text PERFORM / GO TO edges to compute `reachable` per paragraph.
- No scope drift against G0.
