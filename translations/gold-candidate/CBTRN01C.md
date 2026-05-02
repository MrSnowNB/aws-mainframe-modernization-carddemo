---
# ── Identity ───────────────────────────────────────────────────────────────────
schema_version: "cobol-md/1.0"
program_id: "CBTRN01C"
source_file: "app/cbl/CBTRN01C.cbl"
source_sha: "6494be3b695bd33f27b39f8d13dc5b510f92b7ed"
translation_date: "2026-04-23"
translating_agent: "claude-opus-4-5 (subagent)"
aifirst_task_id: "T-2026-04-23-001"
cfg_source: "validation/structure/CBTRN01C_cfg.json"

# ── Classification ─────────────────────────────────────────────────────────────
business_domain: "Transaction Processing"
subtype: "Batch"

# ── Structural Metadata ────────────────────────────────────────────────────────
author: "AWS"
date_written: null
lines_of_code: 340
divisions:
  identification: true
  environment: true
  data: true
  procedure: true
environment:
  compiler: "IBM Enterprise COBOL"
  target: "Batch/VSAM"
  runtime: "z/OS"

# ── Graph Edges ────────────────────────────────────────────────────────────────
calls_to:
  - program: "CEE3ABD"
    condition: "Unrecoverable I/O error detected on any file open, read, or close operation"
    call_type: "STATIC"

called_by: []

copybooks_used:
  - name: "CVTRA06Y"
    path: "app/cpy/CVTRA06Y.cpy"
    sha: null
  - name: "CVCUS01Y"
    path: "app/cpy/CVCUS01Y.cpy"
    sha: null
  - name: "CVACT03Y"
    path: "app/cpy/CVACT03Y.cpy"
    sha: null
  - name: "CVACT02Y"
    path: "app/cpy/CVACT02Y.cpy"
    sha: null
  - name: "CVACT01Y"
    path: "app/cpy/CVACT01Y.cpy"
    sha: null
  - name: "CVTRA05Y"
    path: "app/cpy/CVTRA05Y.cpy"
    sha: null

# ── File I/O ───────────────────────────────────────────────────────────────────
file_control:
  - ddname: "DALYTRAN"
    organization: "SEQUENTIAL"
    access: "SEQUENTIAL"
    record_key: null
    crud: ["READ"]
  - ddname: "CUSTFILE"
    organization: "INDEXED"
    access: "RANDOM"
    record_key: "FD-CUST-ID"
    crud: ["READ"]
  - ddname: "XREFFILE"
    organization: "INDEXED"
    access: "RANDOM"
    record_key: "FD-XREF-CARD-NUM"
    crud: ["READ"]
  - ddname: "CARDFILE"
    organization: "INDEXED"
    access: "RANDOM"
    record_key: "FD-CARD-NUM"
    crud: ["READ"]
  - ddname: "ACCTFILE"
    organization: "INDEXED"
    access: "RANDOM"
    record_key: "FD-ACCT-ID"
    crud: ["READ"]
  - ddname: "TRANFILE"
    organization: "INDEXED"
    access: "RANDOM"
    record_key: "FD-TRANS-ID"
    crud: ["READ"]

# ── CICS ───────────────────────────────────────────────────────────────────────
cics_commands: []
transaction_ids: []

