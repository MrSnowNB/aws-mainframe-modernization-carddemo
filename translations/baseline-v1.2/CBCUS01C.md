---
schema_version: cobol-md/1.2
program_id: CBCUS01C
source_file: app/cbl/CBCUS01C.cbl
source_sha: 88a99d7fc534579e538c438a4860e72ec068730c
translation_date: '2026-04-23'
translating_agent: claude-opus-4-5 (subagent)
aifirst_task_id: T-2026-04-23-001
cfg_source: validation/structure/CBCUS01C_cfg.json
business_domain: Customer Management
subtype: Batch
author: AWS
date_written: null
lines_of_code: 120
divisions:
  identification: true
  environment: true
  data: true
  procedure: true
environment:
  compiler: IBM Enterprise COBOL
  target: Batch/VSAM
  runtime: z/OS
calls_to:
- program: CEE3ABD
  condition: APPL-RESULT is neither zero nor sixteen after a file operation fails
  call_type: STATIC
called_by: []
copybooks_used:
- name: CVCUS01Y
  path: app/cpy/CVCUS01Y.cpy
  sha: null
file_control:
- ddname: CUSTFILE
  organization: INDEXED
  access: SEQUENTIAL
  record_key: FD-CUST-ID
  crud:
  - READ
  logical_name: CUSTFILE-FILE
  file_status: CUSTFILE-STATUS
  record_format: FB
  record_length: 500
  input_codepage: IBM-1047
  codepage_default_applied: true
  sign_convention: mainframe-ebcdic
  endianness: big
cics_commands: []
transaction_ids: []
data_items:
- name: FD-CUSTFILE-REC
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: File Description record group for CUSTFILE; the top-level container for the raw 500-byte customer record read
    from the VSAM KSDS, comprising a nine-digit customer ID and a 491-byte data payload.
- name: CUSTFILE-STATUS
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Two-character VSAM file-status code for CUSTFILE; the first byte carries the primary status class and the second
    byte carries the secondary status detail; tested after every OPEN, READ, and CLOSE.
- name: IO-STATUS
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Two-character general-purpose I/O status staging area; populated by copying CUSTFILE-STATUS into it before passing
    control to the display and abend error handlers.
- name: TWO-BYTES-BINARY
  level: 1
  picture: 9(4)
  usage: BINARY
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Four-digit unsigned binary integer occupying two bytes; used as the numeric operand in the I/O-status display
    helper to convert a single-byte character status code into a three-digit printable decimal.
- name: TWO-BYTES-ALPHA
  level: 1
  picture: null
  usage: BINARY
  value: null
  redefines: TWO-BYTES-BINARY
  redefines_interpretations:
  - condition: IO-STAT1 = '9' or IO-STATUS is NOT NUMERIC — the non-numeric I/O status path is active
    interpreted_as: Two individual single-character fields (TWO-BYTES-LEFT and TWO-BYTES-RIGHT) overlaying the same two bytes;
      TWO-BYTES-RIGHT receives the raw second status byte so that TWO-BYTES-BINARY can be read back as a numeric value for
      display
    encoding: DISPLAY
  - condition: IO-STATUS is NUMERIC and IO-STAT1 is not '9' — the numeric I/O status path is active
    interpreted_as: The same two bytes treated as a four-digit unsigned binary integer; the field is zeroed and only TWO-BYTES-BINARY
      is used directly, so the alpha overlay is dormant and the storage is interpreted purely as a binary number
    encoding: BINARY
  dead_code_flag: false
  semantic: Character overlay of TWO-BYTES-BINARY; exposes the two bytes as left and right single-character subfields so the
    I/O-status display routine can move an individual status byte into the high or low byte of the binary integer without
    arithmetic conversion.
- name: IO-STATUS-04
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Four-character formatted I/O status display group; assembled at runtime into a human-readable four-character string
    and passed to DISPLAY so operators can read the file status code in the job log.
- name: APPL-RESULT
  level: 1
  picture: S9(9)
  usage: COMP
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Signed nine-digit binary integer used as a return-code accumulator; set to 0 on success, 16 on end-of-file, 12
    on unexpected error, and 8 as a sentinel before each file operation; condition-name APPL-AOK tests for zero and APPL-EOF
    tests for sixteen.
- name: END-OF-FILE
  level: 1
  picture: X(01)
  usage: null
  value: N
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Single-character end-of-file flag initialised to 'N'; set to 'Y' when a sequential READ returns the end-of-file
    status code, which terminates the main processing loop.
