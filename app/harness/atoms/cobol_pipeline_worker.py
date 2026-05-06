#!/usr/bin/env python3
import asyncio
import json
import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone

# We can reuse the logic from the existing atom but make it a standalone worker
from cobol_llm_evaluate import prepare, verify, _record

SESSIONS_ROOT = Path("/app/securatron/sessions")

async def run_worker(target_file: str, session_id: str):
    session_dir = SESSIONS_ROOT / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    program_id = Path(target_file).stem
    
    gate_ok = False
    try:
        print(f"[WORKER] Starting pipeline for {program_id} (session: {session_id})")
        
        # 1. Prepare
        props_path = await prepare(session_id, target_file)
        if not props_path:
            print(f"[WORKER] Preparation failed for {program_id}")
            raise RuntimeError("Preparation failed")
            
        # 2. Synthesize (Pass 3 Run)
        import os
        from cobol_llm_evaluate import _run
        
        INFERENCE_ENDPOINT = os.getenv("INFERENCE_ENDPOINT", "http://localhost:1234/v1")
        INFERENCE_MODEL    = os.getenv("INFERENCE_MODEL", "local-model")
        INFERENCE_API_KEY = os.getenv("INFERENCE_API_KEY", "local")
        
        print(f"[WORKER] Synthesizing {program_id}...")
        synth_path = Path("/app/validation/pass3") / f"{program_id}_synthesis.jsonl"
        cfg_path   = Path("/app/validation/structure") / f"{program_id}_cfg.json"
        ann_path   = session_dir / f"{program_id}_annotations.json"
        
        rc, stdout, err = await _run([
            "python3", "/app/scripts/pass3_run.py",
            "--program-id",     program_id,
            "--base-url",       INFERENCE_ENDPOINT,
            "--model",          INFERENCE_MODEL,
            "--api-key",        INFERENCE_API_KEY,
            "--synthesis-path", str(synth_path),
            "--cfg-path",       str(cfg_path),
            "--ann-path",       str(ann_path),
        ], cwd="/app")
        
        if rc != 0:
            print(f"[WORKER] Synthesis failed for {program_id}: {err}")
            (session_dir / "post_mortem.md").write_text(f"SYNTHESIZE FAILED\n{rc}\n{err}\n")
            raise RuntimeError(f"Synthesis failed with exit code {rc}")
            
        # 3. Verify
        print(f"[WORKER] Verifying {program_id}...")
        gate_ok = await verify(session_id, program_id)
        
        if gate_ok:
            print(f"[WORKER] Pipeline SUCCESS for {program_id}")
        else:
            print(f"[WORKER] Pipeline GATE FAILURE for {program_id}")

    except Exception as e:
        print(f"[WORKER] CRITICAL FAILURE for {program_id}: {str(e)}")
        gate_ok = False
        
    # ALWAYS Return structured result for SecuraTron dispatch
    result = {
        "status": "success" if gate_ok else "failure",
        "program_id": program_id,
        "session_id": session_id,
        "gate_pass": gate_ok
    }
    print(f"RESULT: {json.dumps(result)}")
    return gate_ok

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--session", required=True)
    args = parser.parse_args()
    
    success = asyncio.run(run_worker(args.target, args.session))
    sys.exit(0 if success else 1)
