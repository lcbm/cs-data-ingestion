VENV := .venv
BIN := $(VENV)/bin
PRE_COMMIT := $(BIN)/pre-commit

bootstrap:
	@poetry install
	@$(PRE_COMMIT) install

clean:
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +

clean-all: clean
	@rm -r $(VENV)

format: clean
	@poetry run black .

lint:
	@poetry run flake8 .
