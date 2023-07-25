VENV_DIR=venv

venv:
	python3.9 -m venv $(VENV_DIR)
	@echo "\nUse '. $(VENV_DIR)/bin/activate' to activate"

deps-pre:
	pip install --upgrade pip==23.2.1 pip-tools==7.1.0

deps-compile:
	pip-compile requirements.in --output-file requirements.txt

deps-install:
	pip-sync

deps: deps-pre deps-compile deps-install

install: deps-pre deps-install

seed:
	APP_ENV=development python -m app.infrastructure.seed

server-dev:
	APP_ENV=development uvicorn app.main:app --reload

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

format: format-isort format-black

lint: check-types check-flake8 check-isort check-black

# Testing

test:
	APP_ENV=test pytest app

# TODO: Tune coverage settings
test-cov:
	APP_ENV=test pytest app --verbose \
		--cov=app \
		--cov-report=term:skip-covered \
		--cov-report=html \
		--cov-report=xml \
		--cov-branch \
		--cov-fail-under=60

test-watch:
	APP_ENV=test ptw app
