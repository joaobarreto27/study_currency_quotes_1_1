"""Módulo de execução de dags no Airflow para extração de cotações de CAD."""

import os
from datetime import datetime

from airflow import DAG  # type:ignore
from airflow.operators.bash import BashOperator  # type:ignore

BASE_DIR = os.path.dirname(__file__)

with DAG(
    dag_id="spark_worker_quotes_cad_dag",
    start_date=datetime(2025, 9, 27),
    schedule="22 21 * * 1-5",
    catchup=False,
    tags=["quotes_cad"],
) as dag:

    run_worker = BashOperator(
        task_id="run_worker_quotes_cad_dag",
        bash_command=(
            f"export PYTHONPATH={BASE_DIR}/../src && "
            "python -m worker.quotes_cad.etl_quotes_cad_daily_event"
        ),
    )
