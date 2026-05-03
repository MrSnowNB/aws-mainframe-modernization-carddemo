---
# ── Identity ──────────────────────────────────────────────────────────────────
schema_version: "cobol-md/1.0"
program_id: "COMEN01C"
source_file: "app/cbl/COMEN01C.cbl"
source_sha: "a404313748b0715a306336ac599b3e585697c05c"
translation_date: "2026-04-23"
translating_agent: "claude-opus-4-5 (subagent)"
aifirst_task_id: "T-2026-04-23-001"
cfg_source: "validation/structure/COMEN01C_cfg.json"

# ── Classification ─────────────────────────────────────────────────────────────
business_domain: "Administration"
subtype: "Menu"

# ── Structural Metadata ────────────────────────────────────────────────────────
author: "AWS"
date_written: null
lines_of_code: 213
divisions:
  identification: true
  environment: true
  data: true
  procedure: true
environment:
  compiler: "IBM Enterprise COBOL"
  target: "CICS/VSAM"
  runtime: "z/OS"

# ── Graph Edges ────────────────────────────────────────────────────────────────
calls_to:
  - program: "COSGN00C"
    condition: "EIBCALEN = 0 (no commarea on first entry)"
    call_type: "EXEC CICS XCTL"
  - program: "COSGN00C"
    condition: "PF3 pressed by user"
    call_type: "EXEC CICS XCTL"
  - program: "CDEMO-MENU-OPT-PGMNAME(WS-OPTION)"
    condition: "Valid option selected and program is COPAUS0C, EXEC CICS INQUIRE returns NORMAL"
    call_type: "EXEC CICS XCTL"
  - program: "CDEMO-MENU-OPT-PGMNAME(WS-OPTION)"
    condition: "Valid option selected and program name does not begin with DUMMY and is not COPAUS0C"
    call_type: "EXEC CICS XCTL"

called_by:
  - "COSGN00C"
  - "COACTUPC"
  - "COACTVWC"
  - "COBIL00C"
  - "COCRDLIC"
  - "COCRDSLC"
  - "COCRDUPC"
  - "CORPT00C"
  - "COTRN00C"
  - "COTRN01C"
  - "COTRN02C"

copybooks_used:
  - name: "COCOM01Y"
    path: "app/cpy/COCOM01Y.cpy"
    sha: null
  - name: "COMEN02Y"
    path: "app/cpy/COMEN02Y.cpy"
    sha: null
  - name: "COMEN01"
    path: "app/cpy-bms/COMEN01.CPY"
    sha: null
  - name: "COTTL01Y"
    path: "app/cpy/COTTL01Y.cpy"
    sha: null
  - name: "CSDAT01Y"
    path: "app/cpy/CSDAT01Y.cpy"
    sha: null
  - name: "CSMSG01Y"
    path: "app/cpy/CSMSG01Y.cpy"
    sha: null
  - name: "CSUSR01Y"
    path: "app/cpy/CSUSR01Y.cpy"
    sha: null
  - name: "DFHAID"
    path: null
    sha: null
  - name: "DFHBMSCA"
    path: null
    sha: null

# ── File I/O ───────────────────────────────────────────────────────────────────
file_control: []

# ── CICS ───────────────────────────────────────────────────────────────────────
cics_commands:
  - "RETURN"
  - "INQUIRE"
  - "XCTL"
  - "SEND"
  - "RECEIVE"

transaction_ids:
  - "CM00"

# ── Data Layer ─────────────────────────────────────────────────────────────────
data_items:
  - name: "WS-VARIABLES"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Top-level working-storage group holding all program-local scalar variables"

  - name: "DFHCOMMAREA"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Linkage-section entry mapped by CICS to the commarea passed by the invoking transaction; its single repeating-occurrence subordinate field is used to copy the inbound commarea into CARDDEMO-COMMAREA"

# ── Procedure Paragraphs ───────────────────────────────────────────────────────
procedure_paragraphs:
  - name: "MAIN-PARA"
    reachable: true
    performs:
      - "RETURN-TO-SIGNON-SCREEN"
      - "SEND-MENU-SCREEN"
      - "RECEIVE-MENU-SCREEN"
      - "PROCESS-ENTER-KEY"
    goto_targets: []
    summary: "Entry point for transaction CM00; initializes the error flag, routes first-entry requests to the sign-on screen, controls the pseudo-conversational receive/send cycle, and dispatches ENTER or PF3 keystrokes before issuing EXEC CICS RETURN to suspend the task"

  - name: "PROCESS-ENTER-KEY"
    reachable: true
    performs:
      - "SEND-MENU-SCREEN"
    goto_targets: []
    summary: "Validates the numeric option entered on the menu map, enforces admin-only access restrictions, and issues an EXEC CICS XCTL to the program associated with the chosen option, with special handling for the COPAUS0C availability check and DUMMY placeholder options"

  - name: "SEND-MENU-SCREEN"
    reachable: true
    performs:
      - "POPULATE-HEADER-INFO"
      - "BUILD-MENU-OPTIONS"
    goto_targets: []
    summary: "Prepares the BMS map COMEN1AO by populating the header and menu-option lines, moves the current message into the error-message field, and sends the COMEN1A map from mapset COMEN01 with ERASE"

  - name: "RECEIVE-MENU-SCREEN"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Issues EXEC CICS RECEIVE for the COMEN1A map into COMEN1AI, capturing the user's keyboard input and storing CICS response codes in WS-RESP-CD and WS-REAS-CD"

  - name: "POPULATE-HEADER-INFO"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Reads the current date and time using FUNCTION CURRENT-DATE, formats them as MM/DD/YY and HH:MM:SS strings, and moves the application title lines, transaction ID, program name, date, and time into the output map header fields"

  - name: "BUILD-MENU-OPTIONS"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Iterates over the CDEMO-MENU-OPT table (up to twelve entries) and assembles each option's display text as a concatenation of option number, separator, and option name, placing the result in the corresponding OPTN001O through OPTN012O map output field"

