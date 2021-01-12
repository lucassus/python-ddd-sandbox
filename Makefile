VENV_DIR=venv

venv:
	python3.9 -m venv $(VENV_DIR)
	@echo "\nUse '. $(VENV_DIR)/bin/activate' to activate"

deps-pre:
	pip install pip-tools

deps-compile:
	pip-compile requirements.in --output-file=requirements.txt

deps-install:
	pip-sync

deps: deps-pre deps-compile deps-install

install: deps-pre deps-install

server-dev:
	uvicorn todos.main:app --reload

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

check-mypy:
	mypy todos

format: format-isort format-black

lint: check-mypy check-isort check-black check-flake8

# Testing

test:
	pytest --cov=todos --cov-report=term

test-watch:
	ptw .
