import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

sys.path.insert(0, "/opt/airflow")

from pipelines.processing import clean_sensor_data, normalize_features, join_with_image_metadata

RAW_SENSOR_CSV  = "/opt/airflow/data/raw/sensor/sensor_data.csv"
RAW_IMAGE_CSV   = "/opt/airflow/data/raw/image_metadata/image_metadata.csv"
PROCESSED_DIR   = "/opt/airflow/data/processed"


def _clean(**context):
    path = clean_sensor_data(RAW_SENSOR_CSV, PROCESSED_DIR)
    context["ti"].xcom_push(key="clean_path", value=path)


def _normalize(**context):
    clean_path = context["ti"].xcom_pull(key="clean_path", task_ids="clean")
    path = normalize_features(clean_path, PROCESSED_DIR)
    context["ti"].xcom_push(key="normalized_path", value=path)


def _join(**context):
    normalized_path = context["ti"].xcom_pull(key="normalized_path", task_ids="normalize")
    path = join_with_image_metadata(normalized_path, RAW_IMAGE_CSV, PROCESSED_DIR)
    context["ti"].xcom_push(key="processed_path", value=path)


with DAG(
    dag_id="processing_dag",
    description="Clean, normalize, and join sensor + image data",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["processing", "ml-sensor-pipeline"],
) as dag:

    clean_task = PythonOperator(task_id="clean",     python_callable=_clean)
    norm_task  = PythonOperator(task_id="normalize", python_callable=_normalize)
    join_task  = PythonOperator(task_id="join",      python_callable=_join)

    trigger_curation = TriggerDagRunOperator(
        task_id="trigger_curation_dag",
        trigger_dag_id="curation_dag",
    )

    clean_task >> norm_task >> join_task >> trigger_curation
