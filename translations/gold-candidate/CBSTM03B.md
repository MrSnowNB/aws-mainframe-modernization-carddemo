---
schema_version: "cobol-md/1.0"
program_id: "CBSTM03B"
source_file: "app/cbl/CBSTM03B.CBL"
source_sha: "d076c44dffe71113e3bc5acf3dda68a14e1c54b2"
translation_date: "2026-05-03"
translating_agent: "perplexity-sonar (subagent)"
aifirst_task_id: "T-2026-05-03-002"
cfg_source: "validation/structure/CBSTM03B_cfg.json"

business_domain: "File Access Service"
subtype: "Batch"

author: "AWS"
date_written: null
lines_of_code: 172
divisions:
  identification: true
  environment: true
  data: true
  procedure: true
environment:
  compiler: "IBM Enterprise COBOL"
  target: "Batch/VSAM"
  runtime: "z/OS"

calls_to: []

called_by:
  - program: "CBSTM03A"
    call_type: "STATIC"
    condition: "delegated file operation (TRNXFILE / XREFFILE / CUSTFILE / ACCTFILE open, read, close)"

copybooks_used: []

file_control:
  - ddname: "TRNXFILE"
    organization: "INDEXED"
    access: "SEQUENTIAL"
    record_key: "FD-TRNXS-ID"
    crud: ["READ"]
  - ddname: "XREFFILE"
    organization: "INDEXED"
    access: "SEQUENTIAL"
    record_key: "FD-XREF-CARD-NUM"
    crud: ["READ"]
  - ddname: "CUSTFILE"
    organization: "INDEXED"
    access: "RANDOM"
    record_key: "FD-CUST-ID"
    crud: ["READ"]
  - ddname: "ACCTFILE"
    organization: "INDEXED"
    access: "RANDOM"
    record_key: "FD-ACCT-ID"
    crud: ["READ"]

cics_commands: []
transaction_ids: []

data_items:
  - name: "FD-TRNXFILE-REC"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "File descriptor record for TRNXFILE; top-level 01 group record for the transaction VSAM KSDS input file"

  - name: "FD-XREFFILE-REC"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "File descriptor record for XREFFILE; top-level 01 group record for the card cross-reference VSAM KSDS input file"

  - name: "FD-CUSTFILE-REC"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "File descriptor record for CUSTFILE; top-level 01 group record for the customer VSAM KSDS random-access input file"

  - name: "FD-ACCTFILE-REC"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "File descriptor record for ACCTFILE; top-level 01 group record for the account VSAM KSDS random-access input file"

  - name: "TRNXFILE-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file-status code returned after every I/O operation on TRNXFILE; propagated to LK-M03B-RC on completion"

  - name: "XREFFILE-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file-status code returned after every I/O operation on XREFFILE; propagated to LK-M03B-RC on completion"

  - name: "CUSTFILE-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file-status code returned after every I/O operation on CUSTFILE; propagated to LK-M03B-RC on completion"

  - name: "ACCTFILE-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file-status code returned after every I/O operation on ACCTFILE; propagated to LK-M03B-RC on completion"

  - name: "LK-M03B-AREA"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "1050-byte LINKAGE SECTION parameter area passed by CBSTM03A via STATIC CALL; contains LK-M03B-DD (8-char file selector), LK-M03B-OPER (1-char operation code with 88-levels for OPEN/CLOSE/READ/READ-K/WRITE/REWRITE), LK-M03B-RC (2-char returned file status), LK-M03B-KEY (25-char key buffer for READ-K), LK-M03B-KEY-LN (S9(4) key length), and LK-M03B-FLDT (1000-byte record buffer)"

