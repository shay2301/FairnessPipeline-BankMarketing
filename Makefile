#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = fairnesspipeline-bankmarketing
PYTHON_VERSION = 3.11
PYTHON_INTERPRETER = python3

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8 and black (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 fairnesspipeline_bankmarketing
	isort --check --diff --profile black fairnesspipeline_bankmarketing
	black --check --config pyproject.toml fairnesspipeline_bankmarketing

## Format source code with black
.PHONY: format
format:
	black --config pyproject.toml fairnesspipeline_bankmarketing

## Download Data from storage system
.PHONY: sync_data_down
sync_data_down:
	aws s3 sync s3://bucket-name/data/ data/

## Upload Data to storage system
.PHONY: sync_data_up
sync_data_up:
	aws s3 sync data/ s3://bucket-name/data/ --profile $(PROFILE)

## Set up python interpreter environment
.PHONY: create_environment
create_environment:
	@bash -c "if [ ! -z `which virtualenvwrapper.sh` ]; then source `which virtualenvwrapper.sh`; mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER); else mkvirtualenv.bat $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER); fi"
	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Make Dataset
.PHONY: data
data: requirements
	$(PYTHON_INTERPRETER) fairnesspipeline_bankmarketing/data/make_dataset.py

## Run all scripts sequentially
.PHONY: run_all
run_all: requirements
	echo "Running all scripts..."
	$(PYTHON_INTERPRETER) fairnesspipeline_bankmarketing/modeling/config.py
	$(PYTHON_INTERPRETER) fairnesspipeline_bankmarketing/modeling/dataset.py
	$(PYTHON_INTERPRETER) fairnesspipeline_bankmarketing/modeling/features.py
	$(PYTHON_INTERPRETER) fairnesspipeline_bankmarketing/modeling/train.py
	$(PYTHON_INTERPRETER) fairnesspipeline_bankmarketing/modeling/predict.py
	$(PYTHON_INTERPRETER) fairnesspipeline_bankmarketing/modeling/database.py

.DEFAULT_GOAL := help

## Help command
.PHONY: help
help:
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
