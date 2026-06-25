import streamlit as st
import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from components.module_template import render_header, render_footer

st.set_page_config(page_title="Bivariate Analysis - ReadyNest - ReadyNest", layout="wide")

render_header(
    title="Bivariate Analysis - ReadyNest",
    description="Analyze relationships and correlations between two variables.",
    business_value="Discovers hidden correlations that drive key business metrics like conversion rates."
)

# --- RESTORED LEGACY LOGIC ---
"""
src/app/pages/4_Bivariate_Analysis.py — Bivariate EDA UI
=================================================
Streamlit dashboard for Exploratory Data Analysis of two variables.
"""

import sys
import importlib
import pandas as pd
import streamlit as st

# Force reload the bivariate backend to fix caching issues
if "src.analytics.bivariate_analysis" in sys.modules:
    importlib.reload(sys.modules["src.analytics.bivariate_analysis"])
from src.analytics.bivariate_analysis import BivariateEngine
from src.config.config import APP_ICON, APP_TITLE


# ── Setup & State ─────────────────────────────────────────────────────────────

def get_current_df() -> pd.DataFrame | None:
    if st.session_state.get("clean_df") is not None:
        return st.session_state["clean_df"]
    if st.session_state.get("df") is not None:
        return st.session_state["df"]
    return None

df = get_current_df()

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        """
        <div style='text-align:center; padding: 12px 0 4px 0;'>
            <span style='font-size:2.4rem;'>🔗</span><br>
            <span style='font-size:1.1rem; font-weight:800;
                         letter-spacing:.08em; color:#14235F;'>
                READYNEST
            </span><br>
            <span style='font-size:.72rem; color:#6b7280; letter-spacing:.12em;'>
                BIVARIATE EDA
            </span>
        </div>
        <hr style='margin:12px 0;'>
        """,
        unsafe_allow_html=True,
    )
    
    st.info("💡 **Tip:** Discover hidden relationships and correlations between numerical variables.")

# ── Main UI ───────────────────────────────────────────────────────────────────


st.markdown("Analyze relationships, detect correlations, and visualize trends between two variables.")

if df is None:
    st.warning("⚠️ No dataset loaded. Please go to **Data Loading** to upload a file.")
    st.stop()

engine = BivariateEngine()
num_cols = engine.get_numerical_columns(df)

if len(num_cols) < 2:
    st.error("❌ Not enough numerical columns available for bivariate analysis. You need at least 2.")
    st.warning("💡 **Tip:** Go to **Data Cleaning** -> **Type & Format** to auto-convert text columns (like $ Sales) into numbers.")
    st.stop()

# ── Tabs ──────────────────────────────────────────────────────────────────────

tab1, tab2 = st.tabs(["🌐 Global Correlation", "🎯 Targeted Relationship Analysis"])

# ── Tab 1: Global Correlation ─────────────────────────────────────────────────

with tab1:
    st.subheader("Correlation Heatmap & Pair Plot")
    st.write("Understand the big picture. How do all numeric variables relate to one another?")
    
    method = st.radio("Correlation Method:", ["pearson", "spearman"], horizontal=True, format_func=lambda x: x.capitalize())
    
    with st.spinner("Calculating Correlation Matrix..."):
        corr_matrix = engine.generate_correlation_matrix(df, method=method)
    
    if corr_matrix is not None:
        col_h1, col_h2 = st.columns([1.5, 1])
        
        with col_h1:
            st.markdown(f"**{method.capitalize()} Correlation Heatmap**")
            fig_heat = engine.generate_heatmap(corr_matrix, f"{method.capitalize()} Correlation Matrix")
            st.pyplot(fig_heat, clear_figure=True)
            
        with col_h2:
            st.markdown("**Pair Plot (Top 5 Correlated Variables)**")
            st.write("A matrix of scatterplots showing the relationship between the strongest correlated features.")
            with st.spinner("Rendering Pair Plot..."):
                fig_pair = engine.generate_pairplot(df)
            if fig_pair:
                st.pyplot(fig_pair, clear_figure=True)
            else:
                st.info("Could not generate pair plot.")

# ── Tab 2: Targeted Analysis ──────────────────────────────────────────────────

with tab2:
    st.subheader("Scatter Plot & Trend Analysis")
    
    col_x, col_y = st.columns(2)
    with col_x:
        x_col = st.selectbox("Select X-Axis Variable:", options=num_cols, index=0)
    with col_y:
        y_col = st.selectbox("Select Y-Axis Variable:", options=num_cols, index=1 if len(num_cols) > 1 else 0)
        
    if x_col == y_col:
        st.warning("⚠️ Please select two different variables.")
    else:
        with st.spinner("Analyzing Relationship..."):
            analysis = engine.analyze_relationship(df, x_col, y_col)
            
        if analysis:
            col_s1, col_s2 = st.columns([2, 1])
            
            with col_s1:
                st.pyplot(analysis.fig_scatter, clear_figure=True)
                
            with col_s2:
                st.markdown("### 📊 Correlation Scores")
                st.metric("Pearson (Linear)", f"{analysis.pearson_r:.3f}")
                st.metric("Spearman (Monotonic)", f"{analysis.spearman_rho:.3f}")
                
                st.markdown("---")
                st.markdown("### 💡 Business Insights")
                for ins in analysis.insights:
                    st.markdown(f"- {ins}")
        else:
            st.error("Could not analyze relationship. Check for missing data.")


# --- FOOTER ---
render_footer("Bivariate Analysis - ReadyNest")
