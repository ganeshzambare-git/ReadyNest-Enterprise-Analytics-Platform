import streamlit as st
import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from components.module_template import render_header, render_footer

st.set_page_config(page_title="Predictive Modeling & AI - ReadyNest - ReadyNest", layout="wide")

render_header(
    title="Predictive Modeling & AI - ReadyNest",
    description="Train and deploy ML models to predict future outcomes.",
    business_value="Transitions the business from reactive reporting to proactive decision making."
)

# --- RESTORED LEGACY LOGIC ---
"""
src/app/pages/07_Predictive_Modeling.py — Predictive ML Dashboard
==========================================================
Streamlit UI to train and explore Random Forest and XGBoost 
models for Sales Regression and Customer Churn Classification.
"""

import sys
import importlib
import pandas as pd
import streamlit as st

# Force reload backend engines
for module in ["feature_engineering", "predictive_models"]:
    if f"data_analysis.{module}" in sys.modules:
        importlib.reload(sys.modules[f"data_analysis.{module}"])

from src.machine_learning.model_training import PredictiveEngine
from src.config.config import APP_ICON, APP_TITLE

# ── Setup ─────────────────────────────────────────────────────────────────────



def get_current_df() -> pd.DataFrame | None:
    if st.session_state.get("clean_df") is not None:
        return st.session_state["clean_df"]
    if st.session_state.get("df") is not None:
        return st.session_state["df"]
    return None

df = get_current_df()

with st.sidebar:
    st.markdown("## 🤖 Predictive ML Core")
    st.info("Train Random Forest and XGBoost models on-the-fly to predict future sales and customer churn.")

st.markdown("Leverage Machine Learning to understand drivers of Revenue and predict Customer Churn.")

if df is None:
    st.warning("⚠️ No dataset loaded. Please go to **Data Loading** to upload a file.")
    st.stop()

engine = PredictiveEngine()

# ── Tabs ──────────────────────────────────────────────────────────────────────

tab1, tab2 = st.tabs(["📈 Sales Prediction (Random Forest)", "🏃‍♂️ Churn Prediction (XGBoost)"])

# ── Tab 1: Sales Predictor ────────────────────────────────────────────────────
with tab1:
    st.subheader("Revenue Drivers (Regression)")
    st.write("Trains a Random Forest Regressor to identify which numerical features most heavily impact total revenue.")
    
    if st.button("Train Sales Model (Random Forest)", type="primary", key="train_sales"):
        with st.spinner("Training Random Forest Regressor (100 Estimators)..."):
            res = engine.train_sales_predictor(df)
            
            if res is None:
                st.error("Missing Revenue column to predict.")
            elif "error" in res:
                st.error(f"Error: {res['error']}")
            else:
                st.success(f"Model Trained Successfully on {res['dataset_size']:,} records!")
                
                col1, col2 = st.columns(2)
                col1.metric("Model R² Score", f"{res['r2_score']:.3f}", "Higher is better")
                col2.metric("Mean Absolute Error (MAE)", f"{res['mae']:.2f}", "Lower is better")
                
                st.markdown("#### Top 5 Feature Importances")
                st.dataframe(res["feature_importance"], use_container_width=True)

# ── Tab 2: Churn Predictor ────────────────────────────────────────────────────
with tab2:
    st.subheader("Customer Churn Risk (Classification)")
    st.write("Engineers Customer Lifetime Value (CLV) and Retention Scores, then trains an XGBoost classifier to predict churn probability.")
    
    if st.button("Train Churn Model (XGBoost)", type="primary", key="train_churn"):
        with st.spinner("Engineering features & Training XGBoost Classifier..."):
            res = engine.train_churn_predictor(df)
            
            if res is None:
                st.error("Missing columns to engineer customer features.")
            elif "error" in res:
                st.error(f"Error: {res['error']}")
            else:
                st.success(f"Model Trained Successfully on {res['customer_count']:,} customers!")
                
                st.metric("Model Accuracy", f"{res['accuracy'] * 100:.2f}%", "Out-of-sample Test Set")
                
                st.markdown("#### Top Drivers of Churn")
                st.dataframe(res["feature_importance"], use_container_width=True)


# --- FOOTER ---
render_footer("Predictive Modeling & AI - ReadyNest")
