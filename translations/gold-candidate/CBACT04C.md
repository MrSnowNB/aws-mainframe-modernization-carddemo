---
schema_version: "cobol-md/1.0"
program_id: "CBACT04C"
source_file: "app/cbl/CBACT04C.cbl"
source_sha: "1da48c0015ca11995d2c02d8ece3fcbc63b84ec1"
translation_date: "2026-05-03"
translating_agent: "perplexity-sonar (subagent)"
aifirst_task_id: "T-2026-05-03-001"
cfg_source: "validation/structure/CBACT04C_cfg.json"

business_domain: "Account Management"
subtype: "Batch"

author: "AWS"
date_written: null
lines_of_code: 652
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
    condition: "fatal I/O or open/close/rewrite failure detected"
    call_type: "STATIC"

called_by: []

copybooks_used:
  - name: "CVTRA01Y"
    path: "app/cpy/CVTRA01Y.cpy"
    sha: null
  - name: "CVACT03Y"
    path: "app/cpy/CVACT03Y.cpy"
    sha: null
  - name: "CVTRA02Y"
    path: "app/cpy/CVTRA02Y.cpy"
    sha: null
  - name: "CVACT01Y"
    path: "app/cpy/CVACT01Y.cpy"
    sha: null
  - name: "CVTRA05Y"
    path: "app/cpy/CVTRA05Y.cpy"
    sha: null

file_control:
  - ddname: "TCATBALF"
    organization: "INDEXED"
    access: "SEQUENTIAL"
    record_key: "FD-TRAN-CAT-KEY"
    crud: ["READ"]
  - ddname: "XREFFILE"
    organization: "INDEXED"
    access: "RANDOM"
    record_key: "FD-XREF-CARD-NUM"
    crud: ["READ"]
  - ddname: "DISCGRP"
    organization: "INDEXED"
    access: "RANDOM"
    record_key: "FD-DISCGRP-KEY"
    crud: ["READ"]
  - ddname: "ACCTFILE"
    organization: "INDEXED"
    access: "RANDOM"
    record_key: "FD-ACCT-ID"
    crud: ["READ", "UPDATE"]
  - ddname: "TRANSACT"
    organization: "SEQUENTIAL"
    access: "SEQUENTIAL"
    record_key: null
    crud: ["CREATE"]

cics_commands: []
transaction_ids: []

