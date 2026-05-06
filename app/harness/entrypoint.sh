#!/bin/bash

# Start the Inbox Watcher in the background
python3 /app/securatron/global/bin/inbox_watcher.py \
  --config /app/securatron/config.yaml \
  --test-mode \
  --log-level INFO &

# Start the Self-Improvement Loop (SIL) in the background
(
  while true; do
    echo "[SIL] Scanning for recurring failure patterns..."
    python3 /app/harness/self_improve.py
    sleep 300
  done
) &

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port 8000
