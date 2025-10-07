"""Módulo de execução de dags no Airflow para extração extração da cotação de GBP."""

import os
from datetime import datetime

from airflow import DAG  # type:ignore
from airflow.operators.bash import BashOperator  # type:ignore

BASE_DIR = os.path.dirname(__file__)

with DAG(
    dag_id="spark_worker_quotes_gbp_dag",
    start_date=datetime(2025, 9, 29),
    schedule="*/10 * * * *",
    catchup=False,
    tags=["quotes_gbp"],
) as dag:

    run_worker = BashOperator(
        task_id="run_worker",
        bash_command=(
            f" export PYTHONPATH={BASE_DIR}/../src && "
            "python -m worker.quotes_gbp.etl_quotes_gbp_daily_event"
        ),
    )
