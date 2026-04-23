---
title: ClawBot Troubleshooting Log
version: "1.0"
last_updated: "2026-04-01"
---

# TROUBLESHOOTING.md

This is a **living document**. Agents must append a new entry before halting on any failure.
Do not delete entries. Entries are append-only.

## Entry Format

```yaml
---
id: TS-<sequential number>
date: "YYYY-MM-DD"
phase: <Plan|Build|Validate|Review|Release>
---
```

**Context**: What was the agent doing when this occurred?
**Symptom**: What observable behavior indicated a problem?
**Error Snippet**:
```
<paste exact error output here>
```
**Probable Cause**: Why did this likely occur?
**Quick Fix**: Immediate workaround to unblock.
**Permanent Fix**: Root-cause resolution to implement.
**Prevention**: What rule, test, or check prevents recurrence?

---

## Seeded Entries

---
id: TS-001
date: "2026-04-01"
phase: Build
---

**Context**: Agent resolving Python package dependencies during environment setup.
**Symptom**: `pip install` enters an infinite resolution loop; process does not terminate.
**Error Snippet**:
```
ERROR: Cannot determine installation order for packages; dependency conflict detected.
ResolutionImpossible: for help visit https://pip.pypa.io/en/stable/topics/dependency-resolution/
```
**Probable Cause**: Transitive dependency version conflicts between indirect packages not pinned in `requirements.txt`.
**Quick Fix**: Add a `constraints.txt` file pinning the conflicting indirect dependency to a known-compatible version. Run `pip install -r requirements.txt -c constraints.txt`.
**Permanent Fix**: Audit all direct dependencies with `pip-compile` (pip-tools) to generate a fully-resolved `requirements.txt` with pinned transitive deps. Commit the compiled file.
**Prevention**: Add a CI step that runs `pip check` after install to catch dependency conflicts before they reach the agent environment.

---
id: TS-002
date: "2026-04-01"
phase: Build
---

**Context**: Agent loading an embedding model for vector search or semantic similarity tasks.
**Symptom**: Process killed or CUDA/ROCm OOM error during model initialization or batch inference.
**Error Snippet**:
```
RuntimeError: CUDA out of memory. Tried to allocate X GiB.
# or ROCm equivalent:
RuntimeError: HIP error: out of memory
```
**Probable Cause**: Batch size or sequence length exceeds available VRAM; model loaded in full float32 precision when fp16 is sufficient.
**Quick Fix**: (1) Reduce `batch_size` to 1 or 2. (2) Set `max_seq_length` truncation to 512 or lower. (3) Load model with `model.half()` or `torch_dtype=torch.float16`.
**Permanent Fix**: Profile peak VRAM usage with `torch.cuda.max_memory_allocated()` at baseline batch sizes and document hardware limits in `REPLICATION-NOTES.md`. Add memory guard assertions before large inference calls.
**Prevention**: Add a pre-flight VRAM check that compares model size estimate against available VRAM before loading. Fail fast with a clear message rather than OOM during inference.

---
id: TS-003
date: "2026-04-01"
phase: Build
---

**Context**: Agent starting a local orchestrator service (FastAPI, gRPC, or similar) that binds to a fixed port.
**Symptom**: Service fails to start; address already in use error.
**Error Snippet**:
```
OSError: [Errno 98] Address already in use: ('0.0.0.0', 8000)
# or Windows equivalent:
[WinError 10048] Only one usage of each socket address is permitted
```
**Probable Cause**: A previous agent run or dev server left a process bound to the hardcoded port.
**Quick Fix**: Use randomized port binding with retry logic:
```python
import socket, random
def get_free_port(start=8100, end=8200, retries=10):
    for _ in range(retries):
        port = random.randint(start, end)
        with socket.socket() as s:
            try:
                s.bind(('', port))
                return port
            except OSError:
                continue
    raise RuntimeError("No free port found in range")
```
**Permanent Fix**: Never hardcode ports in orchestrator startup. Always use `get_free_port()` or an OS-assigned port (`port=0`). Write the selected port to a `runtime.yaml` file so sub-agents can discover it.
**Prevention**: Add a port availability check to the pre-flight validation step. Document the port range in `REPLICATION-NOTES.md`.
