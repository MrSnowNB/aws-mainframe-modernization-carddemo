import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

SESSIONS_ROOT   = Path("/app/securatron/sessions")
SCRIPTS_ROOT    = Path("/app/scripts")
VALIDATION_ROOT = Path("/app/validation")
REPO_ROOT       = Path("/app")


async def _run(cmd: list[str], cwd: str = None) -> tuple[int, str, str]:
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=3600)
        return proc.returncode, stdout.decode().strip(), stderr.decode().strip()
    except asyncio.TimeoutError:
        proc.kill()
        return -1, "", "timeout after 3600s"


def _record(session_dir: Path, session_id: str, step: str,
            status: str, metrics: dict, err: str = "") -> None:
    trial = {
        "ts":      datetime.now(timezone.utc).isoformat(),
        "session": session_id,
        "atom":    "cobol.llm_evaluate",
        "step":    step,
        "status":  status,
        "metrics": metrics,
    }
    with (session_dir / "trials.jsonl").open("a") as f:
        f.write(json.dumps(trial) + "\n")
    if status == "failure" and err:
        (session_dir / "post_mortem.md").write_text(
            f"FAILED at {step}\nError: {err}\n"
        )


async def prepare(session_id: str, target_file: str) -> Optional[Path]:
    """
    Runs the deterministic preparation chain:
      pass1_annotate -> pass2_template -> pass2_llm -> pass3_synthesize

    Returns path to the session-dir propositions JSON on success (used by
    main.py to confirm prepare completed), None on any step failure.

    pass3_synthesize writes to validation/pass3/{program_id}_synthesis.jsonl
    which is the hardcoded input path pass3_run.py expects.
    """
    session_dir = SESSIONS_ROOT / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    target_path = Path(target_file).resolve()
    if not target_path.is_relative_to(REPO_ROOT) or target_path.suffix not in (".cbl", ".cpy"):
        raise ValueError("Path traversal or invalid file type blocked")

    program_id  = target_path.stem
    p1_out      = session_dir / f"{program_id}_annotations.json"
    p2_tmpl_out = session_dir / f"{program_id}_propositions.json"
    p2_llm_out  = session_dir / f"{program_id}_llm_requests.jsonl"
    synth_out   = VALIDATION_ROOT / "pass3" / f"{program_id}_synthesis.jsonl"
    cfg_path    = VALIDATION_ROOT / "structure" / f"{program_id}_cfg.json"

    synth_out.parent.mkdir(parents=True, exist_ok=True)

    steps = [
        ("pass1", [
            "python3", str(SCRIPTS_ROOT / "pass1_annotate.py"),
            "--src",        str(target_path),
            "--cfg",        str(cfg_path),
            "--program-id", program_id,
            "--out",        str(p1_out),
        ], str(session_dir)),
        ("pass2_template", [
            "python3", str(SCRIPTS_ROOT / "pass2_template.py"),
            "--annotations", str(p1_out),
            "--out",         str(p2_tmpl_out),
        ], str(session_dir)),
        ("pass2_llm", [
            "python3", str(SCRIPTS_ROOT / "pass2_llm.py"),
            "--propositions", str(p2_tmpl_out),
            "--program-id",   program_id,
            "--out",          str(p2_llm_out),
        ], str(session_dir)),
        ("pass3_synthesize", [
            "python3", str(SCRIPTS_ROOT / "pass3_synthesize.py"),
            "--propositions", str(p2_tmpl_out),
            "--program-id",   program_id,
            "--out",          str(synth_out),
        ], str(REPO_ROOT)),
    ]

    for step_name, cmd, cwd in steps:
        rc, _, err = await _run(cmd, cwd=cwd)
        _record(session_dir, session_id, step_name,
                "success" if rc == 0 else "failure",
                {"rc": rc}, err)
        if rc != 0:
            return None

    return p2_tmpl_out  # signal to Hermes that prepare succeeded


async def verify(session_id: str, program_id: str) -> bool:
    """
    Runs the gate verification chain:
      extract_ground_truth -> extract_md_claims -> gate_compare

    Called by Hermes after pass3_run.py has written the gold-candidate .md.
    Returns True if gate passes.
    """
    session_dir = SESSIONS_ROOT / session_id

    Path("/app/validation/claims").mkdir(parents=True, exist_ok=True)
    Path("/app/validation/ground_truth").mkdir(parents=True, exist_ok=True)

    steps = [
        ("extract_ground_truth", [
            "python3", str(VALIDATION_ROOT / "extract_ground_truth.py"), program_id,
        ], str(REPO_ROOT)),
        ("extract_md_claims", [
            "python3", str(VALIDATION_ROOT / "extract_md_claims.py"), program_id,
        ], str(REPO_ROOT)),
        ("gate_compare", [
            "python3", str(VALIDATION_ROOT / "gate_compare.py"), program_id,
        ], str(REPO_ROOT)),
    ]

    for step_name, cmd, cwd in steps:
        rc, _, err = await _run(cmd, cwd=cwd)
        _record(session_dir, session_id, step_name,
                "success" if rc == 0 else "failure",
                {"rc": rc}, err)
        if rc != 0:
            return False

    return True
