"""Módulo de execução de dags no Airflow para extração de cotação de JPY."""

import os
from datetime import datetime

from airflow import DAG  # type:ignore
from airflow.operators.bash import BashOperator  # type:ignore

BASE_DIR = os.path.dirname(__file__)

with DAG(
    dag_id="spark_worker_quotes_jpy_dag",
    start_date=datetime(2025, 9, 30),
    schedule="*/10 * * * *",
    catchup=False,
    tags=["quotes_jpy"],
) as dag:

    run_worker = BashOperator(
        task_id="run_worker",
        bash_command=(
            f"export PYTHONPATH={BASE_DIR}/../src &&"
            "python -m worker.quotes_jpy.etl_quotes_jpy_daily_event"
        ),
    )
