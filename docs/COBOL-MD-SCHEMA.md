---
schema_version: "cobol-md/1.0"
document: "COBOL-MD-SCHEMA"
version: "1.0.1"
status: "ACTIVE"
changelog:
  - version: "1.0.0"
    date: "2026-04-23"
    author: "Mark Snow"
    notes: "Initial schema — core fields, validation tiers, knowledge graph edges"
  - version: "1.0.1"
    date: "2026-04-23"
    author: "Mark Snow"
    notes: "Added business_domain (Grok integration) and subtype (Grok integration) as top-level required fields"
---

# COBOL-MD Schema v1.0.1

## Purpose

This schema defines the **required YAML front-matter structure** for every `.md` file produced by the COBOL→English middle-layer translation pipeline. Each translated file is a **semantic artifact**, not a decorated source file. The raw COBOL source is never embedded in the MD output — it remains in `app/cbl/`. The MD file is the independent English representation, designed for knowledge graph ingestion, LLM reasoning, and intelligence layer construction.

> **Design principle:** If a business rule, data item, or procedure paragraph exists in the COBOL source, it MUST appear in the MD file. Absence = T02/T03 validation failure.

---

## Full Schema

```yaml
---
# ── Identity ──────────────────────────────────────────────────────────────────
schema_version: "cobol-md/1.0"          # REQUIRED — always "cobol-md/1.0"
program_id: "CBCUS01C"                   # REQUIRED — matches PROGRAM-ID in source
source_file: "app/cbl/CBCUS01C.cbl"     # REQUIRED — repo-relative path
source_sha: "88a99d7f..."               # REQUIRED — git blob SHA of source at translation time
translation_date: "2026-04-23"          # REQUIRED — ISO-8601 date
translating_agent: "qwen3-235b-a22b"    # REQUIRED — exact model identifier
aifirst_task_id: "T-2026-04-23-001"     # REQUIRED — links to /aifirst run log

# ── Classification (Grok-integrated fields) ───────────────────────────────────
business_domain: "Account Management"   # REQUIRED — knowledge graph cluster label
                                         # Valid values:
                                         # Account Management | Transaction Processing |
                                         # Customer Management | Authorization |
                                         # Reporting | Administration | Utility | Menu

subtype: "Batch"                         # REQUIRED — graph partitioning key
                                         # Valid values:
                                         # CICS-Online | Batch | Utility | Menu | Copybook

# ── Structural Metadata ───────────────────────────────────────────────────────
author: ""                               # from AUTHOR paragraph, null if absent
date_written: ""                         # from DATE-WRITTEN paragraph, null if absent
lines_of_code: 0                         # total non-blank, non-comment lines
divisions:
  identification: true
  environment: true
  data: true
  procedure: true
environment:
  compiler: "IBM Enterprise COBOL"       # IBM Enterprise COBOL | GnuCOBOL | MicroFocus
  target: "CICS/VSAM"                    # CICS/VSAM | Batch/VSAM | Batch/DB2 | Utility
  runtime: "z/OS"                        # z/OS | AWS Blu Age | other

# ── Graph Edges ───────────────────────────────────────────────────────────────
calls_to:                                # REQUIRED — directed outbound call edges
  - program: "CBCUS01C"
    condition: "WS-CUST-STATUS = 'ACTIVE'"
    call_type: "STATIC"                  # STATIC | DYNAMIC | EXEC CICS LINK | EXEC CICS XCTL
called_by:                               # REQUIRED — inbound call edges (reverse index)
  - "COACTUPC"
copybooks_used:                          # REQUIRED — shared schema edges
  - name: "CVACTREC"
    path: "app/cpy/CVACTREC.cpy"
    sha: "abc123..."

# ── File I/O ──────────────────────────────────────────────────────────────────
file_control:
  - ddname: "CUSTFILE"
    organization: "INDEXED"              # INDEXED | SEQUENTIAL | RELATIVE
    access: "DYNAMIC"                    # SEQUENTIAL | RANDOM | DYNAMIC
    record_key: "WS-CUSTOMER-ID"
    crud: ["READ", "WRITE", "DELETE"]    # CREATE | READ | UPDATE | DELETE

# ── CICS (online programs only) ───────────────────────────────────────────────
cics_commands: []                        # list of EXEC CICS commands used
transaction_ids: []                      # CICS transaction IDs this program services

# ── Data Layer ────────────────────────────────────────────────────────────────
data_items:                              # REQUIRED — every 01-level working storage item
  - name: "WS-CUSTOMER-ID"
    level: 01
    picture: "X(10)"
    usage: null                          # COMP | COMP-3 | BINARY | DISPLAY | null
    value: null
    redefines: null                      # name of item this redefines, or null
    semantic: "Unique 10-char identifier linking to CUSTFILE VSAM index key"

# ── Business Rules ────────────────────────────────────────────────────────────
business_rules:                          # REQUIRED — implicit rules surfaced from conditional logic
  - id: "BR-001"
    rule: "A customer record cannot be deleted if WS-CUST-STATUS is not 'INACTIVE'"
    source_paragraph: "1200-DELETE-VALIDATE"
    rule_type: "guard"                   # guard | transform | lookup | audit | display
    confidence: "high"                  # high | medium | low
  - id: "BR-002"
    rule: "Customer ID must be exactly 10 characters; shorter values are left-padded with spaces"
    source_paragraph: "0100-INIT"
    rule_type: "transform"
    confidence: "high"

# ── Validation Status (populated by /aifirst G3) ─────────────────────────────
validation:
  t01_schema_valid: null                 # true | false | null (PENDING)
  t02_structural_complete: null
  t03_functional_score: null             # 0.0–1.0
  t04_semantic_score: null              # 0.0–1.0
  t05_regression_pass: null
  overall: "PENDING"                    # PENDING | PASS | FAIL
---
```

