#!/usr/bin/env bash
set -euo pipefail

echo "Running Alembic migrations..."
docker compose exec backend alembic upgrade head

echo "Seeding companies & skills..."
docker compose exec backend python scripts/seed.py

echo "Done."
