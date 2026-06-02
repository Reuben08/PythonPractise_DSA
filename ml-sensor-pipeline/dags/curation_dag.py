import os
import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.insert(0, "/opt/airflow")

from pipelines.curation import create_splits, generate_dataset_card, log_dataset_stats

PROCESSED_CSV = "/opt/airflow/data/processed/processed_data.csv"
CURATED_DIR   = "/opt/airflow/data/curated"


def _get_conn_params() -> dict:
    return {
        "host":     os.environ.get("ML_PIPELINE_DB_HOST", "postgres"),
        "port":     int(os.environ.get("ML_PIPELINE_DB_PORT", 5432)),
        "dbname":   os.environ.get("ML_PIPELINE_DB_NAME", "ml_pipeline"),
        "user":     os.environ.get("ML_PIPELINE_DB_USER", "airflow"),
        "password": os.environ.get("ML_PIPELINE_DB_PASSWORD", "airflow"),
    }


def _split(**context):
    split_paths = create_splits(PROCESSED_CSV, CURATED_DIR)
    context["ti"].xcom_push(key="split_paths", value=split_paths)


def _dataset_card(**context):
    split_paths = context["ti"].xcom_pull(key="split_paths", task_ids="split")
    card_path = generate_dataset_card(split_paths, CURATED_DIR)
    context["ti"].xcom_push(key="card_path", value=card_path)


def _log_stats(**context):
    split_paths = context["ti"].xcom_pull(key="split_paths", task_ids="split")
    log_dataset_stats(
        conn_params=_get_conn_params(),
        run_id=context["run_id"],
        split_paths=split_paths,
    )


with DAG(
    dag_id="curation_dag",
    description="Split processed data into train/val/test and generate dataset card",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["curation", "ml-sensor-pipeline"],
) as dag:

    split_task       = PythonOperator(task_id="split",        python_callable=_split)
    card_task        = PythonOperator(task_id="dataset_card", python_callable=_dataset_card)
    log_stats_task   = PythonOperator(task_id="log_stats",    python_callable=_log_stats)

    # card and log_stats both only need split_paths — they can run in parallel
    split_task >> [card_task, log_stats_task]
