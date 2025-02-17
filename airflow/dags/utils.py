import csv

from airflow.hooks.base_hook import BaseHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import Connection

from airflow import settings

SESSIONS_TABLE_COLUMN_TYPE_MAP = {
    0: int,
    1: int,
    2: int,
    3: int,
    4: int,
    5: float,
    6: float,
    7: float,
    8: str,
}


def setup_connection():
    session = settings.Session()
    try:
        BaseHook.get_connection("postgres_custom")
    except Exception:
        connection = Connection(
            conn_id="postgres_custom",
            conn_type="Postgres",
            host="postgresql",
            login="airflow",
            password="airflow",
            port=5432,
        )
        session.add(connection)
        session.commit()


def copy_csv_to_postgres():
    query = """
    INSERT INTO airflow.sessions (
        patient_id,
        environment_id,
        activity_id,
        session,
        frame,
        x,
        y,
        z,
        timestamp
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    with open("/opt/bitnami/airflow/csv/report.csv", "r") as file:
        reader = csv.reader(file, delimiter=",")
        next(reader)
        for line in reader:
            line_casted = [
                SESSIONS_TABLE_COLUMN_TYPE_MAP[index](element)
                for index, element in enumerate(line)
            ]
            hook = PostgresHook(
                postgres_conn_id="postgres_custom",
                database="airflow",
            )
            hook.run(query, parameters=tuple(line_casted))
