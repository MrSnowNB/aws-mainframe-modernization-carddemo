---
schema_version: cobol-md/1.2
program_id: COSGN00C
source_file: app/cbl/COSGN00C.cbl
source_sha: c3e7f8e4fb96466d3822ad82ceda8a96fb555d78
translation_date: '2026-04-23'
translating_agent: claude-opus-4-5 (subagent)
aifirst_task_id: T-2026-04-23-001
cfg_source: validation/structure/COSGN00C_cfg.json
business_domain: Administration
subtype: CICS-Online
author: AWS
date_written: null
lines_of_code: 197
divisions:
  identification: true
  environment: true
  data: true
  procedure: true
environment:
  compiler: IBM Enterprise COBOL
  target: CICS/VSAM
  runtime: z/OS
calls_to:
- program: COADM01C
  condition: CDEMO-USRTYP-ADMIN is true (user type flag indicates administrator)
  call_type: EXEC CICS XCTL
- program: COMEN01C
  condition: CDEMO-USRTYP-ADMIN is false (user type flag indicates regular user)
  call_type: EXEC CICS XCTL
called_by:
- CC00 (CICS transaction initiator)
copybooks_used:
- name: COCOM01Y
  path: app/cpy/COCOM01Y.cpy
  sha: null
- name: COSGN00
  path: app/cpy-bms/COSGN00.CPY
  sha: null
- name: COTTL01Y
  path: app/cpy/COTTL01Y.cpy
  sha: null
- name: CSDAT01Y
  path: app/cpy/CSDAT01Y.cpy
  sha: null
- name: CSMSG01Y
  path: app/cpy/CSMSG01Y.cpy
  sha: null
- name: CSUSR01Y
  path: app/cpy/CSUSR01Y.cpy
  sha: null
- name: DFHAID
  path: app/cpy-stubs/DFHAID.cpy
  sha: null
- name: DFHBMSCA
  path: app/cpy-stubs/DFHBMSCA.cpy
  sha: null
file_control:
- ddname: USRSEC
  organization: INDEXED
  access: RANDOM
  record_key: WS-USER-ID
  crud:
  - READ
cics_commands:
- RETURN
- RECEIVE
- SEND
- ASSIGN
- READ
- XCTL
transaction_ids:
- CC00
data_items:
- name: WS-VARIABLES
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Top-level working-storage group holding all program-local variables including program name, transaction ID, message
    buffer, file name, error flag, response codes, and user credential fields
- name: DFHCOMMAREA
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: CICS Communication Area passed into this program from the transaction invocation; contains the variable-length
    linkage area whose actual size is determined by the CICS-managed EIBCALEN field at runtime
procedure_paragraphs:
- name: MAIN-PARA
  reachable: true
  performs:
  - SEND-SIGNON-SCREEN
  - PROCESS-ENTER-KEY
  - SEND-PLAIN-TEXT
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  - READ-USER-SEC-FILE
  - POPULATE-HEADER-INFO
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  goto_targets: []
  summary: Entry point for transaction CC00; resets error state, then branches based on whether a commarea exists (first invocation
    shows the screen) and which AID key was pressed (Enter processes credentials, PF3 displays a thank-you and exits, any
    other key shows an invalid-key error), before issuing a CICS RETURN to re-invoke the same transaction with the commarea.
- name: END-IF
  reachable: false
  performs:
  - SEND-SIGNON-SCREEN
  - PROCESS-ENTER-KEY
  - SEND-PLAIN-TEXT
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  - READ-USER-SEC-FILE
  - POPULATE-HEADER-INFO
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  goto_targets: []
  summary: Unreachable paragraph artifact produced by the CFG tool from an inline END-IF delimiter; contains no independent
    logic and is flagged as dead code by static analysis.
- name: END-EXEC
  reachable: false
  performs:
  - SEND-SIGNON-SCREEN
  - PROCESS-ENTER-KEY
  - SEND-PLAIN-TEXT
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  - READ-USER-SEC-FILE
  - POPULATE-HEADER-INFO
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  goto_targets: []
  summary: Unreachable paragraph artifact produced by the CFG tool from an inline END-EXEC delimiter; contains no independent
    logic and is flagged as dead code by static analysis.
- name: PROCESS-ENTER-KEY
  reachable: true
  performs:
  - SEND-SIGNON-SCREEN
  - SEND-PLAIN-TEXT
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  - READ-USER-SEC-FILE
  - POPULATE-HEADER-INFO
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  goto_targets: []
  summary: Receives the BMS map from the terminal, validates that neither the user ID nor password field is blank (re-displaying
    the sign-on screen with an error message if either is empty), then uppercases both fields and invokes READ-USER-SEC-FILE
    when no error flag is set.
- name: END-EVALUATE
  reachable: false
  performs:
  - SEND-SIGNON-SCREEN
  - PROCESS-ENTER-KEY
  - SEND-PLAIN-TEXT
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  - READ-USER-SEC-FILE
  - POPULATE-HEADER-INFO
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  - SEND-SIGNON-SCREEN
  goto_targets: []
  summary: Unreachable paragraph artifact produced by the CFG tool from an inline END-EVALUATE delimiter; contains no independent
    logic and is flagged as dead code by static analysis.
- name: SEND-SIGNON-SCREEN
  reachable: true
  performs:
  - POPULATE-HEADER-INFO
  goto_targets: []
  summary: Populates the BMS output map header fields, copies the current message to the error-message area of the map, and
    issues a CICS SEND to display the sign-on screen (COSGN0A in mapset COSGN00) with cursor positioning and screen erase.
- name: SEND-PLAIN-TEXT
  reachable: true
  performs: []
  goto_targets: []
  summary: Sends a plain-text message string directly to the terminal (used for the PF3 thank-you farewell message) and then
    issues an unconditional CICS RETURN with no TRANSID, ending the conversation.
- name: POPULATE-HEADER-INFO
  reachable: true
  performs: []
  goto_targets: []
  summary: Obtains the current date and time via FUNCTION CURRENT-DATE, formats them into month/day/year and hours/minutes/seconds
    display strings, moves the application title lines, transaction ID, and program name into the BMS output map, and queries
    CICS for the APPLID and SYSID to display in the header.
- name: READ-USER-SEC-FILE
  reachable: true
  performs:
  - SEND-SIGNON-SCREEN
  goto_targets: []
  summary: Issues a CICS READ against the USRSEC VSAM dataset keyed on WS-USER-ID; on a successful read (response code 0)
    it verifies the stored password matches WS-USER-PWD and, if correct, populates the commarea with identity/role data before
    transferring control via XCTL to either the administrator menu (COADM01C) or the regular-user menu (COMEN01C); on response
    code 13 (record not found) or any other error it displays an appropriate error message.
business_rules:
- id: BR-001
  rule: If no commarea is present (EIBCALEN equals zero), the program is on its first invocation and must display the sign-on
    screen immediately without attempting to process any input.
  source_paragraph: MAIN-PARA
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-002
  rule: Only the Enter key (DFHENTER) triggers credential processing; PF3 triggers a graceful exit with a thank-you message;
    any other AID key is rejected as invalid and causes an error message to be displayed on the sign-on screen.
  source_paragraph: MAIN-PARA
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-003
  rule: If the user ID field on the sign-on screen is blank or contains low-values, processing is halted and the user is prompted
    to enter a user ID before any authentication attempt is made.
  source_paragraph: PROCESS-ENTER-KEY
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-004
  rule: If the password field on the sign-on screen is blank or contains low-values, processing is halted and the user is
    prompted to enter a password before any authentication attempt is made.
  source_paragraph: PROCESS-ENTER-KEY
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-005
  rule: Both the user ID and password values received from the terminal are uppercased before comparison and storage, ensuring
    that authentication is case-insensitive for the user but stored in a canonical form.
  source_paragraph: PROCESS-ENTER-KEY
  rule_type: transform
  confidence: high
  reachable: true
- id: BR-006
  rule: The user security file (USRSEC) is only read when no error flag is set; if any prior validation step raised the error
    flag, the file read is skipped entirely.
  source_paragraph: PROCESS-ENTER-KEY
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-007
  rule: If the USRSEC record is found (response code 0) and the stored password matches the entered password, the user is
    authenticated; a mismatched password results in a 'Wrong Password' error message without distinguishing which field was
    wrong.
  source_paragraph: READ-USER-SEC-FILE
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-008
  rule: Authenticated users whose user-type flag indicates administrator status (CDEMO-USRTYP-ADMIN) are routed to the administration
    menu program (COADM01C) via XCTL; all other authenticated users are routed to the standard main menu program (COMEN01C).
  source_paragraph: READ-USER-SEC-FILE
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-009
  rule: If the USRSEC READ returns response code 13 (record not found), the user is told their user ID was not found and is
    prompted to try again; the error flag is set to suppress further processing in the current cycle.
  source_paragraph: READ-USER-SEC-FILE
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-010
  rule: Any USRSEC READ response code other than 0 or 13 triggers a generic 'Unable to verify the User' error message, masking
    the underlying system error from the end user while still preventing sign-on.
  source_paragraph: READ-USER-SEC-FILE
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-011
  rule: Upon successful authentication the commarea is populated with the originating transaction ID, program name, user ID,
    and user type before control is transferred, ensuring downstream programs receive a fully initialized session context.
  source_paragraph: READ-USER-SEC-FILE
  rule_type: audit
  confidence: high
  reachable: true
