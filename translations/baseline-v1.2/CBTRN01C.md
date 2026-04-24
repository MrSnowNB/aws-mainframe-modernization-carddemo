---
schema_version: cobol-md/1.2
program_id: CBTRN01C
source_file: app/cbl/CBTRN01C.cbl
source_sha: 6494be3b695bd33f27b39f8d13dc5b510f92b7ed
translation_date: '2026-04-23'
translating_agent: claude-opus-4-5 (subagent)
aifirst_task_id: T-2026-04-23-001
cfg_source: validation/structure/CBTRN01C_cfg.json
business_domain: Transaction Processing
subtype: Batch
author: AWS
date_written: null
lines_of_code: 340
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
  condition: Unrecoverable I/O error detected on any file open, read, or close operation
  call_type: STATIC
called_by: []
copybooks_used:
- name: CVTRA06Y
  path: app/cpy/CVTRA06Y.cpy
  sha: null
- name: CVCUS01Y
  path: app/cpy/CVCUS01Y.cpy
  sha: null
- name: CVACT03Y
  path: app/cpy/CVACT03Y.cpy
  sha: null
- name: CVACT02Y
  path: app/cpy/CVACT02Y.cpy
  sha: null
- name: CVACT01Y
  path: app/cpy/CVACT01Y.cpy
  sha: null
- name: CVTRA05Y
  path: app/cpy/CVTRA05Y.cpy
  sha: null
file_control:
- ddname: DALYTRAN
  organization: SEQUENTIAL
  access: SEQUENTIAL
  record_key: null
  crud:
  - READ
  logical_name: DALYTRAN-FILE
  file_status: DALYTRAN-STATUS
  record_format: FB
  record_length: 350
  input_codepage: IBM-1047
  codepage_default_applied: true
  sign_convention: none
  endianness: big
- ddname: CUSTFILE
  organization: INDEXED
  access: RANDOM
  record_key: FD-CUST-ID
  crud:
  - READ
  logical_name: CUSTOMER-FILE
  file_status: CUSTFILE-STATUS
  record_format: FB
  record_length: 500
  input_codepage: IBM-1047
  codepage_default_applied: true
  sign_convention: mainframe-ebcdic
  endianness: big
- ddname: XREFFILE
  organization: INDEXED
  access: RANDOM
  record_key: FD-XREF-CARD-NUM
  crud:
  - READ
  logical_name: XREF-FILE
  file_status: XREFFILE-STATUS
  record_format: FB
  record_length: 50
  input_codepage: IBM-1047
  codepage_default_applied: true
  sign_convention: none
  endianness: big
- ddname: CARDFILE
  organization: INDEXED
  access: RANDOM
  record_key: FD-CARD-NUM
  crud:
  - READ
  logical_name: CARD-FILE
  file_status: CARDFILE-STATUS
  record_format: FB
  record_length: 150
  input_codepage: IBM-1047
  codepage_default_applied: true
  sign_convention: none
  endianness: big
- ddname: ACCTFILE
  organization: INDEXED
  access: RANDOM
  record_key: FD-ACCT-ID
  crud:
  - READ
  logical_name: ACCOUNT-FILE
  file_status: ACCTFILE-STATUS
  record_format: FB
  record_length: 300
  input_codepage: IBM-1047
  codepage_default_applied: true
  sign_convention: mainframe-ebcdic
  endianness: big
- ddname: TRANFILE
  organization: INDEXED
  access: RANDOM
  record_key: FD-TRANS-ID
  crud:
  - READ
  logical_name: TRANSACT-FILE
  file_status: TRANFILE-STATUS
  record_format: FB
  record_length: 350
  input_codepage: IBM-1047
  codepage_default_applied: true
  sign_convention: none
  endianness: big
cics_commands: []
transaction_ids: []
data_items:
- name: FD-TRAN-RECORD
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Root record layout for the daily transaction sequential input file; contains a 16-character transaction identifier
    followed by 334 bytes of payload data
- name: FD-CUSTFILE-REC
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Root record layout for the customer VSAM indexed file; primary key is a 9-digit numeric customer identifier
- name: FD-XREFFILE-REC
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Root record layout for the card-to-account cross-reference VSAM indexed file; primary key is the 16-character
    card number
- name: FD-CARDFILE-REC
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Root record layout for the card detail VSAM indexed file; primary key is the 16-character card number
- name: FD-ACCTFILE-REC
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Root record layout for the account VSAM indexed file; primary key is an 11-digit numeric account identifier
- name: FD-TRANFILE-REC
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Root record layout for the posted-transaction VSAM indexed file; primary key is a 16-character transaction identifier
- name: DALYTRAN-STATUS
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Two-character file status code returned by the operating system after each I/O operation on the daily transaction
    sequential file
- name: CUSTFILE-STATUS
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Two-character file status code for the customer VSAM indexed file; populated after every open, read, and close
- name: XREFFILE-STATUS
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Two-character file status code for the card cross-reference VSAM indexed file; used to detect invalid-key conditions
    during random reads
- name: CARDFILE-STATUS
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Two-character file status code for the card detail VSAM indexed file
- name: ACCTFILE-STATUS
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Two-character file status code for the account VSAM indexed file; used to detect invalid-key conditions during
    random account reads
- name: TRANFILE-STATUS
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Two-character file status code for the posted-transaction VSAM indexed file
- name: IO-STATUS
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Staging area that holds the file status code from the most recently failed I/O operation before it is formatted
    and displayed by Z-DISPLAY-IO-STATUS
- name: TWO-BYTES-BINARY
  level: 1
  picture: 9(4)
  usage: BINARY
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Two-byte binary integer workspace used to convert a single file-status character (IO-STAT2) into a displayable
    three-digit decimal number for non-standard status codes
- name: TWO-BYTES-ALPHA
  level: 1
  picture: null
  usage: BINARY
  value: null
  redefines: TWO-BYTES-BINARY
  redefines_interpretations:
  - condition: IO-STAT1 = '9' (non-numeric, vendor-specific file status in IO-STATUS)
    interpreted_as: Two single-character fields (TWO-BYTES-LEFT and TWO-BYTES-RIGHT) overlaying the same two bytes; IO-STAT2
      is moved into TWO-BYTES-RIGHT so that TWO-BYTES-BINARY can be read as an integer for display
    encoding: DISPLAY
  - condition: IO-STATUS is numeric and IO-STAT1 is not '9' (standard ANSI file status)
    interpreted_as: The two bytes are treated as a packed integer holding the numeric file status value, allowing it to be
      extracted and moved into the three-digit display field IO-STATUS-0403
    encoding: BINARY
  dead_code_flag: false
  semantic: Character overlay of TWO-BYTES-BINARY; exposes left and right byte positions independently so that non-numeric
    file status codes can be decomposed and converted to a printable four-character diagnostic string
- name: IO-STATUS-04
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Four-character formatted I/O status diagnostic buffer composed of a one-digit severity prefix (IO-STATUS-0401)
    and a three-digit numeric status code (IO-STATUS-0403); displayed to the operator on error
- name: APPL-RESULT
  level: 1
  picture: S9(9)
  usage: COMP
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Signed 9-digit binary application return code set after each file operation; condition name APPL-AOK (value 0)
    signals success, APPL-EOF (value 16) signals end-of-file, and any other non-zero value triggers abend
- name: END-OF-DAILY-TRANS-FILE
  level: 1
  picture: X(01)
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Single-character end-of-file sentinel; initialized to 'N' and set to 'Y' when the daily transaction file returns
    a status-10 (end-of-file) condition, terminating the main processing loop
- name: ABCODE
  level: 1
  picture: S9(9)
  usage: BINARY
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Abend code passed to the Language Environment CEE3ABD service; set to 999 before the abnormal termination call
- name: TIMING
  level: 1
  picture: S9(9)
  usage: BINARY
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Timing parameter passed to CEE3ABD alongside ABCODE; set to 0 (immediate abend) before each abnormal termination
    call
- name: WS-MISC-VARIABLES
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Group item holding runtime read-status accumulators for the cross-reference and account file lookups; used to
    gate downstream processing within the main transaction loop
procedure_paragraphs:
- name: MAIN-PARA
  reachable: true
  performs:
  - 0000-DALYTRAN-OPEN
  - 0100-CUSTFILE-OPEN
  - 0200-XREFFILE-OPEN
  - 0300-CARDFILE-OPEN
  - 0400-ACCTFILE-OPEN
  - 0500-TRANFILE-OPEN
  - 1000-DALYTRAN-GET-NEXT
  - 2000-LOOKUP-XREF
  - 3000-READ-ACCOUNT
  - 9000-DALYTRAN-CLOSE
  - 9100-CUSTFILE-CLOSE
  - 9200-XREFFILE-CLOSE
  - 9300-CARDFILE-CLOSE
  - 9400-ACCTFILE-CLOSE
  - 9500-TRANFILE-CLOSE
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Program entry point that opens all six files, drives the sequential read-validate loop over the daily transaction
    file, and closes all files before returning control to the operating system via GOBACK
