---
schema_version: "cobol-md/1.0"
program_id: "CBSTM03A"
source_file: "app/cbl/CBSTM03A.cbl"
source_sha: "290c3f4a9c51e1f9aa5bb180237dfbeb1d02b26a"
translation_date: "2026-05-05"
translating_agent: "claude-sonnet-4.6"
aifirst_task_id: "T-2026-05-05-003"
cfg_source: "validation/structure/CBSTM03A_cfg.json"

business_domain: "Account Statement Generation"
subtype: "Batch"

author: "AWS"
date_written: null
lines_of_code: 924
divisions:
  identification: true
  environment: true
  data: true
  procedure: true
environment:
  compiler: "IBM Enterprise COBOL"
  target: "Batch/VSAM"
  runtime: "z/OS"

calls_to:
  - program: "CBSTM03B"
    call_type: "STATIC"
    condition: "file operations (open, close, read, read-key) on TRNXFILE/XREFFILE/CUSTFILE/ACCTFILE"

called_by: []

copybooks_used:
  - "COSTM01"
  - "CVACT03Y"
  - "CUSTREC"
  - "CVACT01Y"

file_control:
  - ddname: "STMTFILE"
    organization: "SEQUENTIAL"
    access: "OUTPUT"
    record_length: 80
    crud: ["WRITE"]
  - ddname: "HTMLFILE"
    organization: "SEQUENTIAL"
    access: "OUTPUT"
    record_length: 100
    crud: ["WRITE"]

cics_commands: []
transaction_ids: []

data_items:
  - name: "FD-STMTFILE-REC"
    level: 01
    picture: X(80)
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "File descriptor record for STMTFILE; 80-byte sequential output for plain text statements"

  - name: "FD-HTMLFILE-REC"
    level: 01
    picture: X(100)
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "File descriptor record for HTMLFILE; 100-byte sequential output for HTML statements"

  - name: "COMP-VARIABLES"
    level: 01
    picture: null
    usage: COMP
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Binary COMP variables for counters: CR-CNT (card count), TR-CNT (transaction count), CR-JMP, TR-JMP (loop indices)"

  - name: "COMP3-VARIABLES"
    level: 01
    picture: S9(9)V99
    usage: COMP-3
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "PACKED-DECIMAL COMP-3 variable: WS-TOTAL-AMT for accumulating transaction totals"

  - name: "MISC-VARIABLES"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Miscellaneous working variables: WS-FL-DD (file selector), WS-TRN-AMT, WS-SAVE-CARD, END-OF-FILE flag"

  - name: "WS-M03B-AREA"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "1050-byte working storage area passed to CBSTM03B: DD selector, operation code with 88-levels, return code, key buffer, key length, record buffer"

  - name: "STATEMENT-LINES"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Statement output format definitions: header/footer lines, account details, transaction summary lines"

  - name: "HTML-LINES"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "HTML output format definitions: DOCTYPE, table layout, fixed lines, address/name/transaction lines"

  - name: "WS-TRNX-TABLE"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-dimensional array (51 cards x 10 transactions) for in-memory transaction buffering"

  - name: "WS-TRN-TBL-CNTR"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Counter array tracking transaction count per card in WS-TRNX-TABLE"

  - name: "PSAPTR"
    level: 01
    picture: null
    usage: POINTER
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Pointer to PSA (Program Security Area) for system control block access"

  - name: "BUMP-TIOT"
    level: 01
    picture: S9(08)
    usage: BINARY
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Binary counter for TIOT (Task Information Output Table) traversal"

  - name: "TIOT-INDEX"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: BUMP-TIOT
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Pointer redefinition of BUMP-TIOT for TIOT entry address calculation"

  - name: "TIOT-ENTRY"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "TIOT entry structure: segment, job name, step name, program step, DD name, UCB address"

  - name: "ALIGN-PSA"
    level: 01
    picture: 9(16)
    usage: BINARY
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "LINKAGE SECTION: 16-byte binary alignment variable for PSA pointer setup"

  - name: "PSA-BLOCK"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "LINKAGE SECTION: 536-byte PSA area + TCB-POINT pointer for system control block access"

  - name: "TCB-BLOCK"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "LINKAGE SECTION: 12-byte TCB area + TIOT-POINT pointer for task control block access"

  - name: "TIOT-BLOCK"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "LINKAGE SECTION: 24-byte TIOT structure (job name + step name + program step) for DD name enumeration"