- id: BR-012
  rule: The CICS RETURN at the end of MAIN-PARA always specifies TRANSID 'CC00' and passes the CARDDEMO-COMMAREA, so if control
    returns without a successful XCTL the sign-on screen will be re-presented on the next keystroke.
  source_paragraph: MAIN-PARA
  rule_type: display
  confidence: high
  reachable: true
byte_layout:
  file: []
  working_storage:
  - level: 1
    name: WS-VARIABLES
    line: 35
    usage: DISPLAY
    children:
    - level: 5
      name: WS-PGMNAME
      line: 36
      usage: DISPLAY
      pic: X(08)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: WS-VARIABLES.WS-PGMNAME
    - level: 5
      name: WS-TRANID
      line: 37
      usage: DISPLAY
      pic: X(04)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: WS-VARIABLES.WS-TRANID
    - level: 5
      name: WS-MESSAGE
      line: 38
      usage: DISPLAY
      pic: X(80)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 80
      qualified_name: WS-VARIABLES.WS-MESSAGE
    - level: 5
      name: WS-USRSEC-FILE
      line: 39
      usage: DISPLAY
      pic: X(08)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: WS-VARIABLES.WS-USRSEC-FILE
    - level: 5
      name: WS-ERR-FLG
      line: 40
      usage: DISPLAY
      pic: X(01)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: WS-VARIABLES.WS-ERR-FLG
    - level: 5
      name: WS-RESP-CD
      line: 43
      usage: COMP
      pic: S9(09)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: WS-VARIABLES.WS-RESP-CD
    - level: 5
      name: WS-REAS-CD
      line: 44
      usage: COMP
      pic: S9(09)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: WS-VARIABLES.WS-REAS-CD
    - level: 5
      name: WS-USER-ID
      line: 45
      usage: DISPLAY
      pic: X(08)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: WS-VARIABLES.WS-USER-ID
    - level: 5
      name: WS-USER-PWD
      line: 46
      usage: DISPLAY
      pic: X(08)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: WS-VARIABLES.WS-USER-PWD
    slack_bytes_before: 0
    total_bytes: 125
    qualified_name: WS-VARIABLES
    section: working_storage
  - level: 1
    name: CARDDEMO-COMMAREA
    line: 19
    usage: DISPLAY
    children:
    - level: 5
      name: CDEMO-GENERAL-INFO
      line: 20
      usage: DISPLAY
      children:
      - level: 10
        name: CDEMO-FROM-TRANID
        line: 21
        usage: DISPLAY
        pic: X(04)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 4
        qualified_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-FROM-TRANID
      - level: 10
        name: CDEMO-FROM-PROGRAM
        line: 22
        usage: DISPLAY
        pic: X(08)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 8
        qualified_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-FROM-PROGRAM
      - level: 10
        name: CDEMO-TO-TRANID
        line: 23
        usage: DISPLAY
        pic: X(04)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 4
        qualified_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-TO-TRANID
      - level: 10
        name: CDEMO-TO-PROGRAM
        line: 24
        usage: DISPLAY
        pic: X(08)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 8
        qualified_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-TO-PROGRAM
      - level: 10
        name: CDEMO-USER-ID
        line: 25
        usage: DISPLAY
        pic: X(08)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 8
        qualified_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-USER-ID
      - level: 10
        name: CDEMO-USER-TYPE
        line: 26
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-USER-TYPE
      - level: 10
        name: CDEMO-PGM-CONTEXT
        line: 29
        usage: DISPLAY
        pic: 9(01)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-PGM-CONTEXT
      slack_bytes_before: 0
      total_bytes: 34
      qualified_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO
    - level: 5
      name: CDEMO-CUSTOMER-INFO
      line: 32
      usage: DISPLAY
      children:
      - level: 10
        name: CDEMO-CUST-ID
        line: 33
        usage: DISPLAY
        pic: 9(09)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 9
        qualified_name: CARDDEMO-COMMAREA.CDEMO-CUSTOMER-INFO.CDEMO-CUST-ID
      - level: 10
        name: CDEMO-CUST-FNAME
        line: 34
        usage: DISPLAY
        pic: X(25)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 25
        qualified_name: CARDDEMO-COMMAREA.CDEMO-CUSTOMER-INFO.CDEMO-CUST-FNAME
      - level: 10
        name: CDEMO-CUST-MNAME
        line: 35
        usage: DISPLAY
        pic: X(25)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 25
        qualified_name: CARDDEMO-COMMAREA.CDEMO-CUSTOMER-INFO.CDEMO-CUST-MNAME
      - level: 10
        name: CDEMO-CUST-LNAME
        line: 36
        usage: DISPLAY
        pic: X(25)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 25
        qualified_name: CARDDEMO-COMMAREA.CDEMO-CUSTOMER-INFO.CDEMO-CUST-LNAME
      slack_bytes_before: 0
      total_bytes: 84
      qualified_name: CARDDEMO-COMMAREA.CDEMO-CUSTOMER-INFO
    - level: 5
      name: CDEMO-ACCOUNT-INFO
      line: 37
      usage: DISPLAY
      children:
      - level: 10
        name: CDEMO-ACCT-ID
        line: 38
        usage: DISPLAY
        pic: 9(11)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 11
        qualified_name: CARDDEMO-COMMAREA.CDEMO-ACCOUNT-INFO.CDEMO-ACCT-ID
      - level: 10
        name: CDEMO-ACCT-STATUS
        line: 39
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: CARDDEMO-COMMAREA.CDEMO-ACCOUNT-INFO.CDEMO-ACCT-STATUS
      slack_bytes_before: 0
      total_bytes: 12
      qualified_name: CARDDEMO-COMMAREA.CDEMO-ACCOUNT-INFO
    - level: 5
      name: CDEMO-CARD-INFO
      line: 40
      usage: DISPLAY
      children:
      - level: 10
        name: CDEMO-CARD-NUM
        line: 41
        usage: DISPLAY
        pic: 9(16)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 16
        qualified_name: CARDDEMO-COMMAREA.CDEMO-CARD-INFO.CDEMO-CARD-NUM
      slack_bytes_before: 0
      total_bytes: 16
      qualified_name: CARDDEMO-COMMAREA.CDEMO-CARD-INFO
    - level: 5
      name: CDEMO-MORE-INFO
      line: 42
      usage: DISPLAY
      children:
      - level: 10
        name: CDEMO-LAST-MAP
        line: 43
        usage: DISPLAY
        pic: X(7)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 7
        qualified_name: CARDDEMO-COMMAREA.CDEMO-MORE-INFO.CDEMO-LAST-MAP
      - level: 10
        name: CDEMO-LAST-MAPSET
        line: 44
        usage: DISPLAY
        pic: X(7)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 7
        qualified_name: CARDDEMO-COMMAREA.CDEMO-MORE-INFO.CDEMO-LAST-MAPSET
      slack_bytes_before: 0
      total_bytes: 14
      qualified_name: CARDDEMO-COMMAREA.CDEMO-MORE-INFO
    slack_bytes_before: 0
    total_bytes: 160
    qualified_name: CARDDEMO-COMMAREA
    section: working_storage
  - level: 1
    name: COSGN0AI
    line: 17
    usage: DISPLAY
    children:
    - level: 2
      name: FILLER
      line: 18
      usage: DISPLAY
      pic: X(12)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 12
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: TRNNAMEL
      line: 19
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COSGN0AI.TRNNAMEL
    - level: 2
      name: TRNNAMEF
      line: 20
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AI.TRNNAMEF
    - level: 2
      name: FILLER
      line: 21
      redefines: TRNNAMEF
      usage: DISPLAY
      children:
      - level: 3
        name: TRNNAMEA
        line: 22
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COSGN0AI.FILLER.TRNNAMEA
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: FILLER
      line: 23
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: TRNNAMEI
      line: 24
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COSGN0AI.TRNNAMEI
    - level: 2
      name: TITLE01L
      line: 25
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COSGN0AI.TITLE01L
    - level: 2
      name: TITLE01F
      line: 26
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AI.TITLE01F
    - level: 2
      name: FILLER
      line: 27
      redefines: TITLE01F
      usage: DISPLAY
      children:
      - level: 3
        name: TITLE01A
        line: 28
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COSGN0AI.FILLER.TITLE01A
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: FILLER
      line: 29
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: TITLE01I
      line: 30
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COSGN0AI.TITLE01I
    - level: 2
      name: CURDATEL
      line: 31
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COSGN0AI.CURDATEL
    - level: 2
      name: CURDATEF
      line: 32
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AI.CURDATEF
    - level: 2
      name: FILLER
      line: 33
      redefines: CURDATEF
      usage: DISPLAY
      children:
      - level: 3
        name: CURDATEA
        line: 34
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COSGN0AI.FILLER.CURDATEA
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: FILLER
      line: 35
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: CURDATEI
      line: 36
      usage: DISPLAY
      pic: X(8)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: COSGN0AI.CURDATEI
    - level: 2
      name: PGMNAMEL
      line: 37
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COSGN0AI.PGMNAMEL
    - level: 2
      name: PGMNAMEF
      line: 38
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AI.PGMNAMEF
    - level: 2
      name: FILLER
      line: 39
      redefines: PGMNAMEF
      usage: DISPLAY
      children:
      - level: 3
        name: PGMNAMEA
        line: 40
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COSGN0AI.FILLER.PGMNAMEA
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: FILLER
      line: 41
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: PGMNAMEI
      line: 42
      usage: DISPLAY
      pic: X(8)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: COSGN0AI.PGMNAMEI
    - level: 2
      name: TITLE02L
      line: 43
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COSGN0AI.TITLE02L
    - level: 2
      name: TITLE02F
      line: 44
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AI.TITLE02F
    - level: 2
      name: FILLER
      line: 45
      redefines: TITLE02F
      usage: DISPLAY
      children:
      - level: 3
        name: TITLE02A
        line: 46
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COSGN0AI.FILLER.TITLE02A
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: FILLER
      line: 47
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: TITLE02I
      line: 48
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COSGN0AI.TITLE02I
    - level: 2
      name: CURTIMEL
      line: 49
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COSGN0AI.CURTIMEL
    - level: 2
      name: CURTIMEF
      line: 50
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AI.CURTIMEF
    - level: 2
      name: FILLER
      line: 51
      redefines: CURTIMEF
      usage: DISPLAY
      children:
      - level: 3
        name: CURTIMEA
        line: 52
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COSGN0AI.FILLER.CURTIMEA
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: FILLER
      line: 53
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: CURTIMEI
      line: 54
      usage: DISPLAY
      pic: X(9)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 9
      qualified_name: COSGN0AI.CURTIMEI
    - level: 2
      name: APPLIDL
      line: 55
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COSGN0AI.APPLIDL
    - level: 2
      name: APPLIDF
      line: 56
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AI.APPLIDF
    - level: 2
      name: FILLER
      line: 57
      redefines: APPLIDF
      usage: DISPLAY
      children:
      - level: 3
        name: APPLIDA
        line: 58
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COSGN0AI.FILLER.APPLIDA
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: FILLER
      line: 59
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: APPLIDI
      line: 60
      usage: DISPLAY
      pic: X(8)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: COSGN0AI.APPLIDI
    - level: 2
      name: SYSIDL
      line: 61
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COSGN0AI.SYSIDL
    - level: 2
      name: SYSIDF
      line: 62
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AI.SYSIDF
    - level: 2
      name: FILLER
      line: 63
      redefines: SYSIDF
      usage: DISPLAY
      children:
      - level: 3
        name: SYSIDA
        line: 64
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COSGN0AI.FILLER.SYSIDA
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: FILLER
      line: 65
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: SYSIDI
      line: 66
      usage: DISPLAY
      pic: X(8)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: COSGN0AI.SYSIDI
    - level: 2
      name: USERIDL
      line: 67
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COSGN0AI.USERIDL
    - level: 2
      name: USERIDF
      line: 68
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AI.USERIDF
    - level: 2
      name: FILLER
      line: 69
      redefines: USERIDF
      usage: DISPLAY
      children:
      - level: 3
        name: USERIDA
        line: 70
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COSGN0AI.FILLER.USERIDA
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: FILLER
      line: 71
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: USERIDI
      line: 72
      usage: DISPLAY
      pic: X(8)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: COSGN0AI.USERIDI
    - level: 2
      name: PASSWDL
      line: 73
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COSGN0AI.PASSWDL
    - level: 2
      name: PASSWDF
      line: 74
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AI.PASSWDF
    - level: 2
      name: FILLER
      line: 75
      redefines: PASSWDF
      usage: DISPLAY
      children:
      - level: 3
        name: PASSWDA
        line: 76
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COSGN0AI.FILLER.PASSWDA
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: FILLER
      line: 77
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: PASSWDI
      line: 78
      usage: DISPLAY
      pic: X(8)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: COSGN0AI.PASSWDI
    - level: 2
      name: ERRMSGL
      line: 79
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COSGN0AI.ERRMSGL
    - level: 2
      name: ERRMSGF
      line: 80
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AI.ERRMSGF
    - level: 2
      name: FILLER
      line: 81
      redefines: ERRMSGF
      usage: DISPLAY
      children:
      - level: 3
        name: ERRMSGA
        line: 82
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COSGN0AI.FILLER.ERRMSGA
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: FILLER
      line: 83
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COSGN0AI.FILLER
    - level: 2
      name: ERRMSGI
      line: 84
      usage: DISPLAY
      pic: X(78)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 78
      qualified_name: COSGN0AI.ERRMSGI
    slack_bytes_before: 0
    total_bytes: 308
    qualified_name: COSGN0AI
    section: working_storage
  - level: 1
    name: COSGN0AO
    line: 85
    redefines: COSGN0AI
    usage: DISPLAY
    children:
    - level: 2
      name: FILLER
      line: 86
      usage: DISPLAY
      pic: X(12)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 12
      qualified_name: COSGN0AO.FILLER
    - level: 2
      name: FILLER
      line: 87
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COSGN0AO.FILLER
    - level: 2
      name: TRNNAMEC
      line: 88
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.TRNNAMEC
    - level: 2
      name: TRNNAMEP
      line: 89
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.TRNNAMEP
    - level: 2
      name: TRNNAMEH
      line: 90
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.TRNNAMEH
    - level: 2
      name: TRNNAMEV
      line: 91
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.TRNNAMEV
    - level: 2
      name: TRNNAMEO
      line: 92
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COSGN0AO.TRNNAMEO
    - level: 2
      name: FILLER
      line: 93
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COSGN0AO.FILLER
    - level: 2
      name: TITLE01C
      line: 94
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.TITLE01C
    - level: 2
      name: TITLE01P
      line: 95
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.TITLE01P
    - level: 2
      name: TITLE01H
      line: 96
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.TITLE01H
    - level: 2
      name: TITLE01V
      line: 97
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.TITLE01V
    - level: 2
      name: TITLE01O
      line: 98
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COSGN0AO.TITLE01O
    - level: 2
      name: FILLER
      line: 99
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COSGN0AO.FILLER
    - level: 2
      name: CURDATEC
      line: 100
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.CURDATEC
    - level: 2
      name: CURDATEP
      line: 101
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.CURDATEP
    - level: 2
      name: CURDATEH
      line: 102
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.CURDATEH
    - level: 2
      name: CURDATEV
      line: 103
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.CURDATEV
    - level: 2
      name: CURDATEO
      line: 104
      usage: DISPLAY
      pic: X(8)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: COSGN0AO.CURDATEO
    - level: 2
      name: FILLER
      line: 105
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COSGN0AO.FILLER
    - level: 2
      name: PGMNAMEC
      line: 106
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.PGMNAMEC
    - level: 2
      name: PGMNAMEP
      line: 107
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.PGMNAMEP
    - level: 2
      name: PGMNAMEH
      line: 108
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.PGMNAMEH
    - level: 2
      name: PGMNAMEV
      line: 109
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.PGMNAMEV
    - level: 2
      name: PGMNAMEO
      line: 110
      usage: DISPLAY
      pic: X(8)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: COSGN0AO.PGMNAMEO
    - level: 2
      name: FILLER
      line: 111
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COSGN0AO.FILLER
    - level: 2
      name: TITLE02C
      line: 112
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.TITLE02C
    - level: 2
      name: TITLE02P
      line: 113
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.TITLE02P
    - level: 2
      name: TITLE02H
      line: 114
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.TITLE02H
    - level: 2
      name: TITLE02V
      line: 115
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.TITLE02V
    - level: 2
      name: TITLE02O
      line: 116
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COSGN0AO.TITLE02O
    - level: 2
      name: FILLER
      line: 117
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COSGN0AO.FILLER
    - level: 2
      name: CURTIMEC
      line: 118
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.CURTIMEC
    - level: 2
      name: CURTIMEP
      line: 119
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.CURTIMEP
    - level: 2
      name: CURTIMEH
      line: 120
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.CURTIMEH
    - level: 2
      name: CURTIMEV
      line: 121
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.CURTIMEV
    - level: 2
      name: CURTIMEO
      line: 122
      usage: DISPLAY
      pic: X(9)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 9
      qualified_name: COSGN0AO.CURTIMEO
    - level: 2
      name: FILLER
      line: 123
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COSGN0AO.FILLER
    - level: 2
      name: APPLIDC
      line: 124
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.APPLIDC
    - level: 2
      name: APPLIDP
      line: 125
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.APPLIDP
    - level: 2
      name: APPLIDH
      line: 126
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.APPLIDH
    - level: 2
      name: APPLIDV
      line: 127
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.APPLIDV
    - level: 2
      name: APPLIDO
      line: 128
      usage: DISPLAY
      pic: X(8)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: COSGN0AO.APPLIDO
    - level: 2
      name: FILLER
      line: 129
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COSGN0AO.FILLER
    - level: 2
      name: SYSIDC
      line: 130
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.SYSIDC
    - level: 2
      name: SYSIDP
      line: 131
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.SYSIDP
    - level: 2
      name: SYSIDH
      line: 132
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.SYSIDH
    - level: 2
      name: SYSIDV
      line: 133
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.SYSIDV
    - level: 2
      name: SYSIDO
      line: 134
      usage: DISPLAY
      pic: X(8)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: COSGN0AO.SYSIDO
    - level: 2
      name: FILLER
      line: 135
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COSGN0AO.FILLER
    - level: 2
      name: USERIDC
      line: 136
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.USERIDC
    - level: 2
      name: USERIDP
      line: 137
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.USERIDP
    - level: 2
      name: USERIDH
      line: 138
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.USERIDH
    - level: 2
      name: USERIDV
      line: 139
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.USERIDV
    - level: 2
      name: USERIDO
      line: 140
      usage: DISPLAY
      pic: X(8)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: COSGN0AO.USERIDO
    - level: 2
      name: FILLER
      line: 141
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COSGN0AO.FILLER
    - level: 2
      name: PASSWDC
      line: 142
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.PASSWDC
    - level: 2
      name: PASSWDP
      line: 143
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.PASSWDP
    - level: 2
      name: PASSWDH
      line: 144
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.PASSWDH
    - level: 2
      name: PASSWDV
      line: 145
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.PASSWDV
    - level: 2
      name: PASSWDO
      line: 146
      usage: DISPLAY
      pic: X(8)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: COSGN0AO.PASSWDO
    - level: 2
      name: FILLER
      line: 147
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COSGN0AO.FILLER
    - level: 2
      name: ERRMSGC
      line: 148
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.ERRMSGC
    - level: 2
      name: ERRMSGP
      line: 149
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.ERRMSGP
    - level: 2
      name: ERRMSGH
      line: 150
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.ERRMSGH
    - level: 2
      name: ERRMSGV
      line: 151
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COSGN0AO.ERRMSGV
    - level: 2
      name: ERRMSGO
      line: 152
      usage: DISPLAY
      pic: X(78)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 78
      qualified_name: COSGN0AO.ERRMSGO
    total_bytes: 308
    slack_bytes_before: 0
    qualified_name: COSGN0AO
    section: working_storage
  - level: 1
    name: CCDA-SCREEN-TITLE
    line: 17
    usage: DISPLAY
    children:
    - level: 5
      name: CCDA-TITLE01
      line: 18
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: CCDA-SCREEN-TITLE.CCDA-TITLE01
    - level: 5
      name: CCDA-TITLE02
      line: 20
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: CCDA-SCREEN-TITLE.CCDA-TITLE02
    - level: 5
      name: CCDA-THANK-YOU
      line: 23
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: CCDA-SCREEN-TITLE.CCDA-THANK-YOU
    slack_bytes_before: 0
    total_bytes: 120
    qualified_name: CCDA-SCREEN-TITLE
    section: working_storage
  - level: 1
    name: WS-DATE-TIME
    line: 17
    usage: DISPLAY
    children:
    - level: 5
      name: WS-CURDATE-DATA
      line: 18
      usage: DISPLAY
      children:
      - level: 10
        name: WS-CURDATE
        line: 19
        usage: DISPLAY
        children:
        - level: 15
          name: WS-CURDATE-YEAR
          line: 20
          usage: DISPLAY
          pic: 9(04)
          children: []
          encoding: zoned-decimal
          slack_bytes_before: 0
          total_bytes: 4
          qualified_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURDATE.WS-CURDATE-YEAR
        - level: 15
          name: WS-CURDATE-MONTH
          line: 21
          usage: DISPLAY
          pic: 9(02)
          children: []
          encoding: zoned-decimal
          slack_bytes_before: 0
          total_bytes: 2
          qualified_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURDATE.WS-CURDATE-MONTH
        - level: 15
          name: WS-CURDATE-DAY
          line: 22
          usage: DISPLAY
          pic: 9(02)
          children: []
          encoding: zoned-decimal
          slack_bytes_before: 0
          total_bytes: 2
          qualified_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURDATE.WS-CURDATE-DAY
        slack_bytes_before: 0
        total_bytes: 8
        qualified_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURDATE
      - level: 10
        name: WS-CURDATE-N
        line: 23
        redefines: WS-CURDATE
        usage: DISPLAY
        pic: 9(08)
        children: []
        total_bytes: 8
        slack_bytes_before: 0
        qualified_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURDATE-N
      - level: 10
        name: WS-CURTIME
        line: 24
        usage: DISPLAY
        children:
        - level: 15
          name: WS-CURTIME-HOURS
          line: 25
          usage: DISPLAY
          pic: 9(02)
          children: []
          encoding: zoned-decimal
          slack_bytes_before: 0
          total_bytes: 2
          qualified_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURTIME.WS-CURTIME-HOURS
        - level: 15
          name: WS-CURTIME-MINUTE
          line: 26
          usage: DISPLAY
          pic: 9(02)
          children: []
          encoding: zoned-decimal
          slack_bytes_before: 0
          total_bytes: 2
          qualified_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURTIME.WS-CURTIME-MINUTE
        - level: 15
          name: WS-CURTIME-SECOND
          line: 27
          usage: DISPLAY
          pic: 9(02)
          children: []
          encoding: zoned-decimal
          slack_bytes_before: 0
          total_bytes: 2
          qualified_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURTIME.WS-CURTIME-SECOND
        - level: 15
          name: WS-CURTIME-MILSEC
          line: 28
          usage: DISPLAY
          pic: 9(02)
          children: []
          encoding: zoned-decimal
          slack_bytes_before: 0
          total_bytes: 2
          qualified_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURTIME.WS-CURTIME-MILSEC
        slack_bytes_before: 0
        total_bytes: 8
        qualified_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURTIME
      - level: 10
        name: WS-CURTIME-N
        line: 29
        redefines: WS-CURTIME
        usage: DISPLAY
        pic: 9(08)
        children: []
        total_bytes: 8
        slack_bytes_before: 0
        qualified_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURTIME-N
      slack_bytes_before: 0
      total_bytes: 16
      qualified_name: WS-DATE-TIME.WS-CURDATE-DATA
    - level: 5
      name: WS-CURDATE-MM-DD-YY
      line: 30
      usage: DISPLAY
      children:
      - level: 10
        name: WS-CURDATE-MM
        line: 31
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: WS-DATE-TIME.WS-CURDATE-MM-DD-YY.WS-CURDATE-MM
      - level: 10
        name: FILLER
        line: 32
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: WS-DATE-TIME.WS-CURDATE-MM-DD-YY.FILLER
      - level: 10
        name: WS-CURDATE-DD
        line: 33
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: WS-DATE-TIME.WS-CURDATE-MM-DD-YY.WS-CURDATE-DD
      - level: 10
        name: FILLER
        line: 34
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: WS-DATE-TIME.WS-CURDATE-MM-DD-YY.FILLER
      - level: 10
        name: WS-CURDATE-YY
        line: 35
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: WS-DATE-TIME.WS-CURDATE-MM-DD-YY.WS-CURDATE-YY
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: WS-DATE-TIME.WS-CURDATE-MM-DD-YY
    - level: 5
      name: WS-CURTIME-HH-MM-SS
      line: 36
      usage: DISPLAY
      children:
      - level: 10
        name: WS-CURTIME-HH
        line: 37
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: WS-DATE-TIME.WS-CURTIME-HH-MM-SS.WS-CURTIME-HH
      - level: 10
        name: FILLER
        line: 38
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: WS-DATE-TIME.WS-CURTIME-HH-MM-SS.FILLER
      - level: 10
        name: WS-CURTIME-MM
        line: 39
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: WS-DATE-TIME.WS-CURTIME-HH-MM-SS.WS-CURTIME-MM
      - level: 10
        name: FILLER
        line: 40
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: WS-DATE-TIME.WS-CURTIME-HH-MM-SS.FILLER
      - level: 10
        name: WS-CURTIME-SS
        line: 41
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: WS-DATE-TIME.WS-CURTIME-HH-MM-SS.WS-CURTIME-SS
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: WS-DATE-TIME.WS-CURTIME-HH-MM-SS
    - level: 5
      name: WS-TIMESTAMP
      line: 42
      usage: DISPLAY
      children:
      - level: 10
        name: WS-TIMESTAMP-DT-YYYY
        line: 43
        usage: DISPLAY
        pic: 9(04)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 4
        qualified_name: WS-DATE-TIME.WS-TIMESTAMP.WS-TIMESTAMP-DT-YYYY
      - level: 10
        name: FILLER
        line: 44
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: WS-DATE-TIME.WS-TIMESTAMP.FILLER
      - level: 10
        name: WS-TIMESTAMP-DT-MM
        line: 45
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: WS-DATE-TIME.WS-TIMESTAMP.WS-TIMESTAMP-DT-MM
      - level: 10
        name: FILLER
        line: 46
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: WS-DATE-TIME.WS-TIMESTAMP.FILLER
      - level: 10
        name: WS-TIMESTAMP-DT-DD
        line: 47
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: WS-DATE-TIME.WS-TIMESTAMP.WS-TIMESTAMP-DT-DD
      - level: 10
        name: FILLER
        line: 48
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: WS-DATE-TIME.WS-TIMESTAMP.FILLER
      - level: 10
        name: WS-TIMESTAMP-TM-HH
        line: 49
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: WS-DATE-TIME.WS-TIMESTAMP.WS-TIMESTAMP-TM-HH
      - level: 10
        name: FILLER
        line: 50
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: WS-DATE-TIME.WS-TIMESTAMP.FILLER
      - level: 10
        name: WS-TIMESTAMP-TM-MM
        line: 51
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: WS-DATE-TIME.WS-TIMESTAMP.WS-TIMESTAMP-TM-MM
      - level: 10
        name: FILLER
        line: 52
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: WS-DATE-TIME.WS-TIMESTAMP.FILLER
      - level: 10
        name: WS-TIMESTAMP-TM-SS
        line: 53
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: WS-DATE-TIME.WS-TIMESTAMP.WS-TIMESTAMP-TM-SS
      - level: 10
        name: FILLER
        line: 54
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: WS-DATE-TIME.WS-TIMESTAMP.FILLER
      - level: 10
        name: WS-TIMESTAMP-TM-MS6
        line: 55
        usage: DISPLAY
        pic: 9(06)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 6
        qualified_name: WS-DATE-TIME.WS-TIMESTAMP.WS-TIMESTAMP-TM-MS6
      slack_bytes_before: 0
      total_bytes: 26
      qualified_name: WS-DATE-TIME.WS-TIMESTAMP
    slack_bytes_before: 0
    total_bytes: 58
    qualified_name: WS-DATE-TIME
    section: working_storage
  - level: 1
    name: CCDA-COMMON-MESSAGES
    line: 17
    usage: DISPLAY
    children:
    - level: 5
      name: CCDA-MSG-THANK-YOU
      line: 18
      usage: DISPLAY
      pic: X(50)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 50
      qualified_name: CCDA-COMMON-MESSAGES.CCDA-MSG-THANK-YOU
    - level: 5
      name: CCDA-MSG-INVALID-KEY
      line: 20
      usage: DISPLAY
      pic: X(50)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 50
      qualified_name: CCDA-COMMON-MESSAGES.CCDA-MSG-INVALID-KEY
    slack_bytes_before: 0
    total_bytes: 100
    qualified_name: CCDA-COMMON-MESSAGES
    section: working_storage
  - level: 1
    name: SEC-USER-DATA
    line: 17
    usage: DISPLAY
    children:
    - level: 5
      name: SEC-USR-ID
      line: 18
      usage: DISPLAY
      pic: X(08)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: SEC-USER-DATA.SEC-USR-ID
    - level: 5
      name: SEC-USR-FNAME
      line: 19
      usage: DISPLAY
      pic: X(20)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 20
      qualified_name: SEC-USER-DATA.SEC-USR-FNAME
    - level: 5
      name: SEC-USR-LNAME
      line: 20
      usage: DISPLAY
      pic: X(20)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 20
      qualified_name: SEC-USER-DATA.SEC-USR-LNAME
    - level: 5
      name: SEC-USR-PWD
      line: 21
      usage: DISPLAY
      pic: X(08)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: SEC-USER-DATA.SEC-USR-PWD
    - level: 5
      name: SEC-USR-TYPE
      line: 22
      usage: DISPLAY
      pic: X(01)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: SEC-USER-DATA.SEC-USR-TYPE
    - level: 5
      name: SEC-USR-FILLER
      line: 23
      usage: DISPLAY
      pic: X(23)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 23
      qualified_name: SEC-USER-DATA.SEC-USR-FILLER
    slack_bytes_before: 0
    total_bytes: 80
    qualified_name: SEC-USER-DATA
    section: working_storage
  - level: 1
    name: DFHAID
    line: 1
    usage: DISPLAY
    children:
    - level: 5
      name: DFHNULL
      line: 2
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHAID.DFHNULL
    - level: 5
      name: DFHENTER
      line: 3
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHAID.DFHENTER
    - level: 5
      name: DFHCLEAR
      line: 4
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHAID.DFHCLEAR
    - level: 5
      name: DFHPF1
      line: 5
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHAID.DFHPF1
    - level: 5
      name: DFHPF2
      line: 6
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHAID.DFHPF2
    - level: 5
      name: DFHPF3
      line: 7
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHAID.DFHPF3
    - level: 5
      name: DFHPF4
      line: 8
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHAID.DFHPF4
    - level: 5
      name: DFHPF5
      line: 9
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHAID.DFHPF5
    - level: 5
      name: DFHPF6
      line: 10
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHAID.DFHPF6
    - level: 5
      name: DFHPF7
      line: 11
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHAID.DFHPF7
    - level: 5
      name: DFHPF8
      line: 12
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHAID.DFHPF8
    - level: 5
      name: DFHPF9
      line: 13
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHAID.DFHPF9
    - level: 5
      name: DFHPF10
      line: 14
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHAID.DFHPF10
    - level: 5
      name: DFHPF11
      line: 15
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHAID.DFHPF11
    - level: 5
      name: DFHPF12
      line: 16
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHAID.DFHPF12
    slack_bytes_before: 0
    total_bytes: 15
    qualified_name: DFHAID
    section: working_storage
  - level: 1
    name: DFHBMSCA
    line: 1
    usage: DISPLAY
    children:
    - level: 5
      name: DFHBMPEM
      line: 2
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHBMSCA.DFHBMPEM
    - level: 5
      name: DFHBMPNL
      line: 3
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHBMSCA.DFHBMPNL
    - level: 5
      name: DFHBMPFF
      line: 4
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHBMSCA.DFHBMPFF
    - level: 5
      name: DFHBMPCR
      line: 5
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: DFHBMSCA.DFHBMPCR
    slack_bytes_before: 0
    total_bytes: 4
    qualified_name: DFHBMSCA
    section: working_storage
  linkage:
  - level: 1
    name: DFHCOMMAREA
    line: 65
    usage: DISPLAY
    children:
    - level: 5
      name: LK-COMMAREA
      line: 66
      occurs_min: 1
      occurs_max: 32767
      occurs_depending_on: EIBCALEN
      variable_length: true
      usage: DISPLAY
      pic: X(01)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes_min: 1
      total_bytes_max: 32767
      total_bytes: 32767
      qualified_name: DFHCOMMAREA.LK-COMMAREA
    slack_bytes_before: 0
    total_bytes_min: 1
    total_bytes_max: 32767
    variable_length: true
    total_bytes: 32767
    qualified_name: DFHCOMMAREA
    section: linkage
  totals:
    working_storage_bytes: 970
    linkage_bytes: 32767
