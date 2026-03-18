#!/bin/sh

set -e

uvicorn src.main:app --host 0.0.0.0 --port 8000 &

wait