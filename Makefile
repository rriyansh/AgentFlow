.PHONY: install dev test lint format docker-up docker-down docker-logs migrate seed run-agent clean

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

docker-logs:
	docker compose logs -f

docker-dev:
	docker compose -f docker-compose.dev.yml up --build

migrate:
	uv run alembic upgrade head

seed:
	uv run python scripts/seed_db.py

run-agent:
	uv run python scripts/run_agent.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
