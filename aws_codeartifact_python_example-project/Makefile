# -*- coding: utf-8 -*-

help: ## ** Show this help message
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-40s\033[0m %s\n", $$1, $$2}'


info: ## ** Show Project Information
	python ./bin/s00_show_project_info.py


venv-create: ## ** Create Virtual Environment
	python ./bin/s01_1_venv_create.py


venv-remove: ## ** Remove Virtual Environment
	python ./bin/s01_2_venv_remove.py


poetry-add-source: ## Add AWS CodeArtifact as secondary source in poetry
	python ./bin/s02_0_configure_poetry.py


install: ## ** Install main dependencies and Package itself
	python ./bin/s02_1_install.py


install-dev: ## Install Development Dependencies
	python ./bin/s02_2_install_dev.py


install-test: ## Install Test Dependencies
	python ./bin/s02_3_install_test.py


install-doc: ## Install Document Dependencies
	python ./bin/s02_4_install_doc.py


install-automation: ## Install Dependencies for Automation Script
	python ./bin/s02_5_install_automation.py


install-all: ## Install All Dependencies
	python ./bin/s02_6_install_all.py


poetry-export: ## Export requirements-*.txt from poetry.lock file
	python ./bin/s02_7_poetry_export.py


poetry-lock: ## Resolve dependencies using poetry, update poetry.lock file
	python ./bin/s02_8_poetry_lock.py


test: install install-test test-only ## ** Run test


test-only: ## Run test without checking test dependencies
	./.venv/bin/python ./bin/s03_1_run_unit_test.py


cov: install install-test cov-only ## ** Run code coverage test


cov-only: ## Run code coverage test without checking test dependencies
	./.venv/bin/python ./bin/s03_2_run_cov_test.py


int: install install-test int-only ## ** Run integration test


int-only: ## Run integration test without checking test dependencies
	./.venv/bin/python ./bin/s03_3_run_int_test.py


build-doc: install install-doc ## Build documentation website locally
	./.venv/bin/python ./bin/s04_1_build_doc.py


view-doc: ## View documentation website locally
	./.venv/bin/python ./bin/s04_2_view_doc.py


publish: ## Publish Python library to AWS CodeArtifact
	./.venv/bin/python ./bin/s05_1_publish.py