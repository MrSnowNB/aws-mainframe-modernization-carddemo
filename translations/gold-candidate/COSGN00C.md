---
schema_version: "cobol-md/1.0"
program_id: "COSGN00C"
source_file: "app/cbl/COSGN00C.cbl"
source_sha: "c3e7f8e4fb96466d3822ad82ceda8a96fb555d78"
translation_date: "2026-04-23"
translating_agent: "claude-opus-4-5 (subagent)"
aifirst_task_id: "T-2026-04-23-001"
cfg_source: "validation/structure/COSGN00C_cfg.json"

business_domain: "Administration"
subtype: "CICS-Online"

author: "AWS"
date_written: null
lines_of_code: 197
divisions:
  identification: true
  environment: true
  data: true
  procedure: true
environment:
  compiler: "IBM Enterprise COBOL"
  target: "CICS/VSAM"
  runtime: "z/OS"

calls_to:
  - program: "COADM01C"
    condition: "CDEMO-USRTYP-ADMIN is true (user type flag indicates administrator)"
    call_type: "EXEC CICS XCTL"
  - program: "COMEN01C"
    condition: "CDEMO-USRTYP-ADMIN is false (user type flag indicates regular user)"
    call_type: "EXEC CICS XCTL"

called_by:
  - "CC00 (CICS transaction initiator)"

copybooks_used:
  - name: "COCOM01Y"
    path: "app/cpy/COCOM01Y.cpy"
    sha: null
  - name: "COSGN00"
    path: "app/cpy-bms/COSGN00.CPY"
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
    path: "app/cpy-stubs/DFHAID.cpy"
    sha: null
  - name: "DFHBMSCA"
    path: "app/cpy-stubs/DFHBMSCA.cpy"
    sha: null

file_control:
  - ddname: "USRSEC"
    organization: "INDEXED"
    access: "RANDOM"
    record_key: "WS-USER-ID"
    crud: ["READ"]

cics_commands:
  - "RETURN"
  - "RECEIVE"
  - "SEND"
  - "ASSIGN"
  - "READ"
  - "XCTL"

transaction_ids:
  - "CC00"

data_items:
  - name: "WS-VARIABLES"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "Top-level working-storage group holding all program-local variables including program name, transaction ID, message buffer, file name, error flag, response codes, and user credential fields"

  - name: "DFHCOMMAREA"
    level: 01
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []
    dead_code_flag: false
    semantic: "CICS Communication Area passed into this program from the transaction invocation; contains the variable-length linkage area whose actual size is determined by the CICS-managed EIBCALEN field at runtime"

procedure_paragraphs:
  - name: "MAIN-PARA"
    reachable: true
    performs:
      - "SEND-SIGNON-SCREEN"
      - "PROCESS-ENTER-KEY"
      - "SEND-PLAIN-TEXT"
      - "SEND-SIGNON-SCREEN"
      - "SEND-SIGNON-SCREEN"
      - "SEND-SIGNON-SCREEN"
      - "READ-USER-SEC-FILE"
      - "POPULATE-HEADER-INFO"
      - "SEND-SIGNON-SCREEN"
      - "SEND-SIGNON-SCREEN"
      - "SEND-SIGNON-SCREEN"
    goto_targets: []
    summary: "Entry point for transaction CC00; resets error state, then branches based on whether a commarea exists (first invocation shows the screen) and which AID key was pressed (Enter processes credentials, PF3 displays a thank-you and exits, any other key shows an invalid-key error), before issuing a CICS RETURN to re-invoke the same transaction with the commarea."

  - name: "PROCESS-ENTER-KEY"
    reachable: true
    performs:
      - "SEND-SIGNON-SCREEN"
      - "SEND-PLAIN-TEXT"
      - "SEND-SIGNON-SCREEN"
      - "SEND-SIGNON-SCREEN"
      - "SEND-SIGNON-SCREEN"
      - "READ-USER-SEC-FILE"
      - "POPULATE-HEADER-INFO"
      - "SEND-SIGNON-SCREEN"
      - "SEND-SIGNON-SCREEN"
      - "SEND-SIGNON-SCREEN"
    goto_targets: []
    summary: "Receives the BMS map from the terminal, validates that neither the user ID nor password field is blank (re-displaying the sign-on screen with an error message if either is empty), then uppercases both fields and invokes READ-USER-SEC-FILE when no error flag is set."

  - name: "SEND-SIGNON-SCREEN"
    reachable: true
    performs:
      - "POPULATE-HEADER-INFO"
    goto_targets: []
    summary: "Populates the BMS output map header fields, copies the current message to the error-message area of the map, and issues a CICS SEND to display the sign-on screen (COSGN0A in mapset COSGN00) with cursor positioning and screen erase."

  - name: "SEND-PLAIN-TEXT"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Sends a plain-text message string directly to the terminal (used for the PF3 thank-you farewell message) and then issues an unconditional CICS RETURN with no TRANSID, ending the conversation."

  - name: "POPULATE-HEADER-INFO"
    reachable: true
    performs: []
    goto_targets: []
    summary: "Obtains the current date and time via FUNCTION CURRENT-DATE, formats them into month/day/year and hours/minutes/seconds display strings, moves the application title lines, transaction ID, and program name into the BMS output map, and queries CICS for the APPLID and SYSID to display in the header."

  - name: "READ-USER-SEC-FILE"
    reachable: true
    performs:
      - "SEND-SIGNON-SCREEN"
    goto_targets: []
    summary: "Issues a CICS READ against the USRSEC VSAM dataset keyed on WS-USER-ID; on a successful read (response code 0) it verifies the stored password matches WS-USER-PWD and, if correct, populates the commarea with identity/role data before transferring control via XCTL to either the administrator menu (COADM01C) or the regular-user menu (COMEN01C); on response code 13 (record not found) or any other error it displays an appropriate error message."

