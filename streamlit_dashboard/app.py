# import streamlit as st
# import pandas as pd
#
# # st.title("Welcome to file uploader")
# #
# # uploaded_file = st.file_uploader("Please upload the file", type = ['csv','xlsx'])
# #
# # if uploaded_file is not None:
# #     try:
# #         if uploaded_file.name.endswith(".csv"):
# #             df = pd.read_csv(uploaded_file)
# #         elif uploaded_file.name.endswith(".xlsx"):
# #             df = pd.read_excel(uploaded_file)
# #         st.success(f"Uploaded the '{uploaded_file.name}' sucessfully")
# #         st.dataframe(df)
# #     except Exception as e:
# #         st.error(f"Uploaded file is failing cox of {e}")
#
#
#####  Data Cleaning and Sanitization

# import streamlit as st
# import pandas as pd
# import numpy as np
#
# st.write("Data Cleansing")
#
# uploaded_file = st.file_uploader("Upload the CSV", type=['csv'])
# if uploaded_file:
#     df = pd.read_csv(uploaded_file)
#     st.write("Number of Null Values in Each Column")
#     st.write(df.isna().sum())
#
#     clean_option = st.radio("Select the type of cleaning", ["Drop Rows", "Fill with Zero", "Fill with 0"])
#     if clean_option == "Drop Rows":
#         df_clean = df.dropna()
#     elif clean_option == "Fill with Zero":
#         df_clean = df.fillna(0)
#     else:
#         df_clean = df.fillna(df.mean(numeric_only=True))
#     st.dataframe(df)
#     st.success("After Cleaning the dataframe")
#     df_clean['Date'] = pd.to_datetime(df['Date'])
#     st.dataframe(df_clean)
#
# ## Type conversion pandas dataframe operations
#
#     st.subheader("🛠️ Type Conversion")
#     for col in df_clean.columns:
#         st.write(f"{col}: {df_clean[col].dtype}")
#
#     convert_col = st.selectbox("Tell me the column to convert", df_clean.columns)
#     convert_type = st.selectbox("Covert to type", ["int","float","str","datetime"])
#
#     try:
#         if convert_type == "int":
#             df_clean[convert_col] = df_clean[convert_col].astype(int)
#         elif convert_type == "float":
#             df_clean[convert_col] = df_clean[convert_col].astype(float)
#         elif convert_type == "str":
#             df_clean[convert_col] = df_clean[convert_col].astype(str)
#         elif convert_type == "datetime":
#             df[convert_col] = df.to_datetime(df_clean[convert_col])
#         st.success(f"{convert_col} converted to {convert_type}")
#     except Exception as e:
#         st.error(f"Conversion failed: {e}")
#     # Invalid column removal
#
#     if "price" in df_clean.columns:
#         df_clean[price] = df_clean[df_clean[price] >= 0]
#         st.write("Sucessfully cleaned the price ")
import streamlit as st
import pandas as pd
from pages.reusable_widgets import time_slider, total_bill_slider_widget, tip_slider_widget
st.title("Time Sliding for Tips Analysis")

uploaded_file = st.file_uploader("Please upload your TIPS File", type=['csv'])

if uploaded_file is not None:
    raw_df = pd.read_csv(uploaded_file)
    raw_df['Date'] = pd.to_datetime(raw_df['Date'])  # ✅ Convert once
    st.dataframe(raw_df)

    min_time, max_time = time_slider(raw_df)
    min_bill, max_bill = total_bill_slider_widget(raw_df)
    min_tip, max_tip = tip_slider_widget(raw_df)

    filtered_df = raw_df[(raw_df['Date'] >= min_time) & (raw_df['Date'] <= max_time) &
                         (raw_df['total_bill'] >= min_bill) & (raw_df['total_bill'] <= max_bill) &
                         (raw_df['tip'] >= min_tip) & (raw_df['tip'] <= max_tip)]
    st.subheader("Filtered Data Based on Time")
    st.dataframe(filtered_df)


    # Sort by total_bill descending
    df_sorted = filtered_df.sort_values(by="total_bill", ascending=True)
    st.subheader("Sorted by total bill")
    st.dataframe(df_sorted)
    # Add a rank colum

    df_sorted["bill_rank"] = df_sorted["total_bill"].rank(method="max", ascending=False).astype(int)

    st.subheader("Adding the rank based on the dataframe")
    st.dataframe(df_sorted)

    #Grouping by and then adding aggregations

    # grouped_df = filtered_df.groupby("day").agg({
    #     "total_bill": ["mean", "sum", "max", "min"],
    #     "tip": ["mean", "max"]
    # }).reset_index()
    grouped_df = filtered_df.groupby("day")["total_bill"].sum()
    # Optional: flatten MultiIndex columns

    st.subheader("Grouped Aggregations by Day")
    st.dataframe(grouped_df)


## this the command for setting up the environment

# import streamlit as st
# import pandas as pd
# from pages.reusable_widgets import time_slider
# from pages.plotly_charts import line_chart, bar_chart
#
# st.title("📊 Tips Dashboard")
#
# # File uploader
# uploaded_file = st.file_uploader("Upload your tips.csv file", type=["csv"])
# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file)
#
#     # Convert Date to datetime
#     df['Date'] = pd.to_datetime(df['Date'])
#
#     # Show full dataset
#     st.subheader("Raw Data")
#     st.dataframe(df)
#
#     # Apply time slider
#     min_date, max_date = time_slider(df)
#     filtered_df = df[(df['Date'] >= min_date) & (df['Date'] <= max_date)]
#
#     st.subheader("Filtered Data")
#     st.dataframe(filtered_df)
#
#     # Show charts
#     line_chart(filtered_df)
#     bar_chart(filtered_df)
# else:
#     st.info("Please upload a valid tips.csv file to proceed.")