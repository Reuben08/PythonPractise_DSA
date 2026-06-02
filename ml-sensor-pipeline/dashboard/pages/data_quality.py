import sys
sys.path.insert(0, "/app")

import streamlit as st
import plotly.express as px
from utils import query

st.set_page_config(page_title="Data Quality", layout="wide")
st.title("Data Quality")

df = query(
    "SELECT run_id, dag_id, check_name, score, passed, created_at "
    "FROM quality_metrics ORDER BY created_at DESC"
)

if df.empty or "error" in df.columns:
    st.info("No quality metrics recorded yet.")
    st.stop()

# ── Latest scores per check ───────────────────────────────────────────────────
st.subheader("Latest Scores by Check")

latest = df.groupby("check_name").first().reset_index()
cols = st.columns(len(latest))

for i, row in latest.iterrows():
    colour = "normal" if row["passed"] else "inverse"
    cols[i].metric(
        label=row["check_name"].replace("_", " ").title(),
        value=round(row["score"], 4),
        delta="PASSED" if row["passed"] else "FAILED",
        delta_color=colour,
    )

st.divider()

# ── Score trend over runs ─────────────────────────────────────────────────────
st.subheader("Score Trend Over Runs")

fig = px.line(
    df.sort_values("created_at"),
    x="created_at",
    y="score",
    color="check_name",
    markers=True,
    title="Quality Score per Check Over Time",
    labels={"created_at": "Run Time", "score": "Score", "check_name": "Check"},
)
fig.add_hline(y=0.95, line_dash="dash", line_color="red", annotation_text="Gate threshold (0.95)")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Full metrics table ────────────────────────────────────────────────────────
st.subheader("All Quality Metrics")
st.dataframe(df, use_container_width=True)
