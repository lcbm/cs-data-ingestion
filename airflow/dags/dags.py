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
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=1),
}

dag_setup = DAG(
    dag_id="setup_application",
    default_args=default_args,
    schedule_interval="@once",
)
dag_data_collection = DAG(
    dag_id="dag_collection",
    default_args=default_args,
    schedule_interval="@daily",
)


Task_I = PythonOperator(
    dag=dag_setup, task_id="setup_connection", python_callable=utils.setup_connection
)
Task_II = PostgresOperator(
    dag=dag_setup,
    task_id="setup_database",
    postgres_conn_id="postgres_custom",
    database="airflow",
    sql="""
    CREATE SCHEMA IF NOT EXISTS airflow;
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

Task_III = PythonOperator(
    dag=dag_data_collection,
    task_id="copy_csv_to_postgres",
    python_callable=utils.copy_csv_to_postgres,
)


Task_I >> Task_II
Task_III
