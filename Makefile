.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -frv build/
	rm -frv dist/
	rm -frv .eggs/
	rm -frv *.egg-info
	rm -frv *.egg
	rm -frv *.pyc
	rm -frv *.pyo
	rm -frv ./**/__pycache__/
	rm -frv ./__pycache__/
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

prereq: ## install prereqs
	python -m pip install --upgrade pip
	pip install --upgrade coverage pytest pytest-cov twine setuptools wheel black

test: ## run tests quickly with the default Python
	pytest tests

coverage: ## check code coverage quickly with the default Python
	coverage run -m pytest tests
	coverage report
	coverage xml -o coverage.xml

push: ## push to remote
	black tempath
	black tests
	git add .
	git commit -m "$m"
	git push

release: test coverage push build ## package and upload a release
	twine upload dist/*

build: prereq clean ## builds source and wheel package
	python setup.py sdist bdist_wheel bdist_egg

install: clean ## install the package to the active Python's site-packages
	python setup.py install
