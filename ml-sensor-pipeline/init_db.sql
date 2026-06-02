-- Creates our ml_pipeline database and its tables on first Postgres startup.
-- The airflow database (Airflow's internal metadata) is created automatically
-- by the POSTGRES_DB env var — we only need to create ml_pipeline here.

CREATE DATABASE ml_pipeline;

\c ml_pipeline;

-- Tracks every DAG run: which pipeline ran, when, how many records it touched
CREATE TABLE IF NOT EXISTS pipeline_runs (
    id              SERIAL PRIMARY KEY,
    dag_id          VARCHAR(255)    NOT NULL,
    run_id          VARCHAR(255)    NOT NULL,
    status          VARCHAR(50)     NOT NULL,   -- running | success | failed
    started_at      TIMESTAMP       DEFAULT NOW(),
    completed_at    TIMESTAMP,
    records_processed INTEGER,
    notes           TEXT
);

-- Stores the result of every quality check for every run
-- One row per check (e.g. null_check, range_check) per pipeline run
CREATE TABLE IF NOT EXISTS quality_metrics (
    id          SERIAL PRIMARY KEY,
    run_id      VARCHAR(255)    NOT NULL,
    dag_id      VARCHAR(255)    NOT NULL,
    check_name  VARCHAR(255)    NOT NULL,   -- e.g. 'null_check', 'range_check'
    score       FLOAT,                      -- 0.0 to 1.0
    passed      BOOLEAN,
    details     JSONB,                      -- flexible: store any extra info as JSON
    created_at  TIMESTAMP       DEFAULT NOW()
);

-- Stores statistics about the final curated dataset after each curation run
CREATE TABLE IF NOT EXISTS dataset_stats (
    id                  SERIAL PRIMARY KEY,
    run_id              VARCHAR(255)    NOT NULL,
    modality            VARCHAR(50),            -- 'sensor' | 'image_metadata'
    num_records         INTEGER,
    num_features        INTEGER,
    class_distribution  JSONB,                  -- e.g. {"WALKING": 1200, "STANDING": 980}
    split               VARCHAR(20),            -- 'train' | 'val' | 'test'
    created_at          TIMESTAMP       DEFAULT NOW()
);
