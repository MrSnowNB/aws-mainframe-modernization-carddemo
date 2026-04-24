---
schema_version: cobol-md/1.2
program_id: COMEN01C
source_file: app/cbl/COMEN01C.cbl
source_sha: a404313748b0715a306336ac599b3e585697c05c
translation_date: '2026-04-23'
translating_agent: claude-opus-4-5 (subagent)
aifirst_task_id: T-2026-04-23-001
cfg_source: validation/structure/COMEN01C_cfg.json
business_domain: Administration
subtype: Menu
author: AWS
date_written: null
lines_of_code: 213
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
- program: COSGN00C
  condition: EIBCALEN = 0 (no commarea on first entry)
  call_type: EXEC CICS XCTL
- program: COSGN00C
  condition: PF3 pressed by user
  call_type: EXEC CICS XCTL
- program: CDEMO-MENU-OPT-PGMNAME(WS-OPTION)
  condition: Valid option selected and program is COPAUS0C, EXEC CICS INQUIRE returns NORMAL
  call_type: EXEC CICS XCTL
- program: CDEMO-MENU-OPT-PGMNAME(WS-OPTION)
  condition: Valid option selected and program name does not begin with DUMMY and is not COPAUS0C
  call_type: EXEC CICS XCTL
called_by:
- COSGN00C
- COACTUPC
- COACTVWC
- COBIL00C
- COCRDLIC
- COCRDSLC
- COCRDUPC
- CORPT00C
- COTRN00C
- COTRN01C
- COTRN02C
copybooks_used:
- name: COCOM01Y
  path: app/cpy/COCOM01Y.cpy
  sha: null
- name: COMEN02Y
  path: app/cpy/COMEN02Y.cpy
  sha: null
- name: COMEN01
  path: app/cpy-bms/COMEN01.CPY
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
  path: null
  sha: null
- name: DFHBMSCA
  path: null
  sha: null
file_control: []
cics_commands:
- RETURN
- INQUIRE
- XCTL
- SEND
- RECEIVE
transaction_ids:
- CM00
data_items:
- name: WS-VARIABLES
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Top-level working-storage group holding all program-local scalar variables
- name: WS-PGMNAME
  level: 5
  picture: X(08)
  usage: null
  value: COMEN01C
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Eight-character literal holding the name of this program, used when setting CDEMO-FROM-PROGRAM in the commarea
    before each XCTL dispatch
- name: WS-TRANID
  level: 5
  picture: X(04)
  usage: null
  value: CM00
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Four-character CICS transaction identifier for this menu program; passed to CDEMO-FROM-TRANID and used on EXEC
    CICS RETURN to re-invoke the program
- name: WS-MESSAGE
  level: 5
  picture: X(80)
  usage: null
  value: SPACES
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Eighty-character buffer holding the user-facing error or status message displayed in the ERRMSGO field of the
    BMS map
- name: WS-USRSEC-FILE
  level: 5
  picture: X(08)
  usage: null
  value: 'USRSEC  '
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Eight-character ddname literal for the user-security VSAM file; defined in working storage but not referenced
    by any reachable logic in this program
- name: WS-ERR-FLG
  level: 5
  picture: X(01)
  usage: null
  value: N
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Single-character error flag; condition names ERR-FLG-ON (value Y) and ERR-FLG-OFF (value N) are used to gate further
    processing and short-circuit XCTL dispatch
- name: ERR-FLG-ON
  level: 88
  picture: null
  usage: null
  value: Y
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Condition-name that evaluates true when WS-ERR-FLG equals Y, indicating an input validation error has been detected
- name: ERR-FLG-OFF
  level: 88
  picture: null
  usage: null
  value: N
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Condition-name that evaluates true when WS-ERR-FLG equals N, indicating no error is currently active
- name: WS-RESP-CD
  level: 5
  picture: S9(09)
  usage: COMP
  value: '0'
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Binary signed fullword receiving the CICS RESP response code from EXEC CICS RECEIVE, used to detect map-receive
    failures
- name: WS-REAS-CD
  level: 5
  picture: S9(09)
  usage: COMP
  value: '0'
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Binary signed fullword receiving the CICS RESP2 reason code from EXEC CICS RECEIVE, providing extended diagnostic
    detail alongside WS-RESP-CD
- name: WS-OPTION-X
  level: 5
  picture: X(02)
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Two-character right-justified work field that holds the raw alphanumeric option string received from the BMS map
    before conversion to numeric WS-OPTION
- name: WS-OPTION
  level: 5
  picture: 9(02)
  usage: null
  value: '0'
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Two-digit numeric field holding the validated menu option number entered by the user, used as the subscript into
    the CDEMO-MENU-OPT table
- name: WS-IDX
  level: 5
  picture: S9(04)
  usage: COMP
  value: '0'
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Binary signed halfword loop index used both in the trailing-space trim of the raw option input and in the PERFORM
    VARYING loop that builds menu-option display lines
- name: WS-MENU-OPT-TXT
  level: 5
  picture: X(40)
  usage: null
  value: SPACES
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Forty-character work buffer built by concatenating the option number, a period-space separator, and the option
    name; moved to the appropriate map output field for each of the twelve possible menu slots
- name: DFHCOMMAREA
  level: 1
  picture: null
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Linkage-section entry mapped by CICS to the commarea passed by the invoking transaction; its single repeating-occurrence
    subordinate field is used to copy the inbound commarea into CARDDEMO-COMMAREA
- name: LK-COMMAREA
  level: 5
  picture: X(01)
  usage: null
  value: null
  redefines: null
  redefines_interpretations: []
  dead_code_flag: false
  semantic: Variable-length character array within DFHCOMMAREA, dimensioned from 1 to 32767 bytes depending on EIBCALEN, providing
    the byte-by-byte copy source for populating CARDDEMO-COMMAREA
procedure_paragraphs:
- name: MAIN-PARA
  reachable: true
  performs:
  - RETURN-TO-SIGNON-SCREEN
  - SEND-MENU-SCREEN
  - RECEIVE-MENU-SCREEN
  - PROCESS-ENTER-KEY
  goto_targets: []
  summary: Entry point for transaction CM00; initializes the error flag, routes first-entry requests to the sign-on screen,
    controls the pseudo-conversational receive/send cycle, and dispatches ENTER or PF3 keystrokes before issuing EXEC CICS
    RETURN to suspend the task
- name: END-EXEC
  reachable: false
  performs: []
  goto_targets: []
  summary: Unreachable artifact paragraph generated by the CFG tool from an EXEC CICS END-EXEC delimiter; contains no executable
    logic and is excluded from business-rule queries
- name: PROCESS-ENTER-KEY
  reachable: true
  performs:
  - SEND-MENU-SCREEN
  goto_targets: []
  summary: Validates the numeric option entered on the menu map, enforces admin-only access restrictions, and issues an EXEC
    CICS XCTL to the program associated with the chosen option, with special handling for the COPAUS0C availability check
    and DUMMY placeholder options
- name: END-IF
  reachable: false
  performs: []
  goto_targets: []
  summary: Unreachable artifact paragraph generated by the CFG tool from an IF/END-IF delimiter; contains no executable logic
    and is excluded from business-rule queries
- name: RETURN-TO-SIGNON-SCREEN
  reachable: true
  performs: []
  goto_targets: []
  summary: Defaults CDEMO-TO-PROGRAM to COSGN00C when the target is not already set, then issues an unconditional EXEC CICS
    XCTL to transfer control to the sign-on screen
- name: SEND-MENU-SCREEN
  reachable: true
  performs:
  - POPULATE-HEADER-INFO
  - BUILD-MENU-OPTIONS
  goto_targets: []
  summary: Prepares the BMS map COMEN1AO by populating the header and menu-option lines, moves the current message into the
    error-message field, and sends the COMEN1A map from mapset COMEN01 with ERASE
- name: RECEIVE-MENU-SCREEN
  reachable: true
  performs: []
  goto_targets: []
  summary: Issues EXEC CICS RECEIVE for the COMEN1A map into COMEN1AI, capturing the user's keyboard input and storing CICS
    response codes in WS-RESP-CD and WS-REAS-CD
- name: POPULATE-HEADER-INFO
  reachable: true
  performs: []
  goto_targets: []
  summary: Reads the current date and time using FUNCTION CURRENT-DATE, formats them as MM/DD/YY and HH:MM:SS strings, and
    moves the application title lines, transaction ID, program name, date, and time into the output map header fields
