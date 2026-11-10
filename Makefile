.PHONY: install dev test lint format docker-up docker-down seed run-agent

install:
	uv sync --extra dev

dev:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	uv run pytest

lint:
	uv run ruff check app tests
	uv run mypy app

format:
	uv run ruff format app tests

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down -v

seed:
	uv run python scripts/seed_db.py

run-agent:
	uv run python scripts/run_agent.py