data_items:
  - name: "FD-TRAN-CAT-BAL-RECORD"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "File descriptor group record for the VSAM KSDS transaction category balance input file; contains the compound key (account ID + transaction type code + category code) and a 33-byte data area"

  - name: "FD-XREFFILE-REC"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "File descriptor record for the VSAM KSDS cross-reference file; maps card number to customer number and account ID"

  - name: "FD-DISCGRP-REC"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "File descriptor record for the VSAM KSDS disclosure group file; keyed by account group ID, transaction type code, and category code; contains a 34-byte data area holding interest rate and fee parameters"

  - name: "FD-ACCTFILE-REC"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "File descriptor record for the VSAM KSDS account master file; keyed by 11-digit account ID with a 289-byte data area; opened in I-O mode to support both random reads and rewrites"

  - name: "FD-TRANFILE-REC"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Output record written to the sequential transaction file; contains a 16-character transaction ID and a 334-byte data area holding the full interest transaction record"

  - name: "TCATBALF-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file-status code returned after every I/O operation on TCATBAL-FILE; first byte is class, second is subclass"

  - name: "XREFFILE-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file-status code for XREF-FILE I/O operations"

  - name: "DISCGRP-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file-status code for DISCGRP-FILE I/O operations; '23' (key not found) is treated as a non-fatal condition triggering a fallback to the DEFAULT group"

  - name: "ACCTFILE-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file-status code for ACCOUNT-FILE I/O operations; used after both random READ and REWRITE"

  - name: "TRANFILE-STATUS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Two-character file-status code for TRANSACT-FILE write operations"

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
        interpreted_as: "Two individual character bytes (left and right) overlaying the binary integer, allowing the second status byte to be extracted as a raw character and converted to a numeric value for display"
        encoding: "DISPLAY"
      - condition: "IO-STATUS is numeric and IO-STAT1 != '9' (standard status path in 9910-DISPLAY-IO-STATUS)"
        interpreted_as: "Two-byte binary integer holding a packed numeric I/O status code; the integer value is moved directly to IO-STATUS-0403 for formatted display"
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
    semantic: "Signed nine-digit binary working register communicating operation outcome within each I/O routine; value 0 = success (APPL-AOK), 16 = end-of-file (APPL-EOF), 12 = error"

  - name: "END-OF-FILE"
    level: 01
    picture: "X(01)"
    usage: null
    value: "N"
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Single-character flag controlling the main read loop; initialised to 'N' and set to 'Y' when TCATBAL-FILE reaches end-of-file, terminating the PERFORM UNTIL loop"

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

  - name: "COBOL-TS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Structured working-storage timestamp group receiving the output of FUNCTION CURRENT-DATE; broken into year, month, day, hour, minute, second, millisecond, and trailing rest subfields"

  - name: "DB2-FORMAT-TS"
    level: 01
    picture: "X(26)"
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "26-character DB2-format timestamp string (YYYY-MM-DD-HH.MM.SS.MMxxxx) constructed from COBOL-TS subfields; written into both TRAN-ORIG-TS and TRAN-PROC-TS on each interest transaction record"

  - name: "FILLER"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: "DB2-FORMAT-TS"
    redefines_interpretations:
      - condition: "Z-GET-DB2-FORMAT-TIMESTAMP is populating the timestamp"
        interpreted_as: "Structured overlay of DB2-FORMAT-TS providing individually addressable subfields (DB2-YYYY, DB2-MM, DB2-DD, DB2-HH, DB2-MIN, DB2-SS, DB2-MIL, DB2-REST and separator characters) so each component can be moved independently from COBOL-TS"
        encoding: "DISPLAY"
    dead_code_flag: false
    semantic: "Named FILLER redefining DB2-FORMAT-TS; provides field-level write access to each date/time component and separator character within the 26-byte DB2 timestamp string"

  - name: "WS-MISC-VARS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Miscellaneous working-storage group holding: WS-LAST-ACCT-NUM (11-char prior account tracker for account-change detection), WS-MONTHLY-INT (signed 11-digit computed monthly interest), WS-TOTAL-INT (signed 11-digit accumulated interest for the current account), and WS-FIRST-TIME (single-char first-iteration guard flag)"

  - name: "WS-COUNTERS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Counter group: WS-RECORD-COUNT accumulates the number of transaction category balance records processed; WS-TRANID-SUFFIX provides a sequential 6-digit suffix appended to PARM-DATE to form unique transaction IDs"

  - name: "EXTERNAL-PARMS"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "LINKAGE SECTION parameter record passed via PROCEDURE DIVISION USING; contains PARM-LENGTH (signed 4-digit binary) and PARM-DATE (10-char date string) supplied by the JCL PARM or calling mechanism; PARM-DATE is used as the prefix for generated transaction IDs"

