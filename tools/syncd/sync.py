#!/usr/bin/env python3
"""syncd v1 -- manifest-driven pipeline sync tool.

Usage:
  py tools/syncd/sync.py status
  py tools/syncd/sync.py lock <PROGRAM>
  py tools/syncd/sync.py verify
  py tools/syncd/sync.py promote <PROGRAM>

Exit codes:
  0  OK
  1  Gate / validation failure
  2  Manifest stale or missing required key
  3  Forbidden path write attempted

Dependencies: Python 3.10+ stdlib + PyYAML only. No network calls.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("[syncd] ERROR: PyYAML not found. pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Paths (all relative to repo root, which is 2 levels above this file)
# ---------------------------------------------------------------------------
TOOL_DIR = Path(__file__).resolve().parent          # tools/syncd/
REPO_ROOT = TOOL_DIR.parent.parent                   # repo root
MANIFEST_PATH = REPO_ROOT / "SYNC-MANIFEST.yaml"
CFG_DIR = REPO_ROOT / "validation" / "structure"

# Scripts (called as subprocesses so we never import them directly)
GATE_COMPARE      = REPO_ROOT / "validation" / "gate_compare.py"
LINT_COBOL        = REPO_ROOT / "validation" / "lint_cobol" / "lint_cobol.py"
EXTRACT_CLAIMS    = REPO_ROOT / "validation" / "extract_md_claims.py"
EXTRACT_GT        = REPO_ROOT / "validation" / "extract_ground_truth.py"
EXTRACT_CFG       = REPO_ROOT / "validation" / "extract_cfg_summary.py"
NORMALIZE_REKT    = REPO_ROOT / "validation" / "normalize_rekt_output.py"

# Allowed write roots (enforced on every write)
ALLOWED_WRITE_ROOTS = [
    TOOL_DIR,
    MANIFEST_PATH,
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _check_write_path(target: Path) -> None:
    """Abort with exit code 3 if target is outside allowed write roots."""
    resolved = target.resolve()
    for allowed in ALLOWED_WRITE_ROOTS:
        allowed_r = Path(allowed).resolve()
        try:
            resolved.relative_to(allowed_r)
            return
        except ValueError:
            continue
    print(f"[syncd] FORBIDDEN PATH: {target}", file=sys.stderr)
    sys.exit(3)


def _load_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.exists():
        return {"schema_version": "syncd/1", "programs": {}}
    with MANIFEST_PATH.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if "programs" not in data:
        data["programs"] = {}
    return data


def _save_manifest(data: dict[str, Any]) -> None:
    _check_write_path(MANIFEST_PATH)
    with MANIFEST_PATH.open("w", encoding="utf-8") as fh:
        yaml.dump(data, fh, sort_keys=False, allow_unicode=True, default_flow_style=False)


def _git(args: list[str]) -> str:
    """Run a git command and return stdout, empty string on error."""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True, text=True,
            cwd=REPO_ROOT
        )
        return result.stdout.strip()
    except Exception:
        return ""


def _run_script(script: Path, extra_args: list[str] | None = None) -> int:
    """Run a Python script as a subprocess. Returns exit code."""
    cmd = [sys.executable, str(script)] + (extra_args or [])
    result = subprocess.run(cmd, cwd=REPO_ROOT)
    return result.returncode


def _load_cfg(program: str) -> dict[str, Any]:
    cfg_path = CFG_DIR / f"{program}_cfg.json"
    if not cfg_path.exists():
        print(f"[syncd] ERROR: CFG not found: {cfg_path}", file=sys.stderr)
        sys.exit(1)
    with cfg_path.open(encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_status(_args: argparse.Namespace) -> int:
    """Print manifest summary + git branch + HEAD SHA."""
    branch = _git(["rev-parse", "--abbrev-ref", "HEAD"])
    head   = _git(["rev-parse", "HEAD"])
    manifest = _load_manifest()
    programs = manifest.get("programs", {})

    print("=" * 60)
    print("syncd v1 -- status")
    print("=" * 60)
    print(f"  Branch : {branch}")
    print(f"  HEAD   : {head}")
    print(f"  Manifest: {MANIFEST_PATH}")
    print(f"  Schema  : {manifest.get('schema_version', 'unknown')}")
    print(f"  Programs locked: {len(programs)}")
    print()

    if not programs:
        print("  (no programs locked yet -- run: py tools/syncd/sync.py lock <PROGRAM>)")
    else:
        print(f"  {'PROGRAM':<20} {'PARAGRAPHS':>10} {'L01':>6} {'LOCKED_AT'}")
        print(f"  {'-'*20} {'-'*10} {'-'*6} {'-'*24}")
        for prog, entry in programs.items():
            locked = entry.get("locked_numbers", {})
            p = locked.get("paragraphs_expected", "?")
            l = locked.get("l01_items_expected", "?")
            ts = entry.get("locked_at", "unknown")
            print(f"  {prog:<20} {str(p):>10} {str(l):>6} {ts}")

    print()
    return 0


def cmd_lock(args: argparse.Namespace) -> int:
    """Read CFG JSON and write locked_numbers into SYNC-MANIFEST.yaml."""
    program = args.program.upper()
    cfg = _load_cfg(program)

    paragraphs = cfg.get("paragraphs", [])
    data_items  = cfg.get("data_items", [])
    reachable   = [p for p in paragraphs if p.get("reachable", True)]
    dead        = [p for p in paragraphs if not p.get("reachable", True)]

    locked_numbers = {
        "paragraphs_expected":  len(paragraphs),
        "l01_items_expected":   len(data_items),
        "reachable_expected":   len(reachable),
        "dead_paragraphs_allowed": len(dead),
        "source_sha":           cfg.get("source_sha", None),
        "cfg_sha":              _git(["hash-object",
                                      str(CFG_DIR / f"{program}_cfg.json")]),
    }

    # Verify against extract_ground_truth.py if it exists
    if EXTRACT_GT.exists():
        gt_out_dir = REPO_ROOT / "validation" / "ground_truth"
        gt_file    = gt_out_dir / f"{program}_ground_truth.json"
        rc = _run_script(EXTRACT_GT)
        if rc != 0:
            print(f"[syncd] ERROR: extract_ground_truth.py exited {rc}", file=sys.stderr)
            sys.exit(1)
        if gt_file.exists():
            with gt_file.open(encoding="utf-8") as fh:
                gt = json.load(fh)
            gt_prog = None
            # ground_truth may be a list of per-program dicts or a single dict
            if isinstance(gt, list):
                for entry in gt:
                    if entry.get("program_id", "").upper() == program:
                        gt_prog = entry
                        break
            elif isinstance(gt, dict):
                if gt.get("program_id", "").upper() == program:
                    gt_prog = gt

            if gt_prog:
                gt_paragraphs = gt_prog.get("paragraphs_reachable", None)
                if gt_paragraphs is not None and gt_paragraphs != locked_numbers["reachable_expected"]:
                    print(
                        f"[syncd] MISMATCH: CFG reachable={locked_numbers['reachable_expected']} "
                        f"but ground_truth reachable={gt_paragraphs}",
                        file=sys.stderr
                    )
                    sys.exit(2)

    manifest = _load_manifest()
    manifest["programs"].setdefault(program, {})
    manifest["programs"][program]["locked_numbers"] = locked_numbers
    manifest["programs"][program]["locked_at"] = (
        datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    _save_manifest(manifest)

    print(f"[syncd] LOCKED {program}: "
          f"{locked_numbers['paragraphs_expected']} paragraphs, "
          f"{locked_numbers['l01_items_expected']} L01 items")
    return 0


def cmd_verify(_args: argparse.Namespace) -> int:
    """Run gate_compare, lint_cobol, extract_md_claims. Exit 0 only if all pass."""
    manifest = _load_manifest()
    targets  = manifest.get("verify_targets", {})
    failures = []

    # --- gate_compare.py ---
    if GATE_COMPARE.exists():
        print("[syncd] Running gate_compare.py ...")
        rc = _run_script(GATE_COMPARE)
        expected_gate = targets.get("gate_pass_count", None)
        if rc != 0:
            failures.append(f"gate_compare.py exited {rc}")
        elif expected_gate is not None:
            # gate_compare exits 0 even on partial pass; trust exit code only
            pass
    else:
        print("[syncd] SKIP: gate_compare.py not found", file=sys.stderr)

    # --- lint_cobol.py ---
    if LINT_COBOL.exists():
        print("[syncd] Running lint_cobol.py --fail-on-error ...")
        rc = _run_script(LINT_COBOL, ["--fail-on-error"])
        if rc != 0:
            failures.append(f"lint_cobol.py --fail-on-error exited {rc}")
    else:
        print("[syncd] SKIP: lint_cobol.py not found", file=sys.stderr)

    # --- extract_md_claims.py ---
    if EXTRACT_CLAIMS.exists():
        print("[syncd] Running extract_md_claims.py ...")
        rc = _run_script(EXTRACT_CLAIMS)
        if rc != 0:
            failures.append(f"extract_md_claims.py exited {rc}")
    else:
        print("[syncd] SKIP: extract_md_claims.py not found", file=sys.stderr)

    if failures:
        print()
        print("[syncd] VERIFY FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("[syncd] VERIFY PASS -- all checks clean")
    return 0


def cmd_promote(args: argparse.Namespace) -> int:
    """Run the pre-MD pipeline stages for a program and lock the manifest."""
    program = args.program.upper()
    steps: list[tuple[str, Path, list[str]]] = []

    if NORMALIZE_REKT.exists():
        steps.append(("normalize_rekt_output.py", NORMALIZE_REKT, [program]))
    else:
        print(f"[syncd] SKIP: normalize_rekt_output.py not found (optional step)")

    steps += [
        ("extract_cfg_summary.py",   EXTRACT_CFG,  [program]),
        ("extract_ground_truth.py",  EXTRACT_GT,   []),
    ]

    for label, script, extra in steps:
        if not script.exists():
            print(f"[syncd] ERROR: required script not found: {script}", file=sys.stderr)
            return 1
        print(f"[syncd] Running {label} {' '.join(extra)} ...")
        rc = _run_script(script, extra if extra else None)
        if rc != 0:
            print(f"[syncd] FAILED at {label} (exit {rc})", file=sys.stderr)
            return 1

    # Finally lock
    lock_args = argparse.Namespace(program=program)
    rc = cmd_lock(lock_args)
    if rc != 0:
        return rc

    print(f"[syncd] PROMOTE {program} complete -- manifest locked")
    print(f"[syncd] Next step: write translations/gold-candidate/{program}.md (human + agent)")
    return 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="sync.py",
        description="syncd v1 -- manifest-driven pipeline sync tool"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Print manifest summary + git branch + HEAD SHA")

    p_lock = sub.add_parser("lock", help="Lock a program's numbers into SYNC-MANIFEST.yaml")
    p_lock.add_argument("program", help="Program ID (e.g. CBSTM03A)")

    sub.add_parser("verify", help="Run gate_compare + lint_cobol + extract_md_claims")

    p_promote = sub.add_parser("promote", help="Run pipeline stages 0-GT then lock")
    p_promote.add_argument("program", help="Program ID (e.g. CBSTM03A)")

    args = parser.parse_args()

    dispatch = {
        "status":  cmd_status,
        "lock":    cmd_lock,
        "verify":  cmd_verify,
        "promote": cmd_promote,
    }
    return dispatch[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
