#!/usr/bin/env bash
set -e

echo ">> Executando migrações Alembic..."
alembic upgrade head

echo ">> Iniciando servidor FastAPI..."
exec uvicorn main:app --host localhost --port 8000