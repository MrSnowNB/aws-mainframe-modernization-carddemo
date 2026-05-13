---
agent_task_id: COBOL-TRANSLATE-REPAIR-001
date: "2026-05-06"
repo: MrSnowNB/aws-mainframe-modernization-carddemo
branch: main
model_hint: "qwen3 or equivalent local reasoning model"
priority: critical
mode: first_principles_atomic
max_loop_iterations: 20
failure_protocol: read_postmortem_then_classify_then_fix
gate_protocol: COBOL-TRANSLATE-ATOMIC-V1
session_log: docs/GEMINI_SESSION_SCRATCHPAD_2026-05-05.md
status: closed
---

# Agent Task: Repair COBOL Translation Pipeline

## Mission

The SecuraTron COBOL-to-AI harness (`app/`) is partially operational. The Docker container boots, the FastAPI endpoint accepts requests, and the 3-pass pipeline fires. However, the pipeline **never completes successfully** for any COBOL file. Your job is to work through each failure atomically, using first-principles problem-solving loops, until `translations/gold-candidate/COBSWAIT.md` is produced with non-zero content.

Do NOT attempt multiple fixes at once. Do NOT make assumptions about what is broken — read the artifact evidence first.

---

## Ground Truth Files (Read These First)

```
docs/GEMINI_SESSION_SCRATCHPAD_2026-05-05.md   ← full failure catalog from prior session
app/harness/atoms/cobol_pipeline_worker.py     ← main orchestrator
app/harness/atoms/cobol_llm_evaluate.py        ← 3-pass pipeline atom
app/harness/atoms/infra_patch_worker.py        ← SIL patch worker (ALREADY HARDENED)
scripts/pass3run.py                            ← LLM synthesis executor
validation/gatecompare.py                      ← gate validator
app/securatron/global/bin/parsers.py           ← stdout result parser
docker-compose.yml                             ← env vars: INFERENCE_ENDPOINT, MODEL, KEY
```

---

## Known Unresolved Issues (Start Here)

### ISSUE-01 — Port Shadow / Dual `lemond` Process
- **Category:** `PORT-SHADOW`
- **Risk:** 🔴 Critical
- **Symptom:** Harness fires requests; Lemonade logs show no activity; HTTP 500 or silent hang.
- **Verify:** `ps aux | grep lemond` — should show exactly ONE process bound to `--host 0.0.0.0`.
- **Fix if broken:** `pkill lemond && sleep 2 && lemonade serve --host 0.0.0.0 --port 13305`
- **Gate:** `curl -s http://localhost:13305/v1/models | grep -c id` → must return `>= 1`

### ISSUE-02 — `urllib` Hang in `pass3run.py`
- **Category:** `SOCKET-HANG`
- **Risk:** 🔴 Critical
- **Symptom:** `ps aux` shows `pass3run.py` at 0% CPU; fans silent; session never completes.
- **Verify:** `grep -n 'import urllib' scripts/pass3run.py` — should return nothing.
- **Fix if broken:** Confirm `requests` is used for all LLM calls; `urllib` must be absent.
- **Gate:** `grep -n 'import requests' scripts/pass3run.py` → must match.

### ISSUE-03 — System Prompt Missing for JSON Mode
- **Category:** `LLM-500`
- **Risk:** 🔴 Critical
- **Symptom:** All paragraphs return `FAIL LLM HTTP 500` in `postmortem.md`.
- **Verify:** In `scripts/pass3run.py`, look for auto-inject of system message when `response_format` is `json_object`.
- **Fix if broken:** Before building `req_body`, check `if not any(m.get('role') == 'system' for m in messages)` → insert `{"role": "system", "content": "You are a COBOL modernization expert. Always respond in valid JSON format."}`
- **Gate:** Single-paragraph curl test to Lemonade with a minimal synthesis payload returns HTTP 200 + valid JSON.

### ISSUE-04 — `no_result_json_found` in Global Ledger
- **Category:** `PARSER-MISS`
- **Risk:** 🟠 High
- **Symptom:** `cobol.translate.trials.jsonl` shows `reason: no_result_json_found` even when worker appeared to run.
- **Verify:** In `app/securatron/global/bin/parsers.py`, check the regex search window size.
- **Fix if broken:** Change `raw_stdout[:500]` → `raw_stdout[:5000]`.
- **Verify worker emits:** `cobol_pipeline_worker.py` must `print("RESULT " + json.dumps({...}))` in BOTH success and except paths.
- **Gate:** Run `COBSWAIT.cbl` translation → ledger entry must NOT contain `no_result_json_found`.

### ISSUE-05 — `INFERENCE_API_KEY` Consuming Next CLI Flag
- **Category:** `AUTH-KEY`
- **Risk:** 🟠 High
- **Symptom:** Intermittent HTTP 401 in `postmortem.md`.
- **Verify:** `grep INFERENCE_API_KEY docker-compose.yml` → value must be empty string `INFERENCE_API_KEY=`.
- **Fix if broken:** Set `- INFERENCE_API_KEY=` (no value) in `docker-compose.yml`.
- **Gate:** Rebuild container; `curl -s http://localhost:8000/v1/translate` with `COBSWAIT.cbl` → no 401 in postmortem.

---

## Gated Validation Protocol: `COBOL-TRANSLATE-ATOMIC-V1`

Execute this loop for EVERY fix. Do not skip gates. A gate failure terminates the current fix attempt and restarts the loop from diagnosis.

