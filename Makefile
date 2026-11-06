.PHONY: install test lint format run docker-up docker-down

install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check app tests scripts
	black --check app tests scripts

format:
	ruff check --fix app tests scripts
	black app tests scripts

run:
	python app/main.py

docker-up:
	docker compose up -d

docker-down:
	docker compose down