fall_through:
  paragraphs:
  - paragraph: MAIN-PARA
    first_line: 75
    last_line: 98
    terminator: cics-return
    falls_through_to: null
    last_verb: EXEC CICS
    last_raw: EXEC CICS RETURN
    classification_source: raw
  - paragraph: PROCESS-ENTER-KEY
    first_line: 110
    last_line: 139
    terminator: implicit
    falls_through_to: SEND-SIGNON-SCREEN
    last_verb: PERFORM
    last_raw: PERFORM READ-USER-SEC-FILE
    classification_source: annotations
  - paragraph: SEND-SIGNON-SCREEN
    first_line: 147
    last_line: 151
    terminator: implicit
    falls_through_to: SEND-PLAIN-TEXT
    last_verb: EXEC CICS
    last_raw: EXEC CICS SEND
    classification_source: raw
  - paragraph: SEND-PLAIN-TEXT
    first_line: 164
    last_line: 171
    terminator: cics-return
    falls_through_to: null
    last_verb: EXEC CICS
    last_raw: EXEC CICS RETURN
    classification_source: raw
  - paragraph: POPULATE-HEADER-INFO
    first_line: 179
    last_line: 202
    terminator: implicit
    falls_through_to: READ-USER-SEC-FILE
    last_verb: EXEC CICS
    last_raw: EXEC CICS ASSIGN
    classification_source: raw
  - paragraph: READ-USER-SEC-FILE
    first_line: 211
    last_line: 256
    terminator: implicit-end-of-program
    falls_through_to: null
    last_verb: PERFORM
    last_raw: PERFORM SEND-SIGNON-SCREEN
    classification_source: annotations
  c5_assertion: PASS
  c5_violations: []