# ── Business Rules ─────────────────────────────────────────────────────────────
business_rules:
  - id: "BR-001"
    rule: "If the commarea length (EIBCALEN) is zero on entry, the program immediately transfers control to the sign-on program COSGN00C without displaying the menu, preventing direct transaction invocation without an established session"
    source_paragraph: "MAIN-PARA"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-002"
    rule: "On first entry to the menu (CDEMO-PGM-REENTER flag not set), the program initialises the output map with low-values and displays the menu screen without reading user input, ensuring a clean initial presentation"
    source_paragraph: "MAIN-PARA"
    rule_type: "display"
    confidence: "high"
    reachable: true

  - id: "BR-003"
    rule: "If an attention identifier other than ENTER or PF3 is pressed, the error flag is set and the invalid-key message from CCDA-MSG-INVALID-KEY is displayed; no navigation occurs"
    source_paragraph: "MAIN-PARA"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-004"
    rule: "If the value entered in the option field is non-numeric, equals zero, or exceeds CDEMO-MENU-OPT-COUNT, the program displays 'Please enter a valid option number...' and re-presents the menu without dispatching"
    source_paragraph: "PROCESS-ENTER-KEY"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-005"
    rule: "If the signed-in user type is regular user (CDEMO-USRTYP-USER) and the selected option is flagged as admin-only (option user-type indicator equals 'A'), access is denied with the message 'No access - Admin Only option...' and the menu is re-displayed"
    source_paragraph: "PROCESS-ENTER-KEY"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-006"
    rule: "When the selected program is COPAUS0C, an EXEC CICS INQUIRE is performed first; if COPAUS0C is not installed (EIBRESP is not NORMAL), a red error message is displayed stating the option is not installed instead of dispatching"
    source_paragraph: "PROCESS-ENTER-KEY"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-007"
    rule: "If the program name associated with the selected option begins with 'DUMMY', a green informational message is displayed indicating the feature is coming soon, and no XCTL dispatch is performed"
    source_paragraph: "PROCESS-ENTER-KEY"
    rule_type: "display"
    confidence: "high"
    reachable: true

  - id: "BR-008"
    rule: "For any valid, installed, non-dummy option, the program name is looked up from the CDEMO-MENU-OPT-PGMNAME array using the option number as a subscript, and control is transferred to that program via EXEC CICS XCTL with the shared commarea"
    source_paragraph: "PROCESS-ENTER-KEY"
    rule_type: "lookup"
    confidence: "high"
    reachable: true

  - id: "BR-009"
    rule: "When PF3 is pressed, control is unconditionally transferred to COSGN00C (the sign-on screen), terminating the current menu session"
    source_paragraph: "MAIN-PARA"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-010"
    rule: "Before every EXEC CICS XCTL dispatch to a sub-program, the commarea fields CDEMO-FROM-TRANID, CDEMO-FROM-PROGRAM, and CDEMO-PGM-CONTEXT are set to identify the calling transaction and program, enabling the target to return correctly"
    source_paragraph: "PROCESS-ENTER-KEY"
    rule_type: "transform"
    confidence: "high"
    reachable: true

# ── Validation ─────────────────────────────────────────────────────────────────
validation:
  t01_schema_valid: true
  t02_structural_complete: true
  t02r_redefines_complete: true
  t03_functional_score: null
  t04_semantic_score: null
  t05_regression_pass: null
  overall: "PASS"
---

# COMEN01C — CardDemo Main Menu for Regular Users

## Purpose

COMEN01C is the primary navigation hub for regular (non-administrative) users of the CardDemo CICS application. Running under transaction identifier CM00, it presents a numbered menu of up to eleven functional options and dispatches the user to the appropriate sub-program via a pseudo-conversational EXEC CICS XCTL handoff. The program enforces two access-control rules: it blocks direct invocation without an active session commarea, and it prevents regular users from selecting options marked as admin-only.

## Runtime Context

COMEN01C executes entirely within CICS as an online pseudo-conversational program. It uses five CICS commands: SEND and RECEIVE to exchange the COMEN1A BMS map with the terminal, XCTL to transfer control to destination programs or the sign-on screen, INQUIRE to verify that the optional COPAUS0C program is installed before dispatching to it, and RETURN with a commarea and transaction identifier to suspend the task and await the next terminal input.

## Business Rules Surfaced

- **BR-001** — Session guard: EIBCALEN = 0 redirects immediately to sign-on.
- **BR-002** — First-entry initialisation: clean menu screen on first entry.
- **BR-003** — Invalid AID key: error message, no navigation.
- **BR-004** — Option range validation: non-numeric, zero, or out-of-range causes re-display.
- **BR-005** — Admin-only gating: regular users denied admin options.
- **BR-006** — COPAUS0C availability check before dispatch.
- **BR-007** — DUMMY placeholder: coming-soon message, no dispatch.
- **BR-008** — Table-driven dispatch via CDEMO-MENU-OPT-PGMNAME array.
- **BR-009** — PF3 returns unconditionally to sign-on screen.
- **BR-010** — Commarea navigation fields stamped before every XCTL.
