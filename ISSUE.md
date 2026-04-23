---
title: ClawBot Issue Log
version: "1.0"
last_updated: "2026-04-01"
---

# ISSUE.md

Agents open or update this file as part of the failure handling procedure.
Each issue is a separate H2 section. Issues are never deleted — they are marked `resolved` or `wont-fix`.

## Issue Format

```yaml
---
issue_id: "ISS-<number>"
date_opened: "YYYY-MM-DD"
phase: "<Plan|Build|Validate|Review|Release>"
status: "<open|in-progress|resolved|wont-fix>"
related_ts: "<TS-XXX or none>"
blocked_on: "<human|dependency|investigation>"
---
```

**Summary**: One sentence describing what failed.
**Context**: What the agent was attempting.
**Logs**: Path to captured log file (`logs/ISS-XXX-YYYY-MM-DD.log`).
**Requested Human Action**: Exactly what the human needs to decide or do.

---

_No issues open. This file is ready for agent use._
