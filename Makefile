#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = fairnesspipeline-bankmarketing
PYTHON_VERSION = 3.11
PYTHON_INTERPRETER = python3
VENV_DIR = .venv


#################################################################################
# COMMANDS   
#"In terminal write 'make run_all' to run the full flow :)#                                                                #
#################################################################################

.PHONY: requirements
requirements: $(VENV_DIR)/bin/activate
	$(VENV_DIR)/bin/pip install -U pip
	$(VENV_DIR)/bin/pip install -r requirements.txt

## Create Virtual Environment
$(VENV_DIR)/bin/activate: 
	$(PYTHON_INTERPRETER) -m venv $(VENV_DIR)
	@echo ">>> Virtual environment created at $(VENV_DIR)"
	@echo "source $(VENV_DIR)/bin/activate" > activate

.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

.PHONY: lint
lint: requirements
	$(VENV_DIR)/bin/flake8 modeling
	$(VENV_DIR)/bin/isort --check --diff --profile black modeling
	$(VENV_DIR)/bin/black --check --config pyproject.toml modeling

.PHONY: format
format: requirements
	$(VENV_DIR)/bin/black --config pyproject.toml modeling

.PHONY: sync_data_down
sync_data_down: requirements
	$(VENV_DIR)/bin/aws s3 sync s3://bucket-name/data/ data/

.PHONY: sync_data_up
sync_data_up: requirements
	$(VENV_DIR)/bin/aws s3 sync data/ s3://bucket-name/data/ --profile $(PROFILE)

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Run all scripts sequentially
.PHONY: run_all
run_all: requirements
	@echo "Running all scripts..."
	$(VENV_DIR)/bin/python modeling/config.py
	$(VENV_DIR)/bin/python modeling/dataset.py
	$(VENV_DIR)/bin/python modeling/features.py
	$(VENV_DIR)/bin/python modeling/train.py
	$(VENV_DIR)/bin/python modeling/predict.py
	$(VENV_DIR)/bin/python modeling/database.py

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
