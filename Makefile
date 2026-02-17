PYTHON ?= python

.PHONY: setup lint test run docker-build help

setup:
	$(PYTHON) -m pip install --upgrade pip
	pip install -e ".[dev]"

lint:
	ruff check src tests

test:
	pytest

run:
	uvicorn pf_integrity.api:app --reload --port 8080

docker-build:
	docker build -t pf-integrity-engine -f deploy/Dockerfile .

help:
	@echo "Available targets: setup, lint, test, run, docker-build"