- name: END-PERFORM
  reachable: false
  performs: []
  goto_targets: []
  summary: CFG artifact node representing the syntactic end of the PERFORM UNTIL loop in MAIN-PARA; not a separately callable
    paragraph and marked unreachable by static analysis
- name: GOBACK
  reachable: false
  performs: []
  goto_targets: []
  summary: CFG artifact node representing the GOBACK statement that returns control to the caller; marked unreachable by static
    analysis as it is reached only via fall-through from the last executable statement in MAIN-PARA
- name: 1000-DALYTRAN-GET-NEXT
  reachable: true
  performs:
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Reads the next record from the daily transaction sequential file into working storage, sets APPL-RESULT to reflect
    success, end-of-file, or error, and abends on any unexpected I/O failure
- name: 2000-LOOKUP-XREF
  reachable: true
  performs: []
  goto_targets: []
  summary: Performs a random keyed read of the card cross-reference VSAM file using the card number from the current transaction
    record, setting WS-XREF-READ-STATUS to 4 if the card number is not found
- name: END-READ
  reachable: false
  performs: []
  goto_targets: []
  summary: CFG artifact node representing the syntactic END-READ delimiter within 2000-LOOKUP-XREF; not a callable paragraph
    and marked unreachable by static analysis
- name: 3000-READ-ACCOUNT
  reachable: true
  performs: []
  goto_targets: []
  summary: Performs a random keyed read of the account VSAM file using the account identifier resolved from the cross-reference
    record, setting WS-ACCT-READ-STATUS to 4 if the account is not found
- name: 0000-DALYTRAN-OPEN
  reachable: true
  performs:
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Opens the daily transaction sequential file for input and abends the program if the open fails
- name: 0100-CUSTFILE-OPEN
  reachable: true
  performs:
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Opens the customer VSAM indexed file for input and abends the program if the open fails
- name: 0200-XREFFILE-OPEN
  reachable: true
  performs:
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Opens the card cross-reference VSAM indexed file for input and abends the program if the open fails
- name: 0300-CARDFILE-OPEN
  reachable: true
  performs:
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Opens the card detail VSAM indexed file for input and abends the program if the open fails
- name: 0400-ACCTFILE-OPEN
  reachable: true
  performs:
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Opens the account VSAM indexed file for input and abends the program if the open fails
- name: 0500-TRANFILE-OPEN
  reachable: true
  performs:
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Opens the posted-transaction VSAM indexed file for input and abends the program if the open fails
- name: 9000-DALYTRAN-CLOSE
  reachable: true
  performs:
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Closes the daily transaction sequential file and abends the program if the close operation fails
- name: 9100-CUSTFILE-CLOSE
  reachable: true
  performs:
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Closes the customer VSAM indexed file and abends the program if the close operation fails
- name: 9200-XREFFILE-CLOSE
  reachable: true
  performs:
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Closes the card cross-reference VSAM indexed file and abends the program if the close operation fails
- name: 9300-CARDFILE-CLOSE
  reachable: true
  performs:
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Closes the card detail VSAM indexed file and abends the program if the close operation fails
- name: 9400-ACCTFILE-CLOSE
  reachable: true
  performs:
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Closes the account VSAM indexed file and abends the program if the close operation fails
- name: 9500-TRANFILE-CLOSE
  reachable: true
  performs:
  - Z-DISPLAY-IO-STATUS
  - Z-ABEND-PROGRAM
  goto_targets: []
  summary: Closes the posted-transaction VSAM indexed file and abends the program if the close operation fails
- name: Z-ABEND-PROGRAM
  reachable: true
  performs: []
  goto_targets: []
  summary: Sets ABCODE to 999 and TIMING to 0 then calls the Language Environment CEE3ABD service to force an abnormal termination
    with a user abend code, terminating the job step
- name: Z-DISPLAY-IO-STATUS
  reachable: true
  performs: []
  goto_targets: []
  summary: Formats the two-character IO-STATUS into a four-character printable diagnostic string (handling both numeric and
    non-numeric status codes) and displays it to the operator before an abend
business_rules:
- id: BR-001
  rule: All six files (daily transaction, customer, cross-reference, card, account, and posted-transaction) must be successfully
    opened before any transaction processing begins; a failure on any file open triggers an immediate abend with CEE3ABD code
    999
  source_paragraph: MAIN-PARA
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-002
  rule: The main processing loop continues reading and validating transaction records sequentially until the daily transaction
    file signals end-of-file, at which point the sentinel END-OF-DAILY-TRANS-FILE is set to 'Y' and the loop terminates
  source_paragraph: MAIN-PARA
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-003
  rule: Each transaction record read from the daily file is immediately displayed to the system log before any cross-reference
    lookup is performed, provided end-of-file has not been reached
  source_paragraph: MAIN-PARA
  rule_type: display
  confidence: high
  reachable: true
- id: BR-004
  rule: The card number extracted from each daily transaction record must be validated against the card cross-reference VSAM
    file; if the card number is not found (WS-XREF-READ-STATUS is set to 4), the transaction is skipped with a diagnostic
    message and no account lookup is attempted
  source_paragraph: MAIN-PARA
  rule_type: lookup
  confidence: high
  reachable: true
- id: BR-005
  rule: When a card number cannot be verified in the cross-reference file, a diagnostic message identifying the unverifiable
    card number and the skipped transaction identifier is written to the operator console, and the transaction record is abandoned
    without further processing
  source_paragraph: MAIN-PARA
  rule_type: audit
  confidence: high
  reachable: true
- id: BR-006
  rule: Only when cross-reference lookup succeeds (WS-XREF-READ-STATUS equals zero) is the resolved account identifier used
    to perform a further lookup against the account VSAM file
  source_paragraph: MAIN-PARA
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-007
  rule: If the account record resolved through the cross-reference is not found in the account VSAM file (WS-ACCT-READ-STATUS
    is non-zero), a diagnostic message naming the missing account identifier is displayed, but no abend is triggered and processing
    continues with the next transaction
  source_paragraph: MAIN-PARA
  rule_type: audit
  confidence: high
  reachable: true
- id: BR-008
  rule: 'A read of the daily transaction file that returns a status code other than ''00'' (success) or ''10'' (end-of-file)
    is treated as an unrecoverable I/O error: the status code is formatted and displayed, then CEE3ABD is called with abend
    code 999 to terminate the job'
  source_paragraph: 1000-DALYTRAN-GET-NEXT
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-009
  rule: A status code of '10' returned from the daily transaction file read is the only normal termination signal; it sets
    END-OF-DAILY-TRANS-FILE to 'Y', which causes the PERFORM UNTIL loop to exit cleanly
  source_paragraph: 1000-DALYTRAN-GET-NEXT
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-010
  rule: When a random read of the cross-reference VSAM file returns INVALID KEY, the card number is flagged as unverifiable
    by setting WS-XREF-READ-STATUS to 4, and a diagnostic message is written to the console
  source_paragraph: 2000-LOOKUP-XREF
  rule_type: lookup
  confidence: high
  reachable: true
- id: BR-011
  rule: When a random read of the account VSAM file returns INVALID KEY, WS-ACCT-READ-STATUS is set to 4 and a diagnostic
    message is written to the console; the condition is non-fatal and processing resumes with the next record
  source_paragraph: 3000-READ-ACCOUNT
  rule_type: lookup
  confidence: high
  reachable: true
- id: BR-012
  rule: Any file open or close operation that does not return status '00' is mapped to APPL-RESULT value 12 (error), which
    causes Z-DISPLAY-IO-STATUS and Z-ABEND-PROGRAM to be called, terminating the job with abend code 999
  source_paragraph: 0000-DALYTRAN-OPEN
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-013
  rule: Non-numeric file status codes (IO-STAT1 equal to '9') are decoded by overlaying TWO-BYTES-BINARY with TWO-BYTES-ALPHA
    so that the vendor-specific second byte can be converted to a displayable three-digit decimal before operator notification
  source_paragraph: Z-DISPLAY-IO-STATUS
  rule_type: transform
  confidence: high
  reachable: true
