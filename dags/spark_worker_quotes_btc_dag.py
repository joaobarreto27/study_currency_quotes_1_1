"""Este direciona para a criação da Dag para o processo de quotes btc."""

from datetime import datetime
from pathlib import Path

from airflow import DAG  # type:ignore
from airflow.operators.bash import BashOperator  # type:ignore

WORKER_PATH = Path(
    "/c/projects/automated_projects/study_currency_quotes/"
    "src/worker/quotes_btc/etl_quotes_btc_daily_event.py"
)

with DAG(
    dag_id="spark_worker_quotes_btc_dag",
    start_date=datetime(2025, 8, 30),
    schedule="* * * * *",
    catchup=False,
    tags=["quotes_btc"],
) as dag:

    run_worker = BashOperator(
        task_id="run_worker", bash_command=f"python {WORKER_PATH}"
    )