- name: BUILD-MENU-OPTIONS
  reachable: true
  performs: []
  goto_targets: []
  summary: Iterates over the CDEMO-MENU-OPT table (up to twelve entries) and assembles each option's display text as a concatenation
    of option number, separator, and option name, placing the result in the corresponding OPTN001O through OPTN012O map output
    field
- name: END-PERFORM
  reachable: false
  performs: []
  goto_targets: []
  summary: Unreachable artifact paragraph generated by the CFG tool from a PERFORM/END-PERFORM delimiter; contains no executable
    logic and is excluded from business-rule queries
business_rules:
- id: BR-001
  rule: If the commarea length (EIBCALEN) is zero on entry, the program immediately transfers control to the sign-on program
    COSGN00C without displaying the menu, preventing direct transaction invocation without an established session
  source_paragraph: MAIN-PARA
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-002
  rule: On first entry to the menu (CDEMO-PGM-REENTER flag not set), the program initialises the output map with low-values
    and displays the menu screen without reading user input, ensuring a clean initial presentation
  source_paragraph: MAIN-PARA
  rule_type: display
  confidence: high
  reachable: true
- id: BR-003
  rule: If an attention identifier other than ENTER or PF3 is pressed, the error flag is set and the invalid-key message from
    CCDA-MSG-INVALID-KEY is displayed; no navigation occurs
  source_paragraph: MAIN-PARA
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-004
  rule: If the value entered in the option field is non-numeric, equals zero, or exceeds CDEMO-MENU-OPT-COUNT, the program
    displays 'Please enter a valid option number...' and re-presents the menu without dispatching
  source_paragraph: PROCESS-ENTER-KEY
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-005
  rule: If the signed-in user type is regular user (CDEMO-USRTYP-USER) and the selected option is flagged as admin-only (option
    user-type indicator equals 'A'), access is denied with the message 'No access - Admin Only option...' and the menu is
    re-displayed
  source_paragraph: PROCESS-ENTER-KEY
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-006
  rule: When the selected program is COPAUS0C, an EXEC CICS INQUIRE is performed first; if COPAUS0C is not installed (EIBRESP
    is not NORMAL), a red error message is displayed stating the option is not installed instead of dispatching
  source_paragraph: PROCESS-ENTER-KEY
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-007
  rule: If the program name associated with the selected option begins with 'DUMMY', a green informational message is displayed
    indicating the feature is coming soon, and no XCTL dispatch is performed
  source_paragraph: PROCESS-ENTER-KEY
  rule_type: display
  confidence: high
  reachable: true
- id: BR-008
  rule: For any valid, installed, non-dummy option, the program name is looked up from the CDEMO-MENU-OPT-PGMNAME array using
    the option number as a subscript, and control is transferred to that program via EXEC CICS XCTL with the shared commarea
  source_paragraph: PROCESS-ENTER-KEY
  rule_type: lookup
  confidence: high
  reachable: true
- id: BR-009
  rule: When PF3 is pressed, control is unconditionally transferred to COSGN00C (the sign-on screen), terminating the current
    menu session
  source_paragraph: MAIN-PARA
  rule_type: guard
  confidence: high
  reachable: true
