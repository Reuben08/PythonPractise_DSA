import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

# Tell Python where to find our pipelines/ folder inside the Airflow container.
# Without this, 'from pipelines.ingestion import ...' would fail with ModuleNotFoundError.
sys.path.insert(0, "/opt/airflow")

from pipelines.ingestion import download_uci_har, parse_uci_har, generate_image_metadata

# ── File paths inside the container ──────────────────────────────────────────
# These match the volume mount in docker-compose.yml:
#   ./data → /opt/airflow/data
RAW_SENSOR_DIR = "/opt/airflow/data/raw/sensor"
RAW_IMAGE_DIR  = "/opt/airflow/data/raw/image_metadata"


# ── Task wrapper functions ────────────────────────────────────────────────────
# These are thin wrappers. They:
#   1. Pull any inputs from XCom (data passed from the previous task)
#   2. Call the real pipeline function
#   3. Push the result to XCom (so the next task can use it)
#
# The **context argument is injected by Airflow automatically.
# context["ti"] is the TaskInstance — it gives us access to XCom.

def _download(**context):
    extract_path = download_uci_har(output_dir=RAW_SENSOR_DIR)

    # Push the extracted folder path so the parse task knows where to look
    context["ti"].xcom_push(key="extract_path", value=extract_path)


def _parse(**context):
    # Pull the extract_path that _download pushed
    # task_ids tells XCom which task to pull from
    extract_path = context["ti"].xcom_pull(
        key="extract_path",
        task_ids="download_uci_har"
    )
    sensor_csv_path = parse_uci_har(raw_dir=extract_path, output_dir=RAW_SENSOR_DIR)

    # Push the CSV path so the image metadata task knows where the sensor data is
    context["ti"].xcom_push(key="sensor_csv_path", value=sensor_csv_path)


def _generate_image_metadata(**context):
    # Pull the sensor CSV path that _parse pushed
    sensor_csv_path = context["ti"].xcom_pull(
        key="sensor_csv_path",
        task_ids="parse_sensor_data"
    )
    generate_image_metadata(
        sensor_csv_path=sensor_csv_path,
        output_dir=RAW_IMAGE_DIR
    )


# ── DAG definition ────────────────────────────────────────────────────────────

with DAG(
    dag_id="ingestion_dag",

    description="Download UCI HAR dataset and generate synthetic image metadata",

    # The date from which Airflow considers this DAG active.
    # Since catchup=False, it won't try to backfill missed runs before today.
    start_date=datetime(2024, 1, 1),

    # None = manual trigger only (no automatic schedule).
    # Later we could set "@daily" to re-ingest on a schedule.
    schedule_interval=None,

    # Don't create historical runs for dates between start_date and today
    catchup=False,

    tags=["ingestion", "ml-sensor-pipeline"],
) as dag:

    # ── Task 1: Download ──────────────────────────────────────────────────────
    download_task = PythonOperator(
        task_id="download_uci_har",
        python_callable=_download,
    )

    # ── Task 2: Parse ─────────────────────────────────────────────────────────
    parse_task = PythonOperator(
        task_id="parse_sensor_data",
        python_callable=_parse,
    )

    # ── Task 3: Generate image metadata ──────────────────────────────────────
    image_task = PythonOperator(
        task_id="generate_image_metadata",
        python_callable=_generate_image_metadata,
    )

    # ── Task ordering ─────────────────────────────────────────────────────────
    # >> means "the right task depends on the left task completing successfully"
    # Airflow won't start parse_task until download_task succeeds.
    # Airflow won't start image_task until parse_task succeeds.
    download_task >> parse_task >> image_task