byte_layout:
  file:
  - level: 1
    name: FD-TRAN-RECORD
    line: 67
    usage: DISPLAY
    fd: DALYTRAN-FILE
    children:
    - level: 5
      name: FD-TRAN-ID
      line: 68
      usage: DISPLAY
      pic: X(16)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 16
      qualified_name: FD-TRAN-RECORD.FD-TRAN-ID
    - level: 5
      name: FD-CUST-DATA
      line: 69
      usage: DISPLAY
      pic: X(334)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 334
      qualified_name: FD-TRAN-RECORD.FD-CUST-DATA
    slack_bytes_before: 0
    total_bytes: 350
    qualified_name: FD-TRAN-RECORD
    section: file
  - level: 1
    name: FD-CUSTFILE-REC
    line: 72
    usage: DISPLAY
    fd: CUSTOMER-FILE
    children:
    - level: 5
      name: FD-CUST-ID
      line: 73
      usage: DISPLAY
      pic: 9(09)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 9
      qualified_name: FD-CUSTFILE-REC.FD-CUST-ID
    - level: 5
      name: FD-CUST-DATA
      line: 74
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
  - level: 1
    name: FD-XREFFILE-REC
    line: 77
    usage: DISPLAY
    fd: XREF-FILE
    children:
    - level: 5
      name: FD-XREF-CARD-NUM
      line: 78
      usage: DISPLAY
      pic: X(16)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 16
      qualified_name: FD-XREFFILE-REC.FD-XREF-CARD-NUM
    - level: 5
      name: FD-XREF-DATA
      line: 79
      usage: DISPLAY
      pic: X(34)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 34
      qualified_name: FD-XREFFILE-REC.FD-XREF-DATA
    slack_bytes_before: 0
    total_bytes: 50
    qualified_name: FD-XREFFILE-REC
    section: file
  - level: 1
    name: FD-CARDFILE-REC
    line: 82
    usage: DISPLAY
    fd: CARD-FILE
    children:
    - level: 5
      name: FD-CARD-NUM
      line: 83
      usage: DISPLAY
      pic: X(16)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 16
      qualified_name: FD-CARDFILE-REC.FD-CARD-NUM
    - level: 5
      name: FD-CARD-DATA
      line: 84
      usage: DISPLAY
      pic: X(134)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 134
      qualified_name: FD-CARDFILE-REC.FD-CARD-DATA
    slack_bytes_before: 0
    total_bytes: 150
    qualified_name: FD-CARDFILE-REC
    section: file
  - level: 1
    name: FD-ACCTFILE-REC
    line: 87
    usage: DISPLAY
    fd: ACCOUNT-FILE
    children:
    - level: 5
      name: FD-ACCT-ID
      line: 88
      usage: DISPLAY
      pic: 9(11)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 11
      qualified_name: FD-ACCTFILE-REC.FD-ACCT-ID
    - level: 5
      name: FD-ACCT-DATA
      line: 89
      usage: DISPLAY
      pic: X(289)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 289
      qualified_name: FD-ACCTFILE-REC.FD-ACCT-DATA
    slack_bytes_before: 0
    total_bytes: 300
    qualified_name: FD-ACCTFILE-REC
    section: file
  - level: 1
    name: FD-TRANFILE-REC
    line: 92
    usage: DISPLAY
    fd: TRANSACT-FILE
    children:
    - level: 5
      name: FD-TRANS-ID
      line: 93
      usage: DISPLAY
      pic: X(16)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 16
      qualified_name: FD-TRANFILE-REC.FD-TRANS-ID
    - level: 5
      name: FD-ACCT-DATA
      line: 94
      usage: DISPLAY
      pic: X(334)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 334
      qualified_name: FD-TRANFILE-REC.FD-ACCT-DATA
    slack_bytes_before: 0
    total_bytes: 350
    qualified_name: FD-TRANFILE-REC
    section: file
  working_storage:
  - level: 1
    name: DALYTRAN-RECORD
    line: 4
    usage: DISPLAY
    children:
    - level: 5
      name: DALYTRAN-ID
      line: 5
      usage: DISPLAY
      pic: X(16)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 16
      qualified_name: DALYTRAN-RECORD.DALYTRAN-ID
    - level: 5
      name: DALYTRAN-TYPE-CD
      line: 6
      usage: DISPLAY
      pic: X(02)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: DALYTRAN-RECORD.DALYTRAN-TYPE-CD
    - level: 5
      name: DALYTRAN-CAT-CD
      line: 7
      usage: DISPLAY
      pic: 9(04)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: DALYTRAN-RECORD.DALYTRAN-CAT-CD
    - level: 5
      name: DALYTRAN-SOURCE
      line: 8
      usage: DISPLAY
      pic: X(10)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 10
      qualified_name: DALYTRAN-RECORD.DALYTRAN-SOURCE
    - level: 5
      name: DALYTRAN-DESC
      line: 9
      usage: DISPLAY
      pic: X(100)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 100
      qualified_name: DALYTRAN-RECORD.DALYTRAN-DESC
    - level: 5
      name: DALYTRAN-AMT
      line: 10
      usage: DISPLAY
      pic: S9(09)V99
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 11
      qualified_name: DALYTRAN-RECORD.DALYTRAN-AMT
    - level: 5
      name: DALYTRAN-MERCHANT-ID
      line: 11
      usage: DISPLAY
      pic: 9(09)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 9
      qualified_name: DALYTRAN-RECORD.DALYTRAN-MERCHANT-ID
    - level: 5
      name: DALYTRAN-MERCHANT-NAME
      line: 12
      usage: DISPLAY
      pic: X(50)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 50
      qualified_name: DALYTRAN-RECORD.DALYTRAN-MERCHANT-NAME
    - level: 5
      name: DALYTRAN-MERCHANT-CITY
      line: 13
      usage: DISPLAY
      pic: X(50)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 50
      qualified_name: DALYTRAN-RECORD.DALYTRAN-MERCHANT-CITY
    - level: 5
      name: DALYTRAN-MERCHANT-ZIP
      line: 14
      usage: DISPLAY
      pic: X(10)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 10
      qualified_name: DALYTRAN-RECORD.DALYTRAN-MERCHANT-ZIP
    - level: 5
      name: DALYTRAN-CARD-NUM
      line: 15
      usage: DISPLAY
      pic: X(16)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 16
      qualified_name: DALYTRAN-RECORD.DALYTRAN-CARD-NUM
    - level: 5
      name: DALYTRAN-ORIG-TS
      line: 16
      usage: DISPLAY
      pic: X(26)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 26
      qualified_name: DALYTRAN-RECORD.DALYTRAN-ORIG-TS
    - level: 5
      name: DALYTRAN-PROC-TS
      line: 17
      usage: DISPLAY
      pic: X(26)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 26
      qualified_name: DALYTRAN-RECORD.DALYTRAN-PROC-TS
    - level: 5
      name: FILLER
      line: 18
      usage: DISPLAY
      pic: X(20)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 20
      qualified_name: DALYTRAN-RECORD.FILLER
    slack_bytes_before: 0
    total_bytes: 350
    qualified_name: DALYTRAN-RECORD
    section: working_storage
  - level: 1
    name: DALYTRAN-STATUS
    line: 100
    usage: DISPLAY
    children:
    - level: 5
      name: DALYTRAN-STAT1
      line: 101
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DALYTRAN-STATUS.DALYTRAN-STAT1
    - level: 5
      name: DALYTRAN-STAT2
      line: 102
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DALYTRAN-STATUS.DALYTRAN-STAT2
    slack_bytes_before: 0
    total_bytes: 2
    qualified_name: DALYTRAN-STATUS
    section: working_storage
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
    line: 105
    usage: DISPLAY
    children:
    - level: 5
      name: CUSTFILE-STAT1
      line: 106
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: CUSTFILE-STATUS.CUSTFILE-STAT1
    - level: 5
      name: CUSTFILE-STAT2
      line: 107
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
    name: CARD-XREF-RECORD
    line: 4
    usage: DISPLAY
    children:
    - level: 5
      name: XREF-CARD-NUM
      line: 5
      usage: DISPLAY
      pic: X(16)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 16
      qualified_name: CARD-XREF-RECORD.XREF-CARD-NUM
    - level: 5
      name: XREF-CUST-ID
      line: 6
      usage: DISPLAY
      pic: 9(09)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 9
      qualified_name: CARD-XREF-RECORD.XREF-CUST-ID
    - level: 5
      name: XREF-ACCT-ID
      line: 7
      usage: DISPLAY
      pic: 9(11)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 11
      qualified_name: CARD-XREF-RECORD.XREF-ACCT-ID
    - level: 5
      name: FILLER
      line: 8
      usage: DISPLAY
      pic: X(14)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 14
      qualified_name: CARD-XREF-RECORD.FILLER
    slack_bytes_before: 0
    total_bytes: 50
    qualified_name: CARD-XREF-RECORD
    section: working_storage
  - level: 1
    name: XREFFILE-STATUS
    line: 110
    usage: DISPLAY
    children:
    - level: 5
      name: XREFFILE-STAT1
      line: 111
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: XREFFILE-STATUS.XREFFILE-STAT1
    - level: 5
      name: XREFFILE-STAT2
      line: 112
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: XREFFILE-STATUS.XREFFILE-STAT2
    slack_bytes_before: 0
    total_bytes: 2
    qualified_name: XREFFILE-STATUS
    section: working_storage
  - level: 1
    name: CARD-RECORD
    line: 4
    usage: DISPLAY
    children:
    - level: 5
      name: CARD-NUM
      line: 5
      usage: DISPLAY
      pic: X(16)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 16
      qualified_name: CARD-RECORD.CARD-NUM
    - level: 5
      name: CARD-ACCT-ID
      line: 6
      usage: DISPLAY
      pic: 9(11)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 11
      qualified_name: CARD-RECORD.CARD-ACCT-ID
    - level: 5
      name: CARD-CVV-CD
      line: 7
      usage: DISPLAY
      pic: 9(03)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: CARD-RECORD.CARD-CVV-CD
    - level: 5
      name: CARD-EMBOSSED-NAME
      line: 8
      usage: DISPLAY
      pic: X(50)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 50
      qualified_name: CARD-RECORD.CARD-EMBOSSED-NAME
    - level: 5
      name: CARD-EXPIRAION-DATE
      line: 9
      usage: DISPLAY
      pic: X(10)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 10
      qualified_name: CARD-RECORD.CARD-EXPIRAION-DATE
    - level: 5
      name: CARD-ACTIVE-STATUS
      line: 10
      usage: DISPLAY
      pic: X(01)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: CARD-RECORD.CARD-ACTIVE-STATUS
    - level: 5
      name: FILLER
      line: 11
      usage: DISPLAY
      pic: X(59)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 59
      qualified_name: CARD-RECORD.FILLER
    slack_bytes_before: 0
    total_bytes: 150
    qualified_name: CARD-RECORD
    section: working_storage
  - level: 1
    name: CARDFILE-STATUS
    line: 115
    usage: DISPLAY
    children:
    - level: 5
      name: CARDFILE-STAT1
      line: 116
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: CARDFILE-STATUS.CARDFILE-STAT1
    - level: 5
      name: CARDFILE-STAT2
      line: 117
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: CARDFILE-STATUS.CARDFILE-STAT2
    slack_bytes_before: 0
    total_bytes: 2
    qualified_name: CARDFILE-STATUS
    section: working_storage
  - level: 1
    name: ACCOUNT-RECORD
    line: 4
    usage: DISPLAY
    children:
    - level: 5
      name: ACCT-ID
      line: 5
      usage: DISPLAY
      pic: 9(11)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 11
      qualified_name: ACCOUNT-RECORD.ACCT-ID
    - level: 5
      name: ACCT-ACTIVE-STATUS
      line: 6
      usage: DISPLAY
      pic: X(01)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: ACCOUNT-RECORD.ACCT-ACTIVE-STATUS
    - level: 5
      name: ACCT-CURR-BAL
      line: 7
      usage: DISPLAY
      pic: S9(10)V99
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 12
      qualified_name: ACCOUNT-RECORD.ACCT-CURR-BAL
    - level: 5
      name: ACCT-CREDIT-LIMIT
      line: 8
      usage: DISPLAY
      pic: S9(10)V99
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 12
      qualified_name: ACCOUNT-RECORD.ACCT-CREDIT-LIMIT
    - level: 5
      name: ACCT-CASH-CREDIT-LIMIT
      line: 9
      usage: DISPLAY
      pic: S9(10)V99
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 12
      qualified_name: ACCOUNT-RECORD.ACCT-CASH-CREDIT-LIMIT
    - level: 5
      name: ACCT-OPEN-DATE
      line: 10
      usage: DISPLAY
      pic: X(10)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 10
      qualified_name: ACCOUNT-RECORD.ACCT-OPEN-DATE
    - level: 5
      name: ACCT-EXPIRAION-DATE
      line: 11
      usage: DISPLAY
      pic: X(10)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 10
      qualified_name: ACCOUNT-RECORD.ACCT-EXPIRAION-DATE
    - level: 5
      name: ACCT-REISSUE-DATE
      line: 12
      usage: DISPLAY
      pic: X(10)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 10
      qualified_name: ACCOUNT-RECORD.ACCT-REISSUE-DATE
    - level: 5
      name: ACCT-CURR-CYC-CREDIT
      line: 13
      usage: DISPLAY
      pic: S9(10)V99
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 12
      qualified_name: ACCOUNT-RECORD.ACCT-CURR-CYC-CREDIT
    - level: 5
      name: ACCT-CURR-CYC-DEBIT
      line: 14
      usage: DISPLAY
      pic: S9(10)V99
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 12
      qualified_name: ACCOUNT-RECORD.ACCT-CURR-CYC-DEBIT
    - level: 5
      name: ACCT-ADDR-ZIP
      line: 15
      usage: DISPLAY
      pic: X(10)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 10
      qualified_name: ACCOUNT-RECORD.ACCT-ADDR-ZIP
    - level: 5
      name: ACCT-GROUP-ID
      line: 16
      usage: DISPLAY
      pic: X(10)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 10
      qualified_name: ACCOUNT-RECORD.ACCT-GROUP-ID
    - level: 5
      name: FILLER
      line: 17
      usage: DISPLAY
      pic: X(178)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 178
      qualified_name: ACCOUNT-RECORD.FILLER
    slack_bytes_before: 0
    total_bytes: 300
    qualified_name: ACCOUNT-RECORD
    section: working_storage
  - level: 1
    name: ACCTFILE-STATUS
    line: 120
    usage: DISPLAY
    children:
    - level: 5
      name: ACCTFILE-STAT1
      line: 121
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: ACCTFILE-STATUS.ACCTFILE-STAT1
    - level: 5
      name: ACCTFILE-STAT2
      line: 122
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: ACCTFILE-STATUS.ACCTFILE-STAT2
    slack_bytes_before: 0
    total_bytes: 2
    qualified_name: ACCTFILE-STATUS
    section: working_storage
  - level: 1
    name: TRAN-RECORD
    line: 4
    usage: DISPLAY
    children:
    - level: 5
      name: TRAN-ID
      line: 5
      usage: DISPLAY
      pic: X(16)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 16
      qualified_name: TRAN-RECORD.TRAN-ID
    - level: 5
      name: TRAN-TYPE-CD
      line: 6
      usage: DISPLAY
      pic: X(02)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: TRAN-RECORD.TRAN-TYPE-CD
    - level: 5
      name: TRAN-CAT-CD
      line: 7
      usage: DISPLAY
      pic: 9(04)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: TRAN-RECORD.TRAN-CAT-CD
    - level: 5
      name: TRAN-SOURCE
      line: 8
      usage: DISPLAY
      pic: X(10)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 10
      qualified_name: TRAN-RECORD.TRAN-SOURCE
    - level: 5
      name: TRAN-DESC
      line: 9
      usage: DISPLAY
      pic: X(100)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 100
      qualified_name: TRAN-RECORD.TRAN-DESC
    - level: 5
      name: TRAN-AMT
      line: 10
      usage: DISPLAY
      pic: S9(09)V99
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 11
      qualified_name: TRAN-RECORD.TRAN-AMT
    - level: 5
      name: TRAN-MERCHANT-ID
      line: 11
      usage: DISPLAY
      pic: 9(09)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 9
      qualified_name: TRAN-RECORD.TRAN-MERCHANT-ID
    - level: 5
      name: TRAN-MERCHANT-NAME
      line: 12
      usage: DISPLAY
      pic: X(50)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 50
      qualified_name: TRAN-RECORD.TRAN-MERCHANT-NAME
    - level: 5
      name: TRAN-MERCHANT-CITY
      line: 13
      usage: DISPLAY
      pic: X(50)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 50
      qualified_name: TRAN-RECORD.TRAN-MERCHANT-CITY
    - level: 5
      name: TRAN-MERCHANT-ZIP
      line: 14
      usage: DISPLAY
      pic: X(10)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 10
      qualified_name: TRAN-RECORD.TRAN-MERCHANT-ZIP
    - level: 5
      name: TRAN-CARD-NUM
      line: 15
      usage: DISPLAY
      pic: X(16)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 16
      qualified_name: TRAN-RECORD.TRAN-CARD-NUM
    - level: 5
      name: TRAN-ORIG-TS
      line: 16
      usage: DISPLAY
      pic: X(26)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 26
      qualified_name: TRAN-RECORD.TRAN-ORIG-TS
    - level: 5
      name: TRAN-PROC-TS
      line: 17
      usage: DISPLAY
      pic: X(26)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 26
      qualified_name: TRAN-RECORD.TRAN-PROC-TS
    - level: 5
      name: FILLER
      line: 18
      usage: DISPLAY
      pic: X(20)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 20
      qualified_name: TRAN-RECORD.FILLER
    slack_bytes_before: 0
    total_bytes: 350
    qualified_name: TRAN-RECORD
    section: working_storage
  - level: 1
    name: TRANFILE-STATUS
    line: 125
    usage: DISPLAY
    children:
    - level: 5
      name: TRANFILE-STAT1
      line: 126
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: TRANFILE-STATUS.TRANFILE-STAT1
    - level: 5
      name: TRANFILE-STAT2
      line: 127
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: TRANFILE-STATUS.TRANFILE-STAT2
    slack_bytes_before: 0
    total_bytes: 2
    qualified_name: TRANFILE-STATUS
    section: working_storage
  - level: 1
    name: IO-STATUS
    line: 129
    usage: DISPLAY
    children:
    - level: 5
      name: IO-STAT1
      line: 130
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: IO-STATUS.IO-STAT1
    - level: 5
      name: IO-STAT2
      line: 131
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
    line: 133
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
    line: 134
    redefines: TWO-BYTES-BINARY
    usage: BINARY
    children:
    - level: 5
      name: TWO-BYTES-LEFT
      line: 135
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: TWO-BYTES-ALPHA.TWO-BYTES-LEFT
    - level: 5
      name: TWO-BYTES-RIGHT
      line: 136
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
    line: 138
    usage: DISPLAY
    children:
    - level: 5
      name: IO-STATUS-0401
      line: 139
      usage: DISPLAY
      pic: '9'
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: IO-STATUS-04.IO-STATUS-0401
    - level: 5
      name: IO-STATUS-0403
      line: 140
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
    line: 142
    usage: COMP
    pic: S9(9)
    children: []
    encoding: binary
    slack_bytes_before: 0
    total_bytes: 4
    qualified_name: APPL-RESULT
    section: working_storage
  - level: 1
    name: END-OF-DAILY-TRANS-FILE
    line: 146
    usage: DISPLAY
    pic: X(01)
    children: []
    encoding: display
    slack_bytes_before: 0
    total_bytes: 1
    qualified_name: END-OF-DAILY-TRANS-FILE
    section: working_storage
  - level: 1
    name: ABCODE
    line: 147
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
    line: 148
    usage: BINARY
    pic: S9(9)
    children: []
    encoding: binary
    slack_bytes_before: 0
    total_bytes: 4
    qualified_name: TIMING
    section: working_storage
  - level: 1
    name: WS-MISC-VARIABLES
    line: 149
    usage: DISPLAY
    children:
    - level: 5
      name: WS-XREF-READ-STATUS
      line: 150
      usage: DISPLAY
      pic: 9(04)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: WS-MISC-VARIABLES.WS-XREF-READ-STATUS
    - level: 5
      name: WS-ACCT-READ-STATUS
      line: 151
      usage: DISPLAY
      pic: 9(04)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: WS-MISC-VARIABLES.WS-ACCT-READ-STATUS
    slack_bytes_before: 0
    total_bytes: 8
    qualified_name: WS-MISC-VARIABLES
    section: working_storage
  linkage: []
  totals:
    working_storage_bytes: 1741
    linkage_bytes: 0
