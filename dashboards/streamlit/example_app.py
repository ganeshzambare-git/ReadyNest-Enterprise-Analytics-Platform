# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np

st.set_page_config(page_title="Standalone Example Dashboard", layout="wide")

st.title("ReadyNest Example Streamlit Dashboard")
st.markdown("This is a standalone, lightweight example dashboard. For the full enterprise application, please run `src/app/main.py`.")

# Generate sample data
@st.cache_data
def get_data():
    dates = pd.date_range("2026-01-01", periods=100)
    data = pd.DataFrame({
        'Date': dates,
        'Revenue': np.random.normal(1000, 200, 100).cumsum(),
        'Users': np.random.poisson(50, 100).cumsum()
    })
    return data

df = get_data()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue Trend")
    st.line_chart(df.set_index('Date')['Revenue'])

with col2:
    st.subheader("User Growth")
    st.area_chart(df.set_index('Date')['Users'])

if st.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()
