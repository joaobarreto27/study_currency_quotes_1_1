"""Módulo execução de dags no Airflow para extração da cotação de BTCBR."""

import os
from datetime import datetime

from airflow import DAG  # type:ignore
from airflow.operators.bash import BashOperator  # type:ignore

BASE_DIR = os.path.dirname(__file__)

with DAG(
    dag_id="spark_worker_quotes_btcbr_dag",
    start_date=datetime(2025, 9, 30),
    schedule="*/6 * * * *",
    catchup=False,
    tags=["quotes_btcbr"],
) as dag:

    run_worker = BashOperator(
        task_id="run_worker",
        bash_command=(
            f"export PYTHONPATH={BASE_DIR}/../src && "
            "python -m worker.quotes_btcbr.etl_quotes_btcbr_daily_event"
        ),
    )
