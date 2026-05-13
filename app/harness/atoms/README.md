# SecuraTron COBOL-to-AI Pipeline Atoms

This directory contains the atomic worker scripts for the SecuraTron COBOL modernization pipeline. These "atoms" are designed to be executed independently or orchestrated by the SecuraTron dispatch system.

## Atoms

### `cobol_pipeline_worker.py`
The main orchestrator for a single COBOL program translation.
- **Purpose:** Manages the full lifecycle of a translation request (Prepare -> Synthesize -> Verify).
- **Inputs:** `--target` (COBOL source path), `--session` (unique session ID).
- **Execution:** Runs the 3-pass pipeline and returns a structured `RESULT: {...}` JSON line for parsing.

### `cobol_llm_evaluate.py`
The engine behind the COBOL pipeline, containing core logic functions.
- **`prepare(session_id, target_file)`:** Runs the deterministic preparation chain:
  1. `pass1_annotate`: Identifies logic blocks.
  2. `pass2_template`: Generates translation propositions.
  3. `pass2_llm`: (Optional) Preparatory LLM calls.
  4. `pass3_synthesize`: Builds the JSONL payloads for the final synthesis pass.
- **`verify(session_id, program_id)`:** Runs the gated validation chain:
  1. `extract_ground_truth`: Pulls expectations from legacy data.
  2. `extract_md_claims`: Parses the LLM-generated Markdown for claims.
  3. `gate_compare`: Compares claims against ground truth and returns exit code 0 if within tolerance.
- **`_run` / `_record`:** Utility functions for async process execution and trials logging.

### `infra_patch_worker.py`
Specialized atom for infrastructure-level repairs (SIL patches).
- **Purpose:** Applies targeted string-replacement patches to source code based on error feedback.
- **Harden:** Uses `py_compile` checks to ensure patches do not introduce syntax errors.

## Integration

These atoms are used by the SecuraTron harness to process COBOL files stored in `app/app/cbl/`. Results are written to `translations/gold-candidate/` and detailed trial logs are stored in `app/securatron/sessions/`.
