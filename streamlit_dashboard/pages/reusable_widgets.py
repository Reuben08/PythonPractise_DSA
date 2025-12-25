# import streamlit as st
# import pandas as pd
#
# def select_day_widget(df):
#     return st.selectbox("📅 Select Day", sorted(df["DAY"].unique()))
#
def total_bill_slider_widget(df):
    min_val = float(df["total_bill"].min())
    max_val = float(df["total_bill"].max())
    return st.slider("💵 Total Bill Range", min_val, max_val, (min_val, max_val))

#
# from datetime import datetime
#
# def time_slider(df):
#     # Ensure native datetime objects (not pandas Timestamp)
#     min_val = df['Date'].min().to_pydatetime()
#     max_val = df['Date'].max().to_pydatetime()
#
#     selected_range = st.slider(
#         "Select Time Range",
#         min_value=min_val,
#         max_value=max_val,
#         value=(min_val, max_val),
#         format="YYYY-MM-DD"
#     )
#
#     # Cast back to native datetime for filtering
#     start, end = selected_range
#     return datetime.combine(start.date(), datetime.min.time()), datetime.combine(end.date(), datetime.max.time())
#
#
def tip_slider_widget(df):
    df["tip"] = pd.to_numeric(df["tip"], errors="coerce")  # Clean the column

    min_val = float(df["tip"].min())
    max_val = float(df["tip"].max())

    return st.slider("💰 Select Tip Range",min_value=round(min_val, 2),max_value=round(max_val, 2),value=(round(min_val, 2), round(max_val, 2)))
#
# def speed_slider_widget(df):
#     min_val = float(df["SPEED_KMPH"].min())
#     max_val = float(df["SPEED_KMPH"].max())
#     return st.slider("🚗 Speed (KMPH)", min_val, max_val, (min_val, max_val))
#
# def driver_multiselect_widget(df):
#     drivers = sorted(df["DRIVER_ID"].unique())
#     return st.multiselect("👨‍✈️ Select Drivers", drivers, default=drivers)

import streamlit as st
import pandas as pd
from datetime import datetime

def time_slider(df):
    min_val, max_val = get_min_max_dates(df)
    return st.slider(
        "Select Date Range:",
        min_value=min_val,
        max_value=max_val,
        value=(min_val, max_val),
        format="YYYY-MM-DD"
    )

def get_min_max_dates(df):
    """Returns the min and max dates in py-native datetime format."""
    df['Date'] = pd.to_datetime(df['Date'])
    min_val = df['Date'].min().to_pydatetime()
    max_val = df['Date'].max().to_pydatetime()
    return min_val, max_val