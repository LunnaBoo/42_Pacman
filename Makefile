PYTHON = python3
VENV = .venv
VENV_PYTHON = $(VENV)/bin/python
PIP = $(VENV_PYTHON) -m pip
MAIN = pac-man.py
CONFIG = config.json
SRC_DIR = src
RM = rm -rf

all: run

$(VENV):
	$(PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m ensurepip --upgrade

install: $(VENV)
	$(PIP) install -e '.[dev]'

run:
	PYTHONPATH=$(SRC_DIR) $(VENV_PYTHON) $(MAIN) $(CONFIG)

debug:
	PYTHONPATH=$(SRC_DIR) $(VENV_PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	$(RM) __pycache__ .mypy_cache .pytest_cache build dist *.egg-info
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
	find . -name '*.py[co]' -delete

fclean: clean
	$(RM) $(VENV)

re: fclean all

lint:
	$(VENV_PYTHON) -m flake8 .
	$(VENV_PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(VENV_PYTHON) -m flake8 .
	$(VENV_PYTHON) -m mypy . --strict

test:
	$(VENV_PYTHON) -m pytest
