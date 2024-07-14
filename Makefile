#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = fairnesspipeline-bankmarketing
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = python3
VENV_DIR = .venv
ifeq ($(OS),Windows_NT)
    ACTIVATE_SCRIPT = .venv\Scripts\activate
    PIP = .venv\Scripts\pip
    PYTHON = .venv\Scripts\python
else
    ACTIVATE_SCRIPT = .venv/bin/activate
    PIP = .venv/bin/pip
    PYTHON = .venv/bin/python
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

.PHONY: requirements
requirements: $(ACTIVATE_SCRIPT)
ifeq ($(OS),Windows_NT)
	@echo "Upgrading pip using Python module..."
	$(PYTHON) -m pip install --upgrade pip
	@echo "Installing requirements from requirements.txt using Python module..."
	$(PYTHON) -m pip install -r requirements.txt
else
	@echo "Upgrading pip..."
	$(PIP) install --upgrade pip
	@echo "Installing requirements from requirements.txt..."
	$(PIP) install -r requirements.txt
endif

## Create Virtual Environment
$(ACTIVATE_SCRIPT): 
	$(PYTHON_INTERPRETER) -m venv $(VENV_DIR)
	@echo ">>> Virtual environment created at $(VENV_DIR)"
ifeq ($(OS),Windows_NT)
	@echo "@echo off & call $(ACTIVATE_SCRIPT)" > activate.bat
else
	@echo "source $(ACTIVATE_SCRIPT)" > activate
endif

.PHONY: clean
clean:
ifeq ($(OS),Windows_NT)
	del /s /q *.py[co]
	del /s /q __pycache__
else
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
endif

.PHONY: lint
lint: requirements
	$(PIP) flake8 modeling
	$(PIP) isort --check --diff --profile black modeling
	$(PIP) black --check --config pyproject.toml modeling

.PHONY: format
format: requirements
	$(PIP) black --config pyproject.toml modeling

.PHONY: sync_data_down
sync_data_down: requirements
	$(PIP) aws s3 sync s3://bucket-name/data/ data/

.PHONY: sync_data_up
sync_data_up: requirements
	$(PIP) aws s3 sync data/ s3://bucket-name/data/ --profile $(PROFILE)

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Run all scripts sequentially
.PHONY: config dataset features sanity_checks train predict plots database

config: requirements
	$(PYTHON) modeling/config.py

dataset: config
	$(PYTHON) modeling/dataset.py

features: dataset
	$(PYTHON) modeling/features.py

sanity_checks: features
	$(PYTHON) modeling/sanity_checks.py

train: sanity_checks
	$(PYTHON) modeling/train.py

predict: train
	$(PYTHON) modeling/predict.py

plots: predict
	$(PYTHON) modeling/plots.py

database: plots
	$(PYTHON) modeling/database.py

.PHONY: run_all
run_all: database
	@echo "All scripts executed in order."

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
