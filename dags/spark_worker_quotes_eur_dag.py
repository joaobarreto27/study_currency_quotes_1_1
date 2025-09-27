"""Módulo de execução de dags no Airflow da extração de cotações de EUR."""

import os
from datetime import datetime

from airflow import DAG  # type:ignore
from airflow.operator.bash import BashOperator  # type: ignore

BASE_DIR = os.path.dirname(__file__)

with DAG(
    dag_id="spark_worker_quotes_eur_dag",
    start_date=datetime(2025, 9, 27),
    schedule="*/3 * * * *",
    catchup=False,
    tags=["quotes_eur"],
) as dag:

    run_worker = BashOperator(
        task_id="run_worker_quotes_eur_dag",
        bash_command=(
            f"export PYTHONPATH={BASE_DIR}/../src && "
            "python -m worker.quotes_eur.etl_quotes_eur_daily_event"
        ),
    )
