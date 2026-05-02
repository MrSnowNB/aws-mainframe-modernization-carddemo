---
schema_version: "cobol-md/1.0"
program_id: "CBACT03C"
source_file: "app/cbl/CBACT03C.cbl"
source_sha: "e9adeca181e49c31223cd334919697268782e93e"
translation_date: "2026-04-30"
translating_agent: "Cline (subagent)"
aifirst_task_id: "T-2026-04-23-002"
cfg_source: "validation/structure/CBACT03C_cfg.json"

business_domain: "Account Management"
subtype: "Batch"

author: "AWS"
date_written: null
lines_of_code: 178
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
  - program: "CEE3ABD"
    condition: "unconditional (in 9999-ABEND-PROGRAM, invoked on any I/O error)"
    call_type: "DYNAMIC"

called_by: []

copybooks_used:
  - name: "CVACT03Y"
    path: "app/cpy/CVACT03Y.cpy"
    sha: null

file_control:
  - ddname: "XREFFILE"
    organization: "INDEXED"
    access: "SEQUENTIAL"
    record_key: "FD-XREF-CARD-NUM"
    crud: ["READ"]

cics_commands: []
transaction_ids: []

data_items:
  - name: "FD-XREFFILE-REC"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "File descriptor group record for the VSAM KSDS cross-reference input file; top-level container for FD-XREF-CARD-NUM (16-char card number) and FD-XREF-DATA (34-char data area)"

  - name: "XREFFILE-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file-status code returned by the runtime after every I/O operation on XREFFILE; first byte (XREFFILE-STAT1) is the class, second byte (XREFFILE-STAT2) is the subclass"

  - name: "IO-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Staging area that receives any file-status value immediately before calling the I/O status display routine; normalises status from XREFFILE into a uniform display path"

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
      - condition: "IO-STATUS is non-numeric or IO-STAT1 = '9' (VSAM extended status path in 9910-DISPLAY-IO-STATUS)"
        interpreted_as: "Two individual character bytes (TWO-BYTES-LEFT and TWO-BYTES-RIGHT) overlaying the binary integer, allowing the second status byte to be extracted as a raw character and then converted to a numeric value for display"
        encoding: "DISPLAY"
      - condition: "IO-STATUS is numeric and IO-STAT1 != '9' (standard status path in 9910-DISPLAY-IO-STATUS)"
        interpreted_as: "Two-byte binary integer holding a packed numeric I/O status code; the character decomposition is not invoked in this path"
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
    semantic: "Four-character display buffer for printing a normalised I/O status code; composed of a one-digit class subfield (IO-STATUS-0401) and a three-digit subclass subfield (IO-STATUS-0403)"

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
    semantic: "Single-character flag controlling the main read loop; initialised to 'N' and set to 'Y' when XREFFILE reaches end-of-file, terminating the PERFORM UNTIL loop"

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

procedure_paragraphs:
  - name: "1000-XREFFILE-GET-NEXT"
    reachable: true
    performs:
      - "9910-DISPLAY-IO-STATUS"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Reads the next record from XREFFILE into CARD-XREF-RECORD (from CVACT03Y copybook); if file status is '00' sets APPL-RESULT to 0, displays the record, and continues; if status is '10' sets APPL-RESULT to 16 (EOF); otherwise sets APPL-RESULT to 12 (error) and triggers the error display and abend path"

  - name: "0000-XREFFILE-OPEN"
    reachable: true
    performs:
      - "9910-DISPLAY-IO-STATUS"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Pre-sets APPL-RESULT to 8 (a non-zero sentinel), opens XREFFILE for input, checks that the file status is '00', and on failure sets APPL-RESULT to 12; if APPL-RESULT is not zero after the open, displays 'ERROR OPENING XREFFILE', moves the status to IO-STATUS, calls the display and abend chain"

  - name: "9000-XREFFILE-CLOSE"
    reachable: true
    performs:
      - "9910-DISPLAY-IO-STATUS"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Adds 8 to zero to set APPL-RESULT to 8, then closes XREFFILE; if the file status is '00', subtracts APPL-RESULT from itself to zero it; otherwise adds 12 to set APPL-RESULT to 12. If APPL-RESULT is not zero, displays 'ERROR CLOSING XREFFILE' and invokes the abend chain"

  - name: "9999-ABEND-PROGRAM"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Displays the literal 'ABENDING PROGRAM', sets TIMING to zero and ABCODE to 999, then calls the Language Environment CEE3ABD service to force a controlled abnormal termination"

  - name: "9910-DISPLAY-IO-STATUS"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Decodes and displays the two-byte I/O status code in a normalised four-digit format. If IO-STATUS is non-numeric or IO-STAT1 equals '9', the VSAM extended path is taken: the first status byte is placed in IO-STATUS-04 position 1:1, TWO-BYTES-BINARY is zeroed, IO-STAT2 is moved into TWO-BYTES-RIGHT, the resulting binary integer is placed in IO-STATUS-0403, and the formatted result is displayed. Otherwise, '0000' is moved to IO-STATUS-04 and IO-STATUS is overlaid at positions 3:2 for display"

