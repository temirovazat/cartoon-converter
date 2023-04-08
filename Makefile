# Virtual environment name
VENV = .venv

install: ## Install dependencies
	python -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

activate: ## Activate virtual environment
	source $(VENV)/bin/activate

deactivate: ## Deactivate virtual environment
	deactivate

clean: ## Remove virtual environment
	rm -rf $(VENV)

format: ## Format code
	black *.py &&\
	isort *.py

lint: ## Lint code
	flake8 . --count --statistics --show-source

help: ## Display this help message
	@echo "Available targets:"
	@awk -F '##' '/^[a-z_]+:[a-z ]+##/ { print "\033[34m"$$1"\033[0m" "\n" $$2 }' Makefile

run: ## Run the application
	python app.py

default: help