"""Módulo de execução de dags no Airflow da extração da cotação de BTC."""

import os
from datetime import datetime

from airflow import DAG  # type:ignore
from airflow.operators.bash import BashOperator  # type:ignore

BASE_DIR = os.path.dirname(__file__)
WORKER_PATH = os.path.join(
    BASE_DIR,
    """../etl/study_currency_quotes/src/worker/quotes_usd/
    etl_quotes_usd_daily_event.py""",
)
print(BASE_DIR)
print(WORKER_PATH)


with DAG(
    dag_id="spark_worker_quotes_usd_dag",
    start_date=datetime(2025, 8, 30),
    schedule="*/3 * * * *",
    catchup=False,
    tags=["quotes_usd"],
) as dag:

    run_worker = BashOperator(
        task_id="run_worker",
        bash_command="""
        python -m
        dags.etl.study_currency_quotes.src.worker.quotes_usd.etl_quotes_usd_daily_event""",
    )