fall_through:
  paragraphs:
  - paragraph: MAIN-PARA
    first_line: 156
    last_line: 197
    terminator: goback
    falls_through_to: null
    last_verb: GOBACK
    last_raw: GOBACK.
    classification_source: annotations
  - paragraph: 1000-DALYTRAN-GET-NEXT
    first_line: 203
    last_line: 225
    terminator: implicit
    falls_through_to: 2000-LOOKUP-XREF
    last_verb: EXIT
    last_raw: EXIT.
    classification_source: annotations
  - paragraph: 2000-LOOKUP-XREF
    first_line: 228
    last_line: 238
    terminator: implicit
    falls_through_to: 3000-READ-ACCOUNT
    last_verb: DISPLAY
    last_raw: 'DISPLAY ''CUSTOMER ID: '' XREF-CUST-ID'
    classification_source: annotations
  - paragraph: 3000-READ-ACCOUNT
    first_line: 242
    last_line: 249
    terminator: implicit
    falls_through_to: 0000-DALYTRAN-OPEN
    last_verb: DISPLAY
    last_raw: DISPLAY 'SUCCESSFUL READ OF ACCOUNT FILE'
    classification_source: annotations
  - paragraph: 0000-DALYTRAN-OPEN
    first_line: 253
    last_line: 268
    terminator: implicit
    falls_through_to: 0100-CUSTFILE-OPEN
    last_verb: EXIT
    last_raw: EXIT.
    classification_source: annotations
  - paragraph: 0100-CUSTFILE-OPEN
    first_line: 272
    last_line: 287
    terminator: implicit
    falls_through_to: 0200-XREFFILE-OPEN
    last_verb: EXIT
    last_raw: EXIT.
    classification_source: annotations
  - paragraph: 0200-XREFFILE-OPEN
    first_line: 290
    last_line: 305
    terminator: implicit
    falls_through_to: 0300-CARDFILE-OPEN
    last_verb: EXIT
    last_raw: EXIT.
    classification_source: annotations
  - paragraph: 0300-CARDFILE-OPEN
    first_line: 308
    last_line: 323
    terminator: implicit
    falls_through_to: 0400-ACCTFILE-OPEN
    last_verb: EXIT
    last_raw: EXIT.
    classification_source: annotations
  - paragraph: 0400-ACCTFILE-OPEN
    first_line: 326
    last_line: 341
    terminator: implicit
    falls_through_to: 0500-TRANFILE-OPEN
    last_verb: EXIT
    last_raw: EXIT.
    classification_source: annotations
  - paragraph: 0500-TRANFILE-OPEN
    first_line: 344
    last_line: 359
    terminator: implicit
    falls_through_to: 9000-DALYTRAN-CLOSE
    last_verb: EXIT
    last_raw: EXIT.
    classification_source: annotations
  - paragraph: 9000-DALYTRAN-CLOSE
    first_line: 362
    last_line: 377
    terminator: implicit
    falls_through_to: 9100-CUSTFILE-CLOSE
    last_verb: EXIT
    last_raw: EXIT.
    classification_source: annotations
  - paragraph: 9100-CUSTFILE-CLOSE
    first_line: 380
    last_line: 395
    terminator: implicit
    falls_through_to: 9200-XREFFILE-CLOSE
    last_verb: EXIT
    last_raw: EXIT.
    classification_source: annotations
  - paragraph: 9200-XREFFILE-CLOSE
    first_line: 398
    last_line: 413
    terminator: implicit
    falls_through_to: 9300-CARDFILE-CLOSE
    last_verb: EXIT
    last_raw: EXIT.
    classification_source: annotations
  - paragraph: 9300-CARDFILE-CLOSE
    first_line: 416
    last_line: 431
    terminator: implicit
    falls_through_to: 9400-ACCTFILE-CLOSE
    last_verb: EXIT
    last_raw: EXIT.
    classification_source: annotations
  - paragraph: 9400-ACCTFILE-CLOSE
    first_line: 434
    last_line: 449
    terminator: implicit
    falls_through_to: 9500-TRANFILE-CLOSE
    last_verb: EXIT
    last_raw: EXIT.
    classification_source: annotations
  - paragraph: 9500-TRANFILE-CLOSE
    first_line: 452
    last_line: 467
    terminator: implicit
    falls_through_to: Z-ABEND-PROGRAM
    last_verb: EXIT
    last_raw: EXIT.
    classification_source: annotations
  - paragraph: Z-ABEND-PROGRAM
    first_line: 470
    last_line: 473
    terminator: implicit
    falls_through_to: Z-DISPLAY-IO-STATUS
    last_verb: CALL
    last_raw: CALL 'CEE3ABD' USING ABCODE TIMING.
    classification_source: annotations
  - paragraph: Z-DISPLAY-IO-STATUS
    first_line: 477
    last_line: 489
    terminator: implicit-end-of-program
    falls_through_to: null
    last_verb: EXIT
    last_raw: EXIT.
    classification_source: annotations
  c5_assertion: PASS
  c5_violations: []