```
FOR EACH issue in [ISSUE-01, ISSUE-02, ISSUE-03, ISSUE-04, ISSUE-05]:

  STEP 1 — DIAGNOSE
    Read postmortem.md from most recent session
    Classify failure using taxonomy (see scratchpad)
    State: "Root cause is [category] because [evidence]"

  STEP 2 — PROPOSE
    Identify the ONE file and ONE function to change
    Write the minimal diff — no unrelated changes
    State: "I will change [file]:[function] by [description]"

  GATE-0: SYNTAX CHECK
    Run: py_compile.compile(target_file, doraise=True)
    FAIL → abort fix, log error, return to STEP 1

  STEP 3 — APPLY
    Write the fix to disk
    If modifying Python: run GATE-0 again on written file

  GATE-1: CONTAINER BUILD
    Run: docker compose build
    FAIL → read build log, identify new failure category, return to STEP 1

  GATE-2: SERVER BOOT
    Run: docker compose up -d
    Run: curl -s http://localhost:8000/docs | grep -c openapi
    FAIL → docker compose logs harness | tail -50 → return to STEP 1

  GATE-3: INFERENCE REACHABLE
    Run from HOST: curl -s http://localhost:13305/v1/models
    Run from CONTAINER: docker exec harness curl -s http://host.docker.internal:13305/v1/models
    FAIL → check lemond process, check port binding → ISSUE-01

  GATE-4: PIPELINE TRIGGER
    Run: curl -X POST http://localhost:8000/v1/translate \
         -H "Content-Type: application/json" \
         -d '{"target_path": "app/app/cbl/COBSWAIT.cbl"}'
    Assert: response contains "status":"started"
    Note: session_id from response

  GATE-5: SESSION ARTIFACT CHECK
    Run: docker exec harness cat /app/securatron/sessions/<session_id>/trials.jsonl
    Assert: file exists AND last entry does NOT contain "status":"failure"
    FAIL → read postmortem.md → classify → return to STEP 1

  GATE-6: GATE COMPARE
    Assert: last trials.jsonl entry contains "gate_rc": 0
    FAIL → read synthesis output in /app/securatron/sessions/<session_id>/
            check LLM response quality → classify as LLM-500, PARSER-MISS, or CONCURRENT

  GATE-7: TRANSLATION OUTPUT
    Run: docker exec harness cat /app/translations/gold-candidate/COBSWAIT.md | wc -w
    Assert: word count > 100
    FAIL → check pass3run.py output writer → ensure .md is being written

  PASS → git add -p, git commit -m "fix(<category>): <description>", git push
         Log: "ISSUE-0X RESOLVED at $(date -u)"
         Advance to next ISSUE
```

---

## Failure Taxonomy Quick Reference

| Code | Meaning | First Tool to Run |
|------|---------|-------------------|
| `INFRA-PATH` | Wrong file path in Dockerfile or atom | `docker exec harness ls <expected_path>` |
| `ARGPARSE-SIG` | CLI flag mismatch caller vs script | `python3 <script> --help` |
| `MODEL-ROUTE` | Wrong model name in inference call | `grep INFERENCE_MODEL docker-compose.yml` |
| `PORT-SHADOW` | Dual process on same port | `ps aux | grep lemond` |
| `AUTH-KEY` | API key format rejected | `grep INFERENCE_API_KEY docker-compose.yml` |
| `LLM-500` | Backend crash on malformed request | `grep 'system' scripts/pass3run.py` |
| `SOCKET-HANG` | urllib/requests silent deadlock | `grep 'import urllib' scripts/pass3run.py` |
| `PARSER-MISS` | `RESULT` line not captured | `grep 'raw_stdout' app/securatron/global/bin/parsers.py` |
| `SIL-PATCH` | String-replace corrupts Python file | `py_compile.compile(target)` |
| `CONCURRENT` | Parallel LLM requests saturate slot | `grep 'sleep' scripts/pass3run.py` |

---

## Commit Message Convention

```
fix(PORT-SHADOW): kill stale lemond, restart with --host 0.0.0.0
fix(SOCKET-HANG): replace urllib with requests in pass3run.py
fix(LLM-500): inject system prompt for json_object mode
fix(PARSER-MISS): expand raw_stdout search window to 5000 chars
fix(AUTH-KEY): set INFERENCE_API_KEY empty in docker-compose.yml
```

---

## Success Criteria

This task is **COMPLETE** when ALL of the following are true:

- [ ] `docker compose logs harness` shows no ERROR lines
- [ ] `curl POST /v1/translate` with `COBSWAIT.cbl` returns `status: started`
- [ ] `cobol.translate.trials.jsonl` shows `result: success` for COBSWAIT
- [ ] `translations/gold-candidate/COBSWAIT.md` exists and has > 100 words
- [ ] All 5 ISSUE fixes are committed with correct commit message convention
- [ ] `docs/AGENT_TASK_2026-05-06.md` `status:` field updated to `closed`

---

## Agent Self-Check Before Each Loop

Before writing any code, answer these three questions aloud in your reasoning:

1. **What is the exact error message?** (Quote from `postmortem.md` or `trials.jsonl`)
2. **What is the single file I am changing?** (Full path)
3. **Will this change break anything else?** (Check callers and imports)

If you cannot answer all three, read more artifacts before proceeding.

---

*Task created: 2026-05-06 | Created from: docs/GEMINI_SESSION_SCRATCHPAD_2026-05-05.md*
