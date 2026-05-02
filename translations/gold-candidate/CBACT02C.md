---
schema_version: "cobol-md/1.0"
program_id: "CBACT02C"
source_file: "app/cbl/CBACT02C.cbl"
source_sha: null
translation_date: "2026-04-23"
translating_agent: "recovery/restore-green-baseline (gate repair)"
aifirst_task_id: "T-2026-04-23-002"
cfg_source: "validation/structure/CBACT02C_cfg.json"

business_domain: "Account Management"
subtype: "Batch"

author: "AWS"
date_written: null
lines_of_code: null
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
    condition: "fatal I/O or open/close failure detected"
    call_type: "STATIC"

called_by: []

copybooks_used:
  - name: "CVACT02Y"
    path: "app/cpy/CVACT02Y.cpy"
    sha: null

file_control:
  - ddname: "CARDFILE"
    organization: "INDEXED"
    access: "SEQUENTIAL"
    record_key: "FD-CARD-NUM"
    crud: ["READ"]

cics_commands: []
transaction_ids: []

data_items:
  - name: "FD-CARDFILE-REC"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "File descriptor group record for the VSAM KSDS card input file; top-level container for FD-CARD-NUM and FD-CARD-DATA"

  - name: "CARDFILE-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file-status code returned by the runtime after every I/O operation on CARDFILE; first byte (CARDFILE-STAT1) is the class, second byte is the subclass"

  - name: "IO-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Staging area that receives any file-status value immediately before calling the I/O status display routine"

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
        interpreted_as: "Two individual character bytes overlaying the binary integer, allowing the second status byte to be extracted and converted to a numeric value for display"
        encoding: "DISPLAY"
      - condition: "IO-STATUS is numeric and IO-STAT1 != '9' (standard status path)"
        interpreted_as: "Two-byte binary integer holding a packed numeric I/O status code used directly for display"
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
    semantic: "Four-character display buffer for printing a normalised I/O status code"

  - name: "APPL-RESULT"
    level: 01
    picture: "S9(9)"
    usage: "COMP"
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Signed nine-digit binary working register; value 0 = success (APPL-AOK), 16 = end-of-file (APPL-EOF), 12 = error"

  - name: "END-OF-FILE"
    level: 01
    picture: "X(01)"
    usage: null
    value: "N"
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Single-character flag controlling the main read loop; initialised to 'N' and set to 'Y' when CARDFILE reaches end-of-file"

  - name: "ABCODE"
    level: 01
    picture: "S9(9)"
    usage: "BINARY"
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Abend code passed to CEE3ABD; always set to 999 before the abend call"

  - name: "TIMING"
    level: 01
    picture: "S9(9)"
    usage: "BINARY"
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Timing parameter passed to CEE3ABD alongside ABCODE; set to 0 indicating immediate abend"

procedure_paragraphs:
  - name: "CBACT02C-MAIN"
    reachable: true
    performs:
      - "0000-CARDFILE-OPEN"
      - "1000-CARDFILE-GET-NEXT"
      - "9000-CARDFILE-CLOSE"
    goto_targets: []
    summary: "Main control paragraph: displays start banner, opens CARDFILE, drives a PERFORM UNTIL read loop while END-OF-FILE is 'N', closes CARDFILE, displays end banner, and issues GOBACK"

  - name: "1000-CARDFILE-GET-NEXT"
    reachable: true
    performs:
      - "9910-DISPLAY-IO-STATUS"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Reads the next card record from CARDFILE; if status is '00' sets APPL-RESULT to 0 and continues; if '10' sets APPL-RESULT to 16 (EOF); any other status sets APPL-RESULT to 12 then triggers error display and abend"

  - name: "0000-CARDFILE-OPEN"
    reachable: true
    performs:
      - "9910-DISPLAY-IO-STATUS"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Pre-sets APPL-RESULT to 8, opens CARDFILE for input, checks status '00', and abends with 'ERROR OPENING CARDFILE' on failure"

  - name: "9000-CARDFILE-CLOSE"
    reachable: true
    performs:
      - "9910-DISPLAY-IO-STATUS"
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Closes CARDFILE and abends with 'ERROR CLOSING CARDFILE' if the close status is not '00'"

  - name: "9999-ABEND-PROGRAM"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Displays 'ABENDING PROGRAM', sets TIMING to 0 and ABCODE to 999, then calls CEE3ABD to force a controlled abnormal termination"

  - name: "9910-DISPLAY-IO-STATUS"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Decodes and displays the two-byte I/O status code in normalised four-digit format; VSAM extended ('9x') codes are decoded via binary/character overlay, standard numeric codes are displayed as-is"

business_rules:
  - id: "BR-001"
    rule: "The main read loop continues only while END-OF-FILE equals 'N'; once any read sets END-OF-FILE to 'Y', the program exits the loop, closes CARDFILE, and terminates"
    source_paragraph: "CBACT02C-MAIN"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-002"
    rule: "A file status of '00' from CARDFILE sets APPL-RESULT to 0 (APPL-AOK) and allows processing to continue; '10' sets APPL-RESULT to 16 (APPL-EOF); any other status sets APPL-RESULT to 12 (error) and triggers abend"
    source_paragraph: "1000-CARDFILE-GET-NEXT"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-003"
    rule: "Any file open that returns a status other than '00' is treated as fatal; the program displays the error and abends immediately"
    source_paragraph: "0000-CARDFILE-OPEN"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-004"
    rule: "Any file close that returns a status other than '00' is treated as fatal; the program displays the error and abends immediately"
    source_paragraph: "9000-CARDFILE-CLOSE"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-005"
    rule: "Non-numeric or VSAM extended ('9x') I/O status codes are decoded via a binary/character overlay before display; standard numeric codes are displayed as a normalised four-digit value"
    source_paragraph: "9910-DISPLAY-IO-STATUS"
    rule_type: "transform"
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

# CBACT02C — Card File Sequential Read and Diagnostic Output

## Purpose

CBACT02C is a batch utility program in the CardDemo application that reads every card record from a VSAM Key-Sequenced Data Set (KSDS) sequentially and displays each record to standard output for diagnostic purposes. It implements the standard guarded I/O pattern: open, read in a PERFORM UNTIL loop until end-of-file, close. Any I/O failure triggers a controlled abnormal termination via the Language Environment CEE3ABD service.

## Runtime Context

The program runs as a standard z/OS batch job step with no CICS dependency. It accesses one VSAM KSDS input file (CARDFILE, opened for sequential input). One external sub-program is called: CEE3ABD, the Language Environment abnormal termination service. One copybook provides the shared data layout: CVACT02Y defines the card record structure used as the read target.

## Procedure Logic Summary

The program displays a start banner, opens CARDFILE, then drives a PERFORM UNTIL loop reading card records sequentially. Inside the loop, if END-OF-FILE is still 'N', it performs 1000-CARDFILE-GET-NEXT. After the read, if END-OF-FILE is still 'N', it displays the card record. After the loop exits, it closes CARDFILE, displays an end banner, and issues GOBACK.

## Business Rules Surfaced

- **BR-001** — The read loop is governed by END-OF-FILE; 'Y' on end-of-file is the only normal exit.
- **BR-002** — File-status '00' continues processing; '10' triggers EOF exit; all other values trigger abend.
- **BR-003** — Failure to open CARDFILE is immediately fatal.
- **BR-004** — Failure to close CARDFILE is immediately fatal.
- **BR-005** — I/O status codes are decoded and displayed in a normalised four-digit format.