- name: ABCODE
  level: 1
  picture: S9(9)
  usage: BINARY
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Signed nine-digit binary integer holding the abend code passed to the Language Environment abnormal-termination
    service CEE3ABD; set to 999 before the call to force a user abend.
- name: TIMING
  level: 1
  picture: S9(9)
  usage: BINARY
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Signed nine-digit binary integer holding the timing option passed to CEE3ABD; set to 0 to request immediate abend
    without a timing delay.
procedure_paragraphs:
- name: END-PERFORM
  reachable: true
  performs:
  - 0000-CUSTFILE-OPEN
  - 1000-CUSTFILE-GET-NEXT
  - 9000-CUSTFILE-CLOSE
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Main inline control block that announces program start, opens the customer file, loops sequentially through all
    records displaying each one, closes the file, and returns to the caller.
- name: GOBACK
  reachable: false
  performs:
  - 0000-CUSTFILE-OPEN
  - 1000-CUSTFILE-GET-NEXT
  - 9000-CUSTFILE-CLOSE
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Static-analysis artifact representing the GOBACK statement that terminates program execution; marked unreachable
    by the CFG tool because it is structurally subsumed by the END-PERFORM node in the extracted control-flow graph.
- name: 1000-CUSTFILE-GET-NEXT
  reachable: true
  performs:
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Reads the next sequential record from CUSTFILE into the CUSTOMER-RECORD working-storage area, sets APPL-RESULT
    to reflect success, end-of-file, or error, and either continues, sets the end-of-file flag, or invokes the error-display
    and abend handlers.
- name: 0000-CUSTFILE-OPEN
  reachable: true
  performs:
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Opens CUSTFILE for sequential input, checks the file status, sets APPL-RESULT to zero on success or twelve on failure,
    and abends the program if the open did not succeed.
- name: 9000-CUSTFILE-CLOSE
  reachable: true
  performs:
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Closes CUSTFILE, checks the file status, resets APPL-RESULT to zero on success or twelve on failure, and abends
    the program if the close did not succeed.
- name: Z-ABEND-PROGRAM
  reachable: true
  performs: []
  goto_targets: []
  summary: Sets TIMING to zero and ABCODE to 999, then calls the IBM Language Environment abnormal-termination service CEE3ABD
    to force an immediate user abend with abend code 999.
- name: Z-DISPLAY-IO-STATUS
  reachable: true
  performs: []
  goto_targets: []
  summary: Formats the two-byte I/O status code into a four-character printable string and displays it on the operator console,
    using the TWO-BYTES-BINARY/TWO-BYTES-ALPHA overlay pair to convert a non-numeric or physical-error status byte into a
    decimal integer.
business_rules:
- id: BR-001
  rule: The customer file must open with status '00'; any other status causes an immediate program abend via CEE3ABD.
  source_paragraph: 0000-CUSTFILE-OPEN
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-002
  rule: A sequential read returning status '00' is treated as a successful record retrieval and the customer record is displayed;
    status '10' signals normal end-of-file and is mapped to APPL-RESULT value 16; any other status is treated as an unrecoverable
    error.
  source_paragraph: 1000-CUSTFILE-GET-NEXT
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-003
  rule: When APPL-RESULT equals 16 (end-of-file condition), the END-OF-FILE flag is set to 'Y', which terminates the main
    processing loop without an abend.
  source_paragraph: 1000-CUSTFILE-GET-NEXT
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-004
  rule: When APPL-RESULT is neither zero nor sixteen after a read attempt, the program displays an error message, formats
    the file status for the operator, and abends unconditionally — no retry or skip logic exists.
  source_paragraph: 1000-CUSTFILE-GET-NEXT
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-005
  rule: The customer file must close with status '00'; any other close status causes an immediate program abend via CEE3ABD.
  source_paragraph: 9000-CUSTFILE-CLOSE
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-006
  rule: When the I/O status is non-numeric or the first status byte is '9' (indicating a physical or hardware error), the
    status is formatted using the TWO-BYTES-BINARY overlay to produce a numeric representation of the second status byte;
    otherwise the status is displayed directly as a four-character code.
  source_paragraph: Z-DISPLAY-IO-STATUS
  rule_type: transform
  confidence: high
  reachable: true
