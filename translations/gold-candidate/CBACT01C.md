---
# ── Identity ──────────────────────────────────────────────────────────────────
schema_version: "cobol-md/1.0"
program_id: "CBACT01C"
source_file: "app/cbl/CBACT01C.cbl"
source_sha: "a9a14e021e6fe1c14caa544213d938abd15b6681"
translation_date: "2026-04-23"
translating_agent: "claude-opus-4-5 (subagent)"
aifirst_task_id: "T-2026-04-23-001"
cfg_source: "validation/structure/CBACT01C_cfg.json"

# ── Classification ─────────────────────────────────────────────────────────────
business_domain: "Account Management"
subtype: "Batch"

# ── Structural Metadata ────────────────────────────────────────────────────────
author: "AWS"
date_written: null
lines_of_code: 248
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
  - program: "COBDATFT"
    condition: "unconditional"
    call_type: "STATIC"
  - program: "CEE3ABD"
    condition: "fatal I/O or open/close failure detected"
    call_type: "STATIC"

called_by: []

copybooks_used:
  - name: "CVACT01Y"
    path: "app/cpy/CVACT01Y.cpy"
    sha: null
  - name: "CODATECN"
    path: "app/cpy/CODATECN.cpy"
    sha: null

# ── File I/O ──────────────────────────────────────────────────────────────────
file_control:
  - ddname: "ACCTFILE"
    organization: "INDEXED"
    access: "SEQUENTIAL"
    record_key: "FD-ACCT-ID"
    crud: ["READ"]
  - ddname: "OUTFILE"
    organization: "SEQUENTIAL"
    access: "SEQUENTIAL"
    record_key: null
    crud: ["CREATE"]
  - ddname: "ARRYFILE"
    organization: "SEQUENTIAL"
    access: "SEQUENTIAL"
    record_key: null
    crud: ["CREATE"]
  - ddname: "VBRCFILE"
    organization: "SEQUENTIAL"
    access: "SEQUENTIAL"
    record_key: null
    crud: ["CREATE"]

# ── CICS ───────────────────────────────────────────────────────────────────────
cics_commands: []
transaction_ids: []

