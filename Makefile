VENV_DIR=venv

venv:
	python3.9 -m venv $(VENV_DIR)
	@echo "\nUse '. $(VENV_DIR)/bin/activate' to activate"

deps-pre:
	pip install pip-tools

deps-compile:
	pip-compile requirements.in --output-file=requirements.txt

deps-install:
	pip-sync && yarn install

deps: deps-pre deps-compile deps-install

install: deps-pre deps-install

seed:
	python -m app.entrypoints.cli.seed

server-dev:
	uvicorn app.main:app --reload

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
	yarn pyright

format: format-isort format-black

lint: check-types check-flake8 check-isort check-black

# Testing

test:
	pytest app

test-watch:
	ptw app
