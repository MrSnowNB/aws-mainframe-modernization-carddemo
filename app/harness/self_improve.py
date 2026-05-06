#!/usr/bin/env python3
"""
self_improve.py — SecuraTron-style SIL for the COBOL harness
Watches post-mortems, detects repeated failure patterns, emits IT-NNN tickets.
"""
import json
import os
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

# Root of the SecuraTron system inside the container
BASE_DIR = Path("/app/securatron")
# We scan all session directories for post_mortem.md files
SESSIONS_DIR = BASE_DIR / "sessions"
INBOX_NEW = BASE_DIR / "inbox" / "new"
THRESHOLD = 3   # same pattern 3+ times → ticket

def extract_pattern(pm_text: str) -> str:
    """Classifies the failure based on SecuraTron FM-taxonomy."""
    text = pm_text.lower()
    
    # HTTP errors (likely infrastructure/lemonade)
    if "llm http 500" in text:
        return "FM-1:llm_server_500"
    if "llm http 401" in text:
        return "FM-1:llm_auth_error"
    if "connection refused" in text:
        return "FM-1:llm_connectivity_refused"
    
    # Logic/Verification errors
    if "hallucinated_paragraphs" in text or "hallucinated-para" in text:
        return "FM-3:hallucination_detected"
    if "context" in text and "overflow" in text:
        return "FM-7:context_overflow"
    if "cics" in text and "screen" in text:
        return "FM-4:cics_screen_edge"
    
    # Pipeline step failures
    if "pipeline failed at pass1" in text:
        return "FM-10:preprocessing_failure"
    if "gate_compare failed" in text:
        return "FM-11:gate_refusal"

    return "FM-99:unknown"

def main():
    INBOX_NEW.mkdir(parents=True, exist_ok=True)
    
    pattern_counts = defaultdict(int)
    pattern_examples = {}
    pattern_sessions = defaultdict(list)

    # Scan all sessions for post_mortems
    for pm_file in SESSIONS_DIR.glob("**/post_mortem.md"):
        try:
            text = pm_file.read_text()
            if not text.strip():
                continue
            
            pattern = extract_pattern(text)
            pattern_counts[pattern] += 1
            pattern_sessions[pattern].append(pm_file.parent.name)
            
            if pattern not in pattern_examples:
                pattern_examples[pattern] = text[:500] # Save snippet
        except Exception as e:
            print(f"Error reading {pm_file}: {e}")

    print(f"--- SIL Scan: {datetime.now(timezone.utc).isoformat()} ---")
    for pattern, count in pattern_counts.items():
        print(f"  {pattern}: {count} occurrences")
        
        if count >= THRESHOLD and pattern != "FM-99:unknown":
            ticket_id = f"IT-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
            
            # Robust duplicate check across all queues
            INBOX_QUEUES = [
                INBOX_NEW,
                BASE_DIR / "inbox" / "cur",
                BASE_DIR / "inbox" / "archive"
            ]

            existing = []
            for queue in INBOX_QUEUES:
                if queue.exists():
                    existing.extend(queue.glob(f"IT-*{pattern.replace(':', '_')}*"))

            if existing:
                print(f"  → Duplicate ticket already exists in {existing[0].parent.name}/ — skipping")
                continue

            ticket = {
                "ticket_id": ticket_id,
                "type": "self_improvement",
                "pattern": pattern,
                "occurrences": count,
                "affected_sessions": pattern_sessions[pattern][-5:], # last 5
                "suggested_action": "Evaluate FM-taxonomy recovery protocol.",
                "created_at": datetime.now(timezone.utc).isoformat() + "Z",
                "status": "pending",
                "human_gate": True, # SIL tickets always require review in Stagecraft
                "skill": "infra.patch", # Placeholder for the auto-patcher skill
                "inputs": {
                    "pattern": pattern,
                    "example_context": pattern_examples[pattern]
                }
            }
            
            ticket_path = INBOX_NEW / f"{ticket_id}.json"
            ticket_path.write_text(json.dumps(ticket, indent=2))
            print(f">>> EMITTED IMPROVEMENT TICKET: {ticket_id} for {pattern}")

if __name__ == "__main__":
    main()
