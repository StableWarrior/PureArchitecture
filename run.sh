#!/bin/sh

set -e

python -m src.core.scheduler_outbox &
python -m src.core.scheduler_inbox &
python -m src.core.scheduler_notifications &
uvicorn src.main:app --host 0.0.0.0 --port 8000 &

wait