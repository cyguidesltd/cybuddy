.PHONY: install run validate lint format typecheck

install:
	pip install -e .[dev]

run:
	python -m cybuddy --help || true

validate:
	python3 -c "import src.cybuddy; print('Package imports successfully')"
	pip install -e . > /dev/null 2>&1
	python3 -m cybuddy --help

lint:
	ruff check . && ruff format --check . && mypy src

format:
	ruff format .

typecheck:
	mypy src

