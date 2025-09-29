.PHONY: install run test lint format typecheck

install:
	pip install -e .[dev]

run:
	python -m secbuddy --help || true

test:
	pytest -q

lint:
	ruff check . && ruff format --check . && mypy src

format:
	ruff format .

typecheck:
	mypy src