procedure_paragraphs:
  - name: "0000-TCATBALF-OPEN"
    reachable: true
    performs:
      - "0100-XREFFILE-OPEN"
      - "9999-ABEND-PROGRAM"
      - "9910-DISPLAY-IO-STATUS"
    goto_targets: []
    summary: "Opens TCATBAL-FILE for sequential input; checks that the file status is '00' and abends with a diagnostic message if the open fails"

  - name: "0100-XREFFILE-OPEN"
    reachable: true
    performs:
      - "0200-DISCGRP-OPEN"
      - "9999-ABEND-PROGRAM"
      - "9910-DISPLAY-IO-STATUS"
    goto_targets: []
    summary: "Opens XREF-FILE for random input; checks file status and abends with a diagnostic message if the open fails"

  - name: "0200-DISCGRP-OPEN"
    reachable: true
    performs:
      - "0300-ACCTFILE-OPEN"
      - "9999-ABEND-PROGRAM"
      - "9910-DISPLAY-IO-STATUS"
    goto_targets: []
    summary: "Opens DISCGRP-FILE for random input; checks file status and abends with a diagnostic message if the open fails"

  - name: "0300-ACCTFILE-OPEN"
    reachable: true
    performs:
      - "0400-TRANFILE-OPEN"
      - "9999-ABEND-PROGRAM"
      - "9910-DISPLAY-IO-STATUS"
    goto_targets: []
    summary: "Opens ACCOUNT-FILE in I-O mode (both read and rewrite); checks file status and abends with a diagnostic message if the open fails"

  - name: "0400-TRANFILE-OPEN"
    reachable: true
    performs:
      - "1000-TCATBALF-GET-NEXT"
      - "9999-ABEND-PROGRAM"
      - "9910-DISPLAY-IO-STATUS"
    goto_targets: []
    summary: "Opens TRANSACT-FILE for output; checks file status and abends with a diagnostic message if the open fails"

  - name: "1000-TCATBALF-GET-NEXT"
    reachable: true
    performs:
      - "1050-UPDATE-ACCOUNT"
      - "9999-ABEND-PROGRAM"
      - "9910-DISPLAY-IO-STATUS"
    goto_targets: []
    summary: "Reads the next record from TCATBAL-FILE into TRAN-CAT-BAL-RECORD; sets APPL-RESULT to 0 on success, 16 on end-of-file (setting END-OF-FILE to 'Y'), or 12 on error triggering an abend"

  - name: "1050-UPDATE-ACCOUNT"
    reachable: true
    performs:
      - "1100-GET-ACCT-DATA"
      - "9999-ABEND-PROGRAM"
      - "9910-DISPLAY-IO-STATUS"
    goto_targets: []
    summary: "Applies accumulated interest to the account balance (adds WS-TOTAL-INT to ACCT-CURR-BAL), resets current-cycle credit and debit to zero, then rewrites the account record to ACCOUNT-FILE; abends on rewrite failure"

  - name: "1100-GET-ACCT-DATA"
    reachable: true
    performs:
      - "1110-GET-XREF-DATA"
      - "9999-ABEND-PROGRAM"
      - "9910-DISPLAY-IO-STATUS"
    goto_targets: []
    summary: "Performs a random READ of ACCOUNT-FILE by FD-ACCT-ID into ACCOUNT-RECORD; displays a 'not found' message on INVALID KEY; abends if the resulting status is not '00'"

  - name: "1110-GET-XREF-DATA"
    reachable: true
    performs:
      - "1200-GET-INTEREST-RATE"
      - "9999-ABEND-PROGRAM"
      - "9910-DISPLAY-IO-STATUS"
    goto_targets: []
    summary: "Performs a random READ of XREF-FILE by alternate key FD-XREF-ACCT-ID into CARD-XREF-RECORD; displays a 'not found' message on INVALID KEY; abends if the resulting status is not '00'"

  - name: "1200-A-GET-DEFAULT-INT-RATE"
    reachable: true
    performs:
      - "1300-COMPUTE-INTEREST"
      - "9999-ABEND-PROGRAM"
      - "9910-DISPLAY-IO-STATUS"
    goto_targets: []
    summary: "Reads the DEFAULT disclosure group record from DISCGRP-FILE; abends if the status is not '00'; provides the fallback interest rate when no group-specific rate is found"

  - name: "1200-GET-INTEREST-RATE"
    reachable: true
    performs:
      - "1200-A-GET-DEFAULT-INT-RATE"
      - "9999-ABEND-PROGRAM"
      - "9910-DISPLAY-IO-STATUS"
    goto_targets: []
    summary: "Reads the disclosure group record for the current account group / transaction type / category combination; accepts both '00' (found) and '23' (not found) as non-error outcomes; on '23' sets the group key to 'DEFAULT' and calls 1200-A-GET-DEFAULT-INT-RATE to retrieve the fallback rate; abends on any other non-zero status"

  - name: "1300-B-WRITE-TX"
    reachable: true
    performs:
      - "1400-COMPUTE-FEES"
      - "9999-ABEND-PROGRAM"
      - "9910-DISPLAY-IO-STATUS"
      - "Z-GET-DB2-FORMAT-TIMESTAMP"
    goto_targets: []
    summary: "Constructs and writes a synthetic interest transaction record to TRANSACT-FILE; builds the transaction ID from PARM-DATE plus an auto-incrementing suffix, sets type '01' / category '05', populates amount, merchant, card number, and DB2-format timestamps; abends on write failure"

  - name: "1300-COMPUTE-INTEREST"
    reachable: true
    performs:
      - "1300-B-WRITE-TX"
    goto_targets: []
    summary: "Computes monthly interest as (TRAN-CAT-BAL x DIS-INT-RATE) / 1200 and accumulates it into WS-TOTAL-INT; then calls 1300-B-WRITE-TX to create the corresponding interest transaction record"

  - name: "1400-COMPUTE-FEES"
    reachable: true
    performs:
      - "9000-TCATBALF-CLOSE"
    goto_targets: []
    summary: "Stub paragraph — body contains only EXIT; fee computation is not yet implemented"

  - name: "9000-TCATBALF-CLOSE"
    reachable: true
    performs:
      - "9100-XREFFILE-CLOSE"
      - "9999-ABEND-PROGRAM"
      - "9910-DISPLAY-IO-STATUS"
    goto_targets: []
    summary: "Closes TCATBAL-FILE and abends if the close operation does not return status '00'"

  - name: "9100-XREFFILE-CLOSE"
    reachable: true
    performs:
      - "9200-DISCGRP-CLOSE"
      - "9999-ABEND-PROGRAM"
      - "9910-DISPLAY-IO-STATUS"
    goto_targets: []
    summary: "Closes XREF-FILE and abends if the close operation does not return status '00'"

  - name: "9200-DISCGRP-CLOSE"
    reachable: true
    performs:
      - "9300-ACCTFILE-CLOSE"
      - "9999-ABEND-PROGRAM"
      - "9910-DISPLAY-IO-STATUS"
    goto_targets: []
    summary: "Closes DISCGRP-FILE and abends if the close operation does not return status '00'"

  - name: "9300-ACCTFILE-CLOSE"
    reachable: true
    performs:
      - "9400-TRANFILE-CLOSE"
      - "9999-ABEND-PROGRAM"
      - "9910-DISPLAY-IO-STATUS"
    goto_targets: []
    summary: "Closes ACCOUNT-FILE and abends if the close operation does not return status '00'"

  - name: "9400-TRANFILE-CLOSE"
    reachable: true
    performs:
      - "Z-GET-DB2-FORMAT-TIMESTAMP"
      - "9999-ABEND-PROGRAM"
      - "9910-DISPLAY-IO-STATUS"
    goto_targets: []
    summary: "Closes TRANSACT-FILE and abends if the close operation does not return status '00'"

  - name: "9910-DISPLAY-IO-STATUS"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Decodes and displays the two-byte I/O status code in a normalised four-digit format, handling both standard numeric status codes and VSAM extended (non-numeric or '9x') status codes"

  - name: "9999-ABEND-PROGRAM"
    reachable: true
    performs:
      - "9910-DISPLAY-IO-STATUS"
    goto_targets: []
    summary: "Displays an abend notification message, sets abend code 999 with zero timing, and calls the Language Environment CEE3ABD service to force a controlled abnormal termination"

  - name: "Z-GET-DB2-FORMAT-TIMESTAMP"
    reachable: true
    performs:
      - "9999-ABEND-PROGRAM"
    goto_targets: []
    summary: "Captures the current system date and time via FUNCTION CURRENT-DATE into COBOL-TS, then reformats the individual components into the 26-character DB2 timestamp format (YYYY-MM-DD-HH.MM.SS.MM0000) in DB2-FORMAT-TS"

