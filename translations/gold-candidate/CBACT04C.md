---
schema_version: "cobol-md/1.0"
program_id: "CBACT04C"
source_file: "app/cbl/CBACT04C.cbl"
source_sha: "c5e0280e2ed0891877b43eda7bc7c6dc86752421"
translation_date: "2026-05-06"
translating_agent: "syncd-scaffold/1.1"
aifirst_task_id: "TODO-assign-task-id"
cfg_source: "validation/structure/CBACT04C_cfg.json"

business_domain: "TODO"
subtype: "TODO"  # Batch | Online | Utility

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
  target: "TODO"  # Batch/VSAM | CICS/Online
  runtime: "z/OS"

calls_to: []  # TODO: fill from source
  # Each entry should have: program, condition, call_type
  # Example: - program: "MVSWAIT", condition: "unconditional", call_type: "STATIC"
called_by: []  # TODO: fill from source
copybooks_used: []  # TODO: fill from source

file_control: []  # TODO: fill from source

cics_commands: []
transaction_ids: []

data_items:

  - name: "FD-TRAN-CAT-BAL-RECORD"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "FD-XREFFILE-REC"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "FD-DISCGRP-REC"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "FD-ACCTFILE-REC"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "FD-TRANFILE-REC"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "TCATBALF-STATUS"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "XREFFILE-STATUS"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "DISCGRP-STATUS"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "ACCTFILE-STATUS"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "TRANFILE-STATUS"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "IO-STATUS"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "TWO-BYTES-BINARY"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "TWO-BYTES-ALPHA"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "IO-STATUS-04"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "APPL-RESULT"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "END-OF-FILE"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "ABCODE"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "TIMING"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "COBOL-TS"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "DB2-FORMAT-TS"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "FILLER"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "WS-MISC-VARS"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "WS-COUNTERS"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"

  - name: "EXTERNAL-PARMS"
    level: 1
    picture: null
    usage: null
    value: null
    redefines: null
    redefines_interpretations: []  # TODO: fill when REDEFINES clause exists in source
      # Each entry should have: interpretation (semantic explanation of the redefined alias)
      # Example: "Redefined as packed decimal for monetary values"
    dead_code_flag: false
    semantic: "TODO"