- id: BR-007
  rule: Each successfully read customer record is displayed immediately to the operator console inside the read loop, making
    the program a sequential audit-print utility rather than a transforming batch job.
  source_paragraph: END-PERFORM
  rule_type: display
  confidence: high
  reachable: true
byte_layout:
  file:
  - level: 1
    name: FD-CUSTFILE-REC
    line: 38
    usage: DISPLAY
    fd: CUSTFILE-FILE
    children:
    - level: 5
      name: FD-CUST-ID
      line: 39
      usage: DISPLAY
      pic: 9(09)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 9
      qualified_name: FD-CUSTFILE-REC.FD-CUST-ID
    - level: 5
      name: FD-CUST-DATA
      line: 40
      usage: DISPLAY
      pic: X(491)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 491
      qualified_name: FD-CUSTFILE-REC.FD-CUST-DATA
    slack_bytes_before: 0
    total_bytes: 500
    qualified_name: FD-CUSTFILE-REC
    section: file
  working_storage:
  - level: 1
    name: CUSTOMER-RECORD
    line: 4
    usage: DISPLAY
    children:
    - level: 5
      name: CUST-ID
      line: 5
      usage: DISPLAY
      pic: 9(09)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 9
      qualified_name: CUSTOMER-RECORD.CUST-ID
    - level: 5
      name: CUST-FIRST-NAME
      line: 6
      usage: DISPLAY
      pic: X(25)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 25
      qualified_name: CUSTOMER-RECORD.CUST-FIRST-NAME
    - level: 5
      name: CUST-MIDDLE-NAME
      line: 7
      usage: DISPLAY
      pic: X(25)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 25
      qualified_name: CUSTOMER-RECORD.CUST-MIDDLE-NAME
    - level: 5
      name: CUST-LAST-NAME
      line: 8
      usage: DISPLAY
      pic: X(25)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 25
      qualified_name: CUSTOMER-RECORD.CUST-LAST-NAME
    - level: 5
      name: CUST-ADDR-LINE-1
      line: 9
      usage: DISPLAY
      pic: X(50)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 50
      qualified_name: CUSTOMER-RECORD.CUST-ADDR-LINE-1
    - level: 5
      name: CUST-ADDR-LINE-2
      line: 10
      usage: DISPLAY
      pic: X(50)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 50
      qualified_name: CUSTOMER-RECORD.CUST-ADDR-LINE-2
    - level: 5
      name: CUST-ADDR-LINE-3
      line: 11
      usage: DISPLAY
      pic: X(50)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 50
      qualified_name: CUSTOMER-RECORD.CUST-ADDR-LINE-3
    - level: 5
      name: CUST-ADDR-STATE-CD
      line: 12
      usage: DISPLAY
      pic: X(02)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: CUSTOMER-RECORD.CUST-ADDR-STATE-CD
    - level: 5
      name: CUST-ADDR-COUNTRY-CD
      line: 13
      usage: DISPLAY
      pic: X(03)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: CUSTOMER-RECORD.CUST-ADDR-COUNTRY-CD
    - level: 5
      name: CUST-ADDR-ZIP
      line: 14
      usage: DISPLAY
      pic: X(10)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 10
      qualified_name: CUSTOMER-RECORD.CUST-ADDR-ZIP
    - level: 5
      name: CUST-PHONE-NUM-1
      line: 15
      usage: DISPLAY
      pic: X(15)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 15
      qualified_name: CUSTOMER-RECORD.CUST-PHONE-NUM-1
    - level: 5
      name: CUST-PHONE-NUM-2
      line: 16
      usage: DISPLAY
      pic: X(15)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 15
      qualified_name: CUSTOMER-RECORD.CUST-PHONE-NUM-2
    - level: 5
      name: CUST-SSN
      line: 17
      usage: DISPLAY
      pic: 9(09)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 9
      qualified_name: CUSTOMER-RECORD.CUST-SSN
    - level: 5
      name: CUST-GOVT-ISSUED-ID
      line: 18
      usage: DISPLAY
      pic: X(20)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 20
      qualified_name: CUSTOMER-RECORD.CUST-GOVT-ISSUED-ID
    - level: 5
      name: CUST-DOB-YYYY-MM-DD
      line: 19
      usage: DISPLAY
      pic: X(10)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 10
      qualified_name: CUSTOMER-RECORD.CUST-DOB-YYYY-MM-DD
    - level: 5
      name: CUST-EFT-ACCOUNT-ID
      line: 20
      usage: DISPLAY
      pic: X(10)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 10
      qualified_name: CUSTOMER-RECORD.CUST-EFT-ACCOUNT-ID
    - level: 5
      name: CUST-PRI-CARD-HOLDER-IND
      line: 21
      usage: DISPLAY
      pic: X(01)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: CUSTOMER-RECORD.CUST-PRI-CARD-HOLDER-IND
    - level: 5
      name: CUST-FICO-CREDIT-SCORE
      line: 22
      usage: DISPLAY
      pic: 9(03)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: CUSTOMER-RECORD.CUST-FICO-CREDIT-SCORE
    - level: 5
      name: FILLER
      line: 23
      usage: DISPLAY
      pic: X(168)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 168
      qualified_name: CUSTOMER-RECORD.FILLER
    slack_bytes_before: 0
    total_bytes: 500
    qualified_name: CUSTOMER-RECORD
    section: working_storage
  - level: 1
    name: CUSTFILE-STATUS
    line: 46
    usage: DISPLAY
    children:
    - level: 5
      name: CUSTFILE-STAT1
      line: 47
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: CUSTFILE-STATUS.CUSTFILE-STAT1
    - level: 5
      name: CUSTFILE-STAT2
      line: 48
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: CUSTFILE-STATUS.CUSTFILE-STAT2
    slack_bytes_before: 0
    total_bytes: 2
    qualified_name: CUSTFILE-STATUS
    section: working_storage
  - level: 1
    name: IO-STATUS
    line: 50
    usage: DISPLAY
    children:
    - level: 5
      name: IO-STAT1
      line: 51
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: IO-STATUS.IO-STAT1
    - level: 5
      name: IO-STAT2
      line: 52
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: IO-STATUS.IO-STAT2
    slack_bytes_before: 0
    total_bytes: 2
    qualified_name: IO-STATUS
    section: working_storage
  - level: 1
    name: TWO-BYTES-BINARY
    line: 53
    usage: BINARY
    pic: 9(4)
    children: []
    encoding: binary
    slack_bytes_before: 0
    total_bytes: 2
    qualified_name: TWO-BYTES-BINARY
    section: working_storage
  - level: 1
    name: TWO-BYTES-ALPHA
    line: 54
    redefines: TWO-BYTES-BINARY
    usage: BINARY
    children:
    - level: 5
      name: TWO-BYTES-LEFT
      line: 55
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: TWO-BYTES-ALPHA.TWO-BYTES-LEFT
    - level: 5
      name: TWO-BYTES-RIGHT
      line: 56
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: TWO-BYTES-ALPHA.TWO-BYTES-RIGHT
    total_bytes: 2
    slack_bytes_before: 0
    qualified_name: TWO-BYTES-ALPHA
    section: working_storage
  - level: 1
    name: IO-STATUS-04
    line: 57
    usage: DISPLAY
    children:
    - level: 5
      name: IO-STATUS-0401
      line: 58
      usage: DISPLAY
      pic: '9'
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: IO-STATUS-04.IO-STATUS-0401
    - level: 5
      name: IO-STATUS-0403
      line: 59
      usage: DISPLAY
      pic: '999'
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: IO-STATUS-04.IO-STATUS-0403
    slack_bytes_before: 0
    total_bytes: 4
    qualified_name: IO-STATUS-04
    section: working_storage
  - level: 1
    name: APPL-RESULT
    line: 61
    usage: COMP
    pic: S9(9)
    children: []
    encoding: binary
    slack_bytes_before: 0
    total_bytes: 4
    qualified_name: APPL-RESULT
    section: working_storage
  - level: 1
    name: END-OF-FILE
    line: 65
    usage: DISPLAY
    pic: X(01)
    children: []
    encoding: display
    slack_bytes_before: 0
    total_bytes: 1
    qualified_name: END-OF-FILE
    section: working_storage
  - level: 1
    name: ABCODE
    line: 66
    usage: BINARY
    pic: S9(9)
    children: []
    encoding: binary
    slack_bytes_before: 0
    total_bytes: 4
    qualified_name: ABCODE
    section: working_storage
  - level: 1
    name: TIMING
    line: 67
    usage: BINARY
    pic: S9(9)
    children: []
    encoding: binary
    slack_bytes_before: 0
    total_bytes: 4
    qualified_name: TIMING
    section: working_storage
  linkage: []
  totals:
    working_storage_bytes: 523
    linkage_bytes: 0
