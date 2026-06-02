# ML Sensor Pipeline — Technical Documentation

## Overview

A production-grade data pipeline that ingests multi-modal ML training data (sensor + image metadata), runs automated quality validation, processes and joins the modalities, and delivers clean train/val/test splits to ML researchers.

**Tech stack:** Python · Apache Airflow · PostgreSQL · Streamlit · Docker

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Docker Network                               │
│                                                                     │
│  ┌─────────────┐   ┌──────────────┐   ┌────────────────────────┐   │
│  │  postgres   │   │   airflow-   │   │   airflow-scheduler    │   │
│  │             │   │  webserver   │   │                        │   │
│  │ - airflow   │   │              │   │  - watches dags/       │   │
│  │   database  │   │  UI :8080    │   │  - executes tasks      │   │
│  │ - ml_pipeline│  └──────────────┘   └────────────────────────┘   │
│  │   database  │                                                    │
│  │  port 5432  │   ┌──────────────┐                               │
│  └─────────────┘   │  streamlit   │                               │
│                    │              │                               │
│                    │  UI :8501    │                               │
│                    └──────────────┘                               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
ml-sensor-pipeline/
├── dags/                        # Airflow DAG definitions (orchestration only)
│   ├── ingestion_dag.py
│   ├── validation_dag.py
│   ├── processing_dag.py
│   └── curation_dag.py
│
├── pipelines/                   # Business logic (no Airflow imports)
│   ├── ingestion.py
│   ├── validation.py
│   ├── processing.py
│   └── curation.py
│
├── data/
│   ├── raw/
│   │   ├── sensor/              # UCI HAR CSV lands here
│   │   └── image_metadata/      # Synthetic image metadata CSV
│   ├── processed/               # Cleaned, normalized, joined data
│   └── curated/                 # train.csv, val.csv, test.csv, dataset_card.json
│
├── dashboard/
│   ├── app.py                   # Home page
│   ├── utils.py                 # DB connection helper
│   └── pages/
│       ├── pipeline_health.py   # DAG run history
│       ├── data_quality.py      # Quality scores and trends
│       └── dataset_stats.py     # Dataset class distribution
│
├── docker-compose.yml
├── Dockerfile.streamlit
├── init_db.sql                  # Creates ml_pipeline DB and tables
├── requirements.txt             # Pipeline dependencies
└── requirements.streamlit.txt  # Dashboard dependencies
```

---

## Modular Design: `pipelines/` vs `dags/`

The most important architectural decision in this project.

| Layer | Folder | Contains | Airflow imports? |
|---|---|---|---|
| Logic | `pipelines/` | Data processing functions | No |
| Orchestration | `dags/` | Task wiring, scheduling, XCom | Yes |

### Why separate them?

**`pipelines/` functions are plain Python.** They take file paths as inputs and return file paths as outputs. No Airflow anywhere. This means:
- You can run them in a notebook or terminal without Airflow
- You can write `pytest` tests against them directly
- They can be reused by any other DAG or script

**`dags/` files are thin wrappers.** Each DAG file imports functions from `pipelines/` and wraps them in Airflow `PythonOperator` tasks. The DAG's only job is to define *when* and *in what order* the pipeline functions run.

### Example

```python
# pipelines/validation.py — pure Python, no Airflow
def check_nulls(file_path: str) -> dict:
    df = pd.read_csv(file_path)
    null_count = int(df.isna().sum().sum())
    score = round(1 - (null_count / (df.shape[0] * df.shape[1])), 4)
    return {"check_name": "null_check", "score": score, "passed": score >= 0.99}
```

```python
# dags/validation_dag.py — Airflow wrapper
def _check_nulls(**context):
    result = check_nulls(SENSOR_CSV)            # calls the pipeline function
    context["ti"].xcom_push(key="null_check", value=result)  # passes result forward

null_check_task = PythonOperator(
    task_id="validate_nulls",
    python_callable=_check_nulls,
)
```

---

## XCom (Cross-Communication)

XCom is how Airflow tasks pass data to each other within a DAG run.

Every task runs in isolation — it has no direct access to what a previous task computed. XCom is the bridge.

### How it works

```python
# Task A: push a value
context["ti"].xcom_push(key="sensor_csv_path", value="/opt/airflow/data/raw/sensor/sensor_data.csv")

# Task B: pull that value
sensor_csv_path = context["ti"].xcom_pull(key="sensor_csv_path", task_ids="parse_sensor_data")
```

- `context["ti"]` is the **TaskInstance** — Airflow's object representing this specific run of this specific task
- `task_ids` tells XCom which task's stored values to read from
- XCom values are stored in Airflow's Postgres database and visible in the Airflow UI under each task's "XCom" tab

### XCom flow in this pipeline

```
ingestion_dag
─────────────────────────────────────────────────────
download_uci_har  →  pushes: extract_path
parse_sensor_data →  pulls: extract_path
                  →  pushes: sensor_csv_path
