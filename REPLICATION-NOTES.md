---
title: ClawBot Replication Notes
version: "1.0"
last_updated: "2026-04-01"
---

# REPLICATION-NOTES.md

This document enables a fresh operator to reproduce the ClawBot environment exactly.
Agents must append entries before halting. Entries are append-only.

## Replicable Setup Checklist

```yaml
checklist:
  - step: "Clone repository"
    command: "git clone <repo-url> && cd ClawBot"
  - step: "Create Python virtual environment"
    command: "python -m venv .venv && source .venv/bin/activate  # Linux/Mac"
    windows: ".venv\\Scripts\\Activate.ps1"
  - step: "Install dependencies with constraints"
    command: "pip install -r requirements.txt -c constraints.txt"
  - step: "Verify Lemonade server is running"
    command: "curl http://localhost:8000/api/v1/models"
    expected: "JSON response containing model list"
  - step: "Confirm Qwen3.5-35B-A3B-GGUF loaded"
    check: "Model visible in Lemonade Model Manager as ACTIVE"
  - step: "Confirm LFM2.5-1.2B-Instruct-FLM loaded on NPU"
    check: "FastFlowLM NPU backend shows model as active"
  - step: "Run validation gates"
    command: "pytest -q && ruff check . && mypy ."
    pass_condition: "All green"
```

## Hardware Notes

```yaml
hardware:
  machine: "HP ZBook Ultra G1a (Strix Halo)"
  cpu: "AMD Ryzen AI Max+ (Strix Halo APU)"
  unified_memory: "128GB DDR5-8000 Hynix/Hyundai (8x16GB)"
  gpu_backend: "ROCm via Llama.cpp GPU"
  npu: "XDNA 2 (FastFlowLM NPU backend)"
  storage: "KIOXIA KXG80ZNV2T04 2TB NVMe"
  os: "Windows 11"
  lemonade_server_port: 8000
  primary_model: "Qwen3.5-35B-A3B-GGUF (19.70 GB, Llama.cpp GPU)"
  sub_agent_model: "LFM2.5-1.2B-Instruct-FLM (983 MB, FastFlowLM NPU)"
  orchestrator_model: "Qwen3-Coder-Next-GGUF (43.70 GB, Llama.cpp GPU)"
```

## Known Pitfalls to Avoid Next Run

1. **Do not hardcode port 8000** — if Lemonade is reconfigured, the orchestrator sub-agent port discovery will fail silently. Always read port from `runtime.yaml`.
2. **Start `--max-loaded-models 2` on Lemonade** — without this flag, the second model (LFM2.5) will be evicted from memory when Qwen3.5 is called, adding 30-90s reload latency per sub-agent call.
3. **Pin indirect dependencies** — see TS-001. `requirements.txt` alone is insufficient for reproducible installs.
4. **fp16 for embedding models** — loading any encoder model in fp32 on this hardware will OOM. Always pass `torch_dtype=torch.float16`.
5. **The `<think>` block budget** — Qwen3-Coder-Next generates `<think>` blocks that consume context rapidly. Enable `/no_think` suffix in terminal and file-write tasks. Reserve thinking for Plan phase and debugging only.

## Recurring Errors

| ID | Error | Resolution | Frequency |
|----|-------|------------|-----------|
| TS-001 | Dependency resolution loop | `constraints.txt` pin | Seen on fresh env setup |
| TS-002 | Embedding OOM | fp16 + batch reduction | Seen on first model load |
| TS-003 | Port conflict on orchestrator | Randomized port bind | Seen on rapid restarts |

## Environment Deltas

_Append entries here when the environment changes (package updates, hardware changes, model version bumps)._

| Date | Delta | Impact |
|------|-------|--------|
| 2026-04-01 | Initial setup — ZBook Strix Halo, Lemonade + Cline + ClawBot | Baseline |