procedure_paragraphs:
  - name: "0000-START"
    reachable: true
    performs: []
    goto_targets:
      - "9999-GOBACK"
    summary: "Entry point; EVALUATE on LK-M03B-DD dispatches to one of four file handler blocks via PERFORM THRU; WHEN OTHER falls through to GO TO 9999-GOBACK for unknown DD name"

  - name: "1000-TRNXFILE-PROC"
    reachable: true
    performs: []
    goto_targets:
      - "1900-EXIT"
    summary: "TRNXFILE handler; three mutually exclusive IF blocks for OPEN, CLOSE, and READ/READ-K operations on TRNXFILE; each block ends with GO TO 1900-EXIT as an early-return short-circuit"

  - name: "1900-EXIT"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Common exit for TRNXFILE handler; copies TRNXFILE-STATUS into LK-M03B-RC; landing target for all GO TO 1900-EXIT sites in 1000-TRNXFILE-PROC"

  - name: "1999-EXIT"
    reachable: true
    performs: []
    goto_targets: []
    summary: "PERFORM THRU sentinel for TRNXFILE handler block; contains only EXIT; marks the end of the 1000 THRU 1999 range"

  - name: "2000-XREFFILE-PROC"
    reachable: true
    performs: []
    goto_targets:
      - "2900-EXIT"
    summary: "XREFFILE handler; three mutually exclusive IF blocks for OPEN, CLOSE, and READ/READ-K operations on XREFFILE; each block ends with GO TO 2900-EXIT as an early-return short-circuit"

  - name: "2900-EXIT"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Common exit for XREFFILE handler; copies XREFFILE-STATUS into LK-M03B-RC; landing target for all GO TO 2900-EXIT sites in 2000-XREFFILE-PROC"

  - name: "2999-EXIT"
    reachable: true
    performs: []
    goto_targets: []
    summary: "PERFORM THRU sentinel for XREFFILE handler block; contains only EXIT; marks the end of the 2000 THRU 2999 range"

  - name: "3000-CUSTFILE-PROC"
    reachable: true
    performs: []
    goto_targets:
      - "3900-EXIT"
    summary: "CUSTFILE handler; three mutually exclusive IF blocks for OPEN, CLOSE, and READ/READ-K operations on CUSTFILE; each block ends with GO TO 3900-EXIT as an early-return short-circuit"

  - name: "3900-EXIT"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Common exit for CUSTFILE handler; copies CUSTFILE-STATUS into LK-M03B-RC; landing target for all GO TO 3900-EXIT sites in 3000-CUSTFILE-PROC"

  - name: "3999-EXIT"
    reachable: true
    performs: []
    goto_targets: []
    summary: "PERFORM THRU sentinel for CUSTFILE handler block; contains only EXIT; marks the end of the 3000 THRU 3999 range"

  - name: "4000-ACCTFILE-PROC"
    reachable: true
    performs: []
    goto_targets:
      - "4900-EXIT"
    summary: "ACCTFILE handler; three mutually exclusive IF blocks for OPEN, CLOSE, and READ/READ-K operations on ACCTFILE; each block ends with GO TO 4900-EXIT as an early-return short-circuit"

  - name: "4900-EXIT"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Common exit for ACCTFILE handler; copies ACCTFILE-STATUS into LK-M03B-RC; landing target for all GO TO 4900-EXIT sites in 4000-ACCTFILE-PROC"

  - name: "4999-EXIT"
    reachable: true
    performs: []
    goto_targets: []
    summary: "PERFORM THRU sentinel for ACCTFILE handler block; contains only EXIT; marks the end of the 4000 THRU 4999 range"

  - name: "9999-GOBACK"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Program termination paragraph; executes GOBACK to return control to CBSTM03A; also the landing target for the WHEN OTHER GO TO in 0000-START"

goto_acceptance:
  rationale: "Common-exit early-return idiom (Cobol-REKT RC8); all targets are forward-only, single-label, structured early-returns — no backward jumps, no arbitrary labels"
  targets:
    - "1900-EXIT"
    - "2900-EXIT"
    - "3900-EXIT"
    - "4900-EXIT"
    - "9999-GOBACK"

business_rules:
  - id: "BR-001"
    rule: "LK-M03B-DD determines which file handler executes; an unrecognised DD name causes an immediate GO TO 9999-GOBACK without setting LK-M03B-RC, returning an indeterminate status to the caller"
    source_paragraph: "0000-START"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-002"
    rule: "WRITE and REWRITE operation codes are declared in the LK-M03B-OPER 88-level list but have no handler branches in any of the four file processor paragraphs; callers requesting these operations receive an indeterminate LK-M03B-RC"
    source_paragraph: "1000-TRNXFILE-PROC"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-003"
    rule: "Each file handler copies its own per-file FILE STATUS variable into LK-M03B-RC at the N900-EXIT paragraph, providing the caller a uniform two-character status regardless of which file was accessed"
    source_paragraph: "1900-EXIT"
    rule_type: "transform"
    confidence: "high"
    reachable: true

  - id: "BR-004"
    rule: "TRNXFILE and XREFFILE use SEQUENTIAL access; only sequential READ is meaningful — READ-K with a key buffer is declared but will receive an access-mode error status if attempted on these files"
    source_paragraph: "1000-TRNXFILE-PROC"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-005"
    rule: "CUSTFILE and ACCTFILE use RANDOM access; keyed READ-K operations are the primary read path; sequential READ may be attempted but is not the intended access pattern"
    source_paragraph: "3000-CUSTFILE-PROC"
    rule_type: "guard"
    confidence: "high"
    reachable: true

