import asyncio
import os
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from atoms.cobol_llm_evaluate import _run, prepare, verify
from state import load_state, save_state

app = FastAPI(title="Tensar Sys COBOL Harness", version="0.3.0")

# Inference config — all via env vars, no model logic in atoms or harness code
INFERENCE_ENDPOINT = os.getenv("INFERENCE_ENDPOINT", "http://localhost:1234/v1")
INFERENCE_MODEL    = os.getenv("INFERENCE_MODEL", "local-model")
INFERENCE_API_KEY  = os.getenv("INFERENCE_API_KEY", "local")


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
    """
    Hermes dispatch loop.

    Phase 1 (prepare)   — deterministic: pass1 + pass2 + pass3_synthesize
    Phase 2 (synthesize)— inference: pass3_run.py owns LLM calls via urllib
    Phase 3 (verify)    — deterministic: gate_compare

    Inference endpoint + model come from env vars only.
    Atoms never see model names or endpoints.
    """
    program_id = Path(target).stem

    # ─ Phase 1: Prepare ──────────────────────────────────────────────────
    _set_status(session_id, "preparing")
    props_path = await prepare(session_id, target)
    if props_path is None:
        _set_status(session_id, "failed", {"phase": "prepare"})
        return

    # ─ Phase 2: Synthesize (pass3_run owns inference) ─────────────────────
    _set_status(session_id, "synthesizing")
    rc, stdout, err = await _run([
        "python3", "/app/scripts/pass3_run.py",
        "--program-id", program_id,
        "--base-url",   INFERENCE_ENDPOINT,
        "--model",      INFERENCE_MODEL,
        "--api-key",    INFERENCE_API_KEY,
    ], cwd="/app")

    if rc != 0:
        session_dir = Path(f"/app/securatron/sessions/{session_id}")
        (session_dir / "post_mortem.md").write_text(
            f"SYNTHESIZE FAILED\npass3_run exit {rc}\n{err}\n"
        )
        _set_status(session_id, "failed", {"phase": "synthesize"})
        return

    # ─ Phase 3: Verify (gate) ─────────────────────────────────────────────
    _set_status(session_id, "verifying")
    gate_ok = await verify(session_id, program_id)
    _set_status(session_id, "success" if gate_ok else "failed",
                {"gate": "PASS" if gate_ok else "FAIL"})


def _set_status(session_id: str, status: str, extra: dict = None) -> None:
    state = load_state(session_id)
    state["status"] = status
    if extra:
        state.update(extra)
    save_state(session_id, state)