fall_through:
  paragraphs:
  - paragraph: CBCUS01C-MAIN
    first_line: 71
    last_line: 87
    terminator: goback
    falls_through_to: null
    last_verb: GOBACK
    last_raw: GOBACK.
    classification_source: annotations
  - paragraph: 1000-CUSTFILE-GET-NEXT
    first_line: 93
    last_line: 116
    terminator: implicit
    falls_through_to: 0000-CUSTFILE-OPEN
    last_verb: EXIT
    last_raw: EXIT.
    classification_source: annotations
  - paragraph: 0000-CUSTFILE-OPEN
    first_line: 119
    last_line: 134
    terminator: implicit
    falls_through_to: 9000-CUSTFILE-CLOSE
    last_verb: EXIT
    last_raw: EXIT.
    classification_source: annotations
  - paragraph: 9000-CUSTFILE-CLOSE
    first_line: 137
    last_line: 152
    terminator: implicit
    falls_through_to: Z-ABEND-PROGRAM
    last_verb: EXIT
    last_raw: EXIT.
    classification_source: annotations
  - paragraph: Z-ABEND-PROGRAM
    first_line: 155
    last_line: 158
    terminator: implicit
    falls_through_to: Z-DISPLAY-IO-STATUS
    last_verb: CALL
    last_raw: CALL 'CEE3ABD' USING ABCODE TIMING.
    classification_source: annotations
  - paragraph: Z-DISPLAY-IO-STATUS
    first_line: 162
    last_line: 174
    terminator: implicit-end-of-program
    falls_through_to: null
    last_verb: EXIT
    last_raw: EXIT.
    classification_source: annotations
  c5_assertion: PASS
  c5_violations: []