paragraph_io:
- paragraph: MAIN-PARA
  classification_source: annotations
  mutates:
  - fd_name: WS-MISC-VARIABLES.WS-XREF-READ-STATUS
    verb: MOVE
    line: 170
    raw: MOVE 0 TO WS-XREF-READ-STATUS
  - fd_name: CARD-XREF-RECORD.XREF-CARD-NUM
    verb: MOVE
    line: 171
    raw: MOVE DALYTRAN-CARD-NUM TO XREF-CARD-NUM
  - fd_name: WS-MISC-VARIABLES.WS-ACCT-READ-STATUS
    verb: MOVE
    line: 174
    raw: MOVE 0 TO WS-ACCT-READ-STATUS
  - fd_name: ACCOUNT-RECORD.ACCT-ID
    verb: MOVE
    line: 175
    raw: MOVE XREF-ACCT-ID TO ACCT-ID
  reads:
  - fd_name: END-OF-DAILY-TRANS-FILE
    verb: IF
    line: 165
    raw: IF END-OF-DAILY-TRANS-FILE = 'N'
  - fd_name: DALYTRAN-RECORD
    verb: DISPLAY
    line: 168
    raw: DISPLAY DALYTRAN-RECORD
  - fd_name: DALYTRAN-RECORD.DALYTRAN-CARD-NUM
    verb: MOVE
    line: 171
    raw: MOVE DALYTRAN-CARD-NUM TO XREF-CARD-NUM
  - fd_name: WS-MISC-VARIABLES.WS-XREF-READ-STATUS
    verb: IF
    line: 173
    raw: IF WS-XREF-READ-STATUS = 0
  - fd_name: CARD-XREF-RECORD.XREF-ACCT-ID
    verb: MOVE
    line: 175
    raw: MOVE XREF-ACCT-ID TO ACCT-ID
  - fd_name: WS-MISC-VARIABLES.WS-ACCT-READ-STATUS
    verb: IF
    line: 177
    raw: IF WS-ACCT-READ-STATUS NOT = 0
  - fd_name: ACCOUNT-RECORD.ACCT-ID
    verb: DISPLAY
    line: 178
    raw: DISPLAY 'ACCOUNT ' ACCT-ID ' NOT FOUND'
