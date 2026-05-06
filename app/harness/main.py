import asyncio
import json
import pathlib
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from atoms.cobol_llm_evaluate import execute as run_llm_evaluate

app = FastAPI(title="Tensar Sys COBOL Harness", version="1.0.0")

# ---------------------------------------------------------------------------
# State persistence
# ---------------------------------------------------------------------------
STATE_DIR = pathlib.Path("/app/securatron/sessions/.state")
STATE_DIR.mkdir(parents=True, exist_ok=True)

SESSION_DIR = pathlib.Path("/app/securatron/sessions")

gate_events: Dict[str, asyncio.Event] = {}
session_store: Dict[str, Dict[str, Any]] = {}


def _state_path(session_id: str) -> pathlib.Path:
    return STATE_DIR / f"{session_id}.json"


def _persist(session_id: str) -> None:
    _state_path(session_id).write_text(
        json.dumps(session_store[session_id], indent=2)
    )


def _load(session_id: str) -> Optional[Dict[str, Any]]:
    p = _state_path(session_id)
    if p.exists():
        return json.loads(p.read_text())
    return None


def _log_trial(session_id: str, atom: str, status: str, metrics: Dict[str, Any]) -> None:
    session_trials = SESSION_DIR / session_id / "trials.jsonl"
    session_trials.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts":           datetime.now(timezone.utc).isoformat(),
        "session":      session_id,
        "phase":        session_store.get(session_id, {}).get("ooda_phase", "unknown"),
        "atom":         atom,
        "atom_version": session_store.get(session_id, {}).get("atom_version", "1.0.0"),
        "status":       status,
        "metrics":      metrics,
    }
    with session_trials.open("a") as f:
        f.write(json.dumps(entry) + "\n")


# ---------------------------------------------------------------------------
# Hermes pipeline — gate-halting async coroutine
# ---------------------------------------------------------------------------
async def hermes_dispatch_loop(session_id: str, target: str) -> None:
    s = session_store[session_id]

    # --- Atom 1: cobol.static_analysis ---
    s.update({"ooda_phase": "observe", "current_atom": "cobol.static_analysis", "gate_status": "active"})
    _persist(session_id)
    # TODO: wire to real smojol-cli subprocess
    await asyncio.sleep(0)
    _log_trial(session_id, "cobol.static_analysis", "success", {"note": "stub"})

    # --- Atom 2: cobol.annotate ---
    s.update({"ooda_phase": "orient", "current_atom": "cobol.annotate"})
    _persist(session_id)
    # TODO: wire to real pass1_annotate.py subprocess
    await asyncio.sleep(0)
    _log_trial(session_id, "cobol.annotate", "success", {"note": "stub"})

    # --- Atom 3: cobol.llm_evaluate (REAL — wired to cobol_llm_evaluate.py) ---
    s.update({"ooda_phase": "decide", "current_atom": "cobol.llm_evaluate"})
    _persist(session_id)

    atom_version = s.get("atom_version", "1.0.0")
    llm_success = await run_llm_evaluate(
        session_id=session_id,
        target_file=target,
        atom_version=atom_version,
    )

    if not llm_success:
        # Atom 3 exhausted retries — halt and wait for operator decision
        s.update({
            "gate_status":    "REQUIRES_PROMOTER_REVIEW",
            "halting_reason": "cobol.llm_evaluate failed after max retries — see post-mortem",
        })
        _persist(session_id)
        await gate_events[session_id].wait()
        gate_events[session_id].clear()

        if s["gate_status"] == "aborted":
            _log_trial(session_id, "cobol.llm_evaluate", "aborted", {"reason": "operator_abort"})
            return
        # RETRY decision: reset retry_count and let self_improve.py run externally
        s["retry_count"] = 0
        s["gate_status"] = "active"
        _persist(session_id)

    # --- Atom 4: cobol.synthesize_and_verify → operator review gate ---
    s.update({"current_atom": "cobol.synthesize_and_verify", "gate_status": "REQUIRES_PROMOTER_REVIEW"})
    _persist(session_id)

    await gate_events[session_id].wait()
    gate_events[session_id].clear()

    if s["gate_status"] == "aborted":
        _log_trial(session_id, "cobol.synthesize_and_verify", "aborted", {"reason": "operator_abort"})
        return

    # Gate cleared — TODO: wire to real pass3_synthesize.py + gate_compare.py
    s.update({"ooda_phase": "act", "gate_status": "active"})
    _persist(session_id)
    await asyncio.sleep(0)
    _log_trial(session_id, "cobol.synthesize_and_verify", "success", {"note": "stub"})

    s.update({"ooda_phase": "complete", "gate_status": "done"})
    _persist(session_id)


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class DispatchRequest(BaseModel):
    target_path: str
    molecule: Optional[str] = "cobol.pipeline.full"


class AuthorizeRequest(BaseModel):
    decision: str  # PROCEED | ABORT | RETRY
    feedback: Optional[str] = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.post("/v1/dispatch", status_code=202)
async def dispatch_harness(req: DispatchRequest, background_tasks: BackgroundTasks):
    session_id = f"sess_{uuid.uuid4().hex[:12]}"
    session_store[session_id] = {
        "session_id":   session_id,
        "ooda_phase":   "init",
        "current_atom": "startup",
        "gate_status":  "active",
        "retry_count":  0,
        "anchor_loaded": False,
        "atom_version": "1.0.0",
        "target":       req.target_path,
        "molecule":     req.molecule,
        "dispatched_at": datetime.now(timezone.utc).isoformat(),
    }
    _persist(session_id)
    gate_events[session_id] = asyncio.Event()
    asyncio.create_task(hermes_dispatch_loop(session_id, req.target_path))
    return {"status": "dispatched", "session_id": session_id}


@app.get("/v1/session/{session_id}/state")
async def get_session_state(session_id: str):
    state = session_store.get(session_id) or _load(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")
    return state


@app.post("/v1/session/{session_id}/authorize")
async def authorize_gate(session_id: str, req: AuthorizeRequest):
    state = session_store.get(session_id) or _load(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")
    if state["gate_status"] != "REQUIRES_PROMOTER_REVIEW":
        raise HTTPException(
            status_code=400,
            detail=f"Session not halted at a gate. Current status: {state['gate_status']}",
        )
    decision = req.decision.upper()
    if decision == "PROCEED":
        state["gate_status"] = "active"
        state["ooda_phase"]  = "act"
    elif decision in ("ABORT", "RETRY"):
        state["gate_status"] = "aborted" if decision == "ABORT" else "retry"
    else:
        raise HTTPException(status_code=422, detail=f"Unknown decision: {req.decision}")
    session_store[session_id] = state
    _persist(session_id)
    if session_id in gate_events:
        gate_events[session_id].set()
    return {
        "status":     decision.lower(),
        "session_id": session_id,
        "message":    f"Gate {'cleared — Hermes resuming.' if decision == 'PROCEED' else 'halted by operator.'}",
    }


@app.get("/v1/session/{session_id}/stream")
async def stream_session_events(session_id: str):
    async def event_generator():
        last = None
        for _ in range(120):
            state = session_store.get(session_id) or _load(session_id)
            if state and state != last:
                yield f"data: {json.dumps(state)}\n\n"
                last = state
            await asyncio.sleep(1)
    return StreamingResponse(event_generator(), media_type="text/event-stream")