# ── Data Layer ─────────────────────────────────────────────────────────────────
data_items:
  # File Section — DALYTRAN-FILE (daily transaction sequential input)
  - name: "FD-TRAN-RECORD"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Root record layout for the daily transaction sequential input file; contains a 16-character transaction identifier followed by 334 bytes of payload data"

  # File Section — CUSTOMER-FILE (customer VSAM indexed)
  - name: "FD-CUSTFILE-REC"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Root record layout for the customer VSAM indexed file; primary key is a 9-digit numeric customer identifier"

  # File Section — XREF-FILE (card cross-reference VSAM indexed)
  - name: "FD-XREFFILE-REC"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Root record layout for the card-to-account cross-reference VSAM indexed file; primary key is the 16-character card number"

  # File Section — CARD-FILE (card VSAM indexed)
  - name: "FD-CARDFILE-REC"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Root record layout for the card detail VSAM indexed file; primary key is the 16-character card number"

  # File Section — ACCOUNT-FILE (account VSAM indexed)
  - name: "FD-ACCTFILE-REC"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Root record layout for the account VSAM indexed file; primary key is an 11-digit numeric account identifier"

  # File Section — TRANSACT-FILE (transaction VSAM indexed)
  - name: "FD-TRANFILE-REC"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Root record layout for the posted-transaction VSAM indexed file; primary key is a 16-character transaction identifier"

  # Working Storage — file status areas
  - name: "DALYTRAN-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file status code returned by the operating system after each I/O operation on the daily transaction sequential file"

  - name: "CUSTFILE-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file status code for the customer VSAM indexed file; populated after every open, read, and close"

  - name: "XREFFILE-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file status code for the card cross-reference VSAM indexed file; used to detect invalid-key conditions during random reads"

  - name: "CARDFILE-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file status code for the card detail VSAM indexed file"

  - name: "ACCTFILE-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file status code for the account VSAM indexed file; used to detect invalid-key conditions during random account reads"

  - name: "TRANFILE-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file status code for the posted-transaction VSAM indexed file"

  - name: "IO-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Staging area that holds the file status code from the most recently failed I/O operation before it is formatted and displayed by Z-DISPLAY-IO-STATUS"

  # REDEFINES pair — binary integer vs. two-byte character overlay
  - name: "TWO-BYTES-BINARY"
    level: 01
    picture: "9(4)"
    usage: "BINARY"
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-byte binary integer workspace used to convert a single file-status character (IO-STAT2) into a displayable three-digit decimal number for non-standard status codes"

  - name: "TWO-BYTES-ALPHA"
    level: 01
    picture: null
    usage: "BINARY"
    value: null
    redefines: "TWO-BYTES-BINARY"
    redefines_interpretations:
      - condition: "IO-STAT1 = '9' (non-numeric, vendor-specific file status in IO-STATUS)"
        interpreted_as: "Two single-character fields (TWO-BYTES-LEFT and TWO-BYTES-RIGHT) overlaying the same two bytes; IO-STAT2 is moved into TWO-BYTES-RIGHT so that TWO-BYTES-BINARY can be read as an integer for display"
        encoding: "DISPLAY"
      - condition: "IO-STATUS is numeric and IO-STAT1 is not '9' (standard ANSI file status)"
        interpreted_as: "The two bytes are treated as a packed integer holding the numeric file status value, allowing it to be extracted and moved into the three-digit display field IO-STATUS-0403"
        encoding: "BINARY"
    dead_code_flag: false
    semantic: "Character overlay of TWO-BYTES-BINARY; exposes left and right byte positions independently so that non-numeric file status codes can be decomposed and converted to a printable four-character diagnostic string"

  - name: "IO-STATUS-04"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Four-character formatted I/O status diagnostic buffer composed of a one-digit severity prefix (IO-STATUS-0401) and a three-digit numeric status code (IO-STATUS-0403); displayed to the operator on error"

  - name: "APPL-RESULT"
    level: 01
    picture: "S9(9)"
    usage: "COMP"
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Signed 9-digit binary application return code set after each file operation; condition name APPL-AOK (value 0) signals success, APPL-EOF (value 16) signals end-of-file, and any other non-zero value triggers abend"

  - name: "END-OF-DAILY-TRANS-FILE"
    level: 01
    picture: "X(01)"
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Single-character end-of-file sentinel; initialized to 'N' and set to 'Y' when the daily transaction file returns a status-10 (end-of-file) condition, terminating the main processing loop"

  - name: "ABCODE"
    level: 01
    picture: "S9(9)"
    usage: "BINARY"
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Abend code passed to the Language Environment CEE3ABD service; set to 999 before the abnormal termination call"

  - name: "TIMING"
    level: 01
    picture: "S9(9)"
    usage: "BINARY"
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Timing parameter passed to CEE3ABD alongside ABCODE; set to 0 (immediate abend) before each abnormal termination call"

  - name: "WS-MISC-VARIABLES"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Group item holding runtime read-status accumulators for the cross-reference and account file lookups; used to gate downstream processing within the main transaction loop"