- paragraph: 1000-DALYTRAN-GET-NEXT
  classification_source: annotations
  mutates:
  - fd_name: APPL-RESULT
    verb: MOVE
    line: 205
    raw: MOVE 0 TO APPL-RESULT
  - fd_name: END-OF-DAILY-TRANS-FILE
    verb: MOVE
    line: 217
    raw: MOVE 'Y' TO END-OF-DAILY-TRANS-FILE
  - fd_name: IO-STATUS
    verb: MOVE
    line: 220
    raw: MOVE DALYTRAN-STATUS TO IO-STATUS
  reads:
  - fd_name: DALYTRAN-STATUS
    verb: IF
    line: 204
    raw: IF DALYTRAN-STATUS = '00'
  - fd_name: APPL-AOK
    verb: IF
    line: 213
    raw: IF APPL-AOK
  - fd_name: APPL-EOF
    verb: IF
    line: 216
    raw: IF APPL-EOF
- paragraph: 2000-LOOKUP-XREF
  classification_source: annotations
  mutates:
  - fd_name: FD-XREFFILE-REC.FD-XREF-CARD-NUM
    verb: MOVE
    line: 228
    raw: MOVE XREF-CARD-NUM TO FD-XREF-CARD-NUM
  - fd_name: WS-MISC-VARIABLES.WS-XREF-READ-STATUS
    verb: MOVE
    line: 233
    raw: MOVE 4 TO WS-XREF-READ-STATUS
  reads:
  - fd_name: CARD-XREF-RECORD.XREF-CARD-NUM
    verb: MOVE
    line: 228
    raw: MOVE XREF-CARD-NUM TO FD-XREF-CARD-NUM
  - fd_name: CARD-XREF-RECORD.XREF-ACCT-ID
    verb: DISPLAY
    line: 237
    raw: 'DISPLAY ''ACCOUNT ID : '' XREF-ACCT-ID'
  - fd_name: CARD-XREF-RECORD.XREF-CUST-ID
    verb: DISPLAY
    line: 238
    raw: 'DISPLAY ''CUSTOMER ID: '' XREF-CUST-ID'
- paragraph: 3000-READ-ACCOUNT
  classification_source: annotations
  mutates:
  - fd_name: FD-ACCTFILE-REC.FD-ACCT-ID
    verb: MOVE
    line: 242
    raw: MOVE ACCT-ID TO FD-ACCT-ID
  - fd_name: WS-MISC-VARIABLES.WS-ACCT-READ-STATUS
    verb: MOVE
    line: 247
    raw: MOVE 4 TO WS-ACCT-READ-STATUS
  reads:
  - fd_name: ACCOUNT-RECORD.ACCT-ID
    verb: MOVE
    line: 242
    raw: MOVE ACCT-ID TO FD-ACCT-ID
- paragraph: 0000-DALYTRAN-OPEN
  classification_source: annotations
  mutates:
  - fd_name: APPL-RESULT
    verb: MOVE
    line: 253
    raw: MOVE 8 TO APPL-RESULT.
  - fd_name: IO-STATUS
    verb: MOVE
    line: 264
    raw: MOVE DALYTRAN-STATUS TO IO-STATUS
  reads:
  - fd_name: DALYTRAN-STATUS
    verb: IF
    line: 255
    raw: IF DALYTRAN-STATUS = '00'
  - fd_name: APPL-AOK
    verb: IF
    line: 260
    raw: IF APPL-AOK
- paragraph: 0100-CUSTFILE-OPEN
  classification_source: annotations
  mutates:
  - fd_name: APPL-RESULT
    verb: MOVE
    line: 272
    raw: MOVE 8 TO APPL-RESULT.
  - fd_name: IO-STATUS
    verb: MOVE
    line: 283
    raw: MOVE CUSTFILE-STATUS TO IO-STATUS
  reads:
  - fd_name: CUSTFILE-STATUS
    verb: IF
    line: 274
    raw: IF CUSTFILE-STATUS = '00'
  - fd_name: APPL-AOK
    verb: IF
    line: 279
    raw: IF APPL-AOK
- paragraph: 0200-XREFFILE-OPEN
  classification_source: annotations
  mutates:
  - fd_name: APPL-RESULT
    verb: MOVE
    line: 290
    raw: MOVE 8 TO APPL-RESULT.
  - fd_name: IO-STATUS
    verb: MOVE
    line: 301
    raw: MOVE XREFFILE-STATUS TO IO-STATUS
  reads:
  - fd_name: XREFFILE-STATUS
    verb: IF
    line: 292
    raw: IF XREFFILE-STATUS = '00'
  - fd_name: APPL-AOK
    verb: IF
    line: 297
    raw: IF APPL-AOK
- paragraph: 0300-CARDFILE-OPEN
  classification_source: annotations
  mutates:
  - fd_name: APPL-RESULT
    verb: MOVE
    line: 308
    raw: MOVE 8 TO APPL-RESULT.
  - fd_name: IO-STATUS
    verb: MOVE
    line: 319
    raw: MOVE CARDFILE-STATUS TO IO-STATUS
  reads:
  - fd_name: CARDFILE-STATUS
    verb: IF
    line: 310
    raw: IF CARDFILE-STATUS = '00'
  - fd_name: APPL-AOK
    verb: IF
    line: 315
    raw: IF APPL-AOK
- paragraph: 0400-ACCTFILE-OPEN
  classification_source: annotations
  mutates:
  - fd_name: APPL-RESULT
    verb: MOVE
    line: 326
    raw: MOVE 8 TO APPL-RESULT.
  - fd_name: IO-STATUS
    verb: MOVE
    line: 337
    raw: MOVE ACCTFILE-STATUS TO IO-STATUS
  reads:
  - fd_name: ACCTFILE-STATUS
    verb: IF
    line: 328
    raw: IF ACCTFILE-STATUS = '00'
  - fd_name: APPL-AOK
    verb: IF
    line: 333
    raw: IF APPL-AOK
- paragraph: 0500-TRANFILE-OPEN
  classification_source: annotations
  mutates:
  - fd_name: APPL-RESULT
    verb: MOVE
    line: 344
    raw: MOVE 8 TO APPL-RESULT.
  - fd_name: IO-STATUS
    verb: MOVE
    line: 355
    raw: MOVE TRANFILE-STATUS TO IO-STATUS
  reads:
  - fd_name: TRANFILE-STATUS
    verb: IF
    line: 346
    raw: IF TRANFILE-STATUS = '00'
  - fd_name: APPL-AOK
    verb: IF
    line: 351
    raw: IF APPL-AOK
- paragraph: 9000-DALYTRAN-CLOSE
  classification_source: annotations
  mutates:
  - fd_name: APPL-RESULT
    verb: ADD
    line: 362
    raw: ADD 8 TO ZERO GIVING APPL-RESULT.
  - fd_name: IO-STATUS
    verb: MOVE
    line: 373
    raw: MOVE CUSTFILE-STATUS TO IO-STATUS
  reads:
  - fd_name: DALYTRAN-STATUS
    verb: IF
    line: 364
    raw: IF DALYTRAN-STATUS = '00'
  - fd_name: APPL-AOK
    verb: IF
    line: 369
    raw: IF APPL-AOK
  - fd_name: CUSTFILE-STATUS
    verb: MOVE
    line: 373
    raw: MOVE CUSTFILE-STATUS TO IO-STATUS
- paragraph: 9100-CUSTFILE-CLOSE
  classification_source: annotations
  mutates:
  - fd_name: APPL-RESULT
    verb: ADD
    line: 380
    raw: ADD 8 TO ZERO GIVING APPL-RESULT.
  - fd_name: IO-STATUS
    verb: MOVE
    line: 391
    raw: MOVE CUSTFILE-STATUS TO IO-STATUS
  reads:
  - fd_name: CUSTFILE-STATUS
    verb: IF
    line: 382
    raw: IF CUSTFILE-STATUS = '00'
  - fd_name: APPL-AOK
    verb: IF
    line: 387
    raw: IF APPL-AOK
- paragraph: 9200-XREFFILE-CLOSE
  classification_source: annotations
  mutates:
  - fd_name: APPL-RESULT
    verb: ADD
    line: 398
    raw: ADD 8 TO ZERO GIVING APPL-RESULT.
  - fd_name: IO-STATUS
    verb: MOVE
    line: 409
    raw: MOVE XREFFILE-STATUS TO IO-STATUS
  reads:
  - fd_name: XREFFILE-STATUS
    verb: IF
    line: 400
    raw: IF XREFFILE-STATUS = '00'
  - fd_name: APPL-AOK
    verb: IF
    line: 405
    raw: IF APPL-AOK
- paragraph: 9300-CARDFILE-CLOSE
  classification_source: annotations
  mutates:
  - fd_name: APPL-RESULT
    verb: ADD
    line: 416
    raw: ADD 8 TO ZERO GIVING APPL-RESULT.
  - fd_name: IO-STATUS
    verb: MOVE
    line: 427
    raw: MOVE CARDFILE-STATUS TO IO-STATUS
  reads:
  - fd_name: CARDFILE-STATUS
    verb: IF
    line: 418
    raw: IF CARDFILE-STATUS = '00'
  - fd_name: APPL-AOK
    verb: IF
    line: 423
    raw: IF APPL-AOK
