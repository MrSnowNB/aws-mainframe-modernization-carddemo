# Phase 1 Translation Prompt Contract — v2 (T-2026-04-23-002)

> This contract extends the v1 (T-001) contract with three hard rules (8, 9, 10)
> required by AIFIRST-PLAN-3PASS.md §15 for the three-pass architecture.
> Rules 1–7 below are renumbered from the original v1 file (they are unchanged
> in substance). Rules 8, 9, and 10 are NEW in v2.


You are translating a COBOL program into a structured English Markdown file that conforms
to `docs/COBOL-MD-SCHEMA.md` v1.0.2. The output is an **independent semantic artifact** —
the raw COBOL source must never appear in your output.

## Output file path

`translations/baseline-v1.1/<PROGRAM_ID>.md`

(T-002 writes to a new `baseline-v1.1/` directory and MUST NOT overwrite the
T-001 `translations/baseline/` outputs.)

## Inputs (all absolute paths are repo-relative)

1. COBOL source: `app/cbl/<PROGRAM_ID>.cbl` — read the ENTIRE file.
2. CFG JSON artifact: `validation/structure/<PROGRAM_ID>_cfg.json` — read the ENTIRE file.
3. Schema contract: `docs/COBOL-MD-SCHEMA.md` — treat as the authoritative field list.
4. Pre-assigned classification from the pilot corpus table:
   - COBSWAIT  → business_domain="Utility",                subtype="Utility"
   - CBCUS01C  → business_domain="Customer Management",    subtype="Batch"
   - COSGN00C  → business_domain="Administration",         subtype="CICS-Online"
   - COMEN01C  → business_domain="Administration",         subtype="Menu"
   - CBACT01C  → business_domain="Account Management",     subtype="Batch"
   - CBTRN01C  → business_domain="Transaction Processing", subtype="Batch"

## Hard rules

1. Populate ALL required YAML front-matter fields (schema §Full Schema). No required field
   may be null or omitted unless the schema marks it optional.
2. Use the `reachable` values from the CFG artifact for every
   `procedure_paragraphs[].reachable` and every `data_items[].dead_code_flag`
   (dead_code_flag = NOT reachable).
3. For every CFG `redefines_clauses[]` entry, the corresponding `data_items[]` entry in
   your output MUST include a `redefines_interpretations[]` array with ≥2 entries. Each
   entry must contain `condition`, `interpreted_as`, and `encoding`. `condition` must
   reference a field that exists elsewhere in your `data_items[]`.
4. DO NOT embed raw COBOL source, PIC clauses as verbatim COBOL, or fenced COBOL code
   blocks anywhere in the MD. English prose only in the body; YAML metadata only in the
   front-matter.
5. DO NOT populate the `validation` block — leave every sub-field as `null` and `overall`
   as `"PENDING"`.
6. `aifirst_task_id: "T-2026-04-23-001"`.
7. `cfg_source: "validation/structure/<PROGRAM_ID>_cfg.json"`.
8. `source_sha` must match the value already present in the CFG JSON artifact.
9. `translating_agent` must be the EXACT model identifier you are running under (e.g.,
   `"claude-sonnet-4.6 (subagent)"` or `"gpt-5.4"` — include model family and variant).
10. Every paragraph present in the CFG `paragraphs[]` array MUST appear in
    `procedure_paragraphs[]` AND must have a one-sentence summary in the body.
11. Every 01-level data item present in the CFG `data_items[]` array MUST appear in
    `data_items[]` with matching `level`, `picture`, and `usage`.
12. Every item in CFG `copybooks_used[]` MUST appear in `copybooks_used[]` as an object
    with `name` populated. `path` = `app/cpy/<NAME>.cpy` or `app/cpy-bms/<NAME>.cpy` if
    known, else `null`. `sha` may be `null`.
13. Every item in CFG `calls_to[]` MUST appear in `calls_to[]` as an object with
    `program`, `condition` (use "unconditional" when no guard), and `call_type`
    (STATIC / DYNAMIC / EXEC CICS LINK / EXEC CICS XCTL).
14. For every conditional block surfaced in the code (IF / EVALUATE guards that gate
    a PERFORM, CALL, UPDATE, DELETE, or DISPLAY), add a `business_rules[]` entry with
    `id` (BR-NNN), `rule` (English statement), `source_paragraph`, `rule_type`
    (guard|transform|lookup|audit|display), `confidence` (high|medium|low), `reachable`.

## Body (after the YAML front-matter)

Include these sections as Markdown prose (English only — no COBOL):

1. `# <PROGRAM_ID> — <one-line title>`
2. `## Purpose` — one short paragraph.
3. `## Runtime Context` — batch/online, services used, file I/O summary.
4. `## Data Layout` — narrative description of each group structure surfaced in
   `data_items`, especially any REDEFINES and their runtime selectors.
5. `## Procedure Logic` — one subsection per paragraph in CFG order, each with a short
   English description of what it does. Never quote the COBOL.