paragraph_io:
- paragraph: CBCUS01C-MAIN
  classification_source: annotations
  mutates: []
  reads:
  - fd_name: END-OF-FILE
    verb: IF
    line: 75
    raw: IF END-OF-FILE = 'N'
  - fd_name: CUSTOMER-RECORD
    verb: DISPLAY
    line: 78
    raw: DISPLAY CUSTOMER-RECORD
- paragraph: 1000-CUSTFILE-GET-NEXT
  classification_source: annotations
  mutates:
  - fd_name: APPL-RESULT
    verb: MOVE
    line: 95
    raw: MOVE 0 TO APPL-RESULT
  - fd_name: END-OF-FILE
    verb: MOVE
    line: 108
    raw: MOVE 'Y' TO END-OF-FILE
  - fd_name: IO-STATUS
    verb: MOVE
    line: 111
    raw: MOVE CUSTFILE-STATUS TO IO-STATUS
  reads:
  - fd_name: CUSTFILE-STATUS
    verb: IF
    line: 94
    raw: IF CUSTFILE-STATUS = '00'
  - fd_name: CUSTOMER-RECORD
    verb: DISPLAY
    line: 96
    raw: DISPLAY CUSTOMER-RECORD
  - fd_name: APPL-AOK
    verb: IF
    line: 104
    raw: IF APPL-AOK
  - fd_name: APPL-EOF
    verb: IF
    line: 107
    raw: IF APPL-EOF
- paragraph: 0000-CUSTFILE-OPEN
  classification_source: annotations
  mutates:
  - fd_name: APPL-RESULT
    verb: MOVE
    line: 119
    raw: MOVE 8 TO APPL-RESULT.
  - fd_name: IO-STATUS
    verb: MOVE
    line: 130
    raw: MOVE CUSTFILE-STATUS TO IO-STATUS
  reads:
  - fd_name: CUSTFILE-STATUS
    verb: IF
    line: 121
    raw: IF CUSTFILE-STATUS = '00'
  - fd_name: APPL-AOK
    verb: IF
    line: 126
    raw: IF APPL-AOK
- paragraph: 9000-CUSTFILE-CLOSE
  classification_source: annotations
  mutates:
  - fd_name: APPL-RESULT
    verb: ADD
    line: 137
    raw: ADD 8 TO ZERO GIVING APPL-RESULT.
  - fd_name: IO-STATUS
    verb: MOVE
    line: 148
    raw: MOVE CUSTFILE-STATUS TO IO-STATUS
  reads:
  - fd_name: CUSTFILE-STATUS
    verb: IF
    line: 139
    raw: IF CUSTFILE-STATUS = '00'
  - fd_name: APPL-AOK
    verb: IF
    line: 144
    raw: IF APPL-AOK
