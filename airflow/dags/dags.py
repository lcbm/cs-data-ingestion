import datetime

import utils
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from airflow import DAG

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "retries": 0,
    "retry_delay": datetime.timedelta(minutes=1),
    "schedule_interval": "@daily",
}

with DAG(dag_id="load_rehabilitation_data", default_args=default_args) as dag:
    Task_I = PythonOperator(
        task_id="setup_connection", python_callable=utils.setup_connection
    )

    Task_II = PostgresOperator(
        task_id="database_setup",
        postgres_conn_id="postgres_custom",
        database="airflow",
        sql="""
        CREATE SCHEMA IF NOT EXISTS airflow;
        """,
    )

    Task_III = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="postgres_custom",
        database="airflow",
        sql="""
        CREATE TABLE IF NOT EXISTS airflow.sessions (
            patient_id      INT               NOT NULL,
            environment_id  INT               NOT NULL,
            activity_id     INT               NOT NULL,
            session         INT               NOT NULL,
            frame           INT               NOT NULL,
            x               DOUBLE PRECISION  NOT NULL,
            y               DOUBLE PRECISION  NOT NULL,
            z               DOUBLE PRECISION  NOT NULL,
            timestamp       TIMESTAMP         NOT NULL,
            CONSTRAINT sessions_pk
                PRIMARY KEY (patient_id, session, frame)
        );
        """,
    )

    Task_IV = PythonOperator(
        task_id="copy_csv_to_postgres", python_callable=utils.copy_csv_to_postgres
    )


Task_I >> Task_II >> Task_III >> Task_IV
