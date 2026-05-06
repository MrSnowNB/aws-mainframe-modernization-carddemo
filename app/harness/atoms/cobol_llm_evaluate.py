import asyncio
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

# ── Path constants (must match Docker volume layout from blueprint) ──────────
# Blueprint spec: /app/securatron/global/tools/cobol.*
# NOT /app/tools — that path is not mounted per the architecture.
SESSIONS_ROOT    = Path("/app/securatron/sessions")
TOOLS_ROOT       = Path("/app/securatron/global/tools")
POST_MORTEM_ROOT = Path("/app/securatron/global/post-mortems")

MAX_RETRIES        = 3
CONTEXT_THRESHOLD  = 0.80  # fraction of model context window → proactive anchor


def _session_dir(session_id: str) -> Path:
    p = SESSIONS_ROOT / session_id
    p.mkdir(parents=True, exist_ok=True)
    return p


def _log_trial(session_id: str, entry: Dict[str, Any]) -> None:
    """Append one NDJSON entry to this session's trials.jsonl.
    File is opened in append mode on each call — safe under concurrent sessions
    because each session writes to its own directory.
    """
    log_path = _session_dir(session_id) / "trials.jsonl"
    with log_path.open("a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


async def _run_command(cmd: list[str]) -> tuple[int, str, str]:
    """Launch a subprocess, capture stdout/stderr, enforce 5-minute hard timeout."""
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=300)
        return proc.returncode, stdout.decode().strip(), stderr.decode().strip()
    except asyncio.TimeoutError:
        return -1, "", "Command timed out after 5 minutes"


def _estimate_tokens(target_file: str) -> int:
    """Cheap byte-level token estimator (4 bytes ≈ 1 token for COBOL source).
    Swap for tiktoken if sub-500 token precision is needed.
    Returns 0 on any filesystem error so the caller can decide how to proceed.
    """
    try:
        return os.path.getsize(target_file) // 4 + 500
    except OSError:
        return 0


async def execute(
    session_id: str,
    target_file: str,
    atom_version: str = "1.0.0",
    model_context_window: int = 32_000,  # override per model; drives anchor threshold
) -> bool:
    """
    Execute Stage 2 of the COBOL verification pipeline.

    Returns True on success (LLM + gate both exit 0).
    Returns False after MAX_RETRIES failures; writes a post-mortem markdown.
    Raises ValueError immediately on invalid input — don't burn retries on bad targets.
    """
    session_dir = _session_dir(session_id)
    target_path = Path(target_file).resolve()

    # ── Input validation (red-team gate) ────────────────────────────────────
    if not target_path.is_file():
        raise ValueError(f"Target does not exist or is not a file: {target_file}")
    if target_path.suffix not in (".cbl", ".cpy"):
        raise ValueError(f"Target must be .cbl or .cpy, got: {target_path.suffix}")

    attempt   = 0
    last_error = ""

    while attempt < MAX_RETRIES:
        attempt += 1
        # asyncio.get_running_loop() is the correct call inside an async context.
        # get_event_loop() is deprecated in Python 3.12 and raises DeprecationWarning.
        loop  = asyncio.get_running_loop()
        start = loop.time()

        # ── Proactive anchor: write before the LLM call, not after overflow ──
        est_tokens      = _estimate_tokens(str(target_path))
        anchor_threshold = int(model_context_window * CONTEXT_THRESHOLD)
        if est_tokens > 0 and est_tokens > anchor_threshold:
            anchor_path = session_dir / "anchor.md"
            anchor_path.write_text(
                f"# ANCHOR TRIGGERED\n"
                f"session: {session_id}\n"
                f"target: {target_path}\n"
                f"estimated_tokens: {est_tokens}\n"
                f"threshold: {anchor_threshold} ({int(CONTEXT_THRESHOLD*100)}% of {model_context_window})\n"
                f"atom_version: {atom_version}\n"
                f"attempt: {attempt}\n"
            )

        # ── Real pipeline calls ──────────────────────────────────────────────
        llm_cmd = [
            "python3", str(TOOLS_ROOT / "pass2_llm.py"),
            "--target",       str(target_path),
            "--session",      session_id,
            "--atom-version", atom_version,
        ]
        gate_cmd = [
            "python3", str(TOOLS_ROOT / "gate_compare.py"),
            "--target",  str(target_path),
            "--session", session_id,
        ]

        llm_code,  llm_out,  llm_err  = await _run_command(llm_cmd)
        gate_code, gate_out, gate_err = await _run_command(gate_cmd)

        success  = (llm_code == 0 and gate_code == 0)
        duration = round(loop.time() - start, 3)

        _log_trial(session_id, {
            "ts":           datetime.now(timezone.utc).isoformat(),
            "session":      session_id,
            "phase":        "decide",
            "atom":         "cobol.llm_evaluate",
            "atom_version": atom_version,
            "attempt":      attempt,
            "status":       "success" if success else "failure",
            "metrics": {
                "duration_sec": duration,
                "llm_exit":     llm_code,
                "gate_exit":    gate_code,
                "est_tokens":   est_tokens,
            },
        })

        if success:
            return True

        last_error = f"LLM exit={llm_code} stderr={llm_err!r}\nGate exit={gate_code} stderr={gate_err!r}"

        if attempt < MAX_RETRIES:
            await asyncio.sleep(2 ** attempt)  # 2s, 4s, 8s

    # ── Terminal failure: write post-mortem ──────────────────────────────────
    pm_dir  = POST_MORTEM_ROOT
    pm_dir.mkdir(parents=True, exist_ok=True)
    pm_path = pm_dir / f"{session_id}_llm_evaluate.md"
    pm_path.write_text(
        f"# POST-MORTEM: cobol.llm_evaluate\n"
        f"**Session:** {session_id}\n"
        f"**Target:** {target_file}\n"
        f"**Atom Version:** {atom_version}\n"
        f"**Retries exhausted:** {MAX_RETRIES}\n\n"
        f"## Final Error\n"
        f"```\n{last_error}\n```\n\n"
        f"## Self-Improvement Directive\n"
        f"Analyze trials.jsonl for this session.\n"
        f"If failure_type matches a known pattern (FM-3 hallucinated paragraph,\n"
        f"FM-7 context overflow, FM-9 VSAM path mismatch), patch pass2_llm.py\n"
        f"prompt templates and increment atom_version.\n"
    )

    return False
