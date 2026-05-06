import asyncio
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from atoms.cobol_llm_evaluate import execute as run_llm_evaluate
from state import load_state, save_state

app = FastAPI(title="Tensar Sys COBOL Harness", version="0.1.0")


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
    # asyncio.create_task — NOT BackgroundTasks.
    # BackgroundTasks is fire-and-forget with no await point; create_task
    # runs in the event loop and can be monitored, cancelled, or extended
    # with gate events later without changing the call site.
    asyncio.create_task(_run_pipeline(session_id, req.target_path))
    return {"session_id": session_id, "status": "started"}


async def _run_pipeline(session_id: str, target: str) -> None:
    state = load_state(session_id)
    state["status"] = "llm_evaluate"
    save_state(session_id, state)

    success = await run_llm_evaluate(session_id, target)

    state = load_state(session_id)
    state["status"] = "success" if success else "failed"
    save_state(session_id, state)


@app.get("/v1/session/{session_id}")
async def get_session(session_id: str):
    """Poll session state. Returns current status and any logged metrics."""
    state = load_state(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")
    return state