# ── Data Layer ─────────────────────────────────────────────────────────────────
data_items:
  - name: "FD-ACCTFILE-REC"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "File descriptor group record for the VSAM KSDS account input file; top-level container for FD-ACCT-ID and FD-ACCT-DATA"

  - name: "OUT-ACCT-REC"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Output record written to the sequential OUTFILE; contains a fully expanded, formatted account snapshot for downstream consumption"

  - name: "ARR-ARRAY-REC"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Output record written to the sequential ARRYFILE; holds the account identifier plus a five-element balance array for multi-cycle reporting"

  - name: "VBR-REC"
    level: 01
    picture: "X(80)"
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Variable-length output buffer for VBRCFILE; receives short (12-byte) or long (39-byte) segments depending on which record variant is being written"

  - name: "ACCTFILE-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file-status code returned by the runtime after every I/O operation on ACCTFILE; first byte is class, second is subclass"

  - name: "OUTFILE-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file-status code for OUTFILE I/O operations"

  - name: "ARRYFILE-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file-status code for ARRYFILE I/O operations"

  - name: "VBRCFILE-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file-status code for VBRCFILE I/O operations"

  - name: "IO-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Staging area that receives any file-status value immediately before calling the I/O status display routine; normalises status from multiple files into one display path"

  - name: "TWO-BYTES-BINARY"
    level: 01
    picture: "9(4)"
    usage: "BINARY"
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Four-digit binary integer occupying two bytes; used as the numeric form of an I/O status code when decoding non-numeric or VSAM extended status bytes"

  - name: "TWO-BYTES-ALPHA"
    level: 01
    picture: null
    usage: "BINARY"
    value: null
    redefines: "TWO-BYTES-BINARY"
    redefines_interpretations:
      - condition: "IO-STAT1 = '9' (VSAM extended status path in 9910-DISPLAY-IO-STATUS)"
        interpreted_as: "Two individual character bytes (left and right) overlaying the binary integer, allowing the second status byte to be extracted as a raw character and then converted to a numeric value for display"
        encoding: "DISPLAY"
      - condition: "IO-STATUS is numeric and IO-STAT1 != '9' (standard status path in 9910-DISPLAY-IO-STATUS)"
        interpreted_as: "Two-byte binary integer holding a packed numeric I/O status code; not decomposed into left/right characters in this path; the integer value is moved directly to IO-STATUS-0403 for formatted display"
        encoding: "BINARY"
    dead_code_flag: false
    semantic: "Character alias for TWO-BYTES-BINARY; provides byte-level access to the two halves of the binary status word so that VSAM extended return codes can be decoded and printed"

  - name: "IO-STATUS-04"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Four-character display buffer for printing a normalised I/O status code; composed of a one-digit class subfield and a three-digit subclass subfield"

  - name: "APPL-RESULT"
    level: 01
    picture: "S9(9)"
    usage: "COMP"
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Signed nine-digit binary working register used to communicate operation outcome within each I/O routine; value 0 = success (APPL-AOK), 16 = end-of-file (APPL-EOF), 12 = error"

  - name: "END-OF-FILE"
    level: 01
    picture: "X(01)"
    usage: null
    value: "N"
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Single-character flag controlling the main read loop; initialised to 'N' and set to 'Y' when ACCTFILE reaches end-of-file, terminating the PERFORM UNTIL loop"

  - name: "ABCODE"
    level: 01
    picture: "S9(9)"
    usage: "BINARY"
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Abend code passed to CEE3ABD when the program terminates abnormally; always set to 999 before the abend call"

  - name: "TIMING"
    level: 01
    picture: "S9(9)"
    usage: "BINARY"
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Timing parameter passed to CEE3ABD alongside ABCODE; set to 0 indicating immediate (non-delayed) abend"

  - name: "WS-RECD-LEN"
    level: 01
    picture: "9(04)"
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Four-digit unsigned integer specifying the logical length of the current variable-length record before writing to VBRCFILE; set to 12 for the short variant and 39 for the long variant"

  - name: "VBRC-REC1"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Short variable-length record layout containing account identifier (11 digits) and active-status flag (1 character) for the first VBRCFILE write"

  - name: "VBRC-REC2"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Long variable-length record layout containing account identifier, current balance, credit limit, and reissue year for the second VBRCFILE write"

  - name: "WS-ACCT-REISSUE-DATE"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Structured working-storage date group that holds a card reissue date parsed into separate year (4 chars), separator, month (2 chars), separator, and day (2 chars) subfields"

  - name: "WS-REISSUE-DATE"
    level: 01
    picture: "X(10)"
    usage: null
    value: null
    redefines: "WS-ACCT-REISSUE-DATE"
    redefines_interpretations:
      - condition: "WS-REISSUE-DATE is being populated from ACCT-REISSUE-DATE in the account record (in 1300-POPUL-ACCT-RECORD, before date formatting)"
        interpreted_as: "Flat ten-character string view of the reissue date, allowing the entire date to be moved as a single unit from the source account record field into the structured date group in one operation"
        encoding: "DISPLAY"
      - condition: "WS-ACCT-REISSUE-YYYY is being referenced after the flat move (in 1500-POPUL-VBRC-RECORD, extracting the year component)"
        interpreted_as: "Structured date group with individually addressable subfields (year, separator, month, separator, day), enabling the program to extract the four-character year portion independently for population of VB2-ACCT-REISSUE-YYYY"
        encoding: "DISPLAY"
    dead_code_flag: false
    semantic: "Flat ten-character alias for WS-ACCT-REISSUE-DATE; enables bulk assignment of the full date string while WS-ACCT-REISSUE-DATE provides field-level access to individual date components"