# ── Procedure Paragraphs ───────────────────────────────────────────────────────
procedure_paragraphs:
  - name: "MAIN-PARA"
    reachable: true
    performs:
      - "0000-DALYTRAN-OPEN"
      - "0100-CUSTFILE-OPEN"
      - "0200-XREFFILE-OPEN"
      - "0300-CARDFILE-OPEN"
      - "0400-ACCTFILE-OPEN"
      - "0500-TRANFILE-OPEN"
      - "1000-DALYTRAN-GET-NEXT"
      - "2000-LOOKUP-XREF"
      - "3000-READ-ACCOUNT"
      - "9000-DALYTRAN-CLOSE"
      - "9100-CUSTFILE-CLOSE"
      - "9200-XREFFILE-CLOSE"
      - "9300-CARDFILE-CLOSE"
      - "9400-ACCTFILE-CLOSE"
      - "9500-TRANFILE-CLOSE"
      - "Z-DISPLAY-IO-STATUS"
      - "Z-ABEND-PROGRAM"
    goto_targets: []
    summary: "Program entry point that opens all six files, drives the sequential read-validate loop over the daily transaction file, and closes all files before returning control to the operating system via GOBACK"

  - name: "1000-DALYTRAN-GET-NEXT"
    reachable: true
    performs:
      - "Z-DISPLAY-IO-STATUS"
      - "Z-ABEND-PROGRAM"
    goto_targets: []
    summary: "Reads the next record from the daily transaction sequential file into working storage, sets APPL-RESULT to reflect success, end-of-file, or error, and abends on any unexpected I/O failure"

  - name: "2000-LOOKUP-XREF"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Performs a random keyed read of the card cross-reference VSAM file using the card number from the current transaction record, setting WS-XREF-READ-STATUS to 4 if the card number is not found"

  - name: "3000-READ-ACCOUNT"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Performs a random keyed read of the account VSAM file using the account identifier resolved from the cross-reference record, setting WS-ACCT-READ-STATUS to 4 if the account is not found"

  - name: "0000-DALYTRAN-OPEN"
    reachable: true
    performs:
      - "Z-DISPLAY-IO-STATUS"
      - "Z-ABEND-PROGRAM"
    goto_targets: []
    summary: "Opens the daily transaction sequential file for input and abends the program if the open fails"

  - name: "0100-CUSTFILE-OPEN"
    reachable: true
    performs:
      - "Z-DISPLAY-IO-STATUS"
      - "Z-ABEND-PROGRAM"
    goto_targets: []
    summary: "Opens the customer VSAM indexed file for input and abends the program if the open fails"

  - name: "0200-XREFFILE-OPEN"
    reachable: true
    performs:
      - "Z-DISPLAY-IO-STATUS"
      - "Z-ABEND-PROGRAM"
    goto_targets: []
    summary: "Opens the card cross-reference VSAM indexed file for input and abends the program if the open fails"

  - name: "0300-CARDFILE-OPEN"
    reachable: true
    performs:
      - "Z-DISPLAY-IO-STATUS"
      - "Z-ABEND-PROGRAM"
    goto_targets: []
    summary: "Opens the card detail VSAM indexed file for input and abends the program if the open fails"

  - name: "0400-ACCTFILE-OPEN"
    reachable: true
    performs:
      - "Z-DISPLAY-IO-STATUS"
      - "Z-ABEND-PROGRAM"
    goto_targets: []
    summary: "Opens the account VSAM indexed file for input and abends the program if the open fails"

  - name: "0500-TRANFILE-OPEN"
    reachable: true
    performs:
      - "Z-DISPLAY-IO-STATUS"
      - "Z-ABEND-PROGRAM"
    goto_targets: []
    summary: "Opens the posted-transaction VSAM indexed file for input and abends the program if the open fails"

  - name: "9000-DALYTRAN-CLOSE"
    reachable: true
    performs:
      - "Z-DISPLAY-IO-STATUS"
      - "Z-ABEND-PROGRAM"
    goto_targets: []
    summary: "Closes the daily transaction sequential file and abends the program if the close operation fails"

  - name: "9100-CUSTFILE-CLOSE"
    reachable: true
    performs:
      - "Z-DISPLAY-IO-STATUS"
      - "Z-ABEND-PROGRAM"
    goto_targets: []
    summary: "Closes the customer VSAM indexed file and abends the program if the close operation fails"

  - name: "9200-XREFFILE-CLOSE"
    reachable: true
    performs:
      - "Z-DISPLAY-IO-STATUS"
      - "Z-ABEND-PROGRAM"
    goto_targets: []
    summary: "Closes the card cross-reference VSAM indexed file and abends the program if the close operation fails"

  - name: "9300-CARDFILE-CLOSE"
    reachable: true
    performs:
      - "Z-DISPLAY-IO-STATUS"
      - "Z-ABEND-PROGRAM"
    goto_targets: []
    summary: "Closes the card detail VSAM indexed file and abends the program if the close operation fails"

  - name: "9400-ACCTFILE-CLOSE"
    reachable: true
    performs:
      - "Z-DISPLAY-IO-STATUS"
      - "Z-ABEND-PROGRAM"
    goto_targets: []
    summary: "Closes the account VSAM indexed file and abends the program if the close operation fails"

  - name: "9500-TRANFILE-CLOSE"
    reachable: true
    performs:
      - "Z-DISPLAY-IO-STATUS"
      - "Z-ABEND-PROGRAM"
    goto_targets: []
    summary: "Closes the posted-transaction VSAM indexed file and abends the program if the close operation fails"

  - name: "Z-ABEND-PROGRAM"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Sets ABCODE to 999 and TIMING to 0 then calls the Language Environment CEE3ABD service to force an abnormal termination with a user abend code, terminating the job step"

  - name: "Z-DISPLAY-IO-STATUS"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Formats the two-character IO-STATUS into a four-character printable diagnostic string (handling both numeric and non-numeric status codes) and displays it to the operator before an abend"

