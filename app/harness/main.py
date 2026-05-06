import asyncio
import json
import os
import uuid
from pathlib import Path

import aiohttp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from atoms.cobol_llm_evaluate import prepare, verify
from state import load_state, save_state

app = FastAPI(title="Tensar Sys COBOL Harness", version="0.2.0")

# ── Inference config (all overrideable via env vars — no model logic in atoms) ──
INFERENCE_ENDPOINT = os.getenv("INFERENCE_ENDPOINT", "http://localhost:8001/v1/chat/completions")
INFERENCE_MODEL    = os.getenv("INFERENCE_MODEL",    "local-model")
INFERENCE_TIMEOUT  = int(os.getenv("INFERENCE_TIMEOUT_SEC", "120"))


class DispatchRequest(BaseModel):
    target_path: str


@app.post("/v1/translate", status_code=202)
async def translate(req: DispatchRequest):
    """Kick off the COBOL verification pipeline for a single target file."""
    session_id = f"sess_{uuid.uuid4().hex[:12]}"
    save_state(session_id, {
        "session_id": session_id,
        "target":     req.target_path,
        "status":     "running",
    })
    asyncio.create_task(_run_pipeline(session_id, req.target_path))
    return {"session_id": session_id, "status": "started"}


@app.get("/v1/session/{session_id}")
async def get_session(session_id: str):
    """Poll session state."""
    state = load_state(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")
    return state


async def _run_pipeline(session_id: str, target: str) -> None:
    """Hermes dispatch loop. Owns the inference gap between prepare and verify."""
    program_id = Path(target).stem

    # ── Phase 1: Prepare ──────────────────────────────────────────────────────
    _set_status(session_id, "preparing")
    requests_path = await prepare(session_id, target)
    if requests_path is None:
        _set_status(session_id, "failed", {"phase": "prepare"})
        return

    # ── Phase 2: Inference (Hermes owns this) ─────────────────────────────────
    _set_status(session_id, "awaiting_inference")
    responses_path = await _call_inference(session_id, requests_path)
    if responses_path is None:
        _set_status(session_id, "failed", {"phase": "inference"})
        return

    # ── Phase 3: Synthesize (pass3) ───────────────────────────────────────────
    _set_status(session_id, "synthesizing")
    synth_ok = await _run_synthesize(session_id, program_id, responses_path)
    if not synth_ok:
        _set_status(session_id, "failed", {"phase": "synthesize"})
        return

    # ── Phase 4: Verify (gate) ────────────────────────────────────────────────
    _set_status(session_id, "verifying")
    gate_ok = await verify(session_id, program_id)
    _set_status(session_id, "success" if gate_ok else "failed",
                {"gate": "PASS" if gate_ok else "FAIL"})


async def _call_inference(
    session_id: str, requests_path: Path
) -> Path | None:
    """
    Reads _llm_requests.jsonl line by line, POSTs each payload to the
    configured inference endpoint, writes responses to _llm_responses.jsonl.
    Model and endpoint come from env vars — atoms never touch this.
    """
    session_dir = requests_path.parent
    responses_path = session_dir / requests_path.name.replace(
        "_llm_requests.jsonl", "_llm_responses.jsonl"
    )

    requests = []
    with requests_path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                requests.append(json.loads(line))

    if not requests:
        # No LLM work needed (all statements were template-handled)
        responses_path.write_text("")
        return responses_path

    responses = []
    timeout = aiohttp.ClientTimeout(total=INFERENCE_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as http:
        for payload in requests:
            # Strip internal routing keys before sending to inference endpoint
            wire_payload = {k: v for k, v in payload.items() if k != "_routing"}
            wire_payload["model"] = INFERENCE_MODEL
            try:
                async with http.post(
                    INFERENCE_ENDPOINT, json=wire_payload
                ) as resp:
                    body = await resp.json()
                    responses.append({
                        "_routing": payload.get("_routing", {}),
                        "response": body,
                    })
            except Exception as exc:
                # One failed request fails the whole inference phase
                session_dir = requests_path.parent
                (session_dir / "post_mortem.md").write_text(
                    f"INFERENCE FAILED\nEndpoint: {INFERENCE_ENDPOINT}\nError: {exc}\n"
                )
                return None

    with responses_path.open("w") as f:
        for r in responses:
            f.write(json.dumps(r) + "\n")

    return responses_path


async def _run_synthesize(
    session_id: str, program_id: str, responses_path: Path
) -> bool:
    """Calls pass3_synthesize.py with the merged responses."""
    import asyncio
    from atoms.cobol_llm_evaluate import _run  # reuse the same subprocess helper

    session_dir = Path(f"/app/securatron/sessions/{session_id}")
    out_path = Path(f"/app/translations/gold-candidate/{program_id}.md")

    rc, _, err = await _run([
        "python3", "/app/scripts/pass3_synthesize.py",
        "--requests",  str(session_dir / f"{program_id}_llm_requests.jsonl"),
        "--responses", str(responses_path),
        "--program-id", program_id,
        "--out", str(out_path),
    ], cwd="/app")

    if rc != 0:
        (session_dir / "post_mortem.md").write_text(
            f"SYNTHESIZE FAILED\nError: {err}\n"
        )
    return rc == 0


def _set_status(session_id: str, status: str, extra: dict = None) -> None:
    state = load_state(session_id)
    state["status"] = status
    if extra:
        state.update(extra)
    save_state(session_id, state)