- paragraph: 9400-ACCTFILE-CLOSE
  classification_source: annotations
  mutates:
  - fd_name: APPL-RESULT
    verb: ADD
    line: 434
    raw: ADD 8 TO ZERO GIVING APPL-RESULT.
  - fd_name: IO-STATUS
    verb: MOVE
    line: 445
    raw: MOVE ACCTFILE-STATUS TO IO-STATUS
  reads:
  - fd_name: ACCTFILE-STATUS
    verb: IF
    line: 436
    raw: IF ACCTFILE-STATUS = '00'
  - fd_name: APPL-AOK
    verb: IF
    line: 441
    raw: IF APPL-AOK
- paragraph: 9500-TRANFILE-CLOSE
  classification_source: annotations
  mutates:
  - fd_name: APPL-RESULT
    verb: ADD
    line: 452
    raw: ADD 8 TO ZERO GIVING APPL-RESULT.
  - fd_name: IO-STATUS
    verb: MOVE
    line: 463
    raw: MOVE TRANFILE-STATUS TO IO-STATUS
  reads:
  - fd_name: TRANFILE-STATUS
    verb: IF
    line: 454
    raw: IF TRANFILE-STATUS = '00'
  - fd_name: APPL-AOK
    verb: IF
    line: 459
    raw: IF APPL-AOK
- paragraph: Z-ABEND-PROGRAM
  classification_source: annotations
  mutates:
  - fd_name: TIMING
    verb: MOVE
    line: 471
    raw: MOVE 0 TO TIMING
  - fd_name: ABCODE
    verb: MOVE
    line: 472
    raw: MOVE 999 TO ABCODE
  reads: []
- paragraph: Z-DISPLAY-IO-STATUS
  classification_source: annotations
  mutates:
  - fd_name: IO-STATUS-04
    verb: MOVE
    line: 479
    raw: MOVE IO-STAT1 TO IO-STATUS-04(1:1)
  - fd_name: TWO-BYTES-BINARY
    verb: MOVE
    line: 480
    raw: MOVE 0 TO TWO-BYTES-BINARY
  - fd_name: TWO-BYTES-ALPHA.TWO-BYTES-RIGHT
    verb: MOVE
    line: 481
    raw: MOVE IO-STAT2 TO TWO-BYTES-RIGHT
  - fd_name: IO-STATUS-04.IO-STATUS-0403
    verb: MOVE
    line: 482
    raw: MOVE TWO-BYTES-BINARY TO IO-STATUS-0403
  reads:
  - fd_name: IO-STATUS
    verb: IF
    line: 477
    raw: IF IO-STATUS NOT NUMERIC
  - fd_name: IO-STATUS.IO-STAT1
    verb: MOVE
    line: 479
    raw: MOVE IO-STAT1 TO IO-STATUS-04(1:1)
  - fd_name: IO-STATUS.IO-STAT2
    verb: MOVE
    line: 481
    raw: MOVE IO-STAT2 TO TWO-BYTES-RIGHT
  - fd_name: TWO-BYTES-BINARY
    verb: MOVE
    line: 482
    raw: MOVE TWO-BYTES-BINARY TO IO-STATUS-0403
  - fd_name: IO-STATUS-04
    verb: DISPLAY
    line: 483
    raw: 'DISPLAY ''FILE STATUS IS: NNNN'' IO-STATUS-04'
memory_model:
  working_storage_bytes: 1741
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
# CBTRN01C — Daily Transaction File Processor and Cross-Reference Validator

## Purpose

CBTRN01C is a batch COBOL program in the CardDemo application that reads a daily transaction file sequentially and validates each transaction record against a set of VSAM reference files. For every incoming transaction, the program verifies that the card number can be resolved to an account via the card cross-reference file, and then confirms that the resolved account exists in the account master file. The program serves as the first-stage intake filter for the daily transaction posting pipeline, surfacing data-quality problems through operator console messages and aborting the job on unrecoverable I/O errors.

## Runtime Context

The program executes as a z/OS batch job step under IBM Enterprise COBOL with no CICS or DB2 involvement. It opens six VSAM or sequential files at startup — the daily transaction sequential input file (DALYTRAN), a customer indexed file (CUSTFILE), a card-to-account cross-reference indexed file (XREFFILE), a card detail indexed file (CARDFILE), an account indexed file (ACCTFILE), and a posted-transaction indexed file (TRANFILE) — performs all processing in memory, and closes all six files before returning. The program makes one outbound static call: to the Language Environment service CEE3ABD, which is invoked exclusively on unrecoverable error paths to force a user abend with code 999. No records are written or updated during normal processing; the program is read-only against all VSAM stores. Operator diagnostics are emitted to the system console via DISPLAY statements throughout.

## Data Layout

### File Section Records

The file section defines six root-level record layouts, one per file. The daily transaction record (FD-TRAN-RECORD) presents a 16-character transaction identifier field followed by 334 bytes of unstructured payload; the detailed field decomposition for the payload is supplied by the CVTRA06Y copybook, which overlays the working-storage copy area DALYTRAN-RECORD. The customer file record (FD-CUSTFILE-REC) exposes a 9-digit numeric primary key (FD-CUST-ID) and a 491-byte data area; its working-storage expansion is provided by CVCUS01Y. The cross-reference file record (FD-XREFFILE-REC) exposes a 16-character card number key (FD-XREF-CARD-NUM) and a 34-byte data area; its detail layout is provided by CVACT03Y. The card file record (FD-CARDFILE-REC) exposes a 16-character card number (FD-CARD-NUM) and a 134-byte data area; its layout is provided by CVACT02Y. The account file record (FD-ACCTFILE-REC) exposes an 11-digit numeric account key (FD-ACCT-ID) and a 289-byte data area; its layout is provided by CVACT01Y. The posted-transaction file record (FD-TRANFILE-REC) exposes a 16-character transaction key (FD-TRANS-ID) and a 334-byte data area; its layout is provided by CVTRA05Y.

### File Status and I/O Control Areas

Each of the six files has a corresponding two-character file status working-storage group (DALYTRAN-STATUS, CUSTFILE-STATUS, XREFFILE-STATUS, CARDFILE-STATUS, ACCTFILE-STATUS, TRANFILE-STATUS), each split into a left character (first status digit) and a right character (second status digit). A shared staging area, IO-STATUS, receives a copy of the failing file's status code before error display.

### REDEFINES: TWO-BYTES-BINARY / TWO-BYTES-ALPHA

The single REDEFINES clause in this program overlays a two-byte binary integer (TWO-BYTES-BINARY, a 4-digit binary field occupying two bytes) with a character group (TWO-BYTES-ALPHA) that exposes the same storage as two independent single-character fields: TWO-BYTES-LEFT and TWO-BYTES-RIGHT.

The runtime selection between the two interpretations is driven by the value of IO-STAT1 within the IO-STATUS group. When IO-STAT1 equals the character '9' — indicating a vendor-specific, non-standard file status — the I/O status display logic moves the right-hand byte (IO-STAT2) into TWO-BYTES-RIGHT via the character view, then reads TWO-BYTES-BINARY as an integer to obtain the numeric equivalent for display. When IO-STAT1 is not '9' and IO-STATUS is fully numeric — indicating a standard ANSI file status — the two bytes are treated as a packed integer value directly, and the numeric status is moved into the three-digit display field IO-STATUS-0403.

This dual-interpretation mechanism is necessary because IBM z/OS file systems can return non-numeric status codes (beginning with '9') for hardware- or vendor-specific error conditions, which cannot be handled by simple numeric formatting.

### Application Result and Sentinel Flags

APPL-RESULT is a signed binary integer that encodes the outcome of each file operation using condition names: APPL-AOK (value 0) means success, APPL-EOF (value 16) means end-of-file. END-OF-DAILY-TRANS-FILE is a single-character flag initialized to 'N' that acts as the loop termination sentinel. ABCODE and TIMING are binary parameters prepared immediately before each call to CEE3ABD. The WS-MISC-VARIABLES group holds two 4-digit numeric fields — WS-XREF-READ-STATUS and WS-ACCT-READ-STATUS — that capture the outcome of each VSAM random read and gate downstream validation steps.

## Procedure Logic

### MAIN-PARA

The program entry point opens all six files in sequence by performing the six open paragraphs (0000 through 0500). It then enters a PERFORM UNTIL loop that runs as long as END-OF-DAILY-TRANS-FILE is not 'Y'. Within each iteration, if the end-of-file sentinel is still 'N', the program calls 1000-DALYTRAN-GET-NEXT to fetch the next record. If the file is not yet exhausted, the retrieved transaction record is displayed to the console. The card number from the transaction is then moved to the cross-reference key field, WS-XREF-READ-STATUS is zeroed, and 2000-LOOKUP-XREF is called. If the cross-reference lookup succeeds (WS-XREF-READ-STATUS remains zero), WS-ACCT-READ-STATUS is zeroed, the account identifier from the cross-reference record is moved to the account key, and 3000-READ-ACCOUNT is called; if the account is not found, a diagnostic message is displayed. If the cross-reference lookup fails, a diagnostic message naming the unverifiable card number and skipped transaction identifier is displayed and the transaction is abandoned. After the loop exits, the program calls the six close paragraphs (9000 through 9500) in sequence, displays an end-of-execution message, and exits via GOBACK.