6. `## Business Rules Surfaced` — enumerate each BR-NNN with the rule statement.
7. `## Graph Summary` — bullet list of node/edge summaries (CALLS, COPYBOOKS,
   VSAM READS/WRITES/DELETES, RULES).

## Self-check before returning

- Open the file and verify each required schema field is present and non-null
  (except the `validation` block).
- Verify NO fenced ```cobol block exists.
- Verify NO verbatim `PIC X(N)` followed by a dot on its own line appears in the body
  prose (those would indicate pasted COBOL).
- Verify `validation.overall == "PENDING"`.
- Verify every `redefines_interpretations[].condition` uses a fully qualified
  data name (see Rule 9).
- Verify every `logical_groups[].semantic_pattern` is one of the nine allowed
  enum values (see Rule 10).

---

## T-002 additions (AIFIRST-PLAN-3PASS.md §15)

### Rule 8 — Pass 2 LLM call envelope: temperature=0 + structured JSON output

Any Pass 2 LLM invocation (for EXEC CICS verbs, EXEC SQL verbs, complex
EVALUATE blocks, or any statement whose `proposition_source == "LLM"` in the
Pass 2 propositions) MUST be issued with:

- `temperature = 0`
- `response_format` constrained to a JSON object matching the Pass 2
  proposition schema below.
- `max_tokens` bounded to keep payload deterministic.
- `seed` fixed when the provider supports it (e.g., OpenAI `seed: 42`).

**Request payload shape** (emitted by `scripts/pass2_llm.py` and written to
`validation/pass2/<PROGRAM_ID>_llm_requests.jsonl`):

```json
{
  "model": "<model-id>",
  "temperature": 0,
  "seed": 42,
  "response_format": {"type": "json_object"},
  "messages": [
    {"role": "system", "content": "You are a COBOL-to-English semantic annotator. Respond ONLY with a JSON object matching the requested schema."},
    {"role": "user", "content": "<structured prompt with seq, verb, cfg_branch_context, operands, paragraph, program_id>"}
  ]
}
```

**Required response JSON schema** (the LLM MUST produce exactly this shape):

```json
{
  "seq": <int>,
  "proposition": "<single-sentence English description>",
  "modifies": "<fully-qualified data name OR null>",
  "reads": ["<fully-qualified data name>", ...],
  "semantic_pattern": "<one of the nine enum values, see Rule 10>",
  "confidence": <float 0.0–1.0>
}
```

Any response that does not parse as the above object is a T-PASS2-LLM
violation and is rejected; the statement remains flagged for human review.

### Rule 9 — Qualified names in REDEFINES conditions

Every `data_items[].redefines_interpretations[].condition` MUST reference a
fully qualified COBOL data name (either a 01-level name or a group-qualified
path like `WS-REISSUE-DATE OF OUT-REISSUE-DATE-BLOCK`). A bare token that
matches multiple scopes is a **T-PASS1-OPS failure** and the translation is
rejected.

Rationale: this is exactly the T-001 CBACT01C defect (`ACCT-REISSUE-DATE`
appearing bare while the CFG only carried qualified variants `OUT-REISSUE-DATE`,
`WS-REISSUE-DATE`, `VB2-REISSUE-DATE`). In v2, any such unqualified reference
must either be disambiguated against `data_items_inventory` or flagged for
human annotation; it must not silently ship.

Validator: `scripts/validate_pass1.py` raises T-PASS1-OPS for every
redefines condition whose token is not uniquely resolvable to exactly one entry
in `data_items_inventory` without qualification.

### Rule 10 — `semantic_pattern` enum (9 values)

Every `logical_groups[].semantic_pattern` (schema v1.1 addition) and every
Pass 2 proposition whose source is LLM MUST carry a `semantic_pattern` drawn
from the following closed enum:

| Value                 | Meaning                                                            |
| --------------------- | ------------------------------------------------------------------ |
| `guard-with-override` | A default assignment guarded by a later conditional override.      |
| `accumulation`        | A counter or running total being incremented across iterations.    |
| `state-machine`       | A flag / status variable driving subsequent branch decisions.      |
| `delegation`          | A PERFORM or CALL that delegates work to another paragraph/prog.   |
| `sequential`          | Linear, unconditional statement flow inside a paragraph.           |
| `conditional-branch`  | IF / EVALUATE gating that does not itself assign a domain value.   |
| `cics-interaction`    | EXEC CICS SEND / RECEIVE / XCTL / LINK / RETURN / HANDLE.          |
| `file-io`             | READ / WRITE / REWRITE / DELETE / OPEN / CLOSE against a dataset.  |
| `unknown`             | Pattern not identifiable; REQUIRES human annotation before merge.  |

`unknown` is permitted to leave Pass 2 but MUST NOT enter the final MD. Any
`logical_groups[]` entry with `semantic_pattern: unknown` is a blocking
T-PASS3-SEMANTIC failure; the human reviewer must either reclassify the entry
into one of the other eight values or split the group.

Validators: `scripts/validate_pass2.py` checks Pass 2 propositions; `scripts/validate_pass3.py` checks `logical_groups[]` in the final MD.
