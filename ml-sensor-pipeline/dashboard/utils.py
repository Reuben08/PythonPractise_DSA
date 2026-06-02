import os
import pandas as pd
from sqlalchemy import create_engine


def get_engine():
    host     = os.environ.get("DB_HOST", "localhost")
    port     = os.environ.get("DB_PORT", "5432")
    name     = os.environ.get("DB_NAME", "ml_pipeline")
    user     = os.environ.get("DB_USER", "airflow")
    password = os.environ.get("DB_PASSWORD", "airflow")
    return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}")


def query(sql: str) -> pd.DataFrame:
    try:
        return pd.read_sql(sql, get_engine())
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})
