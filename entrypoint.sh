#!/bin/sh

echo "======================================"
echo "Waiting for PostgreSQL..."
echo "======================================"

python - <<EOF
import socket
import time
import os
from urllib.parse import urlparse

database_url = os.environ["DATABASE_URL"]

parsed_url = urlparse(database_url)
host = parsed_url.hostname
port = parsed_url.port


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