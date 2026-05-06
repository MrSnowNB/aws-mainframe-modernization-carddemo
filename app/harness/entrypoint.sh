#!/bin/bash

# Start the Inbox Watcher in the background
# We point it to the container-local inbox path
python3 /app/securatron/global/bin/inbox_watcher.py \
  --config /app/securatron/config.yaml \
  --test-mode \
  --log-level INFO &

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port 8000