generate_images   →  pulls: sensor_csv_path


validation_dag
─────────────────────────────────────────────────────
validate_sensor_schema  →  pushes: schema_check (dict)
validate_nulls          →  pushes: null_check (dict)
validate_sensor_ranges  →  pushes: range_check_sensor (dict)
validate_duplicates     →  pushes: duplicate_check (dict)
validate_image_schema   →  pushes: image_schema_check (dict)
validate_image_ranges   →  pushes: range_check_image (dict)
calculate_overall_score →  pulls: all 6 dicts
                        →  pushes: check_results (list), overall_score (float)
log_to_postgres         →  pulls: check_results, overall_score
quality_gate            →  pulls: overall_score → returns True/False


processing_dag
─────────────────────────────────────────────────────
clean      →  pushes: clean_path
normalize  →  pulls: clean_path → pushes: normalized_path
join       →  pulls: normalized_path → pushes: processed_path


curation_dag
─────────────────────────────────────────────────────
split         →  pushes: split_paths (dict of train/val/test paths)
dataset_card  →  pulls: split_paths
log_stats     →  pulls: split_paths
```

### What XCom is NOT for

XCom is designed for small values — file paths, scores, status strings. Never push a full DataFrame through XCom. If tasks need to share large data, write it to a file and pass the path.

---

## The Four DAGs

### 1. `ingestion_dag`
**Trigger:** Manual  
**Purpose:** Fetch raw data and land it in the raw zone

| Task | What it does |
|---|---|
| `download_uci_har` | Downloads UCI HAR zip, extracts it to `data/raw/sensor/` |
| `parse_sensor_data` | Parses 6 text files into one `sensor_data.csv` (10,299 rows × 563 cols) |
| `generate_image_metadata` | Creates synthetic `image_metadata.csv` aligned row-by-row to sensor data |

---

### 2. `validation_dag`
**Trigger:** Manual (after ingestion)  
**Purpose:** Quality gate — block bad data from reaching processing

| Task | What it does |
|---|---|
| `validate_sensor_schema` | Checks required columns exist |
| `validate_nulls` | Completeness score: `1 - (null_count / total_cells)` |
| `validate_sensor_ranges` | Sensor features must be in `[-1, 1]`, activity_id in `1-6` |
| `validate_duplicates` | Duplicate row rate |
| `validate_image_schema` | Required image columns exist |
| `validate_image_ranges` | quality_score in `[0,1]`, brightness in `[0,255]`, blurry rate < 20% |
| `calculate_overall_score` | Average of all 6 check scores |
| `log_to_postgres` | Writes results to `quality_metrics` and `pipeline_runs` tables |
| `quality_gate` | **ShortCircuitOperator**: if score ≥ 0.95 → continue, else → stop |
| `trigger_processing_dag` | Only reached if gate passes |

#### ShortCircuitOperator
Unlike `PythonOperator`, `ShortCircuitOperator` evaluates the return value of its callable:
- Returns `True` → downstream tasks run normally
- Returns `False` → all downstream tasks are **skipped** (not failed), pipeline halts cleanly

---

### 3. `processing_dag`
**Trigger:** Auto (triggered by `validation_dag` via `TriggerDagRunOperator`)  
**Purpose:** Clean, normalise, and join the two modalities

| Task | What it does |
|---|---|
| `clean` | Drops rows with null metadata, removes duplicates |
| `normalize` | Maps sensor features from `[-1, 1]` to `[0, 1]` using `(x + 1) / 2` |
| `join` | Appends image quality columns to each sensor row (`pd.concat(axis=1)`) |

**Why `concat` not `merge`:** Both files are row-aligned (same index = same capture event). A `merge` on `subject_id + activity_label` would create a cartesian product since both keys repeat thousands of times.

---

### 4. `curation_dag`
**Trigger:** Auto (triggered by `processing_dag`)  
**Purpose:** Produce ML-ready splits and document the dataset

| Task | What it does |
|---|---|
| `split` | Stratified 70/15/15 split by `activity_label` using `sklearn.train_test_split` |
| `dataset_card` | Writes `dataset_card.json` with split sizes, class distribution, feature count |
| `log_stats` | Writes per-split stats to `dataset_stats` table in Postgres |

`dataset_card` and `log_stats` run **in parallel** — both only need `split_paths` from XCom:
```python
split_task >> [card_task, log_stats_task]
```

---

## PostgreSQL Schema

Two databases in one container:

| Database | Owner | Purpose |
|---|---|---|
| `airflow` | Airflow | Airflow's internal metadata — DAG runs, task states, XCom values, logs index |
| `ml_pipeline` | Our pipeline | Pipeline monitoring data |

### `ml_pipeline` tables

**`pipeline_runs`** — one row per DAG run
```sql
id, dag_id, run_id, status, started_at, completed_at, records_processed, notes
```

**`quality_metrics`** — one row per quality check per run
```sql
id, run_id, dag_id, check_name, score, passed, details (JSONB), created_at
```

**`dataset_stats`** — one row per split per curation run
```sql
id, run_id, modality, num_records, num_features, class_distribution (JSONB), split, created_at
```

`JSONB` is used for `details` and `class_distribution` because these fields are flexible — the number of keys varies per check and per dataset. PostgreSQL's JSONB type is indexed and queryable, unlike plain JSON text.

---

## Docker Components

### `docker-compose.yml` — five services

| Service | Image | Port | Role |
|---|---|---|---|
| `postgres` | `postgres:15` | 5432 | Stores both Airflow metadata and pipeline monitoring data |
| `airflow-init` | `apache/airflow:2.9.2` | — | One-shot: initialises Airflow DB and creates admin user, then exits |
| `airflow-webserver` | `apache/airflow:2.9.2` | 8080 | Serves the Airflow UI |
| `airflow-scheduler` | `apache/airflow:2.9.2` | — | Watches `dags/`, triggers and executes tasks (LocalExecutor) |
| `streamlit` | Custom build | 8501 | Monitoring dashboard |

### YAML anchor (`x-airflow-common`)
`airflow-webserver` and `airflow-scheduler` share identical config (same image, same env vars, same volumes). The `&airflow-common` YAML anchor defines it once; both services reference it with `<<: *airflow-common` to avoid repetition.

### Volume types

| Volume | Type | Visible on Mac | Purpose |
|---|---|---|---|
| `./dags` | Bind mount | Yes | Live DAG reloading — edit a file, Airflow picks it up instantly |
| `./pipelines` | Bind mount | Yes | Airflow containers can `import` from `pipelines/` |
| `./data` | Bind mount | Yes | Shared data directory between all pipeline stages |
| `postgres_data` | Named volume | No (Docker-managed) | Persists DB data across restarts |
| `airflow_logs` | Named volume | No (Docker-managed) | Persists task logs across restarts |

### Startup order
```
postgres (healthy)
    └── airflow-init (completes successfully)
            ├── airflow-webserver (stays running)
            └── airflow-scheduler (stays running)