paragraph_io:
- paragraph: MAIN-PARA
  classification_source: annotations
  mutates:
  - fd_name: ERR-FLG-OFF
    verb: SET
    line: 75
    raw: SET ERR-FLG-OFF TO TRUE
  - fd_name: WS-VARIABLES.WS-MESSAGE
    verb: MOVE
    line: 77
    raw: MOVE SPACES TO WS-MESSAGE
  - fd_name: COSGN0AO
    verb: MOVE
    line: 81
    raw: MOVE LOW-VALUES TO COSGN0AO
  - fd_name: COSGN0AI.USERIDL
    verb: MOVE
    line: 82
    raw: MOVE -1 TO USERIDL OF COSGN0AI
  - fd_name: WS-VARIABLES.WS-ERR-FLG
    verb: MOVE
    line: 92
    raw: MOVE 'Y' TO WS-ERR-FLG
  reads:
  - fd_name: EIBCALEN
    verb: IF
    line: 80
    raw: IF EIBCALEN = 0
  - fd_name: EIBAID
    verb: EVALUATE
    line: 85
    raw: EVALUATE EIBAID
  - fd_name: CCDA-COMMON-MESSAGES.CCDA-MSG-THANK-YOU
    verb: MOVE
    line: 89
    raw: MOVE CCDA-MSG-THANK-YOU TO WS-MESSAGE
  - fd_name: CCDA-COMMON-MESSAGES.CCDA-MSG-INVALID-KEY
    verb: MOVE
    line: 93
    raw: MOVE CCDA-MSG-INVALID-KEY TO WS-MESSAGE
