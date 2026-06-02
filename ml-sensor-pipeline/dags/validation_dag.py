import os
import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator, ShortCircuitOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

sys.path.insert(0, "/opt/airflow")

from pipelines.validation import (
    check_schema,
    check_nulls,
    check_sensor_ranges,
    check_image_ranges,
    check_duplicates,
    calculate_overall_score,
    log_quality_to_postgres,
    passes_quality_gate,
    SENSOR_REQUIRED_COLUMNS,
    IMAGE_REQUIRED_COLUMNS,
)

# ── File paths ────────────────────────────────────────────────────────────────
SENSOR_CSV  = "/opt/airflow/data/raw/sensor/sensor_data.csv"
IMAGE_CSV   = "/opt/airflow/data/raw/image_metadata/image_metadata.csv"

# ── Postgres connection params ────────────────────────────────────────────────
# Read from environment variables set in docker-compose.yml.
# In production you would use Airflow Connections (stored encrypted in the DB)
# and access them via PostgresHook — but env vars are fine for this project.
def _get_conn_params() -> dict:
    return {
        "host":     os.environ.get("ML_PIPELINE_DB_HOST", "postgres"),
        "port":     int(os.environ.get("ML_PIPELINE_DB_PORT", 5432)),
        "dbname":   os.environ.get("ML_PIPELINE_DB_NAME", "ml_pipeline"),
        "user":     os.environ.get("ML_PIPELINE_DB_USER", "airflow"),
        "password": os.environ.get("ML_PIPELINE_DB_PASSWORD", "airflow"),
    }


# ── Task wrapper functions ────────────────────────────────────────────────────
# Pattern is identical to ingestion_dag.py:
#   Pull from XCom → call pipeline function → push result to XCom

def _check_sensor_schema(**context):
    result = check_schema(SENSOR_CSV, SENSOR_REQUIRED_COLUMNS)
    print(f"Schema check: {result}")
    context["ti"].xcom_push(key="schema_check", value=result)


def _check_nulls(**context):
    result = check_nulls(SENSOR_CSV)
    print(f"Null check: score={result['score']}, passed={result['passed']}")
    context["ti"].xcom_push(key="null_check", value=result)


def _check_sensor_ranges(**context):
    result = check_sensor_ranges(SENSOR_CSV)
    print(f"Sensor range check: score={result['score']}, passed={result['passed']}")
    context["ti"].xcom_push(key="range_check_sensor", value=result)


def _check_duplicates(**context):
    result = check_duplicates(SENSOR_CSV)
    print(f"Duplicate check: score={result['score']}, passed={result['passed']}")
    context["ti"].xcom_push(key="duplicate_check", value=result)


def _check_image_schema(**context):
    result = check_schema(IMAGE_CSV, IMAGE_REQUIRED_COLUMNS)
    print(f"Image schema check: {result}")
    context["ti"].xcom_push(key="image_schema_check", value=result)


def _check_image_ranges(**context):
    result = check_image_ranges(IMAGE_CSV)
    print(f"Image range check: score={result['score']}, passed={result['passed']}")
    context["ti"].xcom_push(key="range_check_image", value=result)


def _calculate_overall_score(**context):
    ti = context["ti"]

    # Pull every check result from XCom — one pull per upstream task
    check_results = [
        ti.xcom_pull(key="schema_check",       task_ids="validate_sensor_schema"),
        ti.xcom_pull(key="null_check",          task_ids="validate_nulls"),
        ti.xcom_pull(key="range_check_sensor",  task_ids="validate_sensor_ranges"),
        ti.xcom_pull(key="duplicate_check",     task_ids="validate_duplicates"),
        ti.xcom_pull(key="image_schema_check",  task_ids="validate_image_schema"),
        ti.xcom_pull(key="range_check_image",   task_ids="validate_image_ranges"),
    ]

    overall_score = calculate_overall_score(check_results)
    print(f"Overall quality score: {overall_score}")

    # Push both so downstream tasks (log + gate) can pull them
    ti.xcom_push(key="check_results",   value=check_results)
    ti.xcom_push(key="overall_score",   value=overall_score)


def _log_to_postgres(**context):
    ti = context["ti"]
    check_results = ti.xcom_pull(key="check_results",  task_ids="calculate_overall_score")
    overall_score = ti.xcom_pull(key="overall_score",  task_ids="calculate_overall_score")

    log_quality_to_postgres(
        conn_params=_get_conn_params(),
        run_id=context["run_id"],       # Airflow injects run_id into context automatically
        dag_id="validation_dag",
        check_results=check_results,
        overall_score=overall_score,
    )


def _quality_gate(**context):
    overall_score = context["ti"].xcom_pull(
        key="overall_score",
        task_ids="calculate_overall_score"
    )
    # This return value is what ShortCircuitOperator uses to decide:
    # True  → run trigger_processing_dag
    # False → skip trigger_processing_dag, mark run as complete
    return passes_quality_gate(overall_score, threshold=0.95)


# ── DAG definition ────────────────────────────────────────────────────────────

with DAG(
    dag_id="validation_dag",
    description="Run quality checks on raw sensor and image data",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["validation", "ml-sensor-pipeline"],
) as dag:

    # ── Sensor checks ─────────────────────────────────────────────────────────
    sensor_schema_task = PythonOperator(
        task_id="validate_sensor_schema",
        python_callable=_check_sensor_schema,
    )

    null_check_task = PythonOperator(
        task_id="validate_nulls",
        python_callable=_check_nulls,
    )

    sensor_range_task = PythonOperator(
        task_id="validate_sensor_ranges",
        python_callable=_check_sensor_ranges,
    )

    duplicate_task = PythonOperator(
        task_id="validate_duplicates",
        python_callable=_check_duplicates,
    )

    # ── Image checks ──────────────────────────────────────────────────────────
    image_schema_task = PythonOperator(
        task_id="validate_image_schema",
        python_callable=_check_image_schema,
    )

    image_range_task = PythonOperator(
        task_id="validate_image_ranges",
        python_callable=_check_image_ranges,
    )

    # ── Aggregate + log + gate ────────────────────────────────────────────────
    score_task = PythonOperator(
        task_id="calculate_overall_score",
        python_callable=_calculate_overall_score,
    )

    log_task = PythonOperator(
        task_id="log_to_postgres",
        python_callable=_log_to_postgres,
    )

    # ShortCircuitOperator: calls _quality_gate, which returns True or False.
    # If False → all tasks after this one are SKIPPED automatically by Airflow.
    gate_task = ShortCircuitOperator(
        task_id="quality_gate",
        python_callable=_quality_gate,
    )

    # Fires the processing DAG — only reached if quality_gate returned True
    trigger_processing = TriggerDagRunOperator(
        task_id="trigger_processing_dag",
        trigger_dag_id="processing_dag",
    )

    # ── Task ordering ─────────────────────────────────────────────────────────
    sensor_schema_task >> null_check_task >> sensor_range_task >> duplicate_task
    duplicate_task >> image_schema_task >> image_range_task
    image_range_task >> score_task >> log_task >> gate_task >> trigger_processing
