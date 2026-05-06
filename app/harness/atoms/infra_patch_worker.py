#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

# Target scripts that we might need to patch
PASS3_RUN_PY = Path("/app/scripts/pass3_run.py")

def patch_llm_stability():
    """Implements FM-1 recovery: Increase retries and throttling."""
    if not PASS3_RUN_PY.exists():
        return False, "pass3_run.py not found"

    content = PASS3_RUN_PY.read_text()
    
    # 1. Increase max_retries if found (increment by 2)
    match_retries = re.search(r"max_retries = (\d+)", content)
    if match_retries:
        old_val = int(match_retries.group(1))
        new_val = old_val + 2
        content = content.replace(f"max_retries = {old_val}", f"max_retries = {new_val}")
        print(f"[PATCH] Increased max_retries from {old_val} to {new_val}")
    
    # 2. Increase heavy throttle sleep if found (increment by 5s)
    match_sleep = re.search(r"time\.sleep\((\d+)\)  # Heavy throttle", content)
    if match_sleep:
        old_sleep = int(match_sleep.group(1))
        new_sleep = old_sleep + 5
        content = content.replace(f"time.sleep({old_sleep})  # Heavy throttle", f"time.sleep({new_sleep})  # Heavy throttle")
        print(f"[PATCH] Increased heavy throttle from {old_sleep}s to {new_sleep}s")

    PASS3_RUN_PY.write_text(content)
    return True, "Applied LLM stability patches (increased retries/throttle)"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern", required=True)
    parser.add_argument("--context", required=False)
    args = parser.parse_args()

    print(f"[INFRA_PATCH] Evaluating pattern: {args.pattern}")
    
    success = False
    reason = "No patch logic defined for this pattern"

    if "FM-1:" in args.pattern:
        success, reason = patch_llm_stability()
    
    result = {
        "ok": success,
        "pattern": args.pattern,
        "reason": reason,
        "status": "success" if success else "failure"
    }
    
    print(f"RESULT: {json.dumps(result)}")
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
