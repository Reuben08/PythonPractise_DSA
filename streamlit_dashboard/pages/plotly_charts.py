import plotly.express as px
import streamlit as st

def line_chart(df):
    fig = px.line(df, x='Date', y='total_bill', title="Total Bill Over Time")
    st.plotly_chart(fig)

def bar_chart(df):
    fig = px.bar(df, x='Date', y='tip', title="Tips Over Time")
    st.plotly_chart(fig)