- paragraph: PROCESS-ENTER-KEY
  classification_source: annotations
  mutates:
  - fd_name: WS-VARIABLES.WS-ERR-FLG
    verb: MOVE
    line: 119
    raw: MOVE 'Y' TO WS-ERR-FLG
  - fd_name: WS-VARIABLES.WS-MESSAGE
    verb: MOVE
    line: 120
    raw: MOVE 'Please enter User ID ...' TO WS-MESSAGE
  - fd_name: COSGN0AI.USERIDL
    verb: MOVE
    line: 121
    raw: MOVE -1 TO USERIDL OF COSGN0AI
  - fd_name: COSGN0AI.PASSWDL
    verb: MOVE
    line: 126
    raw: MOVE -1 TO PASSWDL OF COSGN0AI
  reads:
  - fd_name: COSGN0AI.USERIDI
    verb: MOVE
    line: 132
    raw: MOVE FUNCTION UPPER-CASE(USERIDI OF COSGN0AI) TO
  - fd_name: COSGN0AI.PASSWDI
    verb: MOVE
    line: 135
    raw: MOVE FUNCTION UPPER-CASE(PASSWDI OF COSGN0AI) TO
  - fd_name: ERR-FLG-ON
    verb: IF
    line: 138
    raw: IF NOT ERR-FLG-ON