- id: BR-010
  rule: Before every EXEC CICS XCTL dispatch to a sub-program, the commarea fields CDEMO-FROM-TRANID, CDEMO-FROM-PROGRAM,
    and CDEMO-PGM-CONTEXT are set to identify the calling transaction and program, enabling the target to return correctly
  source_paragraph: PROCESS-ENTER-KEY
  rule_type: transform
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
      name: WS-OPTION-X
      line: 45
      usage: DISPLAY
      pic: X(02)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: WS-VARIABLES.WS-OPTION-X
    - level: 5
      name: WS-OPTION
      line: 46
      usage: DISPLAY
      pic: 9(02)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: WS-VARIABLES.WS-OPTION
    - level: 5
      name: WS-IDX
      line: 47
      usage: COMP
      pic: S9(04)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: WS-VARIABLES.WS-IDX
    - level: 5
      name: WS-MENU-OPT-TXT
      line: 48
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: WS-VARIABLES.WS-MENU-OPT-TXT
    slack_bytes_before: 0
    total_bytes: 155
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
    name: CARDDEMO-MAIN-MENU-OPTIONS
    line: 19
    usage: DISPLAY
    children:
    - level: 5
      name: CDEMO-MENU-OPT-COUNT
      line: 21
      usage: DISPLAY
      pic: 9(02)
      children: []
      encoding: zoned-decimal
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPT-COUNT
    - level: 5
      name: CDEMO-MENU-OPTIONS-DATA
      line: 23
      usage: DISPLAY
      children:
      - level: 10
        name: FILLER
        line: 25
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 26
        usage: DISPLAY
        pic: X(35)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 35
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 28
        usage: DISPLAY
        pic: X(08)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 8
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 29
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 31
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 32
        usage: DISPLAY
        pic: X(35)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 35
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 34
        usage: DISPLAY
        pic: X(08)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 8
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 35
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 37
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 38
        usage: DISPLAY
        pic: X(35)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 35
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 40
        usage: DISPLAY
        pic: X(08)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 8
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 41
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 43
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 44
        usage: DISPLAY
        pic: X(35)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 35
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 46
        usage: DISPLAY
        pic: X(08)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 8
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 47
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 49
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 50
        usage: DISPLAY
        pic: X(35)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 35
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 52
        usage: DISPLAY
        pic: X(08)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 8
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 53
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 55
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 56
        usage: DISPLAY
        pic: X(35)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 35
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 58
        usage: DISPLAY
        pic: X(08)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 8
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 59
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 61
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 62
        usage: DISPLAY
        pic: X(35)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 35
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 64
        usage: DISPLAY
        pic: X(08)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 8
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 65
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 67
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 68
        usage: DISPLAY
        pic: X(35)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 35
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 71
        usage: DISPLAY
        pic: X(08)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 8
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 72
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 74
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 75
        usage: DISPLAY
        pic: X(35)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 35
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 77
        usage: DISPLAY
        pic: X(08)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 8
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 78
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 80
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 81
        usage: DISPLAY
        pic: X(35)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 35
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 83
        usage: DISPLAY
        pic: X(08)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 8
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 84
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 86
        usage: DISPLAY
        pic: 9(02)
        children: []
        encoding: zoned-decimal
        slack_bytes_before: 0
        total_bytes: 2
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 87
        usage: DISPLAY
        pic: X(35)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 35
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 89
        usage: DISPLAY
        pic: X(08)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 8
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      - level: 10
        name: FILLER
        line: 90
        usage: DISPLAY
        pic: X(01)
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA.FILLER
      slack_bytes_before: 0
      total_bytes: 506
      qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS-DATA
    - level: 5
      name: CDEMO-MENU-OPTIONS
      line: 93
      redefines: CDEMO-MENU-OPTIONS-DATA
      usage: DISPLAY
      children:
      - level: 10
        name: CDEMO-MENU-OPT
        line: 94
        occurs: 12
        usage: DISPLAY
        children:
        - level: 15
          name: CDEMO-MENU-OPT-NUM
          line: 95
          usage: DISPLAY
          pic: 9(02)
          children: []
          encoding: zoned-decimal
          slack_bytes_before: 0
          total_bytes: 2
          qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS.CDEMO-MENU-OPT.CDEMO-MENU-OPT-NUM
        - level: 15
          name: CDEMO-MENU-OPT-NAME
          line: 96
          usage: DISPLAY
          pic: X(35)
          children: []
          encoding: display
          slack_bytes_before: 0
          total_bytes: 35
          qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS.CDEMO-MENU-OPT.CDEMO-MENU-OPT-NAME
        - level: 15
          name: CDEMO-MENU-OPT-PGMNAME
          line: 97
          usage: DISPLAY
          pic: X(08)
          children: []
          encoding: display
          slack_bytes_before: 0
          total_bytes: 8
          qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS.CDEMO-MENU-OPT.CDEMO-MENU-OPT-PGMNAME
        - level: 15
          name: CDEMO-MENU-OPT-USRTYPE
          line: 98
          usage: DISPLAY
          pic: X(01)
          children: []
          encoding: display
          slack_bytes_before: 0
          total_bytes: 1
          qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS.CDEMO-MENU-OPT.CDEMO-MENU-OPT-USRTYPE
        slack_bytes_before: 0
        total_bytes: 552
        qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS.CDEMO-MENU-OPT
      total_bytes: 506
      slack_bytes_before: 0
      qualified_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS
    slack_bytes_before: 0
    total_bytes: 508
    qualified_name: CARDDEMO-MAIN-MENU-OPTIONS
    section: working_storage
  - level: 1
    name: COMEN1AI
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
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: TRNNAMEL
      line: 19
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.TRNNAMEL
    - level: 2
      name: TRNNAMEF
      line: 20
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.TRNNAMEF
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
        qualified_name: COMEN1AI.FILLER.TRNNAMEA
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 23
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: TRNNAMEI
      line: 24
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.TRNNAMEI
    - level: 2
      name: TITLE01L
      line: 25
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.TITLE01L
    - level: 2
      name: TITLE01F
      line: 26
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.TITLE01F
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
        qualified_name: COMEN1AI.FILLER.TITLE01A
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 29
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: TITLE01I
      line: 30
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AI.TITLE01I
    - level: 2
      name: CURDATEL
      line: 31
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.CURDATEL
    - level: 2
      name: CURDATEF
      line: 32
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.CURDATEF
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
        qualified_name: COMEN1AI.FILLER.CURDATEA
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 35
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: CURDATEI
      line: 36
      usage: DISPLAY
      pic: X(8)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: COMEN1AI.CURDATEI
    - level: 2
      name: PGMNAMEL
      line: 37
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.PGMNAMEL
    - level: 2
      name: PGMNAMEF
      line: 38
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.PGMNAMEF
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
        qualified_name: COMEN1AI.FILLER.PGMNAMEA
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 41
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: PGMNAMEI
      line: 42
      usage: DISPLAY
      pic: X(8)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: COMEN1AI.PGMNAMEI
    - level: 2
      name: TITLE02L
      line: 43
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.TITLE02L
    - level: 2
      name: TITLE02F
      line: 44
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.TITLE02F
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
        qualified_name: COMEN1AI.FILLER.TITLE02A
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 47
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: TITLE02I
      line: 48
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AI.TITLE02I
    - level: 2
      name: CURTIMEL
      line: 49
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.CURTIMEL
    - level: 2
      name: CURTIMEF
      line: 50
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.CURTIMEF
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
        qualified_name: COMEN1AI.FILLER.CURTIMEA
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 53
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: CURTIMEI
      line: 54
      usage: DISPLAY
      pic: X(8)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: COMEN1AI.CURTIMEI
    - level: 2
      name: OPTN001L
      line: 55
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.OPTN001L
    - level: 2
      name: OPTN001F
      line: 56
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.OPTN001F
    - level: 2
      name: FILLER
      line: 57
      redefines: OPTN001F
      usage: DISPLAY
      children:
      - level: 3
        name: OPTN001A
        line: 58
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COMEN1AI.FILLER.OPTN001A
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 59
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: OPTN001I
      line: 60
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AI.OPTN001I
    - level: 2
      name: OPTN002L
      line: 61
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.OPTN002L
    - level: 2
      name: OPTN002F
      line: 62
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.OPTN002F
    - level: 2
      name: FILLER
      line: 63
      redefines: OPTN002F
      usage: DISPLAY
      children:
      - level: 3
        name: OPTN002A
        line: 64
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COMEN1AI.FILLER.OPTN002A
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 65
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: OPTN002I
      line: 66
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AI.OPTN002I
    - level: 2
      name: OPTN003L
      line: 67
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.OPTN003L
    - level: 2
      name: OPTN003F
      line: 68
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.OPTN003F
    - level: 2
      name: FILLER
      line: 69
      redefines: OPTN003F
      usage: DISPLAY
      children:
      - level: 3
        name: OPTN003A
        line: 70
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COMEN1AI.FILLER.OPTN003A
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 71
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: OPTN003I
      line: 72
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AI.OPTN003I
    - level: 2
      name: OPTN004L
      line: 73
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.OPTN004L
    - level: 2
      name: OPTN004F
      line: 74
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.OPTN004F
    - level: 2
      name: FILLER
      line: 75
      redefines: OPTN004F
      usage: DISPLAY
      children:
      - level: 3
        name: OPTN004A
        line: 76
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COMEN1AI.FILLER.OPTN004A
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 77
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: OPTN004I
      line: 78
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AI.OPTN004I
    - level: 2
      name: OPTN005L
      line: 79
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.OPTN005L
    - level: 2
      name: OPTN005F
      line: 80
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.OPTN005F
    - level: 2
      name: FILLER
      line: 81
      redefines: OPTN005F
      usage: DISPLAY
      children:
      - level: 3
        name: OPTN005A
        line: 82
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COMEN1AI.FILLER.OPTN005A
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 83
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: OPTN005I
      line: 84
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AI.OPTN005I
    - level: 2
      name: OPTN006L
      line: 85
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.OPTN006L
    - level: 2
      name: OPTN006F
      line: 86
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.OPTN006F
    - level: 2
      name: FILLER
      line: 87
      redefines: OPTN006F
      usage: DISPLAY
      children:
      - level: 3
        name: OPTN006A
        line: 88
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COMEN1AI.FILLER.OPTN006A
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 89
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: OPTN006I
      line: 90
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AI.OPTN006I
    - level: 2
      name: OPTN007L
      line: 91
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.OPTN007L
    - level: 2
      name: OPTN007F
      line: 92
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.OPTN007F
    - level: 2
      name: FILLER
      line: 93
      redefines: OPTN007F
      usage: DISPLAY
      children:
      - level: 3
        name: OPTN007A
        line: 94
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COMEN1AI.FILLER.OPTN007A
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 95
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: OPTN007I
      line: 96
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AI.OPTN007I
    - level: 2
      name: OPTN008L
      line: 97
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.OPTN008L
    - level: 2
      name: OPTN008F
      line: 98
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.OPTN008F
    - level: 2
      name: FILLER
      line: 99
      redefines: OPTN008F
      usage: DISPLAY
      children:
      - level: 3
        name: OPTN008A
        line: 100
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COMEN1AI.FILLER.OPTN008A
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 101
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: OPTN008I
      line: 102
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AI.OPTN008I
    - level: 2
      name: OPTN009L
      line: 103
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.OPTN009L
    - level: 2
      name: OPTN009F
      line: 104
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.OPTN009F
    - level: 2
      name: FILLER
      line: 105
      redefines: OPTN009F
      usage: DISPLAY
      children:
      - level: 3
        name: OPTN009A
        line: 106
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COMEN1AI.FILLER.OPTN009A
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 107
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: OPTN009I
      line: 108
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AI.OPTN009I
    - level: 2
      name: OPTN010L
      line: 109
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.OPTN010L
    - level: 2
      name: OPTN010F
      line: 110
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.OPTN010F
    - level: 2
      name: FILLER
      line: 111
      redefines: OPTN010F
      usage: DISPLAY
      children:
      - level: 3
        name: OPTN010A
        line: 112
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COMEN1AI.FILLER.OPTN010A
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 113
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: OPTN010I
      line: 114
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AI.OPTN010I
    - level: 2
      name: OPTN011L
      line: 115
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.OPTN011L
    - level: 2
      name: OPTN011F
      line: 116
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.OPTN011F
    - level: 2
      name: FILLER
      line: 117
      redefines: OPTN011F
      usage: DISPLAY
      children:
      - level: 3
        name: OPTN011A
        line: 118
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COMEN1AI.FILLER.OPTN011A
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 119
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: OPTN011I
      line: 120
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AI.OPTN011I
    - level: 2
      name: OPTN012L
      line: 121
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.OPTN012L
    - level: 2
      name: OPTN012F
      line: 122
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.OPTN012F
    - level: 2
      name: FILLER
      line: 123
      redefines: OPTN012F
      usage: DISPLAY
      children:
      - level: 3
        name: OPTN012A
        line: 124
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COMEN1AI.FILLER.OPTN012A
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 125
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: OPTN012I
      line: 126
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AI.OPTN012I
    - level: 2
      name: OPTIONL
      line: 127
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.OPTIONL
    - level: 2
      name: OPTIONF
      line: 128
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.OPTIONF
    - level: 2
      name: FILLER
      line: 129
      redefines: OPTIONF
      usage: DISPLAY
      children:
      - level: 3
        name: OPTIONA
        line: 130
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COMEN1AI.FILLER.OPTIONA
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 131
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: OPTIONI
      line: 132
      usage: DISPLAY
      pic: X(2)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.OPTIONI
    - level: 2
      name: ERRMSGL
      line: 133
      usage: COMP
      pic: S9(4)
      children: []
      encoding: binary
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AI.ERRMSGL
    - level: 2
      name: ERRMSGF
      line: 134
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AI.ERRMSGF
    - level: 2
      name: FILLER
      line: 135
      redefines: ERRMSGF
      usage: DISPLAY
      children:
      - level: 3
        name: ERRMSGA
        line: 136
        usage: DISPLAY
        pic: X
        children: []
        encoding: display
        slack_bytes_before: 0
        total_bytes: 1
        qualified_name: COMEN1AI.FILLER.ERRMSGA
      total_bytes: 1
      slack_bytes_before: 0
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: FILLER
      line: 137
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AI.FILLER
    - level: 2
      name: ERRMSGI
      line: 138
      usage: DISPLAY
      pic: X(78)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 78
      qualified_name: COMEN1AI.ERRMSGI
    slack_bytes_before: 0
    total_bytes: 820
    qualified_name: COMEN1AI
    section: working_storage
  - level: 1
    name: COMEN1AO
    line: 139
    redefines: COMEN1AI
    usage: DISPLAY
    children:
    - level: 2
      name: FILLER
      line: 140
      usage: DISPLAY
      pic: X(12)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 12
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: FILLER
      line: 141
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: TRNNAMEC
      line: 142
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.TRNNAMEC
    - level: 2
      name: TRNNAMEP
      line: 143
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.TRNNAMEP
    - level: 2
      name: TRNNAMEH
      line: 144
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.TRNNAMEH
    - level: 2
      name: TRNNAMEV
      line: 145
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.TRNNAMEV
    - level: 2
      name: TRNNAMEO
      line: 146
      usage: DISPLAY
      pic: X(4)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 4
      qualified_name: COMEN1AO.TRNNAMEO
    - level: 2
      name: FILLER
      line: 147
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: TITLE01C
      line: 148
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.TITLE01C
    - level: 2
      name: TITLE01P
      line: 149
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.TITLE01P
    - level: 2
      name: TITLE01H
      line: 150
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.TITLE01H
    - level: 2
      name: TITLE01V
      line: 151
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.TITLE01V
    - level: 2
      name: TITLE01O
      line: 152
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AO.TITLE01O
    - level: 2
      name: FILLER
      line: 153
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: CURDATEC
      line: 154
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.CURDATEC
    - level: 2
      name: CURDATEP
      line: 155
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.CURDATEP
    - level: 2
      name: CURDATEH
      line: 156
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.CURDATEH
    - level: 2
      name: CURDATEV
      line: 157
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.CURDATEV
    - level: 2
      name: CURDATEO
      line: 158
      usage: DISPLAY
      pic: X(8)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: COMEN1AO.CURDATEO
    - level: 2
      name: FILLER
      line: 159
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: PGMNAMEC
      line: 160
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.PGMNAMEC
    - level: 2
      name: PGMNAMEP
      line: 161
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.PGMNAMEP
    - level: 2
      name: PGMNAMEH
      line: 162
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.PGMNAMEH
    - level: 2
      name: PGMNAMEV
      line: 163
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.PGMNAMEV
    - level: 2
      name: PGMNAMEO
      line: 164
      usage: DISPLAY
      pic: X(8)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: COMEN1AO.PGMNAMEO
    - level: 2
      name: FILLER
      line: 165
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: TITLE02C
      line: 166
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.TITLE02C
    - level: 2
      name: TITLE02P
      line: 167
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.TITLE02P
    - level: 2
      name: TITLE02H
      line: 168
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.TITLE02H
    - level: 2
      name: TITLE02V
      line: 169
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.TITLE02V
    - level: 2
      name: TITLE02O
      line: 170
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AO.TITLE02O
    - level: 2
      name: FILLER
      line: 171
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: CURTIMEC
      line: 172
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.CURTIMEC
    - level: 2
      name: CURTIMEP
      line: 173
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.CURTIMEP
    - level: 2
      name: CURTIMEH
      line: 174
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.CURTIMEH
    - level: 2
      name: CURTIMEV
      line: 175
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.CURTIMEV
    - level: 2
      name: CURTIMEO
      line: 176
      usage: DISPLAY
      pic: X(8)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 8
      qualified_name: COMEN1AO.CURTIMEO
    - level: 2
      name: FILLER
      line: 177
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: OPTN001C
      line: 178
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN001C
    - level: 2
      name: OPTN001P
      line: 179
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN001P
    - level: 2
      name: OPTN001H
      line: 180
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN001H
    - level: 2
      name: OPTN001V
      line: 181
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN001V
    - level: 2
      name: OPTN001O
      line: 182
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AO.OPTN001O
    - level: 2
      name: FILLER
      line: 183
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: OPTN002C
      line: 184
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN002C
    - level: 2
      name: OPTN002P
      line: 185
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN002P
    - level: 2
      name: OPTN002H
      line: 186
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN002H
    - level: 2
      name: OPTN002V
      line: 187
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN002V
    - level: 2
      name: OPTN002O
      line: 188
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AO.OPTN002O
    - level: 2
      name: FILLER
      line: 189
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: OPTN003C
      line: 190
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN003C
    - level: 2
      name: OPTN003P
      line: 191
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN003P
    - level: 2
      name: OPTN003H
      line: 192
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN003H
    - level: 2
      name: OPTN003V
      line: 193
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN003V
    - level: 2
      name: OPTN003O
      line: 194
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AO.OPTN003O
    - level: 2
      name: FILLER
      line: 195
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: OPTN004C
      line: 196
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN004C
    - level: 2
      name: OPTN004P
      line: 197
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN004P
    - level: 2
      name: OPTN004H
      line: 198
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN004H
    - level: 2
      name: OPTN004V
      line: 199
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN004V
    - level: 2
      name: OPTN004O
      line: 200
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AO.OPTN004O
    - level: 2
      name: FILLER
      line: 201
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: OPTN005C
      line: 202
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN005C
    - level: 2
      name: OPTN005P
      line: 203
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN005P
    - level: 2
      name: OPTN005H
      line: 204
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN005H
    - level: 2
      name: OPTN005V
      line: 205
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN005V
    - level: 2
      name: OPTN005O
      line: 206
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AO.OPTN005O
    - level: 2
      name: FILLER
      line: 207
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: OPTN006C
      line: 208
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN006C
    - level: 2
      name: OPTN006P
      line: 209
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN006P
    - level: 2
      name: OPTN006H
      line: 210
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN006H
    - level: 2
      name: OPTN006V
      line: 211
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN006V
    - level: 2
      name: OPTN006O
      line: 212
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AO.OPTN006O
    - level: 2
      name: FILLER
      line: 213
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: OPTN007C
      line: 214
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN007C
    - level: 2
      name: OPTN007P
      line: 215
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN007P
    - level: 2
      name: OPTN007H
      line: 216
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN007H
    - level: 2
      name: OPTN007V
      line: 217
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN007V
    - level: 2
      name: OPTN007O
      line: 218
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AO.OPTN007O
    - level: 2
      name: FILLER
      line: 219
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: OPTN008C
      line: 220
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN008C
    - level: 2
      name: OPTN008P
      line: 221
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN008P
    - level: 2
      name: OPTN008H
      line: 222
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN008H
    - level: 2
      name: OPTN008V
      line: 223
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN008V
    - level: 2
      name: OPTN008O
      line: 224
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AO.OPTN008O
    - level: 2
      name: FILLER
      line: 225
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: OPTN009C
      line: 226
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN009C
    - level: 2
      name: OPTN009P
      line: 227
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN009P
    - level: 2
      name: OPTN009H
      line: 228
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN009H
    - level: 2
      name: OPTN009V
      line: 229
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN009V
    - level: 2
      name: OPTN009O
      line: 230
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AO.OPTN009O
    - level: 2
      name: FILLER
      line: 231
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: OPTN010C
      line: 232
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN010C
    - level: 2
      name: OPTN010P
      line: 233
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN010P
    - level: 2
      name: OPTN010H
      line: 234
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN010H
    - level: 2
      name: OPTN010V
      line: 235
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN010V
    - level: 2
      name: OPTN010O
      line: 236
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AO.OPTN010O
    - level: 2
      name: FILLER
      line: 237
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: OPTN011C
      line: 238
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN011C
    - level: 2
      name: OPTN011P
      line: 239
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN011P
    - level: 2
      name: OPTN011H
      line: 240
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN011H
    - level: 2
      name: OPTN011V
      line: 241
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN011V
    - level: 2
      name: OPTN011O
      line: 242
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AO.OPTN011O
    - level: 2
      name: FILLER
      line: 243
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: OPTN012C
      line: 244
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN012C
    - level: 2
      name: OPTN012P
      line: 245
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN012P
    - level: 2
      name: OPTN012H
      line: 246
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN012H
    - level: 2
      name: OPTN012V
      line: 247
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTN012V
    - level: 2
      name: OPTN012O
      line: 248
      usage: DISPLAY
      pic: X(40)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 40
      qualified_name: COMEN1AO.OPTN012O
    - level: 2
      name: FILLER
      line: 249
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: OPTIONC
      line: 250
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTIONC
    - level: 2
      name: OPTIONP
      line: 251
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTIONP
    - level: 2
      name: OPTIONH
      line: 252
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTIONH
    - level: 2
      name: OPTIONV
      line: 253
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.OPTIONV
    - level: 2
      name: OPTIONO
      line: 254
      usage: DISPLAY
      pic: X(2)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 2
      qualified_name: COMEN1AO.OPTIONO
    - level: 2
      name: FILLER
      line: 255
      usage: DISPLAY
      pic: X(3)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 3
      qualified_name: COMEN1AO.FILLER
    - level: 2
      name: ERRMSGC
      line: 256
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.ERRMSGC
    - level: 2
      name: ERRMSGP
      line: 257
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.ERRMSGP
    - level: 2
      name: ERRMSGH
      line: 258
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.ERRMSGH
    - level: 2
      name: ERRMSGV
      line: 259
      usage: DISPLAY
      pic: X
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 1
      qualified_name: COMEN1AO.ERRMSGV
    - level: 2
      name: ERRMSGO
      line: 260
      usage: DISPLAY
      pic: X(78)
      children: []
      encoding: display
      slack_bytes_before: 0
      total_bytes: 78
      qualified_name: COMEN1AO.ERRMSGO
    total_bytes: 820
    slack_bytes_before: 0
    qualified_name: COMEN1AO
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
    line: 67
    usage: DISPLAY
    children:
    - level: 5
      name: LK-COMMAREA
      line: 68
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
    working_storage_bytes: 2020
    linkage_bytes: 32767
