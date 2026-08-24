PROJECT_NAME := $(shell basename $(CURDIR))

define HELP
Manage $(PROJECT_NAME). Usage:

make run          - Run $(PROJECT_NAME).
make install      - Create virtual env and install dependencies via uv.
make update       - Upgrade locked dependencies and refresh requirements.txt.
make requirements - Export uv.lock to requirements.txt.
make format       - Format code with `isort` and `black`.
make lint         - Check code formatting with flake8.
make test         - Run the test suite.
make clean        - Remove cached files.
endef
export HELP


.PHONY: all help run install update requirements format lint test clean

all help:
	@echo "$$HELP"


run:
	uv run main.py


install:
	uv sync


update:
	uv lock --upgrade
	uv sync
	$(MAKE) requirements


requirements:
	uv export --no-hashes --no-dev --output-file requirements.txt


format:
	uv run isort --multi-line=3 .
	uv run black .


lint:
	uv run flake8 . --count \
			--select=E9,F63,F7,F82 \
			--exclude .git,.github,__pycache__,.pytest_cache,.venv,logs,creds,docs \
			--show-source \
			--statistics


test:
	uv run pytest || [ $$? -eq 5 ]  # exit 5 == no tests collected


clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
	find . -name '*.log' -delete
	find . -name '.pytest_cache' -type d -prune -exec rm -rf {} +
	find . -path './logs/*.json' -delete