### END-PERFORM

This is a CFG artifact node that marks the syntactic boundary of the PERFORM UNTIL construct in MAIN-PARA. It is not a callable paragraph; static analysis marks it unreachable.

### GOBACK

This is a CFG artifact node representing the GOBACK statement at the end of MAIN-PARA. Static analysis marks it unreachable as a standalone node because control reaches it by falling through MAIN-PARA rather than by a separate PERFORM.

### 1000-DALYTRAN-GET-NEXT

This paragraph issues a sequential READ against the daily transaction file, moving the data into the DALYTRAN-RECORD working-storage area. A status of '00' sets APPL-RESULT to zero (APPL-AOK). A status of '10' sets APPL-RESULT to 16 (APPL-EOF), which causes the sentinel END-OF-DAILY-TRANS-FILE to be set to 'Y'. Any other status is treated as an unrecoverable error: the status code is copied to IO-STATUS, Z-DISPLAY-IO-STATUS is called to format and print the error, and Z-ABEND-PROGRAM is called to terminate the job.

### 2000-LOOKUP-XREF

This paragraph moves the card number to the VSAM key field FD-XREF-CARD-NUM and issues a random READ of XREF-FILE using that key. On an INVALID KEY condition — meaning the card number is absent from the cross-reference index — a diagnostic message is displayed and WS-XREF-READ-STATUS is set to 4 to signal failure to the caller. On a successful NOT INVALID KEY condition, the resolved card number, account identifier, and customer identifier from the cross-reference record are displayed to the console and WS-XREF-READ-STATUS remains zero.

### END-READ

This is a CFG artifact node marking the END-READ delimiter inside 2000-LOOKUP-XREF. Static analysis marks it unreachable as a standalone callable unit.

### 3000-READ-ACCOUNT

This paragraph moves the account identifier (resolved from the cross-reference) to the VSAM key field FD-ACCT-ID and issues a random READ of ACCOUNT-FILE. On an INVALID KEY condition, a diagnostic message is displayed and WS-ACCT-READ-STATUS is set to 4. On a successful read, a confirmation message is displayed and WS-ACCT-READ-STATUS remains zero. Unlike a failed cross-reference lookup, a failed account read is non-fatal; the main loop continues to the next transaction.

### 0000-DALYTRAN-OPEN

Sets APPL-RESULT to 8 (tentative error), then opens the daily transaction sequential file for INPUT. If DALYTRAN-STATUS is '00', APPL-RESULT is set to 0 (success). Otherwise it is set to 12 (error). If APPL-RESULT is not APPL-AOK, the error message and status code are displayed and the program abends.

### 0100-CUSTFILE-OPEN

Opens the customer VSAM indexed file for INPUT using the same guard logic as 0000-DALYTRAN-OPEN; abends on any status other than '00'.

### 0200-XREFFILE-OPEN

Opens the card cross-reference VSAM indexed file for INPUT; abends on any status other than '00'.

### 0300-CARDFILE-OPEN

Opens the card detail VSAM indexed file for INPUT; abends on any status other than '00'.

### 0400-ACCTFILE-OPEN

Opens the account VSAM indexed file for INPUT; abends on any status other than '00'.

### 0500-TRANFILE-OPEN

Opens the posted-transaction VSAM indexed file for INPUT; abends on any status other than '00'.

### 9000-DALYTRAN-CLOSE

Closes the daily transaction sequential file using the standard guard pattern; abends if DALYTRAN-STATUS is not '00' after the close.

### 9100-CUSTFILE-CLOSE

Closes the customer VSAM indexed file; abends if CUSTFILE-STATUS is not '00'.

### 9200-XREFFILE-CLOSE

Closes the card cross-reference VSAM indexed file; abends if XREFFILE-STATUS is not '00'.

### 9300-CARDFILE-CLOSE

Closes the card detail VSAM indexed file; abends if CARDFILE-STATUS is not '00'.

### 9400-ACCTFILE-CLOSE

Closes the account VSAM indexed file; abends if ACCTFILE-STATUS is not '00'.

### 9500-TRANFILE-CLOSE

Closes the posted-transaction VSAM indexed file; abends if TRANFILE-STATUS is not '00'.

### Z-ABEND-PROGRAM

Moves zero to TIMING and 999 to ABCODE, then issues a static call to the IBM Language Environment service CEE3ABD passing ABCODE and TIMING. This forces an immediate user abend, writing a dump and setting the job step return code to a non-zero value. There is no return from this paragraph under any circumstances.

### Z-DISPLAY-IO-STATUS

Examines IO-STATUS to determine whether the status code is numeric and whether IO-STAT1 is not the character '9'. For standard ANSI numeric status codes, a four-character display string is constructed by placing '00' in the leading positions and moving the two-character status into the trailing positions. For non-numeric or vendor-specific codes (IO-STAT1 equals '9'), the TWO-BYTES-ALPHA redefine is used to copy IO-STAT2 into the right byte of TWO-BYTES-BINARY, whose integer value is then moved to IO-STATUS-0403 for display. In both branches the formatted four-character status string is emitted to the operator console.

## Business Rules Surfaced

**BR-001** — All six files must open successfully before any transaction is processed; failure on any file open causes an immediate job abend with code 999.

**BR-002** — The processing loop iterates until the daily transaction file signals end-of-file, at which point END-OF-DAILY-TRANS-FILE is set to 'Y' and the loop exits cleanly.

**BR-003** — Every successfully read transaction record is echoed to the system console before cross-reference validation begins.

**BR-004** — Each transaction's card number must resolve to an entry in the cross-reference VSAM file; an INVALID KEY result (WS-XREF-READ-STATUS = 4) causes the transaction to be skipped entirely.

**BR-005** — When a card number cannot be verified, a console message identifying the card number and the associated transaction identifier is issued, providing an audit trail of skipped transactions.

**BR-006** — Account lookup (3000-READ-ACCOUNT) is only performed when the cross-reference lookup succeeds; WS-XREF-READ-STATUS must be zero before the account read is attempted.

**BR-007** — A missing account record (WS-ACCT-READ-STATUS non-zero) is logged to the console but is non-fatal; the program continues processing subsequent transactions rather than aborting.

**BR-008** — Any daily transaction file read status other than '00' or '10' is an unrecoverable error that causes the status to be formatted and displayed, then triggers CEE3ABD abend code 999.

**BR-009** — A file status of '10' on the daily transaction read is the sole normal termination condition; it sets the end-of-file sentinel and terminates the loop.

**BR-010** — A failed XREF-FILE random read (INVALID KEY) sets WS-XREF-READ-STATUS to 4 and writes a diagnostic to the console.

**BR-011** — A failed ACCOUNT-FILE random read (INVALID KEY) sets WS-ACCT-READ-STATUS to 4 and writes a diagnostic to the console, but does not abort processing.

**BR-012** — Any file open or close that returns a status other than '00' sets APPL-RESULT to 12 and triggers Z-DISPLAY-IO-STATUS followed by Z-ABEND-PROGRAM, terminating the job.

**BR-013** — Non-numeric (vendor-specific) file status codes are decoded by using the TWO-BYTES-ALPHA character overlay of TWO-BYTES-BINARY to extract and convert the second byte into a printable three-digit decimal before display.

## Graph Summary

- **CALLS**: CBTRN01C —[STATIC, on unrecoverable I/O error]--> CEE3ABD
- **COPYBOOKS**: CBTRN01C uses CVTRA06Y (daily transaction record layout), CVCUS01Y (customer record layout), CVACT03Y (card cross-reference record layout), CVACT02Y (card detail record layout), CVACT01Y (account record layout), CVTRA05Y (posted-transaction record layout)
- **VSAM READS**: CBTRN01C reads DALYTRAN (sequential, all records), XREFFILE (random by card number, each transaction), ACCTFILE (random by account ID, each verified transaction)
- **VSAM OPENS (read-only, no writes)**: CUSTFILE, CARDFILE, TRANFILE opened for input but no records are read from them in the current implementation
- **RULES**: BR-001 (guard — all files must open), BR-002 (guard — EOF terminates loop), BR-003 (display — echo each transaction), BR-004 (lookup — card-xref guard), BR-005 (audit — skip message for unverifiable card), BR-006 (guard — xref success gates account lookup), BR-007 (audit — missing account non-fatal), BR-008 (guard — read error abends job), BR-009 (guard — EOF-10 terminates normally), BR-010 (lookup — xref INVALID KEY), BR-011 (lookup — account INVALID KEY), BR-012 (guard — open/close error abends job), BR-013 (transform — non-numeric status decoding)
- **DEAD CODE**: END-PERFORM, GOBACK, and END-READ are CFG artifact nodes marked unreachable by static analysis; no live code paragraphs are unreachable
- **ABEND PATHS**: Any file open failure, any file close failure, or any daily transaction read error other than end-of-file calls Z-DISPLAY-IO-STATUS then Z-ABEND-PROGRAM (CEE3ABD, code 999); no GOTO statements exist in this program