fall_through:
  paragraphs:
  - paragraph: MAIN-PARA
    first_line: 77
    last_line: 107
    terminator: cics-return
    falls_through_to: null
    last_verb: EXEC CICS
    last_raw: EXEC CICS RETURN
    classification_source: raw
  - paragraph: PROCESS-ENTER-KEY
    first_line: 117
    last_line: 190
    terminator: implicit
    falls_through_to: RETURN-TO-SIGNON-SCREEN
    last_verb: PERFORM
    last_raw: PERFORM SEND-MENU-SCREEN
    classification_source: annotations
  - paragraph: RETURN-TO-SIGNON-SCREEN
    first_line: 198
    last_line: 201
    terminator: cics-xctl
    falls_through_to: null
    last_verb: EXEC CICS
    last_raw: EXEC CICS
    classification_source: source_scan
  - paragraph: SEND-MENU-SCREEN
    first_line: 210
    last_line: 215
    terminator: implicit
    falls_through_to: RECEIVE-MENU-SCREEN
    last_verb: EXEC CICS
    last_raw: EXEC CICS SEND
    classification_source: raw
  - paragraph: RECEIVE-MENU-SCREEN
    first_line: 227
    last_line: 227
    terminator: implicit
    falls_through_to: POPULATE-HEADER-INFO
    last_verb: EXEC CICS
    last_raw: EXEC CICS RECEIVE
    classification_source: raw
  - paragraph: POPULATE-HEADER-INFO
    first_line: 240
    last_line: 257
    terminator: implicit
    falls_through_to: BUILD-MENU-OPTIONS
    last_verb: MOVE
    last_raw: MOVE WS-CURTIME-HH-MM-SS TO CURTIMEO OF COMEN1AO.
    classification_source: annotations
  - paragraph: BUILD-MENU-OPTIONS
    first_line: 264
    last_line: 300
    terminator: implicit-end-of-program
    falls_through_to: null
    last_verb: CONTINUE
    last_raw: CONTINUE
    classification_source: annotations
  c5_assertion: PASS
  c5_violations: []