# ── Procedure Paragraphs ───────────────────────────────────────────────────────
procedure_paragraphs:
  - name: "1000-ACCTFILE-GET-NEXT"
    reachable: true
    performs:
      - "1100-DISPLAY-ACCT-RECORD"
      - "1300-POPUL-ACCT-RECORD"
      - "1350-WRITE-ACCT-RECORD"
      - "1400-POPUL-ARRAY-RECORD"
      - "1450-WRITE-ARRY-RECORD"
      - "1500-POPUL-VBRC-RECORD"
      - "1550-WRITE-VB1-RECORD"
      - "1575-WRITE-VB2-RECORD"
      - "9910-DISPLAY-IO-STATUS"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Reads the next account record from ACCTFILE, evaluates the file status to set APPL-RESULT, and on success drives all display and write sub-paragraphs; on end-of-file sets END-OF-FILE to 'Y'; on any other error displays status and abends"

  - name: "1100-DISPLAY-ACCT-RECORD"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Prints all eleven account fields from the ACCOUNT-RECORD copybook area to standard output as a labelled diagnostic listing, followed by a separator line"

  - name: "1300-POPUL-ACCT-RECORD"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Maps account fields from the input ACCOUNT-RECORD into the OUT-ACCT-REC output layout, calls the COBDATFT date-formatting sub-routine to convert the reissue date, and applies a default debit value of 2525.00 when the current-cycle debit amount is zero"

  - name: "1350-WRITE-ACCT-RECORD"
    reachable: true
    performs:
      - "9910-DISPLAY-IO-STATUS"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Writes the populated OUT-ACCT-REC to OUTFILE and abends if the resulting file status is not successful"

  - name: "1400-POPUL-ARRAY-RECORD"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Builds the ARR-ARRAY-REC output record by copying account ID and current balance into the first two balance-array slots and loading hard-coded test amounts for cycles one through three"

  - name: "1450-WRITE-ARRY-RECORD"
    reachable: true
    performs:
      - "9910-DISPLAY-IO-STATUS"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Writes the populated ARR-ARRAY-REC to ARRYFILE and abends if the file status indicates an error"

  - name: "1500-POPUL-VBRC-RECORD"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Populates both variable-length record staging areas (VBRC-REC1 and VBRC-REC2) from the current account record and displays their content for diagnostic purposes"

  - name: "1550-WRITE-VB1-RECORD"
    reachable: true
    performs:
      - "9910-DISPLAY-IO-STATUS"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Sets the record length to 12, copies VBRC-REC1 into the VBR-REC buffer, writes the short variable-length record to VBRCFILE, and abends on write failure"

  - name: "1575-WRITE-VB2-RECORD"
    reachable: true
    performs:
      - "9910-DISPLAY-IO-STATUS"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Sets the record length to 39, copies VBRC-REC2 into the VBR-REC buffer, writes the long variable-length record to VBRCFILE, and abends on write failure"

  - name: "0000-ACCTFILE-OPEN"
    reachable: true
    performs:
      - "9910-DISPLAY-IO-STATUS"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Opens ACCTFILE for sequential input, checks that the file status is successful, and abends with a diagnostic message if the open fails"

  - name: "2000-OUTFILE-OPEN"
    reachable: true
    performs:
      - "9910-DISPLAY-IO-STATUS"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Opens OUTFILE for output, checks file status, and abends with a diagnostic message if the open fails"

  - name: "3000-ARRFILE-OPEN"
    reachable: true
    performs:
      - "9910-DISPLAY-IO-STATUS"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Opens ARRYFILE for output, checks file status, and abends with a diagnostic message if the open fails"

  - name: "4000-VBRFILE-OPEN"
    reachable: true
    performs:
      - "9910-DISPLAY-IO-STATUS"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Opens VBRCFILE for output in variable-length recording mode, checks file status, and abends with a diagnostic message if the open fails"

  - name: "9000-ACCTFILE-CLOSE"
    reachable: true
    performs:
      - "9910-DISPLAY-IO-STATUS"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Closes ACCTFILE after the read loop completes and abends if the close operation does not return a successful status"

  - name: "9999-ABEND-PROGRAM"
    reachable: true
    performs:
      - "9910-DISPLAY-IO-STATUS"
    goto_targets: []
    summary: "Displays an abend notification message, sets abend code 999 with zero timing, and calls the Language Environment CEE3ABD service to force a controlled abnormal termination"

  - name: "9910-DISPLAY-IO-STATUS"
    reachable: true
    performs:
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Decodes and displays the two-byte I/O status code in a normalised four-digit format, handling both standard numeric status codes and VSAM extended (non-numeric or '9x') status codes"

