VENV_DIR=venv

venv:
	python3.8 -m venv $(VENV_DIR)
	@echo "\nUse '. $(VENV_DIR)/bin/activate' to activate"

install:
	pip install pip-tools
	pip install -r requirements.txt

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
	pytest

test-watch:
	ptw .