procedure_paragraphs:
  - name: "0000-START"
    reachable: true
    performs:
      - "1000-MAINLINE"
    goto_targets:
      - "1000-MAINLINE"
    summary: "Entry point; EVALUATE on WS-FL-DD dispatches to appropriate file operation via ALTER/GO TO constructs; WHEN OTHER falls through to GO TO 9999-GOBACK"

  - name: "1000-MAINLINE"
    reachable: true
    performs:
      - "9999-GOBACK"
      - "9400-ACCTFILE-CLOSE"
      - "9300-CUSTFILE-CLOSE"
      - "9200-XREFFILE-CLOSE"
      - "9100-TRNXFILE-CLOSE"
      - "4000-TRNXFILE-GET"
      - "5000-CREATE-STATEMENT"
      - "3000-ACCTFILE-GET"
      - "2000-CUSTFILE-GET"
      - "1000-XREFFILE-GET-NEXT"
    goto_targets: []
    summary: "Main processing loop; reads XREFFILE, CUSTFILE, ACCTFILE, creates statements, reads TRNXFILE transactions; loops until END-OF-FILE='Y'"

  - name: "1000-XREFFILE-GET-NEXT"
    reachable: true
    performs:
      - "2000-CUSTFILE-GET"
    goto_targets: []
    summary: "Reads next record from XREFFILE; sets END-OF-FILE='Y' on RC=10; DISPLAY error and ABEND on other RC"

  - name: "2000-CUSTFILE-GET"
    reachable: true
    performs:
      - "3000-ACCTFILE-GET"
    goto_targets: []
    summary: "Reads customer record from CUSTFILE using XREF-CUST-ID as key; DISPLAY error and ABEND on non-zero RC"

  - name: "3000-ACCTFILE-GET"
    reachable: true
    performs:
      - "4000-TRNXFILE-GET"
    goto_targets: []
    summary: "Reads account record from ACCTFILE using XREF-ACCT-ID as key; DISPLAY error and ABEND on non-zero RC"

  - name: "4000-TRNXFILE-GET"
    reachable: true
    performs:
      - "5000-CREATE-STATEMENT"
      - "6000-WRITE-TRANS"
    goto_targets: []
    summary: "Iterates through WS-TRNX-TABLE for current card; writes transaction records to STMTFILE and HTMLFILE"

  - name: "5000-CREATE-STATEMENT"
    reachable: true
    performs:
      - "5100-WRITE-HTML-HEADER"
      - "5200-WRITE-HTML-NMADBS"
      - "5200-EXIT"
      - "5100-EXIT"
    goto_targets: []
    summary: "Creates plain text statement header and writes to STMTFILE; calls HTML header and name/address sections"

  - name: "5100-EXIT"
    reachable: true
    performs:
      - "5200-WRITE-HTML-NMADBS"
    goto_targets: []
    summary: "Exit from HTML header section; calls name/address section writer"

  - name: "5100-WRITE-HTML-HEADER"
    reachable: true
    performs:
      - "5100-EXIT"
    goto_targets: []
    summary: "Writes complete HTML document header (DOCTYPE through table layout); writes account identifier line"

  - name: "5200-EXIT"
    reachable: true
    performs:
      - "6000-WRITE-TRANS"
    goto_targets: []
    summary: "Exit from HTML name/address section; calls transaction writer"

  - name: "5200-WRITE-HTML-NMADBS"
    reachable: true
    performs:
      - "5200-EXIT"
    goto_targets: []
    summary: "Writes HTML name, address, basic details, and transaction summary sections to HTMLFILE"

  - name: "6000-WRITE-TRANS"
    reachable: true
    performs:
      - "8100-FILE-OPEN"
    goto_targets: []
    summary: "Writes single transaction line to STMTFILE and HTMLFILE; calls 8100-FILE-OPEN for next operation"

  - name: "8100-FILE-OPEN"
    reachable: true
    performs:
      - "8100-TRNXFILE-OPEN"
    goto_targets:
      - "8100-TRNXFILE-OPEN"
    summary: "ALTER dispatch target; GO TO 8100-TRNXFILE-OPEN; used by ALTER statements in 0000-START"

  - name: "8100-TRNXFILE-OPEN"
    reachable: true
    performs:
      - "8200-XREFFILE-OPEN"
      - "0000-START"
      - "9999-ABEND-PROGRAM"
    goto_targets:
      - "0000-START"
    summary: "TRNXFILE OPEN handler; calls CBSTM03B; GO TO 0000-START after OPEN/READ to continue processing"

  - name: "8200-XREFFILE-OPEN"
    reachable: true
    performs:
      - "8300-CUSTFILE-OPEN"
      - "0000-START"
      - "9999-ABEND-PROGRAM"
    goto_targets:
      - "0000-START"
    summary: "XREFFILE OPEN handler; calls CBSTM03B; GO TO 0000-START after OPEN to continue processing"

  - name: "8300-CUSTFILE-OPEN"
    reachable: true
    performs:
      - "8400-ACCTFILE-OPEN"
      - "0000-START"
      - "9999-ABEND-PROGRAM"
    goto_targets:
      - "0000-START"
    summary: "CUSTFILE OPEN handler; calls CBSTM03B; GO TO 0000-START after OPEN to continue processing"

  - name: "8400-ACCTFILE-OPEN"
    reachable: true
    performs:
      - "8500-READTRNX-READ"
      - "1000-MAINLINE"
      - "9999-ABEND-PROGRAM"
    goto_targets:
      - "1000-MAINLINE"
    summary: "ACCTFILE OPEN handler; calls CBSTM03B; GO TO 1000-MAINLINE after OPEN to begin main processing"

  - name: "8500-READTRNX-READ"
    reachable: true
    performs:
      - "8599-EXIT"
    goto_targets:
      - "8599-EXIT"
    summary: "TRNXFILE sequential read loop; groups transactions by card in WS-TRNX-TABLE; GO TO 0000-START after buffering"

  - name: "8599-EXIT"
    reachable: true
    performs:
      - "9100-TRNXFILE-CLOSE"
      - "0000-START"
    goto_targets:
      - "0000-START"
    summary: "TRNXFILE read loop exit; updates last card counter; GO TO 0000-START to switch to XREFFILE"

  - name: "9100-TRNXFILE-CLOSE"
    reachable: true
    performs:
      - "9200-XREFFILE-CLOSE"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Closes TRNXFILE via CBSTM03B; DISPLAY error and ABEND on non-zero RC"

  - name: "9200-XREFFILE-CLOSE"
    reachable: true
    performs:
      - "9300-CUSTFILE-CLOSE"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Closes XREFFILE via CBSTM03B; DISPLAY error and ABEND on non-zero RC"

  - name: "9300-CUSTFILE-CLOSE"
    reachable: true
    performs:
      - "9400-ACCTFILE-CLOSE"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Closes CUSTFILE via CBSTM03B; DISPLAY error and ABEND on non-zero RC"

  - name: "9400-ACCTFILE-CLOSE"
    reachable: true
    performs:
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Closes ACCTFILE via CBSTM03B; DISPLAY error and ABEND on non-zero RC"

  - name: "9999-ABEND-PROGRAM"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Program abend handler; DISPLAY 'ABENDING PROGRAM' and CALL CEE3ABD to terminate"

  - name: "9999-GOBACK"
    reachable: true
    performs:
      - "1000-XREFFILE-GET-NEXT"
    goto_targets: []
    summary: "Program termination; executes GOBACK to return control to caller"

