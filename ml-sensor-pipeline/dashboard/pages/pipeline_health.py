import sys
sys.path.insert(0, "/app")

import streamlit as st
import plotly.express as px
from utils import query

st.set_page_config(page_title="Pipeline Health", layout="wide")
st.title("Pipeline Health")

df = query(
    "SELECT dag_id, run_id, status, started_at, completed_at, notes "
    "FROM pipeline_runs ORDER BY started_at DESC"
)

if df.empty or "error" in df.columns:
    st.info("No pipeline runs recorded yet.")
    st.stop()

# ── Summary metrics ───────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Total Runs",   len(df))
col2.metric("Successful",   len(df[df["status"] == "success"]))
col3.metric("Failed / Blocked", len(df[df["status"] != "success"]))

st.divider()

# ── Status breakdown chart ────────────────────────────────────────────────────
status_counts = df["status"].value_counts().reset_index()
status_counts.columns = ["status", "count"]

fig = px.bar(
    status_counts,
    x="status", y="count",
    color="status",
    color_discrete_map={"success": "#2ecc71", "failed_quality_gate": "#e74c3c", "running": "#3498db"},
    title="Runs by Status",
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Full run history table ────────────────────────────────────────────────────
st.subheader("Run History")

def colour_status(val):
    if val == "success":
        return "background-color: #d5f5e3"
    elif "failed" in str(val):
        return "background-color: #fadbd8"
    return ""

st.dataframe(
    df.style.applymap(colour_status, subset=["status"]),
    use_container_width=True,
)
