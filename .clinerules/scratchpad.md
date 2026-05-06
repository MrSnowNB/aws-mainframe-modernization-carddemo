# AI First Scratchpad

> **Purpose:** Context management for AI First protocol agents working on this repo.
> **Usage:** Read BRANCH-SCOPE.md first → read this file → execute task.
> **Discipline:** Read-once, write-once per session. Never anchor work on prior session's scratchpad.

---

## Current State Snapshot

| Checkpoint | Value |
|---|---|
| Current Branch | `preserve/local-progress-2026-05-06` |
| HEAD Commit | `386a471 feat(bi): fix CBCUS01C bi_category to batch_utility` |
| Branch Ahead | 0 commits (up to date with origin) |
| Branch Behind | 45 commits behind `origin/main` |
| Working Tree | Clean |
| Locked Programs | 11 (CBSTM03A, CBCUS01C, COBSWAIT, CBACT01C-04C, CBSTM03B, CBTRN01C, COMEN01C, COSGN00C, COCRDUPC) |
| Completed Translations | 8 programs (gate PASS) |
| Pending Programs | ~32 programs |

---

## Repo Architecture Summary

### Pipeline Stages
```
app/cbl/*.cbl → Cobol-REKT → CFG JSON
CFG JSON + pass1_annotate.py → Annotations JSON
Annotations JSON + pass2_llm.py → Propositions JSONL
Propositions + pass3_synthesize.py → MD Translation
MD Translation + Gate Pipeline → Gate Report (PASS/FAIL)
```

### Key Directories
| Directory | Purpose |
|---|---|
| `app/cbl/` | COBOL source (READ ONLY, immutable) |
| `validation/structure/` | CFG JSONs from Cobol-REKT |
| `validation/waves/` | Multi-pass pipeline output (wave-1/2/3/) |
| `translations/gold-candidate/` | Gate-verified MD translations |
| `validation/ground_truth/` | Normalized CFG for gate comparison |
| `validation/claims/` | Extracted MD claims for comparison |
| `tools/syncd/` | syncd v1.1 toolchain |

### Gate Pipeline (Deterministic, No LLM)
```powershell
# Step 1: Build ground truth from CFG
python validation/extract_ground_truth.py

# Step 2: Extract structural claims from MD
python validation/extract_md_claims.py

# Step 3: Diff and gate
python validation/gate_compare.py
```

---

## Current Gating Status

### Programs with Locked Numbers (SYNC-MANIFEST.yaml)
| Program | Paragraphs | L01 Items | Dead Allowed | Source SHA |
|---|---|---|---|---|
| CBSTM03A | 25 | 18 | 0 | 290c3f4... |
| CBCUS01C | 5 | 10 | 0 | ad4c512... |
| COBSWAIT | 0 | 2 | 0 | 7957347... |
| CBACT01C | 16 | 21 | 0 | e680f8e... |
| CBACT02C | 5 | 10 | 0 | c913858... |
| CBACT03C | 5 | 10 | 0 | a548096... |
| CBACT04C | 22 | 24 | 0 | c5e0280... |
| CBSTM03B | 14 | 9 | 0 | 7d70690... |
| CBTRN01C | 18 | 21 | 0 | 450bd63... |
| COMEN01C | 6 | 2 | 0 | 222db83... |
| COSGN00C | 9 | 14 | 3 | 28e2061... |
| COCRDUPC | 0 | 0 | 0 | 10f0655... |

### Completed (Gate PASS)
- CBACT01C, CBACT02C, CBACT03C, CBCUS01C, CBTRN01C, COBSWAIT, COMEN01C, COSGN00C

---

##Ai First Protocol State

### Current Gate Templates (v2.2)
| Gate | Purpose | Status |
|---|---|---|
| G0 DECOMPOSE | First-principles problem decomposition | ACTIVE |
| G1 PLAN | Concrete action sequence | ACTIVE |
| G2 SCAFFOLD | syncd scaffold + frontmatter lock | ACTIVE |
| G3 EXECUTE | Narrative content fill | ACTIVE |
| G4 VALIDATE | syncd verify mechanical check | ACTIVE |
| G5 COMMIT | syncd bundle + audit trail | ACTIVE |

### Recent Gate Runs (from .clinerules/runs/)
- T-2026-05-05-001: CBCUS01C proof-point (G0-G5 completed, HALTED for Operation Tidy)
- T-2026-05-04-001: CBCUS01C gold promotion (G0-G2 completed, G2 HALTED)