procedure_paragraphs:

  - name: "0000-TCATBALF-OPEN"
    reachable: true
    performs:


      - "0100-XREFFILE-OPEN"

      - "9999-ABEND-PROGRAM"

      - "9910-DISPLAY-IO-STATUS"


    goto_targets:

      []

    summary: "TODO"

  - name: "0100-XREFFILE-OPEN"
    reachable: true
    performs:


      - "0200-DISCGRP-OPEN"

      - "9999-ABEND-PROGRAM"

      - "9910-DISPLAY-IO-STATUS"


    goto_targets:

      []

    summary: "TODO"

  - name: "0200-DISCGRP-OPEN"
    reachable: true
    performs:


      - "0300-ACCTFILE-OPEN"

      - "9999-ABEND-PROGRAM"

      - "9910-DISPLAY-IO-STATUS"


    goto_targets:

      []

    summary: "TODO"

  - name: "0300-ACCTFILE-OPEN"
    reachable: true
    performs:


      - "0400-TRANFILE-OPEN"

      - "9999-ABEND-PROGRAM"

      - "9910-DISPLAY-IO-STATUS"


    goto_targets:

      []

    summary: "TODO"

  - name: "0400-TRANFILE-OPEN"
    reachable: true
    performs:


      - "1000-TCATBALF-GET-NEXT"

      - "9999-ABEND-PROGRAM"

      - "9910-DISPLAY-IO-STATUS"


    goto_targets:

      []

    summary: "TODO"

  - name: "1000-TCATBALF-GET-NEXT"
    reachable: true
    performs:


      - "1050-UPDATE-ACCOUNT"

      - "9999-ABEND-PROGRAM"

      - "9910-DISPLAY-IO-STATUS"


    goto_targets:

      []

    summary: "TODO"

  - name: "1050-UPDATE-ACCOUNT"
    reachable: true
    performs:


      - "1100-GET-ACCT-DATA"

      - "9999-ABEND-PROGRAM"

      - "9910-DISPLAY-IO-STATUS"


    goto_targets:

      []

    summary: "TODO"

  - name: "1100-GET-ACCT-DATA"
    reachable: true
    performs:


      - "1110-GET-XREF-DATA"

      - "9999-ABEND-PROGRAM"

      - "9910-DISPLAY-IO-STATUS"


    goto_targets:

      []

    summary: "TODO"

  - name: "1110-GET-XREF-DATA"
    reachable: true
    performs:


      - "1200-GET-INTEREST-RATE"

      - "9999-ABEND-PROGRAM"

      - "9910-DISPLAY-IO-STATUS"


    goto_targets:

      []

    summary: "TODO"

  - name: "1200-A-GET-DEFAULT-INT-RATE"
    reachable: true
    performs:


      - "1300-COMPUTE-INTEREST"

      - "9999-ABEND-PROGRAM"

      - "9910-DISPLAY-IO-STATUS"


    goto_targets:

      []

    summary: "TODO"

  - name: "1200-GET-INTEREST-RATE"
    reachable: true
    performs:


      - "1200-A-GET-DEFAULT-INT-RATE"

      - "9999-ABEND-PROGRAM"

      - "9910-DISPLAY-IO-STATUS"


    goto_targets:

      []

    summary: "TODO"

  - name: "1300-B-WRITE-TX"
    reachable: true
    performs:


      - "1400-COMPUTE-FEES"

      - "9999-ABEND-PROGRAM"

      - "9910-DISPLAY-IO-STATUS"

      - "Z-GET-DB2-FORMAT-TIMESTAMP"


    goto_targets:

      []

    summary: "TODO"

  - name: "1300-COMPUTE-INTEREST"
    reachable: true
    performs:


      - "1300-B-WRITE-TX"


    goto_targets:

      []

    summary: "TODO"

  - name: "1400-COMPUTE-FEES"
    reachable: true
    performs:


      - "9000-TCATBALF-CLOSE"


    goto_targets:

      []

    summary: "TODO"

  - name: "9000-TCATBALF-CLOSE"
    reachable: true
    performs:


      - "9100-XREFFILE-CLOSE"

      - "9999-ABEND-PROGRAM"

      - "9910-DISPLAY-IO-STATUS"


    goto_targets:

      []

    summary: "TODO"

  - name: "9100-XREFFILE-CLOSE"
    reachable: true
    performs:


      - "9200-DISCGRP-CLOSE"

      - "9999-ABEND-PROGRAM"

      - "9910-DISPLAY-IO-STATUS"


    goto_targets:

      []

    summary: "TODO"

  - name: "9200-DISCGRP-CLOSE"
    reachable: true
    performs:


      - "9300-ACCTFILE-CLOSE"

      - "9999-ABEND-PROGRAM"

      - "9910-DISPLAY-IO-STATUS"


    goto_targets:

      []

    summary: "TODO"

  - name: "9300-ACCTFILE-CLOSE"
    reachable: true
    performs:


      - "9400-TRANFILE-CLOSE"

      - "9999-ABEND-PROGRAM"

      - "9910-DISPLAY-IO-STATUS"


    goto_targets:

      []

    summary: "TODO"

  - name: "9400-TRANFILE-CLOSE"
    reachable: true
    performs:


      - "Z-GET-DB2-FORMAT-TIMESTAMP"

      - "9999-ABEND-PROGRAM"

      - "9910-DISPLAY-IO-STATUS"


    goto_targets:

      []

    summary: "TODO"

  - name: "9910-DISPLAY-IO-STATUS"
    reachable: true
    performs:

      []

    goto_targets:

      []

    summary: "TODO"

  - name: "9999-ABEND-PROGRAM"
    reachable: true
    performs:


      - "9910-DISPLAY-IO-STATUS"


    goto_targets:

      []

    summary: "TODO"

  - name: "Z-GET-DB2-FORMAT-TIMESTAMP"
    reachable: true
    performs:


      - "9999-ABEND-PROGRAM"


    goto_targets:

      []

    summary: "TODO"




business_rules: []  # TODO: fill during translation
  # Each entry should have: id, rule, source_paragraph, rule_type, confidence, reachable
  # Example: - id: "BR-001", rule: "Wait duration must be positive", source_paragraph: "PERFORM-INIT", rule_type: "guard", confidence: "high", reachable: true

validation:
  t01_schema_valid: true
  t02_structural_complete: null
  t02r_redefines_complete: null
  t03_functional_score: null
  t04_semantic_score: null
  t05_regression_pass: null
  overall: "PENDING"

# Locked numbers (from SYNC-MANIFEST.yaml):
#   paragraphs_expected:     22
#   l01_items_expected:      24
#   reachable_expected:      22
#   dead_paragraphs_allowed: 0
#   goto_flag: False
#   alter_flag: False
---

# CBACT04C -- TODO: short program description

## Purpose

TODO: Describe what this program does and its business function.

## Data Layout

TODO: Describe the key data structures.

## Control Flow

TODO: Describe paragraph-level logic in plain English.

## GO TO Suppression Rationale


No GO TO statements detected in CFG.


## Translation Targets

TODO: List key COBOL constructs and their target-language equivalents.