goto_acceptance:
  rationale: "ALTER/GO TO dispatch pattern (Cobol-REKT RC8); all targets are forward-only, single-label, structured control flow — no backward jumps, no arbitrary labels"
  targets:
    - "8100-TRNXFILE-OPEN"
    - "8200-XREFFILE-OPEN"
    - "8300-CUSTFILE-OPEN"
    - "8400-ACCTFILE-OPEN"
    - "8599-EXIT"
    - "0000-START"
    - "9999-GOBACK"
    - "1000-MAINLINE"

business_rules:
  - id: "BR-001"
    rule: "WS-FL-DD determines dispatch path: TRNXFILE/XREFFILE/CUSTFILE/ACCTFILE/READTRNX dispatch to respective handlers; unknown values fall through to GO TO 9999-GOBACK"
    source_paragraph: "0000-START"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-002"
    rule: "ALTER statements redirect GO TO 8100-FILE-OPEN to specific file handler paragraphs based on WS-FL-DD value"
    source_paragraph: "0000-START"
    rule_type: "control"
    confidence: "high"
    reachable: true

  - id: "BR-003"
    rule: "Transaction buffering in WS-TRNX-TABLE groups transactions by card (51 cards x 10 transactions max); 8500-READTRNX-READ accumulates until card changes"
    source_paragraph: "8500-READTRNX-READ"
    rule_type: "transform"
    confidence: "high"
    reachable: true

  - id: "BR-004"
    rule: "Statement generation writes two outputs: STMTFILE (plain text) and HTMLFILE (HTML table format); both contain identical transaction data"
    source_paragraph: "5000-CREATE-STATEMENT"
    rule_type: "output"
    confidence: "high"
    reachable: true

  - id: "BR-005"
    rule: "Main loop (1000-MAINLINE) processes all records until END-OF-FILE='Y'; closes all files and GOBACKs at loop exit"
    source_paragraph: "1000-MAINLINE"
    rule_type: "control"
    confidence: "high"
    reachable: true

