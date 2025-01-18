#!/usr/bin/env bash
set -e

echo ">> Executando migrações Alembic..."
alembic upgrade head

echo ">> Iniciando servidor FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000