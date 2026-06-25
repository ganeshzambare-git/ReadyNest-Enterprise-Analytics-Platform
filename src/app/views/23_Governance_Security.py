import streamlit as st
import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from components.module_template import render_header, render_footer

st.set_page_config(page_title="Governance & Security - ReadyNest - ReadyNest", layout="wide")

render_header(
    title="Governance & Security - ReadyNest",
    description="Manage roles, access logs, PII masking, and audit trails.",
    business_value="Ensures compliance with GDPR, CCPA, and enterprise infosec policies."
)

# --- RESTORED LEGACY LOGIC ---
"""
src/app/pages/12_Data_Governance.py — Data Governance & Security Portal
================================================================
Simulates Enterprise Row-Level Security (RLS) and maintains the 
Business Glossary (Data Dictionary).
"""

import pandas as pd
import streamlit as st

from src.config.config import APP_ICON, APP_TITLE
from src.visualization.chart_factory import VisualizationEngine

# ── Setup ─────────────────────────────────────────────────────────────────────




st.markdown("Manage Business Metrics definitions and enforce Row-Level Security (RLS).")

# ── 1. Row-Level Security (RLS) Simulator ─────────────────────────────────────

st.header("1. Row-Level Security (RLS) Simulator")
st.write(
    "In a production Power BI environment, Row-Level Security automatically filters the entire "
    "dataset based on the logged-in user's Azure Active Directory profile. We can simulate that behavior here."
)

if "df" not in st.session_state or st.session_state["df"] is None:
    st.warning("⚠️ No dataset loaded. Please go to **Data Loading** to upload a file.")
    st.stop()

df = st.session_state["df"]
engine = VisualizationEngine()
mapping = engine.auto_map_columns(df)
region_col = mapping["region"]

if not region_col:
    st.info("No Region column detected to simulate RLS filtering.")
else:
    regions = df[region_col].dropna().unique().tolist()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Simulate Login")
        role = st.selectbox(
            "Select User Role", 
            options=["Global Executive (All Regions)"] + [f"{r} Regional Manager" for r in regions]
        )
        
        # Save RLS state
        if role == "Global Executive (All Regions)":
            st.session_state["rls_filter"] = None
        else:
            selected_region = role.replace(" Regional Manager", "")
            st.session_state["rls_filter"] = {region_col: selected_region}
            
    with col2:
        st.subheader("Current Security Context")
        rls = st.session_state.get("rls_filter")
        if rls is None:
            st.success("🟢 **Unrestricted Access:** Viewing all data across all regions.")
        else:
            st.warning(f"🟠 **Restricted Access:** Data strictly filtered to {rls[region_col]}.")
            
        st.info("If you navigate to the Executive Home or Bivariate Analysis pages now, the data will be strictly restricted based on this role!")

st.markdown("---")

# ── 2. Business Glossary (Data Dictionary) ───────────────────────────────────

st.header("2. Enterprise Business Glossary")
st.write("A centralized data dictionary ensuring everyone in the business defines metrics the same way.")

glossary_data = [
    {"Metric": "Revenue", "Definition": "Total top-line sales amount before discounts.", "Source": "ERP Database", "Type": "Currency"},
    {"Metric": "Profit", "Definition": "Revenue minus Cost of Goods Sold (COGS).", "Source": "ERP Database", "Type": "Currency"},
    {"Metric": "Customer Lifetime Value (CLV)", "Definition": "Total historical spend of a unique customer.", "Source": "ML Feature Store", "Type": "Currency"},
    {"Metric": "Recency (Days)", "Definition": "Number of days since the customer's last purchase.", "Source": "ML Feature Store", "Type": "Integer"},
    {"Metric": "Churn Probability", "Definition": "Likelihood of a customer leaving, calculated via XGBoost.", "Source": "Predictive Engine", "Type": "Percentage"},
    {"Metric": "Popularity Score", "Definition": "0-100 score relative to the highest selling product category.", "Source": "ML Feature Store", "Type": "Float"},
]

st.table(pd.DataFrame(glossary_data))


# --- FOOTER ---
render_footer("Governance & Security - ReadyNest")