business_rules:
  - id: "BR-001"
    rule: "The main processing loop continues while END-OF-FILE equals 'N'; setting it to 'Y' on end-of-file is the only normal exit path from the loop"
    source_paragraph: "1000-TCATBALF-GET-NEXT"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-002"
    rule: "Interest computation and transaction writing are only triggered when DIS-INT-RATE is non-zero; a zero rate causes the program to skip both 1300-COMPUTE-INTEREST and 1400-COMPUTE-FEES for that category balance record"
    source_paragraph: "1000-TCATBALF-GET-NEXT"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-003"
    rule: "Account updates (rewrite) are performed only when the account number changes between consecutive transaction category balance records, or when the end-of-file condition is reached on the last account; this batches all interest for a single account before posting"
    source_paragraph: "1050-UPDATE-ACCOUNT"
    rule_type: "transform"
    confidence: "high"
    reachable: true

  - id: "BR-004"
    rule: "On the very first record processed, WS-FIRST-TIME prevents a premature account update; the flag is cleared to 'N' immediately, so all subsequent account-number changes trigger an update of the prior account"
    source_paragraph: "1050-UPDATE-ACCOUNT"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-005"
    rule: "When a disclosure group record is not found (status '23'), the program retries with a hard-coded group ID of 'DEFAULT' rather than abending; only a complete read failure on that fallback triggers an abend"
    source_paragraph: "1200-GET-INTEREST-RATE"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-006"
    rule: "Monthly interest is computed as (TRAN-CAT-BAL x DIS-INT-RATE) / 1200, converting an annual percentage rate to a monthly amount; the result is accumulated into WS-TOTAL-INT across all category records for the same account"
    source_paragraph: "1300-COMPUTE-INTEREST"
    rule_type: "transform"
    confidence: "high"
    reachable: true

  - id: "BR-007"
    rule: "Each interest transaction written to TRANSACT-FILE receives a unique transaction ID constructed by concatenating PARM-DATE (supplied via JCL PARM) with an auto-incrementing 6-digit suffix (WS-TRANID-SUFFIX)"
    source_paragraph: "1300-B-WRITE-TX"
    rule_type: "audit"
    confidence: "high"
    reachable: true

  - id: "BR-008"
    rule: "All synthetic interest transactions are assigned type code '01' and category code '05', source 'System', and zero merchant fields; both TRAN-ORIG-TS and TRAN-PROC-TS are set to the same DB2-format timestamp captured at write time"
    source_paragraph: "1300-B-WRITE-TX"
    rule_type: "transform"
    confidence: "high"
    reachable: true

  - id: "BR-009"
    rule: "Fee computation (1400-COMPUTE-FEES) is a stub — the paragraph body contains only EXIT; no fee logic is implemented in this version"
    source_paragraph: "1400-COMPUTE-FEES"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-010"
    rule: "Failure to open any of the five files is immediately fatal; the program displays the failing status and abends without attempting further processing"
    source_paragraph: "0000-TCATBALF-OPEN"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-011"
    rule: "Failure to close any of the five files is immediately fatal and triggers the same abend path used for I/O errors"
    source_paragraph: "9000-TCATBALF-CLOSE"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-012"
    rule: "When an I/O status code is non-numeric or its first character is '9', the status is decoded as a VSAM extended return code by overlaying the binary integer with character bytes before display"
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

