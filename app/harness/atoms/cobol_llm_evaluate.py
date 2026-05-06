import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

SESSIONS_ROOT = Path("/app/securatron/sessions")
TOOLS_ROOT    = Path("/app/scripts")


async def execute(session_id: str, target_file: str, atom_version: str = "1.0.0") -> bool:
    session_dir = SESSIONS_ROOT / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    target_path = Path(target_file).resolve()

    # Path traversal guard: target must be inside /app and be a .cbl/.cpy file
    if not target_path.is_relative_to(Path("/app")) or target_path.suffix not in (".cbl", ".cpy"):
        raise ValueError("Path traversal or invalid file type blocked")

    program_id = target_path.stem
    p1_out = session_dir / f"{program_id}_annotated.json"
    p2_tmpl_out = session_dir / f"{program_id}_propositions.json"
    p2_llm_out = session_dir / f"{program_id}_llm_requests.jsonl"

    p1_cmd = ["python3", str(TOOLS_ROOT / "pass1_annotate.py"),
              "--target", str(target_path), "--out", str(p1_out)]

    p2_tmpl_cmd = ["python3", str(TOOLS_ROOT / "pass2_template.py"),
                   "--annotated", str(p1_out), "--out", str(p2_tmpl_out)]

    p2_llm_cmd  = ["python3", str(TOOLS_ROOT / "pass2_llm.py"),
                   "--propositions", str(p2_tmpl_out),
                   "--program-id", program_id,
                   "--out", str(p2_llm_out)]

    gate_cmd = ["python3", "/app/validation/gate_compare.py",
                "--target", str(target_path), "--session", session_id]

    async def run(cmd: list[str]) -> tuple[int, str, str]:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=str(session_dir),          # subprocess isolated to session dir
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=300)
            return proc.returncode, stdout.decode().strip(), stderr.decode().strip()
        except asyncio.TimeoutError:
            proc.kill()
            return -1, "", "timeout"

    # Sequential execution of the pipeline
    p1_rc, _, p1_err = await run(p1_cmd)
    if p1_rc != 0:
        return await record_failure(session_id, session_dir, atom_version, "pass1", p1_rc, p1_err)

    p2t_rc, _, p2t_err = await run(p2_tmpl_cmd)
    if p2t_rc != 0:
        return await record_failure(session_id, session_dir, atom_version, "pass2_template", p2t_rc, p2t_err)

    p2l_rc, _, p2l_err = await run(p2_llm_cmd)
    if p2l_rc != 0:
        return await record_failure(session_id, session_dir, atom_version, "pass2_llm", p2l_rc, p2l_err)

    gate_rc, _, gate_err = await run(gate_cmd)

    success = gate_rc == 0

    trial = {
        "ts":           datetime.now(timezone.utc).isoformat(),
        "session":      session_id,
        "atom":         "cobol.llm_evaluate",
        "atom_version": atom_version,
        "status":       "success" if success else "failure",
        "metrics":      {"p1_rc": p1_rc, "p2t_rc": p2t_rc, "p2l_rc": p2l_rc, "gate_rc": gate_rc},
    }
    with (session_dir / "trials.jsonl").open("a") as f:
        f.write(json.dumps(trial) + "\n")

    if not success:
        (session_dir / "post_mortem.md").write_text(
            f"GATE_COMPARE FAILED\nLast error: {gate_err}\n"
        )
        return False

    return True

    async def record_failure(session_id, session_dir, atom_version, step, rc, err):
    trial = {
        "ts":           datetime.now(timezone.utc).isoformat(),
        "session":      session_id,
        "atom":         "cobol.llm_evaluate",
        "atom_version": atom_version,
        "status":       "failure",
        "step_failed":  step,
        "metrics":      {"rc": rc},
    }
    with (session_dir / "trials.jsonl").open("a") as f:
        f.write(json.dumps(trial) + "\n")
    (session_dir / "post_mortem.md").write_text(
        f"PIPELINE FAILED at {step}\nReturn code: {rc}\nError: {err}\n"
    )
    return False