---

## Field Reference

### Identity Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `schema_version` | ✅ | string | Always `"cobol-md/1.0"` |
| `program_id` | ✅ | string | Matches `PROGRAM-ID` in source |
| `source_file` | ✅ | string | Repo-relative path to `.cbl` |
| `source_sha` | ✅ | string | Git blob SHA — enables exact source pinning |
| `translation_date` | ✅ | ISO-8601 | Date translation was produced |
| `translating_agent` | ✅ | string | Model that produced this file |
| `aifirst_task_id` | ✅ | string | Links to `/aifirst` run log |

### Classification Fields *(Grok-integrated v1.0.1)*

| Field | Required | Valid Values | Graph Role |
|-------|----------|-------------|------------|
| `business_domain` | ✅ | Account Management, Transaction Processing, Customer Management, Authorization, Reporting, Administration, Utility, Menu | **Cluster label** — groups nodes by business function |
| `subtype` | ✅ | CICS-Online, Batch, Utility, Menu, Copybook | **Partition key** — separates online vs. batch subgraphs |

`business_domain` maps to knowledge graph cluster labels — when you query "show me all Account Management programs and their call chains," this field is the anchor.

`subtype` enables graph partitioning — CICS-Online programs form one subgraph (user-facing, transaction-driven), Batch programs form another (scheduled, file-driven). Cross-subtype edges (a CICS program calling a Batch utility) become a special edge class worth flagging.

### Graph Edge Fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `calls_to` | ✅ | list | Outbound directed edges with condition and call_type |
| `called_by` | ✅ | list | Inbound reverse-index edges |
| `copybooks_used` | ✅ | list | Shared schema edges (copybook = shared type node) |

`call_type` values distinguish static links from CICS dynamic dispatches — critical for modernization analysis because CICS XCTL transfers control permanently while CALL returns.

### Business Rules Field

`business_rules[]` is the **highest-value field** for the knowledge graph and intelligence layer. These are implicit rules buried in conditional logic — they exist nowhere in any documentation, only in the COBOL source. Surfacing them as first-class data is the core intellectual contribution of this pipeline.

`rule_type` vocabulary:
- `guard` — blocks an operation if a condition isn't met
- `transform` — converts or reformats data
- `lookup` — retrieves from a reference file or table
- `audit` — writes a record for compliance/logging
- `display` — controls what the user sees