postgres (running)
    └── streamlit (stays running)
```

### Executor: LocalExecutor
Tasks execute inside the scheduler container's own process. No Redis or separate worker containers needed. Suitable for a single-machine deployment. The production alternative is `CeleryExecutor` (tasks distributed to worker containers via Redis).

---

## Data Flow Summary

```
UCI HAR website
    │
    ▼ download_uci_har
data/raw/sensor/uci_har.zip
data/raw/sensor/UCI HAR Dataset/    ← extracted
    │
    ▼ parse_uci_har
data/raw/sensor/sensor_data.csv     ← 10,299 rows × 563 cols
    │
    ▼ generate_image_metadata
data/raw/image_metadata/image_metadata.csv  ← 10,299 rows, row-aligned
    │
    ▼ validation (6 quality checks → Postgres)
    │   quality_gate: score ≥ 0.95?  NO → stop
    │                                YES ↓
    ▼ clean + normalize + join
data/processed/processed_data.csv   ← 10,299 rows, sensor + image cols
    │
    ▼ stratified split
data/curated/train.csv              ← ~7,209 rows
data/curated/val.csv                ← ~1,545 rows
data/curated/test.csv               ← ~1,545 rows
data/curated/dataset_card.json      ← metadata summary
    │
    ▼ Postgres
dataset_stats table                 ← class distribution per split
```

---

## Running the Stack

```bash
# Start all containers (first run takes ~5 min to pull images)
cd ml-sensor-pipeline
docker-compose up --build

# Airflow UI → http://localhost:8080  (admin / admin)
# Streamlit  → http://localhost:8501
# Postgres   → localhost:5432

# Trigger order in Airflow UI:
# 1. ingestion_dag   (manual)
# 2. validation_dag  (manual)
# 3. processing_dag  (auto-triggered)
# 4. curation_dag    (auto-triggered)

# Shut down
docker-compose down

# Shut down and wipe all data (full reset)
docker-compose down -v
```
