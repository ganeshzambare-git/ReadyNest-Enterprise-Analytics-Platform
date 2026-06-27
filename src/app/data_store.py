import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

# Define project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

def get_raw_data():
    """Loads the raw dataset, prioritizing the active session state."""
    df = None
    
    # 1. Prioritize dynamically uploaded dataset in session state!
    if "df" in st.session_state and st.session_state["df"] is not None:
        df = st.session_state["df"].copy()
    else:
        # 2. Fallback to standard data lake
        try:
            data_path = os.path.join(project_root, "data_lake", "curated", "feature_store_customers.parquet")
            if os.path.exists(data_path):
                df = pd.read_parquet(data_path)
            else:
                st.toast("Generating 100,000 rows of enterprise data for analysis...", icon="⚙️")
                df = pd.DataFrame({
                    'Customer_ID': [f"CUST-{i:06d}" for i in range(100000)],
                    'Total_Spend_CLV': np.random.uniform(100, 5000, size=100000),
                    'Purchase_Frequency': np.random.randint(1, 15, size=100000),
                    'Recency_Days': np.random.randint(1, 365, size=100000)
                })
        except Exception as e:
            st.error(f"Error loading customer data: {e}")
            df = pd.DataFrame({
                'Customer_ID': [f"CUST-{i:06d}" for i in range(100000)],
                'Total_Spend_CLV': np.random.uniform(100, 5000, size=100000),
                'Purchase_Frequency': np.random.randint(1, 15, size=100000),
                'Recency_Days': np.random.randint(1, 365, size=100000)
            })

    if df.empty:
        return df
        
    # Guarantee necessary columns exist so the dashboard NEVER crashes
    import hashlib
    col_str = "".join(df.columns)
    stable_hash = int(hashlib.md5(col_str.encode()).hexdigest(), 16)
    rng = np.random.RandomState((stable_hash + len(df)) % 10000)
    
    if 'Total_Spend_CLV' not in df.columns:
        # Try to map a revenue column if it exists, else generate
        rev_cols = [c for c in df.columns if 'rev' in c.lower() or 'sales' in c.lower() or 'total' in c.lower()]
        if rev_cols and pd.api.types.is_numeric_dtype(df[rev_cols[0]]):
            df['Total_Spend_CLV'] = df[rev_cols[0]]
        else:
            df['Total_Spend_CLV'] = rng.uniform(100, 5000, size=len(df))  # type: ignore
            
    if 'Purchase_Frequency' not in df.columns:
        df['Purchase_Frequency'] = rng.randint(1, 15, size=len(df))  # type: ignore
        
    if 'Recency_Days' not in df.columns:
        df['Recency_Days'] = rng.randint(1, 365, size=len(df))  # type: ignore
        
    if 'Average_Order_Value' not in df.columns:
        df['Average_Order_Value'] = df['Total_Spend_CLV'] / df['Purchase_Frequency']
        
    return df

def get_augmented_data():
    """Applies universal synthetic augmentations to the dataset.
    This acts as the single source of truth for all dashboard views.
    """
    df = get_raw_data()
    if df.empty:
        return df

    import hashlib
    col_str = "".join(df.columns)
    stable_hash = int(hashlib.md5(col_str.encode()).hexdigest(), 16)
    np.random.seed((stable_hash + len(df)) % 10000)
    
    # 1. Base business fields
    if 'Profit' not in df.columns:
        df['Profit'] = df['Total_Spend_CLV'] * np.random.uniform(0.15, 0.35, size=len(df))  # type: ignore
    df['Repeat_Purchaser'] = (df['Purchase_Frequency'] > 1).astype(int)
    
    # 2. Geographic Data
    regions = ['North America', 'Europe', 'Asia-Pacific', 'Latin America', 'Middle East & Africa']
    if 'Region' not in df.columns:
        df['Region'] = list(np.random.choice(regions, size=len(df), p=[0.45, 0.25, 0.15, 0.10, 0.05]))
    
    # 3. Join Date
    if 'Join_Date' not in df.columns:
        now = pd.to_datetime('today')
        df['Join_Date'] = now - pd.to_timedelta(np.random.randint(1, 1095, size=len(df)).tolist(), unit='D')
    
    # 4. Behavioral Data
    if 'Avg_Session_Duration_Mins' not in df.columns:
        df['Avg_Session_Duration_Mins'] = np.random.normal(loc=12, scale=4, size=len(df)).clip(min=1)  # type: ignore
    if 'Monthly_Sessions' not in df.columns:
        df['Monthly_Sessions'] = (df['Purchase_Frequency'] * np.random.uniform(1.5, 4.0, size=len(df))).astype(int)  # type: ignore
    if 'Time_Between_Purchases_Days' not in df.columns:
        df['Time_Between_Purchases_Days'] = (df['Recency_Days'] + np.random.normal(30, 10, size=len(df))).clip(lower=1)  # type: ignore
    
    product_categories = ['Electronics', 'Apparel', 'Home Goods', 'Beauty', 'Sports']
    if 'Primary_Affinity' not in df.columns:
        df['Primary_Affinity'] = np.random.choice(product_categories, size=len(df))  # type: ignore
    if 'Cart_Abandonment_Rate' not in df.columns:
        df['Cart_Abandonment_Rate'] = np.random.uniform(0.2, 0.8, size=len(df))  # type: ignore
    
    if 'Churn_Indicator' not in df.columns:
        df['Churn_Indicator'] = np.random.choice([0, 1], size=len(df), p=[0.8, 0.2])  # type: ignore

    return df
