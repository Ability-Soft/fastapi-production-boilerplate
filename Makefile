# AbilitySoft Python FastAPI Boilerplate Makefile
# ──────────────────────────────────────────────────────────

.PHONY: help install dev test lint format migrate-gen migrate-run docker-up docker-down clean

help:
	@echo "Available commands:"
	@echo "  install      - Install dependencies"
	@echo "  dev          - Start development server with reload"
	@echo "  test         - Run tests with pytest"
	@echo "  lint         - Run linting checks (ruff, mypy)"
	@echo "  format       - Format code with ruff"
	@echo "  migrate-gen  - Generate a new database migration (requires m=\"message\")"
	@echo "  migrate-run  - Run all pending database migrations"
	@echo "  docker-up    - Start services with Docker Compose"
	@echo "  docker-down  - Stop services and remove containers"
	@echo "  clean        - Remove temporary files and caches"

install:
	pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest tests/ -v --asyncio-mode=auto

lint:
	ruff check .
	mypy app

format:
	ruff format .

migrate-gen:
	alembic revision --autogenerate -m "$(m)"

migrate-run:
	alembic upgrade head

docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf .coverage htmlcov
