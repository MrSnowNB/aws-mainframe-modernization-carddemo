# GeminiCLI Session Scratchpad — 2026-05-05
> **Purpose:** Parse the full GeminiCLI session. Document wins, failures, lessons learned, and define a gated atomic validation protocol for a local agent to use first-principles problem-solving loops.

---

## 🗺️ Session Overview

**Goal:** Bring the SecuraTron COBOL-to-AI harness to first-boot status — Docker container running, 3-pass LLM pipeline firing, gate validation returning a result, and the self-improvement loop (SIL) hardened enough to self-correct.

**COBOL Files Targeted:** `CBTRN01C.cbl`, `CBTRN02C.cbl`, `CBACT04C.cbl`, `COBSWAIT.cbl`

**Agent:** GeminiCLI (Gemini 2.5 Pro) operating autonomously in the `COBOLtoAI/aws-mainframe-modernization-carddemo` workspace.

**Inference Backend:** Lemonade server → `llama-server` serving `Qwen3.6-35B-A3B-GGUF` on port `13305`.

---

## ✅ What Went Well

| # | Win | Evidence |
|---|-----|----------|
| 1 | **Repo clone + first commit landed cleanly** | Agent cloned repo, authored `docker-compose.yml`, fixed `Dockerfile` COPY paths, fixed `TOOLSROOT` in `cobolllmevaluate.py`, and pushed in a single coherent commit. |
| 2 | **Docker image built successfully** | `docker compose build` completed all 13 steps; image `aws-mainframe-modernization-carddemo-harness` created without errors. |
| 3 | **FastAPI harness booted** | `uvicorn` came up cleanly on `0.0.0.0:8000`; `curl POST /v1/translate` returned `{sessionid, status:started}` — proving the REST entry point is live. |
| 4 | **Session artifact structure confirmed** | `trials.jsonl` and `postmortem.md` were written per-session; the ledger at `/app/securatron/global/ledger/cobol.translate.trials.jsonl` accumulated entries. |
| 5 | **pass3run.py retry logic added** | Replaced bare `urllib` with `requests`; added 3-attempt exponential backoff for HTTP 401/500/502/503/504 and JSON parse failures. |
| 6 | **Model override bug fixed** | `pass3run.py` was defaulting to `gpt-4o-2024-08-06` from payload instead of respecting `INFERENCE_MODEL` env var; one-line fix corrected this. |
| 7 | **System prompt injection for JSON mode** | Added automatic system prompt `"Always respond in valid JSON format"` when `response_format: json_object` is used and no system message is present — prevents backend 500 crash. |
| 8 | **Inference reachable from inside container** | `curl` to `host.docker.internal:13305/v1/chat/completions` from within the container returned HTTP 200 with valid content — network path confirmed. |
| 9 | **SIL Red Team analysis completed** | Agent correctly identified all 5 critical weaknesses in `infra.patch.worker.py` (naive string replace, no verify step, no syntax check, weak duplicate check, no `__main__` guard). |
| 10 | **Hardened `infrapatchworker.py` designed** | `validatepython()` using `py_compile`, `backupandpatch()` with rollback, dry-run `--apply` flag all designed and code-ready. |

---

## ❌ What Went Wrong (Failure Catalog)

### F-01 — Dockerfile COPY Path Error
- **Symptom:** Container could not find `app/harness`, `scripts`, or `validation` at runtime.
- **Root Cause:** Original `Dockerfile` used `COPY . /app/harness` which pulled everything including the wrong root-level paths. Correct paths are relative (`app/harness`, `scripts`, `validation`).
- **Fix:** Replaced single `COPY . /app/harness` with three targeted `COPY` statements.

### F-02 — `TOOLSROOT` Pointed to Non-Existent Path
- **Symptom:** `pass2llm.py` not found at runtime.
- **Root Cause:** `cobolllmevaluate.py` had `TOOLSROOT = Path("/app/securatron/globaltools")` — a path that doesn't exist in the container.
- **Fix:** Changed to `TOOLSROOT = Path("/app/scripts")`.

### F-03 — `pass2llm.py` argparse Error (Wrong CLI Signature)
- **Symptom:** `postmortem.md` showed `pass2llm.py: error: the following arguments are required: --propositions, --program-id, --out`
- **Root Cause:** The atom was calling `pass2llm.py --target <file> --session <id>` but the script requires a multi-pass pipeline where Pass 1 (`pass1annotate.py`) and Pass 2 template (`pass2template.py`) must run first to produce the `--propositions` input file.
- **Fix:** Rewrote `cobolllmevaluate.py` atom to execute the full 3-pass sequential pipeline with named intermediate artifacts.

### F-04 — Docker Not Installed in GeminiCLI Sandbox
- **Symptom:** `docker: command not found` inside the Gemini workspace.
- **Root Cause:** GeminiCLI executes in a sandboxed environment without Docker. All container operations had to be handed off to the user's host terminal.
- **Impact:** Broke the agent's ability to self-test. All build/run cycles required human relay.
- **Mitigation:** Agent provided complete host-side command sequences for the user to run separately.