# ── Business Rules ─────────────────────────────────────────────────────────────
business_rules:
  - id: "BR-001"
    rule: "All six files (daily transaction, customer, cross-reference, card, account, and posted-transaction) must be successfully opened before any transaction processing begins; a failure on any file open triggers an immediate abend with CEE3ABD code 999"
    source_paragraph: "MAIN-PARA"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-002"
    rule: "The main processing loop continues reading and validating transaction records sequentially until the daily transaction file signals end-of-file, at which point the sentinel END-OF-DAILY-TRANS-FILE is set to 'Y' and the loop terminates"
    source_paragraph: "MAIN-PARA"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-003"
    rule: "Each transaction record read from the daily file is immediately displayed to the system log before any cross-reference lookup is performed, provided end-of-file has not been reached"
    source_paragraph: "MAIN-PARA"
    rule_type: "display"
    confidence: "high"
    reachable: true

  - id: "BR-004"
    rule: "The card number extracted from each daily transaction record must be validated against the card cross-reference VSAM file; if the card number is not found (WS-XREF-READ-STATUS is set to 4), the transaction is skipped with a diagnostic message and no account lookup is attempted"
    source_paragraph: "MAIN-PARA"
    rule_type: "lookup"
    confidence: "high"
    reachable: true

  - id: "BR-005"
    rule: "When a card number cannot be verified in the cross-reference file, a diagnostic message identifying the unverifiable card number and the skipped transaction identifier is written to the operator console, and the transaction record is abandoned without further processing"
    source_paragraph: "MAIN-PARA"
    rule_type: "audit"
    confidence: "high"
    reachable: true

  - id: "BR-006"
    rule: "Only when cross-reference lookup succeeds (WS-XREF-READ-STATUS equals zero) is the resolved account identifier used to perform a further lookup against the account VSAM file"
    source_paragraph: "MAIN-PARA"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-007"
    rule: "If the account record resolved through the cross-reference is not found in the account VSAM file (WS-ACCT-READ-STATUS is non-zero), a diagnostic message naming the missing account identifier is displayed, but no abend is triggered and processing continues with the next transaction"
    source_paragraph: "MAIN-PARA"
    rule_type: "audit"
    confidence: "high"
    reachable: true

  - id: "BR-008"
    rule: "A read of the daily transaction file that returns a status code other than '00' (success) or '10' (end-of-file) is treated as an unrecoverable I/O error: the status code is formatted and displayed, then CEE3ABD is called with abend code 999 to terminate the job"
    source_paragraph: "1000-DALYTRAN-GET-NEXT"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-009"
    rule: "A status code of '10' returned from the daily transaction file read is the only normal termination signal; it sets END-OF-DAILY-TRANS-FILE to 'Y', which causes the PERFORM UNTIL loop to exit cleanly"
    source_paragraph: "1000-DALYTRAN-GET-NEXT"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-010"
    rule: "When a random read of the cross-reference VSAM file returns INVALID KEY, the card number is flagged as unverifiable by setting WS-XREF-READ-STATUS to 4, and a diagnostic message is written to the console"
    source_paragraph: "2000-LOOKUP-XREF"
    rule_type: "lookup"
    confidence: "high"
    reachable: true

  - id: "BR-011"
    rule: "When a random read of the account VSAM file returns INVALID KEY, WS-ACCT-READ-STATUS is set to 4 and a diagnostic message is written to the console; the condition is non-fatal and processing resumes with the next record"
    source_paragraph: "3000-READ-ACCOUNT"
    rule_type: "lookup"
    confidence: "high"
    reachable: true

  - id: "BR-012"
    rule: "Any file open or close operation that does not return status '00' is mapped to APPL-RESULT value 12 (error), which causes Z-DISPLAY-IO-STATUS and Z-ABEND-PROGRAM to be called, terminating the job with abend code 999"
    source_paragraph: "0000-DALYTRAN-OPEN"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-013"
    rule: "Non-numeric file status codes (IO-STAT1 equal to '9') are decoded by overlaying TWO-BYTES-BINARY with TWO-BYTES-ALPHA so that the vendor-specific second byte can be converted to a displayable three-digit decimal before operator notification"
    source_paragraph: "Z-DISPLAY-IO-STATUS"
    rule_type: "transform"
    confidence: "high"
    reachable: true

