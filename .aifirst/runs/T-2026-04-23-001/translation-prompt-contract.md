# Phase 1 Translation Prompt Contract (T-2026-04-23-001)

You are translating a COBOL program into a structured English Markdown file that conforms
to `docs/COBOL-MD-SCHEMA.md` v1.0.2. The output is an **independent semantic artifact** —
the raw COBOL source must never appear in your output.

## Output file path

`translations/baseline/<PROGRAM_ID>.md`

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
