#!/usr/bin/env python3
"""
infra_patch_worker.py — SecuraTron SIL Act Phase (Hardened)
Safe, validated, dry-run-by-default patching with rollback.
"""
import argparse
import json
import re
import sys
import shutil
import py_compile
from pathlib import Path
from datetime import datetime, timezone

# Target files
PASS3_RUN_PY = Path("/app/scripts/pass3_run.py")
ATOM_PY = Path("/app/harness/atoms/cobol_llm_evaluate.py")

def _validate_python(path: Path) -> tuple[bool, str]:
    """Compile-check Python file. Returns (ok, error_message)."""
    try:
        py_compile.compile(str(path), doraise=True)
        return True, ""
    except py_compile.PyCompileError as e:
        return False, str(e)

def _backup_and_patch(path: Path, new_content: str) -> tuple[bool, str]:
    """Create timestamped backup, apply patch, validate, rollback on failure."""
    if not path.exists():
        return False, f"{path.name} not found"

    # Create backup
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup = path.with_suffix(f".bak.{timestamp}")
    shutil.copy2(path, backup)

    # Apply
    path.write_text(new_content)

    # Validate
    ok, err = _validate_python(path)
    if not ok:
        # Rollback
        shutil.copy2(backup, path)
        return False, f"Validation failed — rolled back. Error: {err}"

    return True, f"Patch applied and validated (backup: {backup.name})"

def patch_llm_stability() -> tuple[bool, str]:
    """FM-1: Increase retries and throttle in pass3_run.py"""
    if not PASS3_RUN_PY.exists():
        return False, "pass3_run.py not found"

    content = PASS3_RUN_PY.read_text()
    patched = False

    # Increase max_retries
    match = re.search(r"max_retries = (\d+)", content)
    if match:
        old = int(match.group(1))
        new = old + 2
        content = content.replace(f"max_retries = {old}", f"max_retries = {new}")
        print(f"[PATCH] max_retries: {old} → {new}")
        patched = True

    # Increase heavy throttle
    match = re.search(r"time\.sleep\((\d+)\)  *# Heavy throttle", content)
    if match:
        old = int(match.group(1))
        new = old + 5
        content = re.sub(r"time\.sleep\(" + str(old) + r"\)  *# Heavy throttle", f"time.sleep({new})  # Heavy throttle", content)
        print(f"[PATCH] heavy throttle: {old}s → {new}s")
        patched = True

    if not patched:
        return False, "No patchable parameters found"

    return _backup_and_patch(PASS3_RUN_PY, content)

def patch_preprocessing_args() -> tuple[bool, str]:
    """FM-10: Fix CLI argument mapping in cobol_llm_evaluate.py"""
    if not ATOM_PY.exists():
        return False, "cobol_llm_evaluate.py not found"

    content = ATOM_PY.read_text()

    old_snippet = '"--target",        str(target_path),'
    new_snippet = '"--src", str(target_path), "--program-id", program_id, "--out", str(session_dir / "_annotated.json"),'

    if old_snippet not in content:
        # Check for alternative spacing
        old_snippet_alt = '"--target", str(target_path),'
        if old_snippet_alt in content:
            content = content.replace(old_snippet_alt, new_snippet)
        else:
            return False, "Target snippet not found (already patched or changed)"
    else:
        content = content.replace(old_snippet, new_snippet)

    return _backup_and_patch(ATOM_PY, content)

def main():
    parser = argparse.ArgumentParser(description="SecuraTron SIL Patch Worker (Hardened)")
    parser.add_argument("--pattern", required=True, help="FM-1:xxx or FM-10:xxx")
    parser.add_argument("--apply", action="store_true", help="Actually apply patch (default = dry-run)")
    args = parser.parse_args()

    print(f"[INFRA_PATCH] Pattern: {args.pattern} | Mode: {'APPLY' if args.apply else 'DRY-RUN'}")

    if not args.apply:
        print("DRY-RUN: No changes made. Use --apply to execute.")
        # Important: must exit 0 so SecuraTron doesn't mark it failed, but we return a clean result
        result = {
            "ok": True,
            "pattern": args.pattern,
            "reason": "DRY-RUN completed successfully",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        print(json.dumps(result, indent=2))
        sys.exit(0)

    if "FM-1:" in args.pattern:
        success, reason = patch_llm_stability()
    elif "FM-10:" in args.pattern:
        success, reason = patch_preprocessing_args()
    else:
        success, reason = False, f"No handler for pattern: {args.pattern}"

    result = {
        "ok": success,
        "pattern": args.pattern,
        "reason": reason,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    print(json.dumps(result, indent=2))
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
