import streamlit as st
from utils import query

st.set_page_config(page_title="ML Sensor Pipeline", layout="wide")
st.title("ML Sensor Pipeline Monitor")
st.caption("UCI HAR + Synthetic Image Metadata | Airflow + PostgreSQL")

st.divider()

runs_df   = query("SELECT status, COUNT(*) as count FROM pipeline_runs GROUP BY status")
quality_df = query("SELECT AVG(score) as avg_score FROM quality_metrics")
stats_df   = query("SELECT SUM(num_records) as total FROM dataset_stats WHERE split = 'train'")

col1, col2, col3, col4 = st.columns(4)

total_runs   = runs_df["count"].sum() if not runs_df.empty and "count" in runs_df.columns else 0
success_runs = runs_df.loc[runs_df["status"] == "success", "count"].sum() if not runs_df.empty and "status" in runs_df.columns else 0
avg_quality  = round(float(quality_df["avg_score"].iloc[0]), 4) if not quality_df.empty and "avg_score" in quality_df.columns and quality_df["avg_score"].iloc[0] else 0
total_train  = int(stats_df["total"].iloc[0]) if not stats_df.empty and "total" in stats_df.columns and stats_df["total"].iloc[0] else 0

col1.metric("Total Pipeline Runs", total_runs)
col2.metric("Successful Runs",     success_runs)
col3.metric("Avg Quality Score",   avg_quality)
col4.metric("Training Records",    total_train)

st.divider()
st.subheader("Recent Pipeline Runs")

recent_df = query(
    "SELECT dag_id, status, started_at, notes FROM pipeline_runs ORDER BY started_at DESC LIMIT 10"
)

if not recent_df.empty and "error" not in recent_df.columns:
    st.dataframe(recent_df, use_container_width=True)
else:
    st.info("No pipeline runs yet. Trigger the ingestion DAG in Airflow to get started.")

st.sidebar.success("Navigate using the pages above.")
