import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

SESSIONS_ROOT = Path("/app/securatron/sessions")
TOOLS_ROOT    = Path("/app/securatron/global/tools")


async def execute(session_id: str, target_file: str, atom_version: str = "1.0.0") -> bool:
    session_dir = SESSIONS_ROOT / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    target_path = Path(target_file).resolve()

    # Path traversal guard: target must be inside /app and be a .cbl/.cpy file
    if not target_path.is_relative_to(Path("/app")) or target_path.suffix not in (".cbl", ".cpy"):
        raise ValueError("Path traversal or invalid file type blocked")

    llm_cmd  = ["python3", str(TOOLS_ROOT / "pass2_llm.py"),
                "--target", str(target_path), "--session", session_id]
    gate_cmd = ["python3", str(TOOLS_ROOT / "gate_compare.py"),
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

    llm_rc,  _, llm_err  = await run(llm_cmd)
    gate_rc, _, gate_err = await run(gate_cmd)

    success = llm_rc == 0 and gate_rc == 0

    trial = {
        "ts":           datetime.now(timezone.utc).isoformat(),
        "session":      session_id,
        "atom":         "cobol.llm_evaluate",
        "atom_version": atom_version,
        "status":       "success" if success else "failure",
        "metrics":      {"llm_rc": llm_rc, "gate_rc": gate_rc},
    }
    # 'with' block ensures the fd is closed even if an exception fires mid-write
    with (session_dir / "trials.jsonl").open("a") as f:
        f.write(json.dumps(trial) + "\n")

    if not success:
        (session_dir / "post_mortem.md").write_text(
            f"LLM_EVALUATE FAILED\nLast error: {llm_err or gate_err}\n"
        )
        return False

    return True