- paragraph: Z-ABEND-PROGRAM
  classification_source: annotations
  mutates:
  - fd_name: TIMING
    verb: MOVE
    line: 156
    raw: MOVE 0 TO TIMING
  - fd_name: ABCODE
    verb: MOVE
    line: 157
    raw: MOVE 999 TO ABCODE
  reads: []
- paragraph: Z-DISPLAY-IO-STATUS
  classification_source: annotations
  mutates:
  - fd_name: IO-STATUS-04
    verb: MOVE
    line: 164
    raw: MOVE IO-STAT1 TO IO-STATUS-04(1:1)
  - fd_name: TWO-BYTES-BINARY
    verb: MOVE
    line: 165
    raw: MOVE 0 TO TWO-BYTES-BINARY
  - fd_name: TWO-BYTES-ALPHA.TWO-BYTES-RIGHT
    verb: MOVE
    line: 166
    raw: MOVE IO-STAT2 TO TWO-BYTES-RIGHT
  - fd_name: IO-STATUS-04.IO-STATUS-0403
    verb: MOVE
    line: 167
    raw: MOVE TWO-BYTES-BINARY TO IO-STATUS-0403
  reads:
  - fd_name: IO-STATUS
    verb: IF
    line: 162
    raw: IF IO-STATUS NOT NUMERIC
  - fd_name: IO-STATUS.IO-STAT1
    verb: MOVE
    line: 164
    raw: MOVE IO-STAT1 TO IO-STATUS-04(1:1)
  - fd_name: IO-STATUS.IO-STAT2
    verb: MOVE
    line: 166
    raw: MOVE IO-STAT2 TO TWO-BYTES-RIGHT
  - fd_name: TWO-BYTES-BINARY
    verb: MOVE
    line: 167
    raw: MOVE TWO-BYTES-BINARY TO IO-STATUS-0403
  - fd_name: IO-STATUS-04
    verb: DISPLAY
    line: 168
    raw: 'DISPLAY ''FILE STATUS IS: NNNN'' IO-STATUS-04'
memory_model:
  working_storage_bytes: 523
  linkage_bytes: 0
  global_memory: true
  persistence: process
hercules_parity:
  ready: false
  jcl_reference: null
  input_dataset_sha256: null
  expected_output_sha256: null
  actual_output_sha256: null
  byte_diff_report: null
validation:
  t01_schema_valid: null
  t02_structural_complete: null
  t02r_redefines_complete: null
  t03_functional_score: null
  t04_semantic_score: null
  t05_regression_pass: null
  overall: PENDING
---
# CBCUS01C — Sequential Customer File Print Utility

## Purpose

CBCUS01C is a batch utility program in the CardDemo application that performs a full sequential scan of the customer VSAM KSDS file and prints every customer record to the operator console. It serves as a diagnostic and audit tool: it opens the file, reads records one at a time until end-of-file is reached, displays each record, then closes the file and exits. No transformation, filtering, or update logic is performed; the program's sole output channel is the system console display.

## Runtime Context

The program runs as a standard IBM z/OS batch job step. It requires no CICS infrastructure and issues no EXEC CICS commands. A single VSAM KSDS data set is assigned to the DD name CUSTFILE; the file is opened in sequential (read-only) input mode and traversed from first record to last. On any file-operation failure the program calls the IBM Language Environment service CEE3ABD to force an abnormal termination with abend code 999, ensuring that job-step completion codes are non-zero and upstream schedulers can detect the failure. The customer record layout is brought in through the CVCUS01Y copybook, which defines a 500-byte record containing customer identity, address, contact, and credit-score fields.

## Data Layout

**File Description area.** The raw file record is modelled as a two-field group: a nine-digit numeric customer identifier followed by a 491-byte character data payload. When a record is read with the INTO phrase, the file-description buffer is bypassed and the data is moved directly into the CUSTOMER-RECORD working-storage group defined by the CVCUS01Y copybook.

**CUSTOMER-RECORD (from CVCUS01Y).** This 500-byte group is the primary data structure. It contains the nine-digit customer ID, three 25-character name fields (first, middle, last), three 50-character address lines, a two-character state code, a three-character country code, a ten-character postal code, two 15-character phone numbers, a nine-digit Social Security Number, a 20-character government-issued ID, a ten-character date-of-birth in YYYY-MM-DD format, a ten-character EFT account identifier, a one-character primary card-holder indicator, a three-digit FICO credit score, and a 168-byte filler pad that rounds the record to 500 bytes.