paragraph_io:
- paragraph: MAIN-PARA
  classification_source: annotations
  mutates:
  - fd_name: ERR-FLG-OFF
    verb: SET
    line: 77
    raw: SET ERR-FLG-OFF TO TRUE
  - fd_name: WS-VARIABLES.WS-MESSAGE
    verb: MOVE
    line: 79
    raw: MOVE SPACES TO WS-MESSAGE
  - fd_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-FROM-PROGRAM
    verb: MOVE
    line: 83
    raw: MOVE 'COSGN00C' TO CDEMO-FROM-PROGRAM
  - fd_name: CARDDEMO-COMMAREA
    verb: MOVE
    line: 86
    raw: MOVE DFHCOMMAREA(1:EIBCALEN) TO CARDDEMO-COMMAREA
  - fd_name: CDEMO-PGM-REENTER
    verb: SET
    line: 88
    raw: SET CDEMO-PGM-REENTER TO TRUE
  - fd_name: COMEN1AO
    verb: MOVE
    line: 89
    raw: MOVE LOW-VALUES TO COMEN1AO
  - fd_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-TO-PROGRAM
    verb: MOVE
    line: 97
    raw: MOVE 'COSGN00C' TO CDEMO-TO-PROGRAM
  - fd_name: WS-VARIABLES.WS-ERR-FLG
    verb: MOVE
    line: 100
    raw: MOVE 'Y' TO WS-ERR-FLG
  reads:
  - fd_name: EIBCALEN
    verb: IF
    line: 82
    raw: IF EIBCALEN = 0
  - fd_name: DFHCOMMAREA
    verb: MOVE
    line: 86
    raw: MOVE DFHCOMMAREA(1:EIBCALEN) TO CARDDEMO-COMMAREA
  - fd_name: CDEMO-PGM-REENTER
    verb: IF
    line: 87
    raw: IF NOT CDEMO-PGM-REENTER
  - fd_name: EIBAID
    verb: EVALUATE
    line: 93
    raw: EVALUATE EIBAID
  - fd_name: CCDA-COMMON-MESSAGES.CCDA-MSG-INVALID-KEY
    verb: MOVE
    line: 101
    raw: MOVE CCDA-MSG-INVALID-KEY TO WS-MESSAGE
- paragraph: PROCESS-ENTER-KEY
  classification_source: annotations
  mutates:
  - fd_name: WS-VARIABLES.WS-OPTION-X
    verb: MOVE
    line: 122
    raw: MOVE OPTIONI OF COMEN1AI(1:WS-IDX) TO WS-OPTION-X
  - fd_name: WS-VARIABLES.WS-OPTION
    verb: MOVE
    line: 124
    raw: MOVE WS-OPTION-X TO WS-OPTION
  - fd_name: COMEN1AO.OPTIONO
    verb: MOVE
    line: 125
    raw: MOVE WS-OPTION TO OPTIONO OF COMEN1AO
  - fd_name: WS-VARIABLES.WS-ERR-FLG
    verb: MOVE
    line: 130
    raw: MOVE 'Y' TO WS-ERR-FLG
  - fd_name: ERR-FLG-ON
    verb: SET
    line: 138
    raw: SET ERR-FLG-ON TO TRUE
  - fd_name: WS-VARIABLES.WS-MESSAGE
    verb: MOVE
    line: 139
    raw: MOVE SPACES TO WS-MESSAGE
  - fd_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-FROM-TRANID
    verb: MOVE
    line: 153
    raw: MOVE WS-TRANID TO CDEMO-FROM-TRANID
  - fd_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-FROM-PROGRAM
    verb: MOVE
    line: 154
    raw: MOVE WS-PGMNAME TO CDEMO-FROM-PROGRAM
  - fd_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-PGM-CONTEXT
    verb: MOVE
    line: 155
    raw: MOVE ZEROS TO CDEMO-PGM-CONTEXT
  - fd_name: COMEN1AO.ERRMSGC
    verb: MOVE
    line: 162
    raw: MOVE DFHRED TO ERRMSGC OF COMEN1AO
  reads:
  - fd_name: COMEN1AI.OPTIONI
    verb: MOVE
    line: 122
    raw: MOVE OPTIONI OF COMEN1AI(1:WS-IDX) TO WS-OPTION-X
  - fd_name: WS-VARIABLES.WS-IDX
    verb: MOVE
    line: 122
    raw: MOVE OPTIONI OF COMEN1AI(1:WS-IDX) TO WS-OPTION-X
  - fd_name: WS-VARIABLES.WS-OPTION-X
    verb: MOVE
    line: 124
    raw: MOVE WS-OPTION-X TO WS-OPTION
  - fd_name: WS-VARIABLES.WS-OPTION
    verb: MOVE
    line: 125
    raw: MOVE WS-OPTION TO OPTIONO OF COMEN1AO
  - fd_name: CDEMO-USRTYP-USER
    verb: IF
    line: 136
    raw: IF CDEMO-USRTYP-USER AND
  - fd_name: ERR-FLG-ON
    verb: IF
    line: 145
    raw: IF NOT ERR-FLG-ON
  - fd_name: EIBRESP
    verb: IF
    line: 152
    raw: IF EIBRESP = DFHRESP(NORMAL)
  - fd_name: DFHRESP
    verb: IF
    line: 152
    raw: IF EIBRESP = DFHRESP(NORMAL)
  - fd_name: NORMAL
    verb: IF
    line: 152
    raw: IF EIBRESP = DFHRESP(NORMAL)
  - fd_name: WS-VARIABLES.WS-TRANID
    verb: MOVE
    line: 153
    raw: MOVE WS-TRANID TO CDEMO-FROM-TRANID
  - fd_name: WS-VARIABLES.WS-PGMNAME
    verb: MOVE
    line: 154
    raw: MOVE WS-PGMNAME TO CDEMO-FROM-PROGRAM
  - fd_name: DFHRED
    verb: MOVE
    line: 162
    raw: MOVE DFHRED TO ERRMSGC OF COMEN1AO
  - fd_name: DFHGREEN
    verb: MOVE
    line: 171
    raw: MOVE DFHGREEN TO ERRMSGC OF COMEN1AO