### Validation Field

The `validation` block is populated by the `/aifirst` G3 gate, not by the translating agent. This ensures the validation is independent of the translation — the agent cannot self-certify. `overall: "PASS"` requires all five tier scores to meet thresholds.

---

## Corpus Map: CardDemo Pilot Files

Stratified selection covering all complexity tiers and subtypes:

| File | Size | `business_domain` | `subtype` | Tier | Run Order |
|------|------|------------------|-----------|------|-----------|
| `COBSWAIT.cbl` | 2KB | Utility | Utility | S | 1 |
| `CBCUS01C.cbl` | 7KB | Customer Management | Batch | S | 2 |
| `COSGN00C.cbl` | 10KB | Administration | CICS-Online | M | 3 |
| `COMEN01C.cbl` | 12KB | Administration | Menu | M | 4 |
| `CBACT01C.cbl` | 17KB | Account Management | Batch | M | 5 |
| `CBTRN01C.cbl` | 18KB | Transaction Processing | Batch | L | 6 |
| `CBTRN02C.cbl` | 59KB | Transaction Processing | Batch | L | Post-FT |
| `COACTUPC.cbl` | 182KB | Account Management | CICS-Online | XL | Post-FT |

Run orders 1–6 are the pre-fine-tune baseline. Post-FT files validate that fine-tuning generalizes to larger, more complex programs.

---

## Output File Convention

Translated MD files live at:
```
translations/
  baseline/          ← pre-fine-tune run
    COBSWAIT.md
    CBCUS01C.md
    ...
  post-finetune/     ← post-fine-tune run (same files, same schema)
    COBSWAIT.md
    CBCUS01C.md
    ...
  gold/              ← human-verified training pairs
    COBSWAIT.md
    CBCUS01C.md
    ...
```

Diff between `baseline/` and `post-finetune/` for the same file = your proof of improvement.
Diff between `post-finetune/` and `gold/` = residual error after fine-tuning.

---

## T02 Structural Completeness Test

T02 is the deterministic gate for "1:1" accuracy. It uses GnuCOBOL's parser to extract a ground-truth list of all structural elements, then diffs against the MD file:

```bash
# Extract all paragraphs and sections from source
cobc -fsyntax-only -fdiagnostics-format=json CBCUS01C.cbl 2>&1 | \
  python3 scripts/extract_structure.py > CBCUS01C_structure.json

# Validate MD file contains all elements
python3 scripts/validate_t02.py \
  --source-structure CBCUS01C_structure.json \
  --translation translations/baseline/CBCUS01C.md \
  --schema docs/COBOL-MD-SCHEMA.md
```

A missing paragraph, DATA DIVISION item, or COPY statement reference = T02 fail. No exceptions.

---

## Knowledge Graph Node Model

Once ≥10 files pass T04, load into graph:

```
(Program {program_id, business_domain, subtype})
  -[:CALLS {condition, call_type}]->(Program)
  -[:USES_COPYBOOK]->(Copybook {name})
  -[:READS | WRITES | DELETES]->(VsamFile {ddname})
  -[:HAS_RULE]->(BusinessRule {id, rule_type, confidence})
  -[:HAS_DATA_ITEM]->(DataItem {name, picture, semantic})
```

`business_domain` → cluster/community label for graph visualization
`subtype` → subgraph partition (CICS-Online | Batch)

Query example (Neo4j Cypher):
```cypher
// All programs that access CUSTFILE and their business rules
MATCH (p:Program)-[:READS|WRITES]->(f:VsamFile {ddname: 'CUSTFILE'})
MATCH (p)-[:HAS_RULE]->(r:BusinessRule)
RETURN p.program_id, p.business_domain, r.rule, r.confidence
ORDER BY p.business_domain
```

---

## Version History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2026-04-23 | Mark Snow | Initial schema — identity, graph edges, data items, business rules, validation block |
| 1.0.1 | 2026-04-23 | Mark Snow | Added `business_domain` and `subtype` (Grok evaluation integration) |