### F-05 — Dual Lemonade Process / Port Shadow on 13305
- **Symptom:** Harness logs showed no inference activity; `trials.jsonl` recorded failures despite the container being "active."
- **Root Cause:** Two `lemond` processes were running simultaneously — one bound to `0.0.0.0:13305` (correct) and one to `127.0.0.1:13305` (shadow/stale). The Docker container's `host.docker.internal:13305` was hitting the stale shadow process not connected to the active `llama-server`.
- **Fix Required:** Kill all `lemond` processes, restart with `--host 0.0.0.0` only.

### F-06 — HTTP 401 "Invalid or Missing API Key" Intermittent
- **Symptom:** Multiple `FAIL LLM HTTP 401` entries in `postmortem.md`.
- **Root Cause:** `INFERENCE_API_KEY=local` was being set, and the argparse in the harness had a bug where an empty API key value consumed the next positional flag. Lemonade doesn't require an API key but was receiving a malformed `Authorization: Bearer local` header that may have triggered rejection under load.
- **Fix:** Set `INFERENCE_API_KEY=` (empty) in `docker-compose.yml`; Lemonade tested to work without auth.

### F-07 — HTTP 500 from `llama-server` Under Pass-3 Load
- **Symptom:** All paragraphs returned `FAIL LLM HTTP 500`.
- **Root Cause:** `pass3run.py` was using `response_format: {type: json_object}` without a system prompt. Local `llama-server` requires a system-level instruction to reliably produce JSON output; without it, the backend aborted with 500.
- **Fix:** Auto-inject system prompt `"You are a COBOL modernization expert. Always respond in valid JSON format."` when no system message exists.

### F-08 — `urllib` Silent Hang / Worker Deadlock
- **Symptom:** `ps aux` showed `pass3run.py` running with 0% CPU; fans silent; no output in `.raw` files; session never completed.
- **Root Cause:** `urllib.request.urlopen` silently hung on a stale or RST socket. The timeout parameter does not protect against all socket-level hangs in Python's `urllib`.
- **Fix:** Replaced `urllib` entirely with `requests` library, which has more robust connection handling and a configurable `timeout=600`.

### F-09 — `no_result_json_found` in Parser
- **Symptom:** Global ledger showed `reason: no_result_json_found` even after worker appeared to run.
- **Root Cause (A):** `dispatch.py` writes the `.raw` artifact only *after* the subprocess finishes. If the subprocess hangs, no `.raw` is written.
- **Root Cause (B):** `parsers.py` was only scanning the first 500 characters of raw stdout for the `RESULT` line; if the worker emitted verbose logs before the result, the parser missed it.
- **Fix A:** `cobolpipelineworker.py` refactored to always `print("RESULT " + json.dumps(...))` even on failure paths (inside `except` block).
- **Fix B:** Parser regex search expanded to 5000 characters.

### F-10 — `infra.patch.worker.py` Naive String Replace (Critical Unresolved)
- **Symptom (Potential):** Self-improvement loop would silently corrupt Python files if the target string had minor whitespace or naming drift.
- **Root Cause:** `patchpreprocessingargs()` and `patchllmstability()` use raw `str.replace()` with no validation, no backup, no rollback, and no `py_compile` check after writing.
- **Status:** Hardened version designed (with `validatepython()`, `backupandpatch()`, `--apply` dry-run flag) but **not yet pushed to repo as of session end**.

---

## 🧠 What We Learned

1. **GeminiCLI cannot run Docker** — any agent operating in a sandboxed CLI must hand off all container lifecycle commands to the user or a host-side runner process.
2. **Lemonade is sensitive to concurrent requests** — single-slot `llama-server` with large COBOL prompts (~37,940 tokens) needs serialized requests and retry backoff, not parallel fire.
3. **`urllib` is not safe for long-running local inference** — always use `requests` with explicit `timeout` for local model calls.
4. **`response_format: json_object` requires a system prompt on local models** — OpenAI enforces this; local llama.cpp derivatives enforce it harder and 500 without it.
5. **Postmortem artifacts are the agent's only observability** — `trials.jsonl` + `postmortem.md` are the ground truth; the agent must be able to read and act on these in its loop.
6. **Port shadowing is a silent killer** — two processes on the same port with different bind addresses will fool any container without explicit healthcheck-before-fire logic.
7. **The SIL patching strategy (naive `str.replace`) is the highest-risk component** — it will corrupt atomically if not hardened with compile-verify-rollback before it runs in production.
8. **Argparse empty-value consumption is a real bug pattern** — `--api-key ""` causes argparse to consume the next flag as the key value; always guard with `or None` and conditionally include the flag.

---

## 🔬 Gated Validation Testing Protocol

> **Design Principle:** Every fix is an atomic unit. Each gate must PASS before the next step executes. The agent resets to last-known-good on any gate failure and logs a structured failure ticket before retrying.

### Protocol: `COBOL-TRANSLATE-ATOMIC-V1`

