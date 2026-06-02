import sys
sys.path.insert(0, "/app")

import json
import streamlit as st
import plotly.express as px
import pandas as pd
from utils import query

st.set_page_config(page_title="Dataset Stats", layout="wide")
st.title("Dataset Stats")

df = query(
    "SELECT run_id, modality, num_records, num_features, class_distribution, split, created_at "
    "FROM dataset_stats ORDER BY created_at DESC"
)

if df.empty or "error" in df.columns:
    st.info("No dataset stats recorded yet.")
    st.stop()

# Use the most recent curation run
latest_run_id = df["run_id"].iloc[0]
latest = df[df["run_id"] == latest_run_id]

# ── Split size metrics ────────────────────────────────────────────────────────
st.subheader("Latest Curated Dataset")
col1, col2, col3, col4 = st.columns(4)

for split in ["train", "val", "test"]:
    row = latest[latest["split"] == split]
    if not row.empty:
        records = int(row["num_records"].iloc[0])
        features = int(row["num_features"].iloc[0])
        if split == "train":
            col1.metric("Train Records", records)
            col2.metric("Features", features)
        elif split == "val":
            col3.metric("Val Records", records)
        elif split == "test":
            col4.metric("Test Records", records)

st.divider()

# ── Class distribution chart ──────────────────────────────────────────────────
st.subheader("Class Distribution by Split")

dist_rows = []
for _, row in latest.iterrows():
    try:
        dist = row["class_distribution"]
        if isinstance(dist, str):
            dist = json.loads(dist)
        for activity, count in dist.items():
            dist_rows.append({"split": row["split"], "activity": activity, "count": count})
    except Exception:
        continue

if dist_rows:
    dist_df = pd.DataFrame(dist_rows)
    fig = px.bar(
        dist_df,
        x="activity", y="count",
        color="split",
        barmode="group",
        title="Activity Class Distribution Across Splits",
        labels={"activity": "Activity", "count": "Record Count"},
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Full history table ────────────────────────────────────────────────────────
st.subheader("Curation Run History")
st.dataframe(
    df.drop(columns=["class_distribution"], errors="ignore"),
    use_container_width=True,
)
