# Check if pip is installed
PIP_CHECK := $(shell pip --version >nul 2>&1;)
ifeq ($(PIP_CHECK), 1)
$(error "You must have pip installed to continue.")
endif

# Check if pipenv is installed
PIPENV_CHECK := $(shell pipenv --version >nul 2>&1;)
ifeq ($(PIPENV_CHECK), 1)
$(info "Installing pipenv...")
PIP_INSTALL := $(shell pip install pipenv)
endif

.PHONY: install run
.DEFAULT_GOAL := run

install:
	@pipenv install

run: install
	@pipenv run uvicorn main:app

dev:
	@pipenv run uvicorn main:app --reload