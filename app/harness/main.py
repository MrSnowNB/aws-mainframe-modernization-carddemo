import asyncio
import os
import uuid
import json
from datetime import datetime, timezone
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
    Emits a ticket to the SecuraTron inbox instead of running directly.
    The inbox_watcher will pick this up and execute sequentially.
    """
    program_id = Path(target).stem
    _set_status(session_id, "ticketed")

    inbox_new = Path("/app/securatron/inbox/new")
    inbox_new.mkdir(parents=True, exist_ok=True)

    ticket_id = f"TICK-{uuid.uuid4().hex[:8].upper()}"
    ticket = {
        "ticket_id":  ticket_id,
        "source":     "agent",
        "skill":      "cobol.translate",
        "priority":   "normal",
        "created_at": datetime.now(timezone.utc).isoformat() + "Z",
        "status":     "pending",
        "target":     target,
        "session_id": session_id,
        "inputs": {
            "target_path": target
        }
    }

    ticket_path = inbox_new / f"{ticket_id}.json"
    with open(ticket_path, "w") as f:
        json.dump(ticket, f, indent=2)
    
    # We'll also symlink/copy the ticket to the session directory for tracking
    session_dir = Path(f"/app/securatron/sessions/{session_id}")
    session_dir.mkdir(parents=True, exist_ok=True)
    with open(session_dir / "ticket.json", "w") as f:
        json.dump(ticket, f, indent=2)

    print(f"[HARNESS] Emitted ticket {ticket_id} for session {session_id}")


def _set_status(session_id: str, status: str, extra: dict = None) -> None:
    state = load_state(session_id)
    state["status"] = status
    if extra:
        state.update(extra)
    save_state(session_id, state)