- paragraph: SEND-SIGNON-SCREEN
  classification_source: annotations
  mutates:
  - fd_name: COSGN0AO.ERRMSGO
    verb: MOVE
    line: 149
    raw: MOVE WS-MESSAGE TO ERRMSGO OF COSGN0AO
  reads:
  - fd_name: WS-VARIABLES.WS-MESSAGE
    verb: MOVE
    line: 149
    raw: MOVE WS-MESSAGE TO ERRMSGO OF COSGN0AO
- paragraph: SEND-PLAIN-TEXT
  classification_source: annotations
  mutates: []
  reads: []
- paragraph: POPULATE-HEADER-INFO
  classification_source: annotations
  mutates:
  - fd_name: WS-DATE-TIME.WS-CURDATE-DATA
    verb: MOVE
    line: 179
    raw: MOVE FUNCTION CURRENT-DATE TO WS-CURDATE-DATA
  - fd_name: COSGN0AO.TITLE01O
    verb: MOVE
    line: 181
    raw: MOVE CCDA-TITLE01 TO TITLE01O OF COSGN0AO
  - fd_name: COSGN0AO.TITLE02O
    verb: MOVE
    line: 182
    raw: MOVE CCDA-TITLE02 TO TITLE02O OF COSGN0AO
  - fd_name: COSGN0AO.TRNNAMEO
    verb: MOVE
    line: 183
    raw: MOVE WS-TRANID TO TRNNAMEO OF COSGN0AO
  - fd_name: COSGN0AO.PGMNAMEO
    verb: MOVE
    line: 184
    raw: MOVE WS-PGMNAME TO PGMNAMEO OF COSGN0AO
  - fd_name: WS-DATE-TIME.WS-CURDATE-MM-DD-YY.WS-CURDATE-MM
    verb: MOVE
    line: 186
    raw: MOVE WS-CURDATE-MONTH TO WS-CURDATE-MM
  - fd_name: WS-DATE-TIME.WS-CURDATE-MM-DD-YY.WS-CURDATE-DD
    verb: MOVE
    line: 187
    raw: MOVE WS-CURDATE-DAY TO WS-CURDATE-DD
  - fd_name: WS-DATE-TIME.WS-CURDATE-MM-DD-YY.WS-CURDATE-YY
    verb: MOVE
    line: 188
    raw: MOVE WS-CURDATE-YEAR(3:2) TO WS-CURDATE-YY
  - fd_name: COSGN0AO.CURDATEO
    verb: MOVE
    line: 190
    raw: MOVE WS-CURDATE-MM-DD-YY TO CURDATEO OF COSGN0AO
  - fd_name: WS-DATE-TIME.WS-CURTIME-HH-MM-SS.WS-CURTIME-HH
    verb: MOVE
    line: 192
    raw: MOVE WS-CURTIME-HOURS TO WS-CURTIME-HH
  - fd_name: WS-DATE-TIME.WS-CURTIME-HH-MM-SS.WS-CURTIME-MM
    verb: MOVE
    line: 193
    raw: MOVE WS-CURTIME-MINUTE TO WS-CURTIME-MM
  - fd_name: WS-DATE-TIME.WS-CURTIME-HH-MM-SS.WS-CURTIME-SS
    verb: MOVE
    line: 194
    raw: MOVE WS-CURTIME-SECOND TO WS-CURTIME-SS
  - fd_name: COSGN0AO.CURTIMEO
    verb: MOVE
    line: 196
    raw: MOVE WS-CURTIME-HH-MM-SS TO CURTIMEO OF COSGN0AO
  reads:
  - fd_name: CCDA-SCREEN-TITLE.CCDA-TITLE01
    verb: MOVE
    line: 181
    raw: MOVE CCDA-TITLE01 TO TITLE01O OF COSGN0AO
  - fd_name: CCDA-SCREEN-TITLE.CCDA-TITLE02
    verb: MOVE
    line: 182
    raw: MOVE CCDA-TITLE02 TO TITLE02O OF COSGN0AO
  - fd_name: WS-VARIABLES.WS-TRANID
    verb: MOVE
    line: 183
    raw: MOVE WS-TRANID TO TRNNAMEO OF COSGN0AO
  - fd_name: WS-VARIABLES.WS-PGMNAME
    verb: MOVE
    line: 184
    raw: MOVE WS-PGMNAME TO PGMNAMEO OF COSGN0AO
  - fd_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURDATE.WS-CURDATE-MONTH
    verb: MOVE
    line: 186
    raw: MOVE WS-CURDATE-MONTH TO WS-CURDATE-MM
  - fd_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURDATE.WS-CURDATE-DAY
    verb: MOVE
    line: 187
    raw: MOVE WS-CURDATE-DAY TO WS-CURDATE-DD
  - fd_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURDATE.WS-CURDATE-YEAR
    verb: MOVE
    line: 188
    raw: MOVE WS-CURDATE-YEAR(3:2) TO WS-CURDATE-YY
  - fd_name: WS-DATE-TIME.WS-CURDATE-MM-DD-YY
    verb: MOVE
    line: 190
    raw: MOVE WS-CURDATE-MM-DD-YY TO CURDATEO OF COSGN0AO
  - fd_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURTIME.WS-CURTIME-HOURS
    verb: MOVE
    line: 192
    raw: MOVE WS-CURTIME-HOURS TO WS-CURTIME-HH
  - fd_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURTIME.WS-CURTIME-MINUTE
    verb: MOVE
    line: 193
    raw: MOVE WS-CURTIME-MINUTE TO WS-CURTIME-MM
  - fd_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURTIME.WS-CURTIME-SECOND
    verb: MOVE
    line: 194
    raw: MOVE WS-CURTIME-SECOND TO WS-CURTIME-SS
  - fd_name: WS-DATE-TIME.WS-CURTIME-HH-MM-SS
    verb: MOVE
    line: 196
    raw: MOVE WS-CURTIME-HH-MM-SS TO CURTIMEO OF COSGN0AO
