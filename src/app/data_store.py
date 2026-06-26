import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

# Define project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

@st.cache_data(show_spinner=False)
def get_raw_data():
    """Loads the raw dataset from the parquet file."""
    try:
        data_path = os.path.join(project_root, "..", "data_lake", "curated", "feature_store_customers.parquet")
        df = pd.read_parquet(data_path)
        return df
    except Exception as e:
        st.error(f"Error loading customer data: {e}")
        # Fallback to prevent app crash
        return pd.DataFrame(columns=['Total_Spend_CLV', 'Purchase_Frequency', 'Recency_Days', 'Average_Order_Value'])

@st.cache_data(show_spinner=False)
def get_augmented_data():
    """Applies universal synthetic augmentations to the dataset.
    This acts as the single source of truth for all dashboard views.
    """
    df = get_raw_data()
    if df.empty:
        return df

    # We use a deterministic seed based on dataset size so it updates if data changes, but remains consistent across pages
    np.random.seed(len(df) % 10000)
    
    # 1. Base business fields
    df['Profit'] = df['Total_Spend_CLV'] * np.random.uniform(0.15, 0.35, size=len(df))  # type: ignore
    df['Repeat_Purchaser'] = (df['Purchase_Frequency'] > 1).astype(int)
    
    # 2. Geographic Data
    regions = ['North America', 'Europe', 'Asia-Pacific', 'Latin America', 'Middle East & Africa']
    df['Region'] = list(np.random.choice(regions, size=len(df), p=[0.45, 0.25, 0.15, 0.10, 0.05]))
    
    # 3. Join Date
    now = pd.to_datetime('today')
    df['Join_Date'] = now - pd.to_timedelta(np.random.randint(1, 1095, size=len(df)).tolist(), unit='D')
    
    # 4. Behavioral Data
    df['Avg_Session_Duration_Mins'] = np.random.normal(loc=12, scale=4, size=len(df)).clip(min=1)  # type: ignore
    df['Monthly_Sessions'] = (df['Purchase_Frequency'] * np.random.uniform(1.5, 4.0, size=len(df))).astype(int)  # type: ignore
    df['Time_Between_Purchases_Days'] = (df['Recency_Days'] + np.random.normal(30, 10, size=len(df))).clip(min=1)  # type: ignore
    
    product_categories = ['Electronics', 'Apparel', 'Home Goods', 'Beauty', 'Sports']
    df['Primary_Affinity'] = np.random.choice(product_categories, size=len(df))  # type: ignore
    df['Cart_Abandonment_Rate'] = np.random.uniform(0.2, 0.8, size=len(df))  # type: ignore
    
    if 'Churn_Indicator' not in df.columns:
        df['Churn_Indicator'] = np.random.choice([0, 1], size=len(df), p=[0.8, 0.2])

    return df