**CUSTFILE-STATUS / IO-STATUS.** Both are two-character group items, each composed of a left and a right single-character subfield. CUSTFILE-STATUS is updated automatically by the runtime after each file operation. IO-STATUS is a staging copy used exclusively within the error-reporting and abend path.

**TWO-BYTES-BINARY / TWO-BYTES-ALPHA — REDEFINES pair.** These two 01-level items share the same two bytes of storage. TWO-BYTES-BINARY declares the storage as a four-digit unsigned binary integer (BINARY usage). TWO-BYTES-ALPHA redefines that same memory as a group of two single-character fields named TWO-BYTES-LEFT and TWO-BYTES-RIGHT. The runtime selector that determines which interpretation is active is the value of IO-STAT1 and the numeric/non-numeric nature of IO-STATUS: when the I/O error is a physical or hardware error (IO-STAT1 equals '9') or when IO-STATUS is not numeric, the program zeroes TWO-BYTES-BINARY, then moves the second status byte into TWO-BYTES-RIGHT via the alpha overlay, and finally reads TWO-BYTES-BINARY back as a decimal integer for display. In the numeric-status path the alpha subfields are not referenced and the storage behaves purely as a binary integer. This dual-interpretation technique avoids a numeric-conversion subroutine and is a common z/OS COBOL idiom for converting a single raw byte to a displayable decimal value.

**IO-STATUS-04.** A four-character group composed of a single leading digit subfield and a three-digit trailing subfield. It is assembled at runtime into a four-character printable representation of the file status code and then displayed. The same memory is also addressable as a four-byte reference-modification target.

**APPL-RESULT.** A signed nine-digit binary (COMP) integer that acts as a return-code accumulator. Two level-88 condition names are defined on it: APPL-AOK is true when the value is zero (operation succeeded) and APPL-EOF is true when the value is sixteen (end-of-file reached). The value 12 is used for unrecoverable errors and 8 is loaded as a sentinel before each file operation.

**END-OF-FILE.** A single-character flag initialised to 'N'; it is set to 'Y' only when end-of-file is confirmed, which causes the outer PERFORM loop to exit normally.

**ABCODE and TIMING.** Two signed nine-digit binary fields used exclusively in the abend handler: ABCODE receives the value 999 and TIMING receives zero before CEE3ABD is called.

## Procedure Logic

### END-PERFORM (main inline control flow)

This is the program's top-level control node as identified by the CFG tool. It represents the inline code in the Procedure Division that executes before any named paragraph. Execution begins by displaying a start-of-program banner to the console. It then calls the file-open paragraph, enters a PERFORM UNTIL loop that iterates as long as the end-of-file flag is 'N', and within each iteration calls the record-read paragraph and, if the flag is still 'N' after the read, displays the customer record. When the loop exits, it calls the file-close paragraph, displays an end-of-program banner, and issues GOBACK to return control to the job scheduler.

### GOBACK

This node is marked unreachable by static analysis and represents the GOBACK statement as a discrete CFG endpoint. In the source it is the final statement of the inline main-block and is always reached at runtime; the CFG tool's reachability classification reflects a graph-traversal artifact rather than genuine dead code. The GOBACK statement terminates the program and returns to the calling environment.

### 1000-CUSTFILE-GET-NEXT

This paragraph performs a single sequential READ of CUSTFILE, directing the record into the CUSTOMER-RECORD working-storage area. It examines CUSTFILE-STATUS immediately after the read: status '00' indicates success and sets APPL-RESULT to zero; status '10' indicates end-of-file and sets APPL-RESULT to sixteen; any other status sets APPL-RESULT to twelve. A second conditional then tests the condition names: if APPL-AOK is true execution continues normally; if APPL-EOF is true the end-of-file flag is set to 'Y'; otherwise an error message is displayed, IO-STATUS is loaded from CUSTFILE-STATUS, and the status-display and abend paragraphs are invoked.

### 0000-CUSTFILE-OPEN

This paragraph loads the sentinel value eight into APPL-RESULT, issues an OPEN INPUT for CUSTFILE, then inspects CUSTFILE-STATUS: status '00' resets APPL-RESULT to zero; any other status sets it to twelve. If APPL-AOK is not true, the paragraph displays an error message, copies the status into IO-STATUS, and delegates to the status-display and abend paragraphs.

