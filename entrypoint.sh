#!/bin/sh

echo "======================================"
echo "Waiting for PostgreSQL..."
echo "======================================"

python - <<EOF
import socket
import time

host = "postgres-service"
port = 5432

while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            print("PostgreSQL is ready!")
            break
    except OSError:
        print("Waiting for PostgreSQL...")
        time.sleep(2)
EOF

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