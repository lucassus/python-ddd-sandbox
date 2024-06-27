VENV_DIR=venv

venv:
	python -m venv $(VENV_DIR)
	@echo "\nUse '. $(VENV_DIR)/bin/activate' to activate"

deps-pre:
	pip install --upgrade pip==24.1.1 pip-tools==7.4.1

deps-compile:
	pip-compile requirements.in --output-file requirements.txt

deps-install:
	pip-sync

deps: deps-pre deps-compile deps-install

install: deps-pre deps-install

seed:
	APP_ENV=development python -m app.seed

server-dev:
	APP_ENV=development uvicorn app:create_app --reload

# Linting

format-isort:
	isort .

check-isort:
	isort . --check-only

format-black:
	black .

check-black:
	black . --check

check-flake8:
	flake8 .

check-types:
	python -m mypy .

format-autoflake:
	autoflake --in-place --recursive \
		--remove-all-unused-imports \
		--remove-unused-variables \
		app tests

format-yesqa:
	yesqa app/**/*.py tests/**/*.py

format: format-yesqa format-autoflake format-isort format-black

lint: check-types check-flake8 check-isort check-black

# Testing

test:
	APP_ENV=test pytest app

test-cov:
	APP_ENV=test pytest app --verbose \
		--cov-config=.coveragerc \
		--cov=app \
		--cov-report=term:skip-covered \
		--cov-report=html \
		--cov-report=xml \
		--cov-branch \
		--cov-fail-under=60

test-watch:
	APP_ENV=test ptw app

test-integration:
	APP_ENV=test pytest tests/integration

test-end-to-end:
	APP_ENV=test pytest tests/end-to-end

test-all: test test-integration test-end-to-end