### 9000-CUSTFILE-CLOSE

This paragraph uses arithmetic expressions to load the sentinel value eight into APPL-RESULT, issues a CLOSE for CUSTFILE, then inspects CUSTFILE-STATUS using the same success/failure logic as the open paragraph. On failure it displays an error message, copies the status, and calls the error and abend helpers. The use of arithmetic (ADD 8 TO ZERO GIVING and SUBTRACT from self) to set and clear APPL-RESULT is functionally equivalent to simple MOVE statements but is a defensive coding pattern sometimes used to suppress optimizer side-effects.

### Z-ABEND-PROGRAM

This paragraph sets TIMING to zero and ABCODE to 999, then calls the IBM Language Environment abnormal-termination routine CEE3ABD with those two values as parameters, causing the job step to abend with a user abend code of 999 and producing a diagnostic dump for problem analysis.

### Z-DISPLAY-IO-STATUS

This paragraph formats the two-byte IO-STATUS value into a four-character printable string for console display. If IO-STATUS is non-numeric or if the first status byte is '9' (signalling a physical I/O error), it moves the first byte directly into the first position of IO-STATUS-04, zeroes TWO-BYTES-BINARY, moves the second byte into TWO-BYTES-RIGHT via the character overlay, reads the resulting numeric value from TWO-BYTES-BINARY into the three-digit trailing subfield of IO-STATUS-04, and displays the assembled string. For normal numeric status codes it blanks IO-STATUS-04, overlays the last two characters with the status string using reference modification, and displays the result.

## Business Rules Surfaced

**BR-001 — File-open guard.** The customer file must open successfully (status '00'); any failure triggers an immediate abend. There is no retry or alternative open path.

**BR-002 — Read-status classification.** A read status of '00' is the only success indicator; '10' is the sole end-of-file signal; all other codes are fatal errors. This three-way classification means any VSAM exceptional-status code outside '00' and '10' will halt the job.

**BR-003 — End-of-file loop termination.** When the end-of-file result code (16) is set, the END-OF-FILE flag transitions from 'N' to 'Y', which is the only mechanism by which the main read loop exits cleanly.

**BR-004 — No error recovery.** When a read error is not end-of-file, the program neither skips the record nor retries; it displays diagnostics and abends unconditionally. This is a zero-tolerance error policy for unexpected VSAM conditions.

**BR-005 — File-close guard.** The customer file must close successfully; failure causes an abend on the way out, ensuring that the operator is notified even if all records were processed correctly.

**BR-006 — Physical-error status formatting.** When the first status byte is '9' or the status is non-numeric, a byte-level conversion via the TWO-BYTES-BINARY/TWO-BYTES-ALPHA overlay is used to render the second status byte as a decimal number, providing the operator with a meaningful numeric error code rather than a raw binary byte.

**BR-007 — Full-file display policy.** Every successfully read customer record is displayed to the console; there is no filtering predicate, no sampling, and no record count limit, so the program will display the entire contents of the customer file on each execution.

## Graph Summary

- **CALLS:** CBCUS01C -[:CALLS {condition: "APPL-RESULT is not 0 or 16 after file operation failure", call_type: "STATIC"}]-> CEE3ABD
- **COPYBOOKS:** CBCUS01C -[:USES_COPYBOOK]-> CVCUS01Y (app/cpy/CVCUS01Y.cpy) — provides the 500-byte CUSTOMER-RECORD group structure
- **VSAM READS:** CBCUS01C -[:READS]-> CUSTFILE (INDEXED, SEQUENTIAL access, key FD-CUST-ID)
- **PARAGRAPHS (reachable):** END-PERFORM, 1000-CUSTFILE-GET-NEXT, 0000-CUSTFILE-OPEN, 9000-CUSTFILE-CLOSE, Z-ABEND-PROGRAM, Z-DISPLAY-IO-STATUS
- **PARAGRAPHS (unreachable/CFG artifact):** GOBACK
- **REDEFINES:** TWO-BYTES-ALPHA redefines TWO-BYTES-BINARY — two interpretations gated by IO-STAT1 value and numeric status test
- **BUSINESS RULES:** 7 rules surfaced (BR-001 through BR-007); all reachable; types: 5 guard, 1 transform, 1 display
- **DEAD CODE:** No data items flagged dead; GOBACK paragraph flagged unreachable by CFG static analysis (likely a graph-extraction artifact — the statement executes at runtime)
