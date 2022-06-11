PYTHON ?= python
ROOT = $(dir $(realpath $(firstword $(MAKEFILE_LIST))))


clean:
	find . -name '__pycache__' | xargs rm -rf
	rm -rf htmlcov .coverage .pytest_cache build dist


format:
	$(PYTHON) -m black src tests
	$(PYTHON) -m isort src tests


install-dev:
	$(PYTHON) -m pip install -e .[dev]


lint:
	$(PYTHON) -m pylint src tests


test:
	$(PYTHON) -m pytest