- paragraph: RETURN-TO-SIGNON-SCREEN
  classification_source: annotations
  mutates:
  - fd_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-TO-PROGRAM
    verb: MOVE
    line: 199
    raw: MOVE 'COSGN00C' TO CDEMO-TO-PROGRAM
  reads:
  - fd_name: CARDDEMO-COMMAREA.CDEMO-GENERAL-INFO.CDEMO-TO-PROGRAM
    verb: IF
    line: 198
    raw: IF CDEMO-TO-PROGRAM = LOW-VALUES OR SPACES
- paragraph: SEND-MENU-SCREEN
  classification_source: annotations
  mutates:
  - fd_name: COMEN1AO.ERRMSGO
    verb: MOVE
    line: 213
    raw: MOVE WS-MESSAGE TO ERRMSGO OF COMEN1AO
  reads:
  - fd_name: WS-VARIABLES.WS-MESSAGE
    verb: MOVE
    line: 213
    raw: MOVE WS-MESSAGE TO ERRMSGO OF COMEN1AO
- paragraph: RECEIVE-MENU-SCREEN
  classification_source: annotations
  mutates: []
  reads: []
- paragraph: POPULATE-HEADER-INFO
  classification_source: annotations
  mutates:
  - fd_name: WS-DATE-TIME.WS-CURDATE-DATA
    verb: MOVE
    line: 240
    raw: MOVE FUNCTION CURRENT-DATE TO WS-CURDATE-DATA
  - fd_name: COMEN1AO.TITLE01O
    verb: MOVE
    line: 242
    raw: MOVE CCDA-TITLE01 TO TITLE01O OF COMEN1AO
  - fd_name: COMEN1AO.TITLE02O
    verb: MOVE
    line: 243
    raw: MOVE CCDA-TITLE02 TO TITLE02O OF COMEN1AO
  - fd_name: COMEN1AO.TRNNAMEO
    verb: MOVE
    line: 244
    raw: MOVE WS-TRANID TO TRNNAMEO OF COMEN1AO
  - fd_name: COMEN1AO.PGMNAMEO
    verb: MOVE
    line: 245
    raw: MOVE WS-PGMNAME TO PGMNAMEO OF COMEN1AO
  - fd_name: WS-DATE-TIME.WS-CURDATE-MM-DD-YY.WS-CURDATE-MM
    verb: MOVE
    line: 247
    raw: MOVE WS-CURDATE-MONTH TO WS-CURDATE-MM
  - fd_name: WS-DATE-TIME.WS-CURDATE-MM-DD-YY.WS-CURDATE-DD
    verb: MOVE
    line: 248
    raw: MOVE WS-CURDATE-DAY TO WS-CURDATE-DD
  - fd_name: WS-DATE-TIME.WS-CURDATE-MM-DD-YY.WS-CURDATE-YY
    verb: MOVE
    line: 249
    raw: MOVE WS-CURDATE-YEAR(3:2) TO WS-CURDATE-YY
  - fd_name: COMEN1AO.CURDATEO
    verb: MOVE
    line: 251
    raw: MOVE WS-CURDATE-MM-DD-YY TO CURDATEO OF COMEN1AO
  - fd_name: WS-DATE-TIME.WS-CURTIME-HH-MM-SS.WS-CURTIME-HH
    verb: MOVE
    line: 253
    raw: MOVE WS-CURTIME-HOURS TO WS-CURTIME-HH
  - fd_name: WS-DATE-TIME.WS-CURTIME-HH-MM-SS.WS-CURTIME-MM
    verb: MOVE
    line: 254
    raw: MOVE WS-CURTIME-MINUTE TO WS-CURTIME-MM
  - fd_name: WS-DATE-TIME.WS-CURTIME-HH-MM-SS.WS-CURTIME-SS
    verb: MOVE
    line: 255
    raw: MOVE WS-CURTIME-SECOND TO WS-CURTIME-SS
  - fd_name: COMEN1AO.CURTIMEO
    verb: MOVE
    line: 257
    raw: MOVE WS-CURTIME-HH-MM-SS TO CURTIMEO OF COMEN1AO.
  reads:
  - fd_name: CCDA-SCREEN-TITLE.CCDA-TITLE01
    verb: MOVE
    line: 242
    raw: MOVE CCDA-TITLE01 TO TITLE01O OF COMEN1AO
  - fd_name: CCDA-SCREEN-TITLE.CCDA-TITLE02
    verb: MOVE
    line: 243
    raw: MOVE CCDA-TITLE02 TO TITLE02O OF COMEN1AO
  - fd_name: WS-VARIABLES.WS-TRANID
    verb: MOVE
    line: 244
    raw: MOVE WS-TRANID TO TRNNAMEO OF COMEN1AO
  - fd_name: WS-VARIABLES.WS-PGMNAME
    verb: MOVE
    line: 245
    raw: MOVE WS-PGMNAME TO PGMNAMEO OF COMEN1AO
  - fd_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURDATE.WS-CURDATE-MONTH
    verb: MOVE
    line: 247
    raw: MOVE WS-CURDATE-MONTH TO WS-CURDATE-MM
  - fd_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURDATE.WS-CURDATE-DAY
    verb: MOVE
    line: 248
    raw: MOVE WS-CURDATE-DAY TO WS-CURDATE-DD
  - fd_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURDATE.WS-CURDATE-YEAR
    verb: MOVE
    line: 249
    raw: MOVE WS-CURDATE-YEAR(3:2) TO WS-CURDATE-YY
  - fd_name: WS-DATE-TIME.WS-CURDATE-MM-DD-YY
    verb: MOVE
    line: 251
    raw: MOVE WS-CURDATE-MM-DD-YY TO CURDATEO OF COMEN1AO
  - fd_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURTIME.WS-CURTIME-HOURS
    verb: MOVE
    line: 253
    raw: MOVE WS-CURTIME-HOURS TO WS-CURTIME-HH
  - fd_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURTIME.WS-CURTIME-MINUTE
    verb: MOVE
    line: 254
    raw: MOVE WS-CURTIME-MINUTE TO WS-CURTIME-MM
  - fd_name: WS-DATE-TIME.WS-CURDATE-DATA.WS-CURTIME.WS-CURTIME-SECOND
    verb: MOVE
    line: 255
    raw: MOVE WS-CURTIME-SECOND TO WS-CURTIME-SS
  - fd_name: WS-DATE-TIME.WS-CURTIME-HH-MM-SS
    verb: MOVE
    line: 257
    raw: MOVE WS-CURTIME-HH-MM-SS TO CURTIMEO OF COMEN1AO.