# ── Validation Status ──────────────────────────────────────────────────────────
validation:
  t01_schema_valid: true
  t02_structural_complete: true
  t02r_redefines_complete: true
  t03_functional_score: null
  t04_semantic_score: null
  t05_regression_pass: null
  overall: "PASS"
---

# CBTRN01C — Daily Transaction File Processor and Cross-Reference Validator

## Purpose

CBTRN01C is a batch COBOL program in the CardDemo application that reads a daily transaction file sequentially and validates each transaction record against a set of VSAM reference files. For every incoming transaction, the program verifies that the card number can be resolved to an account via the card cross-reference file, and then confirms that the resolved account exists in the account master file. The program serves as the first-stage intake filter for the daily transaction posting pipeline, surfacing data-quality problems through operator console messages and aborting the job on unrecoverable I/O errors.

## Runtime Context

The program executes as a z/OS batch job step under IBM Enterprise COBOL with no CICS or DB2 involvement. It opens six VSAM or sequential files at startup — the daily transaction sequential input file (DALYTRAN), a customer indexed file (CUSTFILE), a card-to-account cross-reference indexed file (XREFFILE), a card detail indexed file (CARDFILE), an account indexed file (ACCTFILE), and a posted-transaction indexed file (TRANFILE) — performs all processing in memory, and closes all six files before returning. The program makes one outbound static call: to the Language Environment service CEE3ABD, which is invoked exclusively on unrecoverable error paths to force a user abend with code 999. No records are written or updated during normal processing; the program is read-only against all VSAM stores.

## Business Rules Surfaced

- **BR-001** — All six files must open successfully before any processing begins; any open failure is immediately fatal.
- **BR-002** — The main loop continues until END-OF-DAILY-TRANS-FILE is set to 'Y' on EOF.
- **BR-003** — Each transaction record is displayed to the system log before cross-reference lookup.
- **BR-004** — Card numbers are validated against the cross-reference VSAM file; unresolved cards are skipped.
- **BR-005** — Unverifiable card numbers produce a console diagnostic and the record is abandoned.
- **BR-006** — Account lookup only proceeds when cross-reference lookup succeeds.
- **BR-007** — Missing account records produce a console diagnostic but are non-fatal.
- **BR-008** — Any daily transaction file read error other than EOF triggers an immediate abend.
- **BR-009** — Status '10' is the sole normal EOF signal.
- **BR-010** — INVALID KEY on cross-reference read sets WS-XREF-READ-STATUS to 4.
- **BR-011** — INVALID KEY on account read sets WS-ACCT-READ-STATUS to 4; non-fatal.
- **BR-012** — Any file open or close failure triggers abend with CEE3ABD code 999.
- **BR-013** — Vendor-specific '9x' status codes are decoded via binary/character overlay before display.
