---
schema_version: cobol-md/1.0
program_id: CBACT02C
source_file: app/cbl/CBACT02C.cbl
source_sha: 8a41274180ef6bc01d052e40ece5578e790dc792
translation_date: '2026-04-30'
translating_agent: gemini-cli-agent
aifirst_task_id: T-CBACT02C-TRANSLATION
cfg_source: validation/structure/CBACT02C_cfg.json
business_domain: Account Management
subtype: Batch
data_items:
- name: FD-CARDFILE-REC
  level: 1
  redefines: null
  reachable: true
- name: FD-CARD-NUM
  level: 5
  redefines: null
  reachable: true
- name: FD-CARD-DATA
  level: 5
  redefines: null
  reachable: true
- name: CARD-RECORD
  level: 1
  redefines: null
  reachable: true
- name: CARD-NUM
  level: 5
  redefines: null
  reachable: true
- name: CARD-ACCT-ID
  level: 5
  redefines: null
  reachable: true
- name: CARD-CVV-CD
  level: 5
  redefines: null
  reachable: true
- name: CARD-EMBOSSED-NAME
  level: 5
  redefines: null
  reachable: true
- name: CARD-EXPIRAION-DATE
  level: 5
  redefines: null
  reachable: true
- name: CARD-ACTIVE-STATUS
  level: 5
  redefines: null
  reachable: true
- name: CARDFILE-STATUS
  level: 1
  redefines: null
  reachable: true
- name: CARDFILE-STAT1
  level: 5
  redefines: null
  reachable: true
- name: CARDFILE-STAT2
  level: 5
  redefines: null
  reachable: true
- name: IO-STATUS
  level: 1
  redefines: null
  reachable: true
- name: IO-STAT1
  level: 5
  redefines: null
  reachable: true
- name: IO-STAT2
  level: 5
  redefines: null
  reachable: true
- name: TWO-BYTES-BINARY
  level: 1
  redefines: null
  reachable: true
- name: TWO-BYTES-ALPHA
  level: 1
  redefines: TWO-BYTES-BINARY
  reachable: true
- name: TWO-BYTES-LEFT
  level: 5
  redefines: null
  reachable: true
- name: TWO-BYTES-RIGHT
  level: 5
  redefines: null
  reachable: true
- name: IO-STATUS-04
  level: 1
  redefines: null
  reachable: true
- name: IO-STATUS-0401
  level: 5
  redefines: null
  reachable: true
- name: IO-STATUS-0403
  level: 5
  redefines: null
  reachable: true
- name: APPL-RESULT
  level: 1
  redefines: null
  reachable: true
- name: APPL-AOK
  level: 88
  redefines: null
  reachable: true
- name: APPL-EOF
  level: 88
  redefines: null
  reachable: true
- name: END-OF-FILE
  level: 1
  redefines: null
  reachable: true
- name: ABCODE
  level: 1
  redefines: null
  reachable: true
- name: TIMING
  level: 1
  redefines: null
  reachable: true
procedure_paragraphs:
- name: END-PERFORM
  reachable: true
  synthetic: false
- name: 1000-CARDFILE-GET-NEXT
  reachable: true
  synthetic: false
- name: 0000-CARDFILE-OPEN
  reachable: true
  synthetic: false
- name: 9000-CARDFILE-CLOSE
  reachable: true
  synthetic: false
- name: 9999-ABEND-PROGRAM
  reachable: true
  synthetic: false
- name: 9910-DISPLAY-IO-STATUS
  reachable: true
  synthetic: false
calls_to:
- program: CEE3ABD
  condition: unconditional
  call_type: STATIC
copybooks_used:
- name: CVACT02Y
  path: app/cpy/CVACT02Y.cpy
- name: of
  path: app/cpy/of.cpy
cics_commands: []
---

# File Summary

Automated translation for CBACT02C

## CBACT02C-MAIN

- Display output message
- Execute the 0000-CARDFILE-OPEN procedure
- Execute a procedure
- When END-OF-FILE = 'N'
- Execute the 1000-CARDFILE-GET-NEXT procedure
- When END-OF-FILE = 'N'
- Display output message
- Execute the 9000-CARDFILE-CLOSE procedure
- Display output message
- Return control to caller

## 1000-CARDFILE-GET-NEXT

- Retrieve next record from CARD-RECORD
- When CARDFILE-STATUS = '00'
- Set APPL-RESULT to 0
- When CARDFILE-STATUS = '00'
- Set APPL-RESULT to 16
- Set APPL-RESULT to 12
- When APPL-AOK
- Continue without action
- When APPL-AOK
- Set END-OF-FILE to 'Y'
- Display output message
- Set IO-STATUS to CARDFILE-STATUS
- Execute the 9910-DISPLAY-IO-STATUS procedure
- Execute the 9999-ABEND-PROGRAM procedure
- Exit the current paragraph

## 0000-CARDFILE-OPEN

- Set APPL-RESULT to 8
- Open file
- When CARDFILE-STATUS = '00'
- Set APPL-RESULT to 0
- Set APPL-RESULT to 12
- When APPL-AOK
- Continue without action
- Display output message
- Set IO-STATUS to CARDFILE-STATUS
- Execute the 9910-DISPLAY-IO-STATUS procedure
- Execute the 9999-ABEND-PROGRAM procedure
- Exit the current paragraph

## 9000-CARDFILE-CLOSE

- Accumulate 8 into APPL-RESULT
- Close file
- When CARDFILE-STATUS = '00'
- Reduce APPL-RESULT by APPL-RESULT
- Accumulate 12 into APPL-RESULT
- When APPL-AOK
- Continue without action
- Display output message
- Set IO-STATUS to CARDFILE-STATUS
- Execute the 9910-DISPLAY-IO-STATUS procedure
- Execute the 9999-ABEND-PROGRAM procedure
- Exit the current paragraph

## 9999-ABEND-PROGRAM

- Display output message
- Set TIMING to 0
- Set ABCODE to 999
- Invoke external program 'CEE3ABD'

## 9910-DISPLAY-IO-STATUS

- When IO-STATUS NOT NUMERIC
- Set 1 to IO-STAT1
- Set TWO-BYTES-BINARY to 0
- Set TWO-BYTES-RIGHT to IO-STAT2
- Set IO-STATUS-0403 to TWO-BYTES-BINARY
- Display output message
- Set IO-STATUS-04 to '0000'
- Set 2 to IO-STATUS
- Display output message
- Exit the current paragraph