- paragraph: READ-USER-SEC-FILE
  classification_source: annotations
  mutates:
  - fd_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-FROM-TRANID
    verb: MOVE
    line: 224
    raw: MOVE WS-TRANID TO CDEMO-FROM-TRANID
  - fd_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-FROM-PROGRAM
    verb: MOVE
    line: 225
    raw: MOVE WS-PGMNAME TO CDEMO-FROM-PROGRAM
  - fd_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-USER-ID
    verb: MOVE
    line: 226
    raw: MOVE WS-USER-ID TO CDEMO-USER-ID
  - fd_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-USER-TYPE
    verb: MOVE
    line: 227
    raw: MOVE SEC-USR-TYPE TO CDEMO-USER-TYPE
  - fd_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-PGM-CONTEXT
    verb: MOVE
    line: 228
    raw: MOVE ZEROS TO CDEMO-PGM-CONTEXT
  - fd_name: COSGN0AI.PASSWDL
    verb: MOVE
    line: 244
    raw: MOVE -1 TO PASSWDL OF COSGN0AI
  - fd_name: WS-VARIABLES.WS-ERR-FLG
    verb: MOVE
    line: 248
    raw: MOVE 'Y' TO WS-ERR-FLG
  - fd_name: WS-VARIABLES.WS-MESSAGE
    verb: MOVE
    line: 249
    raw: MOVE 'User not found. Try again ...' TO WS-MESSAGE
  - fd_name: COSGN0AI.USERIDL
    verb: MOVE
    line: 250
    raw: MOVE -1 TO USERIDL OF COSGN0AI
  reads:
  - fd_name: WS-VARIABLES.WS-RESP-CD
    verb: EVALUATE
    line: 221
    raw: EVALUATE WS-RESP-CD
  - fd_name: SEC-USER-DATA.SEC-USR-PWD
    verb: IF
    line: 223
    raw: IF SEC-USR-PWD = WS-USER-PWD
  - fd_name: WS-VARIABLES.WS-USER-PWD
    verb: IF
    line: 223
    raw: IF SEC-USR-PWD = WS-USER-PWD
  - fd_name: WS-VARIABLES.WS-TRANID
    verb: MOVE
    line: 224
    raw: MOVE WS-TRANID TO CDEMO-FROM-TRANID
  - fd_name: WS-VARIABLES.WS-PGMNAME
    verb: MOVE
    line: 225
    raw: MOVE WS-PGMNAME TO CDEMO-FROM-PROGRAM
  - fd_name: WS-VARIABLES.WS-USER-ID
    verb: MOVE
    line: 226
    raw: MOVE WS-USER-ID TO CDEMO-USER-ID
  - fd_name: SEC-USER-DATA.SEC-USR-TYPE
    verb: MOVE
    line: 227
    raw: MOVE SEC-USR-TYPE TO CDEMO-USER-TYPE
  - fd_name: CDEMO-USRTYP-ADMIN
    verb: IF
    line: 230
    raw: IF CDEMO-USRTYP-ADMIN
memory_model:
  working_storage_bytes: 970
  linkage_bytes: 32767
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
# COSGN00C — CardDemo Application Sign-On Screen

## Purpose

COSGN00C is the interactive sign-on gateway for the CardDemo CICS application. It presents a BMS-based credential screen to the end user, validates the supplied user ID and password against a VSAM security file (USRSEC), and—upon successful authentication—transfers control to either the administrator menu or the standard main menu depending on the user's stored role type. It enforces input presence rules, case-normalization of credentials, and provides distinct error messages for each failure mode without leaking internal system details to the terminal user.

## Runtime Context

This program runs under CICS transaction identifier **CC00** on z/OS. It is a pseudo-conversational program: each user interaction causes a CICS RETURN with TRANSID CC00 and a commarea, so the next terminal input re-invokes the same program. The program uses the BMS map COSGN0A within mapset COSGN00 for all screen I/O (RECEIVE to read input, SEND to display output). It reads the USRSEC VSAM indexed dataset keyed on user ID to perform credential lookup. On successful login it issues an EXEC CICS XCTL—a non-returning transfer of control—to either COADM01C (administrator path) or COMEN01C (regular-user path), passing the populated commarea. No file writes or deletes are performed; the only file operation is a single VSAM READ. The DFHCOMMAREA linkage area conveys session state between invocations; EIBCALEN and EIBAID from the Execute Interface Block govern first-invocation detection and AID-key routing respectively.

## Data Layout

### Program Variables (WS-VARIABLES group)

The primary working-storage group bundles all local program state into a single 01-level container. Within it, an eight-character field holds the literal program name "COSGN00C" used to stamp the header display and the commarea's originating-program field. A four-character field holds the transaction identifier "CC00" used both in the screen header and in the CICS RETURN TRANSID clause. An eighty-character message buffer accumulates the human-readable status or error text that is written to the BMS map's error-message output field before each SEND. An eight-character field holds the VSAM dataset name "USRSEC  " (with trailing spaces) used as the CICS READ DATASET argument. A single-character error-flag field is governed by two condition-name (level-88) aliases: ERR-FLG-ON (value "Y") and ERR-FLG-OFF (value "N"), providing readable boolean semantics for setting and testing the flag throughout the procedure. Two binary (COMP) signed nine-digit numeric fields capture the primary and secondary CICS response codes returned by each EXEC CICS command. Two eight-character fields hold the uppercased user ID and password collected from the terminal; WS-USER-ID doubles as the VSAM key for the READ operation.

### Linkage Section (DFHCOMMAREA)

The DFHCOMMAREA group in the Linkage Section provides access to the CICS-supplied communication area. Its sole subordinate field is a one-character element that occurs between 1 and 32,767 times depending on the value of EIBCALEN, giving the program a variable-length view of the commarea byte array. In practice, the program overlays this with the typed CARDDEMO-COMMAREA structure defined in the COCOM01Y copybook, which carries the canonical commarea fields (user ID, user type, transaction ID, program name, context flags) shared across all CardDemo programs.

### Copybook-Contributed Structures

The COCOM01Y copybook provides the CARDDEMO-COMMAREA group, which includes CDEMO-USER-ID, CDEMO-USER-TYPE, CDEMO-FROM-TRANID, CDEMO-FROM-PROGRAM, CDEMO-PGM-CONTEXT, and the condition name CDEMO-USRTYP-ADMIN that tests whether the user-type byte indicates administrator access. The COSGN00 BMS copybook supplies the COSGN0AI (input) and COSGN0AO (output) map structures for screen fields including USERIDI/USERIDL, PASSWDI/PASSWDL, ERRMSGO, TITLE01O, TITLE02O, TRNNAMEO, PGMNAMEO, CURDATEO, CURTIMEO, APPLIDO, and SYSIDO. The COTTL01Y copybook provides the application title constants CCDA-TITLE01 and CCDA-TITLE02. The CSDAT01Y copybook provides the current-date working-storage group including WS-CURDATE-DATA, WS-CURDATE-MONTH, WS-CURDATE-DAY, WS-CURDATE-YEAR, WS-CURDATE-MM, WS-CURDATE-DD, WS-CURDATE-YY, WS-CURDATE-MM-DD-YY, and the parallel time fields for hours, minutes, seconds, and formatted time string. The CSMSG01Y copybook provides CCDA-MSG-THANK-YOU (the PF3 farewell text) and CCDA-MSG-INVALID-KEY (the invalid-AID error text). The CSUSR01Y copybook provides the SEC-USER-DATA group and its SEC-USR-PWD and SEC-USR-TYPE sub-fields used to interpret the VSAM user security record. DFHAID provides the CICS AID-key symbolic constants (DFHENTER, DFHPF3, etc.). DFHBMSCA provides BMS attribute byte constants used in map field control.

No REDEFINES clauses are declared in the program's own data division; the CFG redefines_clauses array is empty, so no redefines_interpretations entries are required.

## Procedure Logic

### MAIN-PARA

