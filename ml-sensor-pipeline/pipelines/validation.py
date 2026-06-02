import json
import psycopg2
import pandas as pd


# ── Expected columns ──────────────────────────────────────────────────────────
# These are the minimum columns we require in each file.
# We don't enumerate all 561 UCI HAR feature columns — just the key metadata ones.

SENSOR_REQUIRED_COLUMNS = {
    "subject_id", "activity_id", "activity_label", "split"
}

IMAGE_REQUIRED_COLUMNS = {
    "image_id", "subject_id", "activity_label", "split",
    "resolution", "file_size_kb", "quality_score",
    "is_blurry", "brightness", "capture_timestamp"
}


# ── Check 1: Schema ───────────────────────────────────────────────────────────

def check_schema(file_path: str, required_columns: set) -> dict:
    """
    Verify that all required columns exist in the file.

    We only read the header row (nrows=0) — no need to load the full dataset
    just to check column names.

    Score: 1.0 if all columns present, 0.0 if any are missing.
    This is binary — a missing column is a hard failure.
    """
    df = pd.read_csv(file_path, nrows=0)
    actual_columns = set(df.columns.tolist())
    missing = list(required_columns - actual_columns)
    passed = len(missing) == 0

    return {
        "check_name": "schema_check",
        "score": 1.0 if passed else 0.0,
        "passed": passed,
        "details": {
            "missing_columns": missing,
            "required_columns": list(required_columns),
        }
    }


# ── Check 2: Nulls ────────────────────────────────────────────────────────────

def check_nulls(file_path: str) -> dict:
    """
    Calculate what fraction of cells are non-null (completeness score).

    Score: 1 - (null_count / total_cells)
    e.g. 5 nulls in a 10,000-cell dataset → score = 0.9995
    Threshold: score must be >= 0.99 to pass.
    """
    df = pd.read_csv(file_path)
    total_cells = df.shape[0] * df.shape[1]
    null_count = int(df.isna().sum().sum())
    score = round(1 - (null_count / total_cells), 4)

    # Find which columns have nulls and how many — useful for debugging
    null_by_column = df.isna().sum()
    null_columns = {
        col: int(count)
        for col, count in null_by_column.items()
        if count > 0
    }

    return {
        "check_name": "null_check",
        "score": score,
        "passed": score >= 0.99,
        "details": {
            "null_count": null_count,
            "total_cells": total_cells,
            "null_by_column": null_columns,
        }
    }


# ── Check 3: Ranges ───────────────────────────────────────────────────────────

def check_sensor_ranges(file_path: str) -> dict:
    """
    Validate that sensor values are within expected bounds.

    UCI HAR features are pre-normalised to [-1, 1].
    We also check that activity_id is 1-6 and subject_id is 1-30.

    We sample the first 20 feature columns for performance —
    checking all 561 is expensive and redundant for a quality gate.
    """
    df = pd.read_csv(file_path)
    violations = {}

    # Activity codes must be 1-6
    bad_activity = int(((df["activity_id"] < 1) | (df["activity_id"] > 6)).sum())
    if bad_activity > 0:
        violations["activity_id"] = bad_activity

    # Subject IDs must be 1-30
    bad_subject = int(((df["subject_id"] < 1) | (df["subject_id"] > 30)).sum())
    if bad_subject > 0:
        violations["subject_id"] = bad_subject

    # Sample first 20 feature columns — all should be in [-1, 1]
    feature_cols = [
        c for c in df.columns
        if c not in {"subject_id", "activity_id", "activity_label", "split"}
    ][:20]

    for col in feature_cols:
        bad = int(((df[col] < -1.0) | (df[col] > 1.0)).sum())
        if bad > 0:
            violations[col] = bad

    passed = len(violations) == 0
    # Score degrades proportionally with number of violating columns
    score = round(1 - (len(violations) / (len(feature_cols) + 2)), 4)

    return {
        "check_name": "range_check_sensor",
        "score": max(score, 0.0),
        "passed": passed,
        "details": {"violations": violations}
    }