```
LOOP:
  READ next_problem from postmortem.md or trials.jsonl
  IDENTIFY root_cause category (see taxonomy below)
  PROPOSE minimal_fix (one file, one function, one change)
  GATE-0: syntax_check → py_compile minimal_fix → FAIL = abort, log, retry
  APPLY minimal_fix to repo
  GATE-1: container_build → docker compose build → FAIL = rollback, log ticket
  GATE-2: server_boot → curl GET /health or /docs → FAIL = check logs, log ticket
  GATE-3: pipeline_trigger → curl POST /v1/translate (COBSWAIT.cbl) → FAIL = read postmortem, next loop
  GATE-4: session_artifact → assert trials.jsonl exists AND status != "failure" → FAIL = read postmortem
  GATE-5: gate_compare → assert gaterc == 0 in trials.jsonl → FAIL = read synthesis output
  GATE-6: translation_output → assert translations/gold-candidate/PROGRAMID.md exists + non-empty
  PASS → commit, push, log success ticket, advance to next COBOL file
```

### Failure Taxonomy (Root Cause Categories)

| Code | Category | Canonical Fix Pattern |
|------|----------|-----------------------|
| `INFRA-PATH` | Wrong file path in Dockerfile or atom | Update COPY/TOOLSROOT constant, rebuild |
| `ARGPARSE-SIG` | CLI flag mismatch between caller and script | Read argparse definition of target script, align caller |
| `MODEL-ROUTE` | Wrong model name reaching inference | Check `INFERENCE_MODEL` env var propagation through dispatch chain |
| `PORT-SHADOW` | Dual process on same port | `pkill lemond`, restart with `--host 0.0.0.0` only |
| `AUTH-KEY` | API key format rejected by local server | Set `INFERENCE_API_KEY=` (empty), remove `Authorization` header |
| `LLM-500` | Backend crash on malformed request | Inject system prompt for JSON mode; verify payload schema |
| `SOCKET-HANG` | urllib/requests silent deadlock | Replace urllib with requests, set `timeout=600`, add retry |
| `PARSER-MISS` | Agent output not captured by parser | Expand parse window; ensure `RESULT <json>` is always emitted |
| `SIL-PATCH` | String-replace corrupts Python file | Use `backupandpatch()` with `py_compile` gate and rollback |
| `CONCURRENT` | Parallel LLM requests saturate single slot | Serialize paragraph processing; add inter-request `time.sleep(3)` |

---

## 🚧 Unresolved / Next Steps for Local Agent

### Priority 1 — Harden SIL Before Next Run
- [ ] Push hardened `infra.patch.worker.py` with `validatepython()`, `backupandpatch()`, `--apply` flag
- [ ] Update `self-improve.py` duplicate check to also scan `inbox/cur` and `inbox/archive`

### Priority 2 — Backend Stability
- [ ] Implement `healthcheck_before_fire()` in `dispatch.py` — ping `host.docker.internal:13305/v1/models` before submitting any paragraph job
- [ ] Add `LEMONADE_PIDS` sanity check on container start: if >1 `lemond` process detected, emit warning ticket

### Priority 3 — Full Pipeline Smoke Test
- [ ] Run `COBSWAIT.cbl` through complete pipeline with the above fixes; confirm `translations/gold-candidate/COBSWAIT.md` is produced
- [ ] Run `CBTRN01C.cbl` as second target; confirm ledger shows `result: success`

### Priority 4 — Gate Expansion
- [ ] Add `gatecompare.py` strict mode: check that all paragraph `semanticPattern` values are valid enum members (not `"unknown"`)
- [ ] Add word count + section count check to `translations/gold-candidate/PROGRAMID.md` as a minimum quality gate

---

## 🔑 Quick Reference: Key File Locations

| File | Purpose |
|------|---------|
| `app/harness/atoms/cobol_pipeline_worker.py` | Main worker; orchestrates pass1→pass2→pass3→gate |
| `app/harness/atoms/cobol_llm_evaluate.py` | Atom that runs the 3-pass pipeline subprocess chain |
| `app/harness/atoms/infra_patch_worker.py` | SIL self-patch worker — **highest risk, harden first** |
| `scripts/pass1_annotate.py` | Pass 1: COBOL annotation extraction |
| `scripts/pass2_template.py` | Pass 2: proposition template generation |
| `scripts/pass3run.py` | Pass 3: LLM synthesis per paragraph |
| `validation/gatecompare.py` | Gate: validates LLM output against propositions |
| `app/securatron/global/bin/parsers.py` | Parses worker stdout for `RESULT <json>` |
| `app/securatron/global/ledger/cobol.translate.trials.jsonl` | Global audit ledger |
| `docker-compose.yml` | Container config; sets `INFERENCE_*` env vars |

---

*Generated: 2026-05-06 | Session: 5_5_26_GeminiCLI_session.md | Repo: [MrSnowNB/aws-mainframe-modernization-carddemo](https://github.com/MrSnowNB/aws-mainframe-modernization-carddemo)*