business_rules:
  - id: "BR-001"
    rule: "The main read loop continues only while END-OF-FILE equals 'N'; once any read sets END-OF-FILE to 'Y', the program exits the loop, closes the file, and terminates"
    source_paragraph: "1000-XREFFILE-GET-NEXT"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-002"
    rule: "If a successful read (file status '00') is obtained from XREFFILE, APPL-RESULT is set to 0 (APPL-AOK) and the record is displayed for diagnostic output; if status is '10', APPL-RESULT is set to 16 (APPL-EOF); any other status sets APPL-RESULT to 12 (error)"
    source_paragraph: "1000-XREFFILE-GET-NEXT"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-003"
    rule: "A file status of '10' from XREFFILE is interpreted as normal end-of-file (maps to APPL-EOF with value 16), causing a clean loop exit; any other non-zero status is treated as an error and triggers an abend"
    source_paragraph: "1000-XREFFILE-GET-NEXT"
    rule_type: "audit"
    confidence: "high"
    reachable: true

  - id: "BR-004"
    rule: "Any file open that returns a status other than '00' is treated as fatal; the program displays 'ERROR OPENING XREFFILE', moves the status to IO-STATUS, displays the decoded status, and abends immediately"
    source_paragraph: "0000-XREFFILE-OPEN"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-005"
    rule: "Any file close that returns a status other than '00' is treated as fatal; the program displays 'ERROR CLOSING XREFFILE', moves the status to IO-STATUS, displays the decoded status, and abends immediately"
    source_paragraph: "9000-XREFFILE-CLOSE"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-006"
    rule: "Each read from XREFFILE is validated; if APPL-RESULT is neither APPL-AOK (0) nor APPL-EOF (16), the program displays 'ERROR READING XREFFILE', moves the file status to IO-STATUS, displays the decoded status, and abends"
    source_paragraph: "1000-XREFFILE-GET-NEXT"
    rule_type: "audit"
    confidence: "high"
    reachable: true

  - id: "BR-007"
    rule: "The I/O status display routine has two code paths: standard numeric status codes are displayed as a four-digit normalised value (with '00' prepended), while non-numeric or VSAM extended codes ('9x') are decoded by overlaying binary and character views of the same two bytes and displaying the reason code in positions 3:4"
    source_paragraph: "9910-DISPLAY-IO-STATUS"
    rule_type: "transform"
    confidence: "high"
    reachable: true

  - id: "BR-008"
    rule: "Every cross-reference record read from XREFFILE is displayed to standard output for diagnostic purposes, providing a complete per-record audit trail"
    source_paragraph: "1000-XREFFILE-GET-NEXT"
    rule_type: "display"
    confidence: "high"
    reachable: true

  - id: "BR-009"
    rule: "The program always calls CEE3ABD with ABCODE=999 and TIMING=0 when an error condition is detected, producing a controlled abnormal termination with a user-specified abend code"
    source_paragraph: "9999-ABEND-PROGRAM"
    rule_type: "audit"
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

# CBACT03C — Cross-Reference File Sequential Read and Diagnostic Output

## Purpose

CBACT03C is a batch utility program in the CardDemo application that reads every record from a VSAM Key-Sequenced Data Set (KSDS) cross-reference file (XREFFILE) sequentially and displays each record to standard output for diagnostic purposes. The program implements a standard guarded I/O pattern: it opens the file, reads records in a PERFORM UNTIL loop until end-of-file, and closes the file. Any I/O failure triggers a controlled abnormal termination via the Language Environment CEE3ABD service.

## Runtime Context

The program runs as a standard z/OS batch job step with no CICS dependency. It accesses one VSAM KSDS input file (XREFFILE, opened for sequential input). One external sub-program is called: CEE3ABD, the Language Environment abnormal termination service. One copybook provides the shared data layout: CVACT03Y defines the cross-reference record structure (CARD-XREF-RECORD) used as the read target.

## Business Rules Surfaced

- **BR-001** — The read loop is governed by END-OF-FILE; setting it to 'Y' on end-of-file is the only normal exit path.
- **BR-002** — File-status '00' triggers record display and continued processing; '10' triggers end-of-file handling; any other value triggers abend.
- **BR-003** — File-status '10' is the sole normal end-of-file condition; all other non-zero values are fatal.
- **BR-004** — Failure to open XREFFILE is immediately fatal.
- **BR-005** — Failure to close XREFFILE is immediately fatal.
- **BR-006** — A read returning neither success nor end-of-file is a fatal error.
- **BR-007** — I/O status codes are decoded and displayed in normalised four-digit format; VSAM extended codes use a binary/character overlay path.
- **BR-008** — Every cross-reference record is displayed to standard output for a complete per-record audit trail.
- **BR-009** — The program always abends via CEE3ABD with ABCODE=999 and TIMING=0 on error.
