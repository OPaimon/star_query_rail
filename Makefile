#* Variables
SHELL := /usr/bin/env bash
PYTHON := python
OS := $(shell python -c "import sys; print(sys.platform)")

ifeq ($(OS),win32)
	PYTHONPATH := $(shell python -c "import os; print(os.getcwd())")
    TEST_COMMAND := set PYTHONPATH=$(PYTHONPATH) && rye run pytest -c pyproject.toml --cov-report=html --cov=star_query_rail tests/
else
	PYTHONPATH := `pwd`
    TEST_COMMAND := PYTHONPATH=$(PYTHONPATH) rye run pytest -c pyproject.toml --cov-report=html --cov=star_query_rail tests/
endif

#* Docker variables
IMAGE := star_query_rail
VERSION := latest

.PHONY: lock install pre-commit-install polish-codestyle formatting test check-codestyle lint docker-build docker-remove cleanup help

lock:
	rye lock

install:
	rye lock
	rye sync
pre-commit-install:
	rye run pre-commit install

polish-codestyle:
	rye run ruff format --config pyproject.toml .
	rye run ruff check --fix --config pyproject.toml .

formatting: polish-codestyle
format: polish-codestyle

test:
	$(TEST_COMMAND)
	rye run coverage-badge -o assets/images/coverage.svg -f

check-codestyle:
	rye run ruff format --check --config pyproject.toml .
	rye run ruff check --config pyproject.toml .



lint: test check-codestyle 

# Example: make docker-build VERSION=latest
# Example: make docker-build IMAGE=some_name VERSION=0.1.0
docker-build:
	@echo Building docker $(IMAGE):$(VERSION) ...
	docker build \
		-t $(IMAGE):$(VERSION) . \
		-f ./docker/Dockerfile --no-cache

# Example: make docker-remove VERSION=latest
# Example: make docker-remove IMAGE=some_name VERSION=0.1.0
docker-remove:
	@echo Removing docker $(IMAGE):$(VERSION) ...
	docker rmi -f $(IMAGE):$(VERSION)

cleanup:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	find . | grep -E ".DS_Store" | xargs rm -rf
	find . | grep -E ".mypy_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	rm -rf build/

help:
	@echo "lock                                      Lock the dependencies."
	@echo "install                                   Install the project dependencies."
	@echo "pre-commit-install                        Install the pre-commit hooks."
	@echo "polish-codestyle                          Format the codebase."
	@echo "formatting                                Format the codebase."
	@echo "test                                      Run the tests."
	@echo "check-codestyle                           Check the codebase for style issues."
	@echo "lint                                      Run the tests and check the codebase for style issues."
	@echo "docker-build                              Build the docker image."
	@echo "docker-remove                             Remove the docker image."
	@echo "cleanup                                   Clean the project directory."
	@echo "help                                      Display this help message."