# ── Business Rules ─────────────────────────────────────────────────────────────
business_rules:
  - id: "BR-001"
    rule: "The main read loop continues only while END-OF-FILE equals 'N'; once any read sets END-OF-FILE to 'Y', the program exits the loop and proceeds to file close and termination"
    source_paragraph: "1000-ACCTFILE-GET-NEXT"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-002"
    rule: "If a successful read (file status '00') is obtained from ACCTFILE, all downstream populate-and-write paragraphs are executed; no processing occurs for a record when the status is not '00'"
    source_paragraph: "1000-ACCTFILE-GET-NEXT"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-003"
    rule: "A file status of '10' from ACCTFILE is interpreted as normal end-of-file (sets APPL-RESULT to 16, which satisfies APPL-EOF), causing a clean loop exit; any other non-zero status is treated as an error and triggers an abend"
    source_paragraph: "1000-ACCTFILE-GET-NEXT"
    rule_type: "audit"
    confidence: "high"
    reachable: true

  - id: "BR-004"
    rule: "If the current-cycle debit amount on an account record is exactly zero, the output field is overridden with the hard-coded default value of 2525.00 before writing to OUTFILE"
    source_paragraph: "1300-POPUL-ACCT-RECORD"
    rule_type: "transform"
    confidence: "high"
    reachable: true

  - id: "BR-005"
    rule: "Any file open that returns a status other than '00' is treated as fatal; the program displays the status and abends immediately without attempting to proceed"
    source_paragraph: "0000-ACCTFILE-OPEN"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-006"
    rule: "Any file open for OUTFILE that returns a status other than '00' is treated as fatal and triggers an immediate abend"
    source_paragraph: "2000-OUTFILE-OPEN"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-007"
    rule: "Any file open for ARRYFILE that returns a status other than '00' is treated as fatal and triggers an immediate abend"
    source_paragraph: "3000-ARRFILE-OPEN"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-008"
    rule: "Any file open for VBRCFILE that returns a status other than '00' is treated as fatal and triggers an immediate abend"
    source_paragraph: "4000-VBRFILE-OPEN"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-009"
    rule: "Each write to OUTFILE is validated; a file status other than '00' or '10' is treated as a fatal write error, triggers display of the status, and abends the program"
    source_paragraph: "1350-WRITE-ACCT-RECORD"
    rule_type: "audit"
    confidence: "high"
    reachable: true

  - id: "BR-010"
    rule: "Each write to ARRYFILE is validated; a file status other than '00' or '10' triggers a fatal abend"
    source_paragraph: "1450-WRITE-ARRY-RECORD"
    rule_type: "audit"
    confidence: "high"
    reachable: true

  - id: "BR-011"
    rule: "Each write of the short variable-length record to VBRCFILE is validated; a file status other than '00' or '10' triggers a fatal abend"
    source_paragraph: "1550-WRITE-VB1-RECORD"
    rule_type: "audit"
    confidence: "high"
    reachable: true

  - id: "BR-012"
    rule: "Each write of the long variable-length record to VBRCFILE is validated; a file status other than '00' or '10' triggers a fatal abend"
    source_paragraph: "1575-WRITE-VB2-RECORD"
    rule_type: "audit"
    confidence: "high"
    reachable: true

  - id: "BR-013"
    rule: "When an I/O status code is non-numeric or its first character is '9', the status is decoded as a VSAM extended return code by overlaying the binary integer with character bytes and converting the second byte to a numeric value before display"
    source_paragraph: "9910-DISPLAY-IO-STATUS"
    rule_type: "transform"
    confidence: "high"
    reachable: true

  - id: "BR-014"
    rule: "Each account record read from ACCTFILE is displayed in full to standard output before any downstream write processing occurs, providing a complete audit trail of every record encountered"
    source_paragraph: "1100-DISPLAY-ACCT-RECORD"
    rule_type: "display"
    confidence: "high"
    reachable: true

  - id: "BR-015"
    rule: "The ACCTFILE close operation is checked for success; a non-zero status triggers the same abend path used for read and write errors, ensuring file integrity on completion"
    source_paragraph: "9000-ACCTFILE-CLOSE"
    rule_type: "guard"
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

# CBACT01C — Account File Sequential Read and Multi-Format Output

## Purpose

CBACT01C is a batch utility program in the CardDemo application that reads every account record from a VSAM Key-Sequenced Data Set (KSDS) sequentially and distributes each record's data into three separate sequential output files in three different structural formats: a flat expanded record, a balance array record, and two variable-length record variants. The program also displays each account record to the standard output stream for diagnostic purposes. It serves as a data extraction and format-conversion batch step within the account management domain.

## Runtime Context

The program runs as a standard z/OS batch job step with no CICS dependency. It accesses five files: one VSAM KSDS input file (ACCTFILE, opened for sequential input with an indexed organisation) and three sequential output files (OUTFILE, ARRYFILE, VBRCFILE). VBRCFILE is opened in variable-length recording mode, with record sizes ranging from 10 to 80 bytes controlled by a working-storage length field. Two external sub-programs are called: COBDATFT, an assembler routine that reformats date strings, and CEE3ABD, the Language Environment abnormal termination service. Two copybooks provide shared data layouts: CVACT01Y defines the canonical account record group (ACCOUNT-RECORD) used as the read target, and CODATECN defines the date-conversion communication record (CODATECN-REC) passed to COBDATFT.

## Procedure Logic Summary

The program opens four output files and ACCTFILE, then drives a PERFORM UNTIL loop reading account records sequentially. For each successful read it displays the record, populates and writes the flat account record (OUTFILE), populates and writes the balance array record (ARRYFILE), and populates and writes two variable-length records (VBRCFILE). On end-of-file the loop exits and ACCTFILE is closed. Any I/O failure in open, read, write, or close triggers the abend path via CEE3ABD.

## Business Rules Surfaced

- **BR-001** — The read loop continues while END-OF-FILE equals 'N'; setting it to 'Y' on end-of-file is the only normal exit path.
- **BR-002** — Only records obtained with status '00' trigger downstream output processing.
- **BR-003** — File-status '10' is the sole normal end-of-file condition; all other non-zero values are fatal.
- **BR-004** — When a source account record carries a zero current-cycle debit, the output record receives an injected default value of 2525.00.
- **BR-005 through BR-008** — Failure to open any of the four files is immediately fatal.
- **BR-009 through BR-012** — Each write to any output file is individually validated; a write error is fatal.
- **BR-013** — Non-numeric or VSAM extended ('9x') I/O status codes are decoded via a binary/character overlay before display.
- **BR-014** — Every account record is echoed to standard output before transformation, providing a complete per-record audit trail.
- **BR-015** — Failure to close ACCTFILE is fatal.