# CBACT04C — Interest Calculation and Transaction Posting Batch

## Purpose

CBACT04C is the interest calculator batch program in the CardDemo application. It reads every transaction category balance record from a VSAM KSDS sequentially, looks up the applicable interest rate from a disclosure group file, computes a monthly interest charge for each category balance, and accumulates the total per account. When the account number changes (or end-of-file is reached), it posts the accumulated interest directly back to the account master record via a REWRITE and writes a corresponding synthetic interest transaction record to a sequential transaction output file.

## Runtime Context

The program runs as a standard z/OS batch job step with no CICS dependency. It accepts a date string and parameter length via the PROCEDURE DIVISION USING EXTERNAL-PARMS linkage, which are passed through JCL PARM. It accesses five files: TCATBAL-FILE (VSAM KSDS, sequential read), XREF-FILE (VSAM KSDS, random read by alternate key), DISCGRP-FILE (VSAM KSDS, random read), ACCOUNT-FILE (VSAM KSDS, random read and rewrite in I-O mode), and TRANSACT-FILE (sequential output). No sub-programs other than CEE3ABD (LE abend service) are called. Five copybooks provide shared data layouts: CVTRA01Y (transaction category balance record), CVACT03Y (card cross-reference record), CVTRA02Y (disclosure group record), CVACT01Y (account record), and CVTRA05Y (transaction record).

## Procedure Logic Summary

The program opens all five files, then drives a PERFORM UNTIL loop reading transaction category balance records. For each record it: displays the record, detects account-number changes (using WS-LAST-ACCT-NUM) to trigger deferred posting of accumulated interest via 1050-UPDATE-ACCOUNT, reads the account master and cross-reference records for new accounts, looks up the disclosure group interest rate (with DEFAULT fallback), computes monthly interest and writes an interest transaction record when the rate is non-zero, and accumulates interest into WS-TOTAL-INT. On end-of-file the final account update is performed, all five files are closed, and the program exits via GOBACK.

## Business Rules Surfaced

- **BR-001** — END-OF-FILE flag controls the main loop; set to 'Y' only on TCATBALF status '10'.
- **BR-002** — Interest and fee computation are skipped entirely when DIS-INT-RATE equals zero.
- **BR-003** — Account updates are deferred and batched: posted only on account-number change or end-of-file.
- **BR-004** — WS-FIRST-TIME prevents a spurious update on the very first record of the run.
- **BR-005** — Missing disclosure group record (status '23') falls back to the hard-coded 'DEFAULT' group rather than aborting.
- **BR-006** — Monthly interest formula: (balance x annual rate) / 1200.
- **BR-007** — Transaction IDs are unique per run, built from PARM-DATE plus an auto-incrementing suffix.
- **BR-008** — All synthetic interest transactions carry type '01', category '05', source 'System', and matched origin/process timestamps.
- **BR-009** — 1400-COMPUTE-FEES is an unimplemented stub (EXIT only).
- **BR-010 / BR-011** — All file open and close failures are immediately fatal.
- **BR-012** — VSAM extended status codes are decoded via binary/character overlay before display.
