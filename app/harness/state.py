import json
from pathlib import Path
from typing import Any, Dict

SESSIONS_ROOT = Path("/app/securatron/sessions")


def get_session_path(session_id: str) -> Path:
    return SESSIONS_ROOT / session_id / "state.json"


def load_state(session_id: str) -> Dict[str, Any]:
    path = get_session_path(session_id)
    if path.exists():
        return json.loads(path.read_text())
    return {}


def save_state(session_id: str, state: Dict[str, Any]) -> None:
    path = get_session_path(session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2))
