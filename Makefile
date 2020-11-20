AIRFLOW := airflow
VENV := .venv
BIN := $(VENV)/bin
PRE_COMMIT := $(BIN)/pre-commit

bootstrap:
	@poetry install
	@$(PRE_COMMIT) install

docker-pull:
	@docker pull bitnami/redis:6.0
	@docker pull bitnami/postgresql:13.1.0
	@docker pull bitnami/airflow-scheduler:1.10.13
	@docker pull bitnami/airflow-worker:1.10.13
	@docker pull bitnami/airflow:1.10.13

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
