# Environment

install:
	uv sync

lock:
	uv lock

seed:
	APP_ENV=development uv run python -m app.seed

server-dev:
	APP_ENV=development uv run uvicorn app:create_app --reload

# Linting & formatting (ruff + ty)

lint:
	uv run ruff check .

check-format:
	uv run ruff format --check .

check-types:
	uv run ty check

format:
	uv run ruff format .
	uv run ruff check . --fix

lint-all: check-types lint check-format

# Testing

test:
	APP_ENV=test uv run pytest app

test-cov:
	APP_ENV=test uv run pytest app --verbose \
		--cov-config=.coveragerc \
		--cov=app \
		--cov-report=term:skip-covered \
		--cov-report=html \
		--cov-report=xml \
		--cov-branch \
		--cov-fail-under=60

test-watch:
	APP_ENV=test uv run ptw app

test-integration:
	APP_ENV=test uv run pytest tests/integration

test-end-to-end:
	APP_ENV=test uv run pytest tests/end-to-end

test-all: test test-integration test-end-to-end