validation:
  t01_schema_valid: true
  t02_structural_complete: true
  t02r_redefines_complete: true
  t03_functional_score: null
  t04_semantic_score: null
  t05_regression_pass: null
  overall: "PENDING"
---

# CBSTM03A — Account Statement Generation Program

## Role

CBSTM03A is a batch COBOL program that generates account statements from transaction data in two formats:
plain text (STMTFILE) and HTML (HTMLFILE). It reads card cross-reference data, customer records, account
records, and transaction data to build formatted statements for each account.

## Control Flow

25 paragraphs organized in functional groups:

### Entry and Dispatch (0000-START)
EVALUATE on `WS-FL-DD` dispatches to appropriate file handler via `ALTER`/`GO TO` constructs:
- `'TRNXFILE'` → GO TO 8100-FILE-OPEN → 8100-TRNXFILE-OPEN
- `'XREFFILE'` → GO TO 8100-FILE-OPEN → 8200-XREFFILE-OPEN
- `'CUSTFILE'` → GO TO 8100-FILE-OPEN → 8300-CUSTFILE-OPEN
- `'ACCTFILE'` → GO TO 8100-FILE-OPEN → 8400-ACCTFILE-OPEN
- `'READTRNX'` → GO TO 8500-READTRNX-READ
- `WHEN OTHER` → GO TO 9999-GOBACK

### Main Processing (1000-MAINLINE)
Loop until `END-OF-FILE='Y'`:
1. Read XREFFILE → 1000-XREFFILE-GET-NEXT
2. Read CUSTFILE → 2000-CUSTFILE-GET
3. Read ACCTFILE → 3000-ACCTFILE-GET
4. Create statement → 5000-CREATE-STATEMENT
5. Process transactions → 4000-TRNXFILE-GET

### File Operations (8100-8400, 9100-9400)
Each file handler calls CBSTM03B with `WS-M03B-AREA`:
- OPEN: set M03B-OPEN, CALL CBSTM03B, GO TO 0000-START or 1000-MAINLINE
- READ: set M03B-READ, CALL CBSTM03B, loop until RC=10 (EOF)
- CLOSE: set M03B-CLOSE, CALL CBSTM03B, GO TO next close

### Statement Generation (5000, 5100, 5200)
- 5000: Initialize statement lines, write header to STMTFILE
- 5100: Write HTML header (DOCTYPE through table layout)
- 5200: Write HTML name/address/basic details/transaction summary

### Transaction Writing (6000)
Writes single transaction to both STMTFILE (plain text) and HTMLFILE (table row)

## GO TO Suppression Rationale (Cobol-REKT RC8)

ALTER/GO TO pattern for file dispatch is accepted under RC8:
- Forward-only jumps only
- Single-label targets
- Structured control flow (no arbitrary labels)

| Source | Target | Count |
|---|---|---|
| `0000-START` WHEN OTHER | `9999-GOBACK` | 1 |
| `0000-START` TRNXFILE | `8100-TRNXFILE-OPEN` | 1 |
| `0000-START` XREFFILE | `8200-XREFFILE-OPEN` | 1 |
| `0000-START` CUSTFILE | `8300-CUSTFILE-OPEN` | 1 |
| `0000-START` ACCTFILE | `8400-ACCTFILE-OPEN` | 1 |
| `8500-READTRNX-READ` | `8599-EXIT` | 1 |

## Files

| DD | Organization | Access | Record Length | CRUD |
|---|---|---|---|---|
| STMTFILE | SEQUENTIAL | OUTPUT | 80 | WRITE |
| HTMLFILE | SEQUENTIAL | OUTPUT | 100 | WRITE |

## Translation Targets

- `EVALUATE WS-FL-DD` → language-native switch/match on file selector enum
- `ALTER`/`GO TO` → dispatch table or switch statement
- `CALL 'CBSTM03B'` → function call to file access module
- `SET M03B-OPEN/CLOSE/READ/READ-K` → boolean flags on parsed operation enum
- `PERFORM UNTIL` → while loop with END-OF-FILE condition
- Two-dimensional WS-TRNX-TABLE → nested arrays or map of card→transactions