- paragraph: BUILD-MENU-OPTIONS
  classification_source: annotations
  mutates:
  - fd_name: WS-VARIABLES.WS-MENU-OPT-TXT
    verb: MOVE
    line: 267
    raw: MOVE SPACES TO WS-MENU-OPT-TXT
  - fd_name: COMEN1AO.OPTN001O
    verb: MOVE
    line: 276
    raw: MOVE WS-MENU-OPT-TXT TO OPTN001O
  - fd_name: COMEN1AO.OPTN002O
    verb: MOVE
    line: 278
    raw: MOVE WS-MENU-OPT-TXT TO OPTN002O
  - fd_name: COMEN1AO.OPTN003O
    verb: MOVE
    line: 280
    raw: MOVE WS-MENU-OPT-TXT TO OPTN003O
  - fd_name: COMEN1AO.OPTN004O
    verb: MOVE
    line: 282
    raw: MOVE WS-MENU-OPT-TXT TO OPTN004O
  - fd_name: COMEN1AO.OPTN005O
    verb: MOVE
    line: 284
    raw: MOVE WS-MENU-OPT-TXT TO OPTN005O
  - fd_name: COMEN1AO.OPTN006O
    verb: MOVE
    line: 286
    raw: MOVE WS-MENU-OPT-TXT TO OPTN006O
  - fd_name: COMEN1AO.OPTN007O
    verb: MOVE
    line: 288
    raw: MOVE WS-MENU-OPT-TXT TO OPTN007O
  - fd_name: COMEN1AO.OPTN008O
    verb: MOVE
    line: 290
    raw: MOVE WS-MENU-OPT-TXT TO OPTN008O
  - fd_name: COMEN1AO.OPTN009O
    verb: MOVE
    line: 292
    raw: MOVE WS-MENU-OPT-TXT TO OPTN009O
  - fd_name: COMEN1AO.OPTN010O
    verb: MOVE
    line: 294
    raw: MOVE WS-MENU-OPT-TXT TO OPTN010O
  - fd_name: COMEN1AO.OPTN011O
    verb: MOVE
    line: 296
    raw: MOVE WS-MENU-OPT-TXT TO OPTN011O
  - fd_name: COMEN1AO.OPTN012O
    verb: MOVE
    line: 298
    raw: MOVE WS-MENU-OPT-TXT TO OPTN012O
  reads:
  - fd_name: CARDDEMO-MAIN-MENU-OPTIONS.CDEMO-MENU-OPTIONS.CDEMO-MENU-OPT.CDEMO-MENU-OPT-NUM
    verb: STRING
    line: 269
    raw: STRING CDEMO-MENU-OPT-NUM(WS-IDX) DELIMITED BY SIZE
  - fd_name: WS-VARIABLES.WS-IDX
    verb: STRING
    line: 269
    raw: STRING CDEMO-MENU-OPT-NUM(WS-IDX) DELIMITED BY SIZE
  - fd_name: WS-VARIABLES.WS-MENU-OPT-TXT
    verb: MOVE
    line: 276
    raw: MOVE WS-MENU-OPT-TXT TO OPTN001O
memory_model:
  working_storage_bytes: 2020
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
# COMEN01C — CardDemo Main Menu for Regular Users

## Purpose

COMEN01C is the primary navigation hub for regular (non-administrative) users of the CardDemo CICS application. Running under transaction identifier CM00, it presents a numbered menu of up to eleven functional options—spanning account viewing, credit-card management, transaction enquiry, bill payment, and reporting—and dispatches the user to the appropriate sub-program via a pseudo-conversational EXEC CICS XCTL handoff. The program enforces two access-control rules: it blocks direct invocation without an active session commarea, and it prevents regular users from selecting options marked as admin-only.

## Runtime Context

COMEN01C executes entirely within CICS as an online pseudo-conversational program. There is no batch, file-channel, or DB2 component. The program uses five CICS commands: SEND and RECEIVE to exchange the COMEN1A BMS map with the terminal, XCTL to transfer control to destination programs or the sign-on screen, INQUIRE to verify that the optional COPAUS0C program is installed before dispatching to it, and RETURN with a commarea and transaction identifier to suspend the task and await the next terminal input.

The BMS mapset is COMEN01 (copybook COMEN01 from the BMS copybook directory), providing two symbolic maps: COMEN1AI for input and COMEN1AO for output. The shared application commarea is defined by copybook COCOM01Y as CARDDEMO-COMMAREA and is passed on every EXEC CICS RETURN and XCTL call. No VSAM file I/O is performed by this program; the user-security file name WS-USRSEC-FILE is declared in working storage but is never opened or read within the reachable logic.

The program runs in the z/OS IBM Enterprise COBOL environment and is invoked either directly from the COSGN00C sign-on program or on return from any of the eleven sub-programs listed in the menu-option table.

## Data Layout

### Working Storage Scalars

The local working-storage group WS-VARIABLES holds all scalar fields the program manipulates at runtime. The program name (eight characters, initialised to "COMEN01C") and transaction identifier (four characters, initialised to "CM00") are constants that are copied into the shared commarea before each XCTL. A general-purpose eighty-character message buffer is moved to the BMS error-message field before each screen send. A single-character error-flag field, with two condition names for the on and off states, is tested before attempting any dispatch. A two-character alphanumeric field holds the raw option input after right-justification trimming; it is inspected to replace spaces with zeros and then moved to a two-digit numeric field that acts as the array subscript. Two binary fullword fields receive CICS response and reason codes from the map-receive command. A binary halfword index field serves as both the option-trimming loop counter and the menu-build iteration counter. A forty-character work buffer is assembled in the menu-build loop and moved to the appropriate map output slot.

### Commarea and Linkage

The linkage section exposes DFHCOMMAREA as a variable-length single-field structure dimensioned by EIBCALEN. On entry, the program copies this into the CARDDEMO-COMMAREA structure defined by COCOM01Y. That structure carries general navigation fields (from/to transaction ID and program name, user ID, user type with admin and regular-user condition names, and a program-context flag distinguishing first entry from re-entry), plus customer, account, card, and miscellaneous navigation fields used by other programs in the suite.

### Menu-Option Table

The most significant data structure for this program is CARDDEMO-MAIN-MENU-OPTIONS, defined by copybook COMEN02Y. A two-digit count field holds the number of active options (currently eleven). The underlying data is laid out as a flat initialised area containing eleven sequential records, each comprising a two-digit option number, a thirty-five-character option name, an eight-character program name, and a one-character user-type indicator ('U' for all eleven options in the current configuration). A REDEFINES overlay maps this flat area as an array of twelve occurrences, each with four named sub-fields: option number, option name, program name, and user-type indicator. This overlay is the mechanism by which the program accesses options by subscript during both validation and dispatch. The array bound of twelve exceeds the active count of eleven, providing a spare slot with no initialised data.

The eleven active menu options and their associated target programs are:

1. Account View → COACTVWC  
2. Account Update → COACTUPC  
3. Credit Card List → COCRDLIC  
4. Credit Card View → COCRDSLC  
5. Credit Card Update → COCRDUPC  
6. Transaction List → COTRN00C  
7. Transaction View → COTRN01C  
8. Transaction Add → COTRN02C  
9. Transaction Reports → CORPT00C  
10. Bill Payment → COBIL00C  
11. Pending Authorization View → COPAUS0C  

All eleven options carry a user-type indicator of 'U', meaning no admin-gating is currently active in the table, though the program logic is fully capable of enforcing it.

### Supporting Copybook Structures

COTTL01Y defines a three-field screen-title group with the application title lines and a thank-you message. CSDAT01Y defines a date/time group with sub-fields for year, month, day, hours, minutes, seconds, and milliseconds, plus REDEFINES overlays that expose the date and time components as eight-digit numeric scalars, and formatted display strings for MM/DD/YY and HH:MM:SS presentation. CSMSG01Y defines two fifty-character common message literals, including the invalid-key message used in this program. CSUSR01Y defines a user-data record with ID, first name, last name, password, type, and filler fields; it is present in working storage but not accessed by reachable logic here. DFHAID and DFHBMSCA are IBM-supplied copybooks providing attention identifier constants and BMS symbolic colour attribute values respectively.

## Procedure Logic

### MAIN-PARA