---

## BRANCH-SCOPE Discipline

### Scope Rules
| Branch Prefix | Deliverable | Scope |
|---|---|---|
| `wave<N>/<program>` | `<PROG>.md`, `<PROG>_cfg.json`, gate PASS | ONLY the named program |
| `fix/<topic>` | Single file or bug class | No unrelated edits |
| `chore/<topic>` | Infrastructure/docs/rules | No pipeline code changes |

### Forbidden Without Explicit Human Approval
- Block F T04 judge dispatch (60+ payload batch)
- extract_cfg_summary.py --all --force
- git push (use `git push -u origin <branch>` for new branches)
- git merge (human-only action)
- Editing validators (gate_compare.py, lint_cobol.py, etc.)
- Hand-editing validation/structure/ or validation/rekt/

### Mandatory Pre-Commit Checklist
1. `git status -sb` — show current branch + clean tree
2. Confirm branch name matches scope rule
3. Confirm files being committed are in scope
4. For any `.md` change: `py validation/extract_md_claims.py <PROG>` must PASS
5. For any validation/ change: `py validation/gate_compare.py` must return N/N PASS
6. For any lint change: `py validation/lint_cobol/lint_cobol.py --fail-on-error` must match baseline

---

## Recent Fixes & Improvements

### Gate Tool Fixes (merged to main)
| Fix | What it addressed |
|---|---|
| `extract_cfg_summary.py` L01 parser | Scans DATA DIVISION for 01-level declarations |
| `extract_cfg_summary.py` paragraph filter | Rejects COBOL verb-prefixed CFG labels |
| CBACT01C.md | Removed hallucinated paragraphs (END-IF, END-PERFORM, GOBACK, etc.) |
| CBACT02C.md | Fixed missing YAML frontmatter; removed hallucinated paragraphs |
| CBACT03C.md | Removed hallucinated data item |
| syncd doctor | Relaxed truncation heuristic to eliminate false positives |
| syncd v2.2 | Reconciled template files to v2.1 spec |

---

## Agent Handoff Requirements

Every agent turn must end with:
1. **Current branch** (git rev-parse --abbrev-ref HEAD)
2. **Files changed** (git diff --stat)
3. **Exit codes** of validators run
4. **Explicit next action** OR "awaiting human instruction"

---

## Context Unloading Checklist

When context window is tight or switching to a new agent:
- [ ] Save current branch name
- [ ] Save current commit SHA
- [ ] Save any uncommitted changes (git stash or commit)
- [ ] Save task_id and current gate (if applicable)
- [ ] Save working state (e.g., "on step X of plan Y")
- [ ] Document any assumptions made
- [ ] Document any blockers or questions

---

## Key Commands Reference

### Validation Pipeline
```powershell
# Verify all programs
py tools/syncd/sync.py verify

# Lock a program's CFG numbers
py tools/syncd/sync.py lock <PROGRAM>

# Generate MD skeleton
py tools/syncd/sync.py scaffold <PROGRAM> [--force]

# Bundle and commit
py tools/syncd/sync.py bundle <PROGRAM> [--pr]

# Health check
py tools/syncd/sync.py doctor
```

### Gate Checks
```powershell
# Full gate pipeline
python validation/extract_ground_truth.py
python validation/extract_md_claims.py
python validation/gate_compare.py

# Single program
python validation/extract_ground_truth.py CBACT01C
python validation/extract_md_claims.py CBACT01C
python validation/gate_compare.py CBACT01C
```

---

## Known Issues & Risks

| Issue | Severity | Status |
|---|---|---|
| source_sha staleness warnings in syncd doctor | LOW | Expected; re-run lock if CFG changes |
| Truncation warnings for programs without 9999- exit paragraph | LOW | COBOL convention; not blocking |
| 45 commits behind origin/main | MEDIUM | Preserving local progress on branch |

---

## Next Action

**Current State:** Branch `preserve/local-progress-2026-05-06` contains current repo state.

**Task:** Create AI First scratchpad for context management across context windows.

**Status:** ✅ Scratchpad created at `.clinerules/scratchpad.md`

**Next Agent Action:** 
- Read BRANCH-SCOPE.md first
- Read this scratchpad.md
- Execute task per scope discipline
- End turn with handoff requirements

---

*Last Updated: 2026-05-06T09:23:00Z*
*Scratchpad Version: ai-first/1.0*