validation:
  t01_schema_valid: true
  t02_structural_complete: true
  t02r_redefines_complete: true
  t03_functional_score: null
  t04_semantic_score: null
  t05_regression_pass: null
  overall: "PASS"
---

# CBSTM03B — File Access Service Module

## Role

CBSTM03B is a file-access service module invoked via COBOL `CALL` by CBSTM03A with a
1050-byte `LK-M03B-AREA` linkage parameter. It dispatches on the DD name
(`TRNXFILE` / `XREFFILE` / `CUSTFILE` / `ACCTFILE`) to one of four handler paragraphs,
each supporting OPEN, CLOSE, READ, and READ-K operations on its respective VSAM KSDS file.

## Invocation Contract

`LK-M03B-AREA` layout (1050 bytes):

| Field | PIC | Purpose |
|---|---|---|
| `LK-M03B-DD` | X(08) | File selector — matches a DD name |
| `LK-M03B-OPER` | X(01) | Operation code (88-levels: OPEN/CLOSE/READ/READ-K/WRITE/REWRITE) |
| `LK-M03B-RC` | X(02) | Returned FILE STATUS written at N900-EXIT |
| `LK-M03B-KEY` | X(25) | Key buffer used by READ-K |
| `LK-M03B-KEY-LN` | S9(4) | Key length |
| `LK-M03B-FLDT` | X(1000) | Record buffer — populated on READ/READ-K |

WRITE and REWRITE are declared in the 88-level list but have no handler branches; callers
requesting them receive an indeterminate `LK-M03B-RC` (BR-002).

## Control Flow

14 paragraphs. `0000-START` evaluates `LK-M03B-DD` and dispatches via `PERFORM THRU`:

- `'TRNXFILE'` → `PERFORM 1000-TRNXFILE-PROC THRU 1999-EXIT`
- `'XREFFILE'` → `PERFORM 2000-XREFFILE-PROC THRU 2999-EXIT`
- `'CUSTFILE'` → `PERFORM 3000-CUSTFILE-PROC THRU 3999-EXIT`
- `'ACCTFILE'` → `PERFORM 4000-ACCTFILE-PROC THRU 4999-EXIT`
- `WHEN OTHER` → `GO TO 9999-GOBACK`

Each handler uses three mutually exclusive IF blocks ending `GO TO N900-EXIT` as an
early-return short-circuit. Each N900-EXIT paragraph copies the per-file FILE STATUS
into `LK-M03B-RC`. Each N999-EXIT is a `PERFORM THRU` sentinel (`EXIT.`).

## GO TO Suppression Rationale (Cobol-REKT RC8)

All 5 GO TO sites fit the common-exit early-return idiom — forward-only, single-label,
structured early-returns; no backward jumps; no arbitrary labels. Accepted under RC8.

| Source | Target | Count |
|---|---|---|
| `0000-START` WHEN OTHER | `9999-GOBACK` | 1 |
| `1000-TRNXFILE-PROC` | `1900-EXIT` | 3 |
| `2000-XREFFILE-PROC` | `2900-EXIT` | 3 |
| `3000-CUSTFILE-PROC` | `3900-EXIT` | 3 |
| `4000-ACCTFILE-PROC` | `4900-EXIT` | 3 |

## Files

| DD | Organization | Access | Record Key | CRUD |
|---|---|---|---|---|
| TRNXFILE | INDEXED | SEQUENTIAL | FD-TRNXS-ID | READ |
| XREFFILE | INDEXED | SEQUENTIAL | FD-XREF-CARD-NUM | READ |
| CUSTFILE | INDEXED | RANDOM | FD-CUST-ID | READ |
| ACCTFILE | INDEXED | RANDOM | FD-ACCT-ID | READ |

## Translation Targets

- `EVALUATE LK-M03B-DD` → language-native switch/match on file selector enum
- `IF M03B-OPEN / M03B-CLOSE / M03B-READ / M03B-READ-K` → boolean check on parsed operation enum
- `GO TO N900-EXIT` → early return / labeled break to status-assignment block
- `PERFORM N000 THRU N999` → function call scoped to the handler block
- Per-file FILE STATUS variables → per-file status accessor, propagated to return struct via `LK-M03B-RC`