MAIN-PARA is the program's sole entry point, always reached first when transaction CC00 fires. It begins by clearing the error flag to its "off" state and blanking both the working-storage message buffer and the BMS output map's error-message field. It then tests the CICS Execute Interface Block field EIBCALEN: if it equals zero the program is being invoked for the first time in this pseudo-conversation (no commarea yet exists), so it clears the BMS output map to low-values, positions the cursor on the user-ID input field, and calls SEND-SIGNON-SCREEN to present a blank sign-on form. If EIBCALEN is non-zero a commarea exists and the program switches on EIBAID to determine which attention key the user pressed. An Enter key routes to PROCESS-ENTER-KEY for credential handling. PF3 moves the configured thank-you message into the message buffer and calls SEND-PLAIN-TEXT to display it and end the conversation. Any other AID key sets the error flag and moves the invalid-key message into the buffer before calling SEND-SIGNON-SCREEN to re-display the form with the error. After all branches, MAIN-PARA issues a CICS RETURN specifying TRANSID "CC00" and the CARDDEMO-COMMAREA so that the next terminal event re-invokes this program.

### END-IF

This entry is a CFG tool artifact representing the END-IF delimiter of the conditional block in MAIN-PARA; it is marked unreachable by static analysis and carries no independent business logic.

### END-EXEC

This entry is a CFG tool artifact representing an END-EXEC delimiter; it is marked unreachable by static analysis and carries no independent business logic.

### PROCESS-ENTER-KEY

Called when the user presses Enter with a commarea present. It first issues a CICS RECEIVE to read the terminal input into the COSGN0AI map structure, capturing the CICS primary and secondary response codes. It then evaluates the input fields in priority order: if the user-ID input field is blank or contains low-values, the error flag is set and the cursor is moved to the user-ID field before SEND-SIGNON-SCREEN is called with a "Please enter User ID" message; if instead the password input field is blank or contains low-values, the same pattern is applied with a "Please enter Password" message targeting the password field; otherwise, processing continues. After the evaluation, both the user-ID and password values are converted to uppercase via FUNCTION UPPER-CASE and stored in WS-USER-ID, CDEMO-USER-ID, and WS-USER-PWD respectively. Finally, if the error flag is still in the "off" state, READ-USER-SEC-FILE is performed to attempt authentication.

### END-EVALUATE

This entry is a CFG tool artifact representing an END-EVALUATE delimiter in PROCESS-ENTER-KEY; it is marked unreachable by static analysis and carries no independent business logic.

### SEND-SIGNON-SCREEN

Invoked from multiple points whenever the sign-on form must be displayed or re-displayed. It first calls POPULATE-HEADER-INFO to ensure the date, time, application ID, and system ID are current in the output map. It then copies the current working-storage message buffer content into the ERRMSGO field of the BMS output map. Finally, it issues a CICS SEND MAP command for map COSGN0A in mapset COSGN00, specifying the output map structure, ERASE (to clear the terminal screen before writing), and CURSOR (to position the cursor at the field previously assigned a cursor-position value of -1).

### SEND-PLAIN-TEXT

Invoked exclusively on the PF3 path. It issues a CICS SEND TEXT command to write the contents of the working-storage message buffer as raw text to the terminal, with ERASE to clear the screen and FREEKB to unlock the terminal keyboard. It then issues an unconditional CICS RETURN (with no TRANSID) to terminate the task, ending the pseudo-conversation entirely rather than re-queuing transaction CC00.

### POPULATE-HEADER-INFO

Called at the start of every SEND-SIGNON-SCREEN invocation to keep the header current. It invokes FUNCTION CURRENT-DATE to obtain the system date and time, then distributes month, day, and two-digit year into display sub-fields and assembles them into the formatted date output field. It performs the parallel operation for the current time, extracting hours, minutes, and seconds into the formatted time output field. It moves the application title lines from the COTTL01Y constants, the transaction ID from WS-TRANID, and the program name from WS-PGMNAME into their respective map output fields. It then issues two CICS ASSIGN commands: one to retrieve the CICS APPLID (application identifier) and a second to retrieve the SYSID (system identifier), storing each in the corresponding BMS output map field for display in the screen header.

### READ-USER-SEC-FILE

Called from PROCESS-ENTER-KEY after all input validations pass and the error flag is clear. It issues a CICS READ against dataset "USRSEC  " using WS-USER-ID as the key, reading the result directly into the SEC-USER-DATA copybook structure. The CICS primary response code is examined in an EVALUATE block. When the response is zero (successful read), the program compares the SEC-USR-PWD field from the VSAM record against WS-USER-PWD: if they match, the commarea is populated with WS-TRANID (from-tranid), WS-PGMNAME (from-program), WS-USER-ID (user-id), SEC-USR-TYPE (user-type), and a zero program-context value, then control is transferred via CICS XCTL to COADM01C if the user-type satisfies CDEMO-USRTYP-ADMIN or to COMEN01C otherwise; if the passwords do not match, a "Wrong Password" message is placed in the buffer and SEND-SIGNON-SCREEN is called with the cursor on the password field. When the response is 13 (record not found), the error flag is set and a "User not found" message causes SEND-SIGNON-SCREEN to be called with the cursor on the user-ID field. Any other response code also sets the error flag and calls SEND-SIGNON-SCREEN with a generic verification-failure message.

## Business Rules Surfaced

**BR-001** — If no commarea is present (first invocation), the program displays the sign-on screen immediately without attempting any input processing.

**BR-002** — Only the Enter key triggers credential processing; PF3 exits gracefully with a thank-you message; all other AID keys produce an invalid-key error on the sign-on screen.

**BR-003** — A blank or low-value user ID field stops processing and prompts the user to supply a user ID before authentication is attempted.

**BR-004** — A blank or low-value password field stops processing and prompts the user to supply a password before authentication is attempted.

**BR-005** — User ID and password values received from the terminal are uppercased before comparison and commarea storage, making authentication effectively case-insensitive.

**BR-006** — The VSAM security file is only read if no error flag was raised during input validation; validation errors prevent the file access entirely.

**BR-007** — A successful VSAM read (response 0) requires an exact password match against the stored record; a mismatch produces a "Wrong Password" error without indicating which field was incorrect.

**BR-008** — Authenticated users flagged as administrators (per the user-type byte in the security record) are routed to the administration program COADM01C; all other authenticated users are routed to the main menu program COMEN01C.

**BR-009** — A VSAM response code of 13 (record not found) produces a "User not found" error, distinguishing a missing user from a wrong password at the message level.

**BR-010** — Any VSAM response code other than 0 or 13 produces a generic "Unable to verify the User" message, hiding internal system error details from the end user.

**BR-011** — On successful authentication, the commarea is fully populated with originating transaction ID, program name, user ID, user type, and a zeroed program-context value before control is transferred, establishing a trusted session context for downstream programs.

**BR-012** — The CICS RETURN at the conclusion of MAIN-PARA always specifies TRANSID CC00 and passes the commarea, ensuring the sign-on screen is re-presented on the next terminal event unless an XCTL has already transferred control away.

## Graph Summary

- **CALLS (XCTL):** COSGN00C → COADM01C (condition: CDEMO-USRTYP-ADMIN is true)
- **CALLS (XCTL):** COSGN00C → COMEN01C (condition: CDEMO-USRTYP-ADMIN is false)
- **COPYBOOK:** COSGN00C uses COCOM01Y (commarea structure / session context)
- **COPYBOOK:** COSGN00C uses COSGN00 (BMS map COSGN0A input/output fields)
- **COPYBOOK:** COSGN00C uses COTTL01Y (application title constants)
- **COPYBOOK:** COSGN00C uses CSDAT01Y (current-date and current-time working-storage fields)
- **COPYBOOK:** COSGN00C uses CSMSG01Y (thank-you and invalid-key message constants)
- **COPYBOOK:** COSGN00C uses CSUSR01Y (user security record structure SEC-USER-DATA)
- **COPYBOOK:** COSGN00C uses DFHAID (AID-key constants DFHENTER, DFHPF3)
- **COPYBOOK:** COSGN00C uses DFHBMSCA (BMS attribute byte constants)
- **VSAM READ:** COSGN00C reads USRSEC (keyed on user ID; no writes or deletes)
- **CICS COMMANDS:** RETURN (pseudo-conversational re-queue to CC00), RECEIVE (BMS map input), SEND (BMS map output and plain-text output), ASSIGN (APPLID and SYSID retrieval), READ (USRSEC security record), XCTL (non-returning transfer to admin or main menu)
- **TRANSACTION:** Services CICS transaction ID CC00
- **RULES (reachable):** BR-001 through BR-012 (all 12 rules originate in reachable paragraphs)
- **DEAD CODE PARAGRAPHS:** END-IF, END-EXEC, END-EVALUATE (CFG tool artifacts; no business logic)
- **NODES:** 9 CFG nodes (per smojol_node_count); 6 reachable procedure paragraphs; 2 data groups; 8 copybooks; 2 XCTL targets
