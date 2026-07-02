#!/bin/sh

echo "======================================"
echo "Running Alembic migrations..."
echo "======================================"

alembic upgrade head

echo "======================================"
echo "Starting FastAPI..."
echo "======================================"

exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000