def check_image_ranges(file_path: str) -> dict:
    """
    Validate that image metadata values are within expected bounds.

    quality_score: must be 0.0-1.0
    file_size_kb:  must be > 0
    brightness:    must be 0-255
    is_blurry rate: must be < 20% (too many blurry images signals a capture problem)
    """
    df = pd.read_csv(file_path)
    violations = {}

    bad_quality = int(((df["quality_score"] < 0) | (df["quality_score"] > 1)).sum())
    if bad_quality > 0:
        violations["quality_score_out_of_range"] = bad_quality

    bad_size = int((df["file_size_kb"] <= 0).sum())
    if bad_size > 0:
        violations["file_size_kb_zero_or_negative"] = bad_size

    bad_brightness = int(((df["brightness"] < 0) | (df["brightness"] > 255)).sum())
    if bad_brightness > 0:
        violations["brightness_out_of_range"] = bad_brightness

    blurry_rate = round(float(df["is_blurry"].mean()), 4)
    if blurry_rate > 0.20:
        violations["blurry_rate_too_high"] = blurry_rate

    passed = len(violations) == 0
    score = round(1 - (len(violations) / 4), 4)  # 4 possible violation types

    return {
        "check_name": "range_check_image",
        "score": max(score, 0.0),
        "passed": passed,
        "details": {"violations": violations, "blurry_rate": blurry_rate}
    }


# ── Check 4: Duplicates ───────────────────────────────────────────────────────

def check_duplicates(file_path: str) -> dict:
    """
    Check what fraction of rows are unique.

    Score: 1 - (duplicate_count / total_rows)
    A fully unique dataset scores 1.0.
    """
    df = pd.read_csv(file_path)
    total_rows = len(df)
    duplicate_count = int(df.duplicated().sum())
    score = round(1 - (duplicate_count / total_rows), 4)

    return {
        "check_name": "duplicate_check",
        "score": score,
        "passed": duplicate_count == 0,
        "details": {
            "duplicate_count": duplicate_count,
            "total_rows": total_rows,
            "duplicate_rate": round(duplicate_count / total_rows, 4),
        }
    }


# ── Aggregate ─────────────────────────────────────────────────────────────────

def calculate_overall_score(check_results: list) -> float:
    """
    Average all individual check scores into one overall quality score.

    Simple mean — every check has equal weight.
    In production you might weight schema_check more heavily (it's binary and critical).
    """
    scores = [r["score"] for r in check_results]
    return round(sum(scores) / len(scores), 4)


# ── Log to Postgres ───────────────────────────────────────────────────────────

def log_quality_to_postgres(
    conn_params: dict,
    run_id: str,
    dag_id: str,
    check_results: list,
    overall_score: float,
) -> None:
    """
    Write every check result and the pipeline run record to Postgres.

    Uses psycopg2 directly — no Airflow dependency so this stays testable.
    conn_params is passed in from the DAG wrapper (read from env vars there).
    """
    conn = psycopg2.connect(**conn_params)
    try:
        with conn.cursor() as cur:

            # One row per check in quality_metrics
            for result in check_results:
                cur.execute(
                    """
                    INSERT INTO quality_metrics
                        (run_id, dag_id, check_name, score, passed, details)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        run_id,
                        dag_id,
                        result["check_name"],
                        result["score"],
                        result["passed"],
                        json.dumps(result["details"]),
                    )
                )

            # One row in pipeline_runs for the overall validation run
            status = "success" if overall_score >= 0.95 else "failed_quality_gate"
            cur.execute(
                """
                INSERT INTO pipeline_runs
                    (dag_id, run_id, status, notes)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    dag_id,
                    run_id,
                    status,
                    f"Overall quality score: {overall_score}",
                )
            )

        conn.commit()
        print(f"Logged {len(check_results)} check results to Postgres.")
    finally:
        conn.close()


# ── Quality gate ──────────────────────────────────────────────────────────────

def passes_quality_gate(overall_score: float, threshold: float = 0.95) -> bool:
    """
    The gate function called by ShortCircuitOperator in the DAG.

    Returns True  → pipeline continues to processing
    Returns False → all downstream tasks are skipped, pipeline halts here
    """
    print(f"Quality gate: score={overall_score}, threshold={threshold}")
    if overall_score >= threshold:
        print("PASSED — proceeding to processing DAG.")
        return True
    print(f"FAILED — score {overall_score} is below threshold {threshold}. Blocking pipeline.")
    return False