MAIN-PARA is the sole entry point for transaction CM00. It first resets the error flag to off and clears both the message buffer and the map error-message field. If EIBCALEN is zero, indicating no commarea was passed, it records COSGN00C as the calling program and performs RETURN-TO-SIGNON-SCREEN immediately. Otherwise it copies the inbound commarea bytes into CARDDEMO-COMMAREA. If the program-context flag indicates this is a first entry (not a re-entry), it sets the re-entry flag, clears the output map to low-values, and performs SEND-MENU-SCREEN. On a re-entry it performs RECEIVE-MENU-SCREEN to capture the user's input and then evaluates the attention identifier: ENTER routes to PROCESS-ENTER-KEY; PF3 sets the target program to COSGN00C and routes to RETURN-TO-SIGNON-SCREEN; any other key sets the error flag, loads the invalid-key message, and performs SEND-MENU-SCREEN. Regardless of path, execution falls through to an EXEC CICS RETURN specifying transaction CM00 and the shared commarea, suspending the task until the next terminal event.

### END-EXEC

END-EXEC is an unreachable artifact paragraph identified by the Phase 0 CFG tool; it has no executable content and is never invoked by any reachable paragraph.

### PROCESS-ENTER-KEY

PROCESS-ENTER-KEY first trims trailing spaces from the raw option field by iterating backward from the field's maximum length until a non-space character or position one is found, then moves the trimmed characters to the right-justified work field, replaces any remaining embedded spaces with zeros, and converts to the numeric option variable. The numeric option value is also echoed back to the map output option field. Two sequential guards then check the input: if the value is non-numeric, zero, or greater than the active option count, an error message is set and SEND-MENU-SCREEN is performed. If the user is a regular user and the selected option carries an admin-only type indicator, an access-denied message is set and SEND-MENU-SCREEN is performed. If no error flag is set after these guards, an EVALUATE on the selected program name handles three cases. When the target is COPAUS0C, an EXEC CICS INQUIRE verifies the program is installed before issuing EXEC CICS XCTL; if not installed, a red error message is composed and SEND-MENU-SCREEN is called. When the program name begins with "DUMMY", a green coming-soon message is composed and SEND-MENU-SCREEN is called. For all other valid programs, the commarea navigation fields are set and EXEC CICS XCTL transfers control to the target program. After the EVALUATE, SEND-MENU-SCREEN is performed as a fallback in case none of the XCTL paths was taken.

### END-IF

END-IF is an unreachable artifact paragraph identified by the Phase 0 CFG tool; it has no executable content and is never invoked by any reachable paragraph.

### RETURN-TO-SIGNON-SCREEN

RETURN-TO-SIGNON-SCREEN ensures that CDEMO-TO-PROGRAM is set to COSGN00C if it currently holds low-values or spaces, providing a safe default target. It then issues an unconditional EXEC CICS XCTL to whatever program is named in CDEMO-TO-PROGRAM, transferring control without a commarea.

### SEND-MENU-SCREEN

SEND-MENU-SCREEN orchestrates the screen-output sequence: it calls POPULATE-HEADER-INFO to update the map header fields, calls BUILD-MENU-OPTIONS to fill the option-line fields, moves the current message buffer content to the map error-message field, and issues EXEC CICS SEND for map COMEN1A in mapset COMEN01 with the ERASE option to clear the terminal before painting.

### RECEIVE-MENU-SCREEN

RECEIVE-MENU-SCREEN issues EXEC CICS RECEIVE for map COMEN1A into the COMEN1AI symbolic input structure, storing the CICS response and reason codes in WS-RESP-CD and WS-REAS-CD for potential error diagnosis, though the current program logic does not explicitly branch on these codes after the receive.

### POPULATE-HEADER-INFO

POPULATE-HEADER-INFO obtains the current timestamp by moving FUNCTION CURRENT-DATE into the date/time working-storage group. It then moves the two application title strings to the map title fields, the transaction identifier to the map transaction-name field, the program name to the map program-name field, and formats the current date as MM/DD/YY and the current time as HH:MM:SS, moving each to the corresponding map display field.

### BUILD-MENU-OPTIONS

BUILD-MENU-OPTIONS loops from subscript one to CDEMO-MENU-OPT-COUNT, building a forty-character display string for each option by concatenating the numeric option number, the literal string ". ", and the option name. An EVALUATE on the current subscript routes the assembled string to the appropriate numbered output field on the map (OPTN001O through OPTN012O). Loop iterations beyond twelve fall through a WHEN OTHER CONTINUE clause harmlessly.

### END-PERFORM

END-PERFORM is an unreachable artifact paragraph identified by the Phase 0 CFG tool; it has no executable content and is never invoked by any reachable paragraph.

## Business Rules Surfaced

**BR-001** — Session guard on entry: if no commarea is present (EIBCALEN = 0), execution is redirected to the sign-on screen immediately, preventing unauthenticated access to the menu.

**BR-002** — First-entry initialisation: when CDEMO-PGM-REENTER indicates this is the first time the transaction has been entered, the program presents a clean menu screen without consuming any user input.

**BR-003** — Invalid attention key handling: pressing any key other than ENTER or PF3 causes the program to display the standard invalid-key message and re-present the menu, with no navigation taking place.

**BR-004** — Option range validation: the entered option must be numeric, non-zero, and within the bounds of the active option count; any value outside these constraints causes an error message and re-display of the menu.

**BR-005** — Admin-only option gating: if the signed-in user is a regular user and the chosen option's user-type indicator is 'A', access is denied with an explanatory message and the menu is re-presented.

**BR-006** — Availability check for COPAUS0C: before transferring to the pending-authorisation view program, the program verifies that COPAUS0C is installed in the CICS region; if the INQUIRE returns an abnormal response, a red error message is displayed instead.

**BR-007** — Placeholder option handling: if the looked-up program name begins with "DUMMY", the option is treated as a not-yet-implemented feature and a green informational message is shown without any XCTL dispatch.

**BR-008** — Table-driven program dispatch: for all other valid options, the target program name is read directly from the menu-option table using the user-supplied option number as an index, and control is transferred via EXEC CICS XCTL; no hard-coded program-name list exists in the procedure logic itself.

**BR-009** — PF3 return to sign-on: pressing PF3 from the menu unconditionally routes the user back to the sign-on screen, terminating the current navigation context.

**BR-010** — Commarea navigation fields stamped before dispatch: CDEMO-FROM-TRANID, CDEMO-FROM-PROGRAM, and CDEMO-PGM-CONTEXT are populated before every XCTL, so the target program knows where to return the user after it completes.

## Graph Summary

- **CALLS (EXEC CICS XCTL):** COMEN01C → COSGN00C (guard: no commarea on entry); COMEN01C → COSGN00C (guard: PF3 pressed); COMEN01C → COPAUS0C (guard: valid option + INQUIRE NORMAL); COMEN01C → CDEMO-MENU-OPT-PGMNAME\[n\] (guard: valid option, not COPAUS0C, not DUMMY)
- **CALLED BY:** COSGN00C, COACTUPC, COACTVWC, COBIL00C, COCRDLIC, COCRDSLC, COCRDUPC, CORPT00C, COTRN00C, COTRN01C, COTRN02C
- **COPYBOOKS:** COCOM01Y (commarea structure), COMEN02Y (menu-option table with REDEFINES), COMEN01 (BMS mapset), COTTL01Y (screen titles), CSDAT01Y (date/time fields), CSMSG01Y (common messages), CSUSR01Y (user record), DFHAID (attention IDs), DFHBMSCA (BMS colour attributes)
- **CICS COMMANDS:** RETURN (transaction CM00, commarea), SEND (map COMEN1A, ERASE), RECEIVE (map COMEN1A), XCTL (COSGN00C or table-looked-up program), INQUIRE (COPAUS0C availability)
- **TRANSACTION IDs:** CM00 (own transaction, used on RETURN and stamped in FROM-TRANID)
- **VSAM FILE I/O:** None (no file-control entries, no OPEN/READ/WRITE/CLOSE commands)
- **BUSINESS RULES:** BR-001 guard (no-commarea redirect), BR-002 display (first-entry init), BR-003 guard (invalid AID), BR-004 guard (option range), BR-005 guard (admin-only access), BR-006 guard (COPAUS0C availability), BR-007 display (DUMMY placeholder), BR-008 lookup (table-driven dispatch), BR-009 guard (PF3 sign-on return), BR-010 transform (commarea stamp before XCTL)
- **DEAD CODE:** Paragraphs END-EXEC, END-IF, and END-PERFORM are unreachable per Phase 0 static analysis and carry no business logic
