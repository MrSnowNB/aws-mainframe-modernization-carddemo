# syncd v1

Manifest-driven pipeline sync tool for the COBOL-MD-PIPELINE.
Locks verified CFG numbers into `SYNC-MANIFEST.yaml` so every agent
and PR can confirm they are working from the same ground truth.

## Requirements

- Python 3.10+
- PyYAML (`pip install pyyaml`)
- No other new dependencies

## Commands

### `status` — show branch + manifest summary

```powershell
py tools/syncd/sync.py status
```

Example output:

```
============================================================
syncd v1 -- status
============================================================
  Branch : wave1/cbstm03a
  HEAD   : cecae47f6a7b37da647d4fba159f0df46ad9e527
  Manifest: C:\...\SYNC-MANIFEST.yaml
  Schema  : syncd/1
  Programs locked: 1

  PROGRAM              PARAGRAPHS    L01 LOCKED_AT
  -------------------- ---------- ------ ------------------------
  CBSTM03A                     25     18 2026-05-04T01:00:00Z
```

---

### `lock <PROGRAM>` — lock CFG numbers into manifest

Reads `validation/structure/<PROGRAM>_cfg.json`, extracts paragraph
and L01 counts, verifies against `extract_ground_truth.py` output,
and writes a `locked_numbers` block into `SYNC-MANIFEST.yaml`.
Idempotent — safe to re-run after any CFG update.

```powershell
py tools/syncd/sync.py lock CBSTM03A
```

Example output:

```
[syncd] LOCKED CBSTM03A: 25 paragraphs, 18 L01 items
```

Resulting `SYNC-MANIFEST.yaml` entry:

```yaml
programs:
  CBSTM03A:
    locked_at: "2026-05-04T01:00:00Z"
    locked_numbers:
      paragraphs_expected: 25
      l01_items_expected: 18
      reachable_expected: 25
      dead_paragraphs_allowed: 0
      source_sha: ea341ec97f2b1a236de57f9c0fbd262f61b23511
      cfg_sha: d1665343e8479bf7fb554d118de0e8fd346bba09
```

Exit codes:
- `0` — locked successfully
- `1` — CFG file missing or `extract_ground_truth.py` failed
- `2` — reachable-paragraph count mismatch between CFG and ground truth
- `3` — forbidden path (should never occur on normal use)

---

### `verify` — run all three pipeline health checks

Runs `gate_compare.py`, `lint_cobol.py --fail-on-error`, and
`extract_md_claims.py` in sequence. Exits `0` only if all three
pass. Use this as your pre-commit check.

```powershell
py tools/syncd/sync.py verify
```

Example output (clean):

```
[syncd] Running gate_compare.py ...
-- Gate Summary -----------------------------------------------
  PASS  CBACT01C
  PASS  CBSTM03A
  11/11 programs passed
--------------------------------------------------------------
[syncd] Running lint_cobol.py --fail-on-error ...
[lint] 62 files | 0 errors | 2 warnings
[syncd] Running extract_md_claims.py ...
[CLAIMS] CBSTM03A: 25 paragraphs, 0 dead declared, 18 L01 items [OK]
[syncd] VERIFY PASS -- all checks clean
```

Example output (gate failure):

```
[syncd] Running gate_compare.py ...
[GATE] CBSTM03A: FAIL -- hallucinated_paragraphs: ['FAKE-PARA']
[syncd] VERIFY FAILED:
  - gate_compare.py exited 1
```

---

### `promote <PROGRAM>` — run pipeline stages 0 through ground-truth then lock

Runs the deterministic pre-MD stages in order and locks the manifest
on success. Does **not** run the MD generator — that remains a
human + agent step.

```powershell
py tools/syncd/sync.py promote CBSTM03A
```

Stages executed:
1. `normalize_rekt_output.py CBSTM03A` (skipped if script absent)
2. `extract_cfg_summary.py CBSTM03A`
3. `extract_ground_truth.py`
4. `sync.py lock CBSTM03A`

Example output:

```
[syncd] Running extract_cfg_summary.py CBSTM03A ...
[OK] CBSTM03A: 25 paragraphs, 18 L01 items
[syncd] Running extract_ground_truth.py  ...
[GT] CBSTM03A: 25 reachable / 0 dead / 18 L01 / 0 redefines [OK]
[syncd] LOCKED CBSTM03A: 25 paragraphs, 18 L01 items
[syncd] PROMOTE CBSTM03A complete -- manifest locked
[syncd] Next step: write translations/gold-candidate/CBSTM03A.md (human + agent)
```

If any stage fails, `promote` exits immediately with a non-zero code
and no manifest write occurs for that step.

---

## Write Safety

`sync.py` enforces a forbidden-path check on every file write.
The only paths it will ever write to are:

- `SYNC-MANIFEST.yaml` (repo root)
- `tools/syncd/` (its own directory)

Any attempt to write elsewhere exits with code `3`.

---

## Schema

`tools/syncd/manifest_schema.json` is a JSON Schema (draft-07)
document that describes the valid shape of `SYNC-MANIFEST.yaml`.
You can validate manually with:

```powershell
# requires jsonschema: pip install jsonschema
py -c "
import json, yaml, jsonschema
schema = json.load(open('tools/syncd/manifest_schema.json'))
data   = yaml.safe_load(open('SYNC-MANIFEST.yaml'))
jsonschema.validate(data, schema)
print('VALID')
"
```