business_rules:
  - id: "BR-001"
    rule: "If no commarea is present (EIBCALEN equals zero), the program is on its first invocation and must display the sign-on screen immediately without attempting to process any input."
    source_paragraph: "MAIN-PARA"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-002"
    rule: "Only the Enter key (DFHENTER) triggers credential processing; PF3 triggers a graceful exit with a thank-you message; any other AID key is rejected as invalid and causes an error message to be displayed on the sign-on screen."
    source_paragraph: "MAIN-PARA"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-003"
    rule: "If the user ID field on the sign-on screen is blank or contains low-values, processing is halted and the user is prompted to enter a user ID before any authentication attempt is made."
    source_paragraph: "PROCESS-ENTER-KEY"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-004"
    rule: "If the password field on the sign-on screen is blank or contains low-values, processing is halted and the user is prompted to enter a password before any authentication attempt is made."
    source_paragraph: "PROCESS-ENTER-KEY"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-005"
    rule: "Both the user ID and password values received from the terminal are uppercased before comparison and storage, ensuring that authentication is case-insensitive for the user but stored in a canonical form."
    source_paragraph: "PROCESS-ENTER-KEY"
    rule_type: "transform"
    confidence: "high"
    reachable: true

  - id: "BR-006"
    rule: "The user security file (USRSEC) is only read when no error flag is set; if any prior validation step raised the error flag, the file read is skipped entirely."
    source_paragraph: "PROCESS-ENTER-KEY"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-007"
    rule: "If the USRSEC record is found (response code 0) and the stored password matches the entered password, the user is authenticated; a mismatched password results in a 'Wrong Password' error message without distinguishing which field was wrong."
    source_paragraph: "READ-USER-SEC-FILE"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-008"
    rule: "Authenticated users whose user-type flag indicates administrator status (CDEMO-USRTYP-ADMIN) are routed to the administration menu program (COADM01C) via XCTL; all other authenticated users are routed to the standard main menu program (COMEN01C)."
    source_paragraph: "READ-USER-SEC-FILE"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-009"
    rule: "If the USRSEC READ returns response code 13 (record not found), the user is told their user ID was not found and is prompted to try again; the error flag is set to suppress further processing in the current cycle."
    source_paragraph: "READ-USER-SEC-FILE"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-010"
    rule: "Any USRSEC READ response code other than 0 or 13 triggers a generic 'Unable to verify the User' error message, masking the underlying system error from the end user while still preventing sign-on."
    source_paragraph: "READ-USER-SEC-FILE"
    rule_type: "guard"
    confidence: "high"
    reachable: true

  - id: "BR-011"
    rule: "Upon successful authentication the commarea is populated with the originating transaction ID, program name, user ID, and user type before control is transferred, ensuring downstream programs receive a fully initialized session context."
    source_paragraph: "READ-USER-SEC-FILE"
    rule_type: "audit"
    confidence: "high"
    reachable: true

  - id: "BR-012"
    rule: "The CICS RETURN at the end of MAIN-PARA always specifies TRANSID 'CC00' and passes the CARDDEMO-COMMAREA, so if control returns without a successful XCTL the sign-on screen will be re-presented on the next keystroke."
    source_paragraph: "MAIN-PARA"
    rule_type: "display"
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

# COSGN00C — CardDemo Application Sign-On Screen

## Purpose

COSGN00C is the interactive sign-on gateway for the CardDemo CICS application. It presents a BMS-based credential screen to the end user, validates the supplied user ID and password against a VSAM security file (USRSEC), and upon successful authentication transfers control to either the administrator menu or the standard main menu depending on the user's stored role type.

## Runtime Context

This program runs under CICS transaction identifier **CC00** on z/OS. It is a pseudo-conversational program: each user interaction causes a CICS RETURN with TRANSID CC00 and a commarea, so the next terminal input re-invokes the same program. The program uses the BMS map COSGN0A within mapset COSGN00 for all screen I/O. It reads the USRSEC VSAM indexed dataset keyed on user ID to perform credential lookup. On successful login it issues an EXEC CICS XCTL to either COADM01C (administrator path) or COMEN01C (regular-user path).

## Business Rules Surfaced

- **BR-001** — First invocation without commarea: display sign-on screen immediately.
- **BR-002** — Only Enter key processes credentials; PF3 exits gracefully; all other keys show invalid-key error.
- **BR-003** — Blank user ID halts processing with a prompt.
- **BR-004** — Blank password halts processing with a prompt.
- **BR-005** — Credentials are uppercased before comparison and storage.
- **BR-006** — USRSEC is only read if no error flag was raised during input validation.
- **BR-007** — Successful read requires exact password match; mismatch shows 'Wrong Password'.
- **BR-008** — Admins route to COADM01C; regular users route to COMEN01C.
- **BR-009** — VSAM response 13 (not found) shows 'User not found' error.
- **BR-010** — Any other VSAM error shows generic 'Unable to verify the User' message.
- **BR-011** — Commarea fully populated with session context before XCTL on successful login.
- **BR-012** — CICS RETURN always re-queues CC00 so sign-on re-presents on next keystroke.
