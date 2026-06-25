import streamlit as st
import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from components.module_template import render_header, render_footer

st.set_page_config(page_title="Univariate Analysis - ReadyNest - ReadyNest", layout="wide")

render_header(
    title="Univariate Analysis - ReadyNest",
    description="Analyze single variables in isolation to understand their distributions.",
    business_value="Critical for identifying highly skewed metrics that require transformation."
)

# --- RESTORED LEGACY LOGIC ---
"""
src/app/pages/3_Univariate_Analysis.py — Univariate EDA UI
===================================================
Streamlit dashboard for Exploratory Data Analysis of single variables.
"""

import sys
import importlib
import pandas as pd
import streamlit as st

# Force reload the univariate backend to fix caching issues
if "src.analytics.univariate_analysis" in sys.modules:
    importlib.reload(sys.modules["src.analytics.univariate_analysis"])
from src.analytics.univariate_analysis import UnivariateEngine
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
            <span style='font-size:2.4rem;'>🔬</span><br>
            <span style='font-size:1.1rem; font-weight:800;
                         letter-spacing:.08em; color:#14235F;'>
                READYNEST
            </span><br>
            <span style='font-size:.72rem; color:#6b7280; letter-spacing:.12em;'>
                UNIVARIATE EDA
            </span>
        </div>
        <hr style='margin:12px 0;'>
        """,
        unsafe_allow_html=True,
    )
    
    st.info("💡 **Tip:** Explore the distributions and hidden patterns of individual columns.")

# ── Main UI ───────────────────────────────────────────────────────────────────


st.markdown("Analyze distributions, detect outliers, and understand the characteristics of individual variables.")

if df is None:
    st.warning("⚠️ No dataset loaded. Please go to **Data Loading** to upload a file.")
    st.stop()

# ── Variable Selection ────────────────────────────────────────────────────────

col1, col2 = st.columns([1, 2])
with col1:
    selected_col = st.selectbox(
        "**Select Variable to Analyze:**", 
        options=df.columns.tolist()
    )

with col2:
    is_numeric = pd.api.types.is_numeric_dtype(df[selected_col])
    dtype_str = str(df[selected_col].dtype)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if is_numeric:
        st.info(f"🔢 **Data Type:** Numerical ({dtype_str})")
    else:
        st.info(f"🔠 **Data Type:** Categorical/Text ({dtype_str})")

st.markdown("---")

engine = UnivariateEngine()

# ── Numerical Analysis Render ─────────────────────────────────────────────────

if is_numeric:
    with st.spinner("Generating Numerical EDA..."):
        analysis = engine.analyze_numerical(df, selected_col)
        
    if not analysis:
        st.error(f"Could not analyze '{selected_col}'. It might be completely empty.")
        st.stop()

    st.subheader(f"📊 Summary Statistics: {selected_col}")
    
    # KPI Cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Mean", f"{analysis.mean:,.2f}")
    kpi2.metric("Median", f"{analysis.median:,.2f}")
    kpi3.metric("Std Deviation", f"{analysis.std_dev:,.2f}")
    kpi4.metric("Total Count", f"{analysis.count:,}")

    kpi5, kpi6, kpi7, kpi8 = st.columns(4)
    kpi5.metric("Minimum", f"{analysis.min_val:,.2f}")
    kpi6.metric("Maximum", f"{analysis.max_val:,.2f}")
    kpi7.metric("Missing Values", f"{analysis.missing:,}")
    kpi8.metric("Outliers Detected", f"{analysis.outlier_count:,}", 
                delta="Warning" if analysis.outlier_count > 0 else None, 
                delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visual Analytics
    st.subheader("📉 Visual Analytics")
    col_v1, col_v2 = st.columns([2, 1])
    
    with col_v1:
        st.pyplot(analysis.fig_dist, clear_figure=True)
        
    with col_v2:
        st.pyplot(analysis.fig_box, clear_figure=True)

    # Business Insights
    if analysis.insights:
        st.markdown("### 💡 Statistical Insights")
        for ins in analysis.insights:
            st.markdown(f"- {ins}")

# ── Categorical Analysis Render ───────────────────────────────────────────────
else:
    with st.spinner("Generating Categorical EDA..."):
        analysis = engine.analyze_categorical(df, selected_col)
        
    if not analysis:
        st.error(f"Could not analyze '{selected_col}'. It might be completely empty.")
        st.stop()

    st.subheader(f"📊 Category Summary: {selected_col}")
    
    # KPI Cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Rows", f"{analysis.count:,}")
    kpi2.metric("Missing Values", f"{analysis.missing:,}")
    kpi3.metric("Unique Categories", f"{analysis.unique_categories:,}")
    kpi4.metric("Mode (Most Common)", str(analysis.mode)[:15])

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visual Analytics
    st.subheader("📉 Frequency Distribution")
    col_v1, col_v2 = st.columns([2, 1])
    
    with col_v1:
        st.pyplot(analysis.fig_count, clear_figure=True)
        
    with col_v2:
        st.dataframe(
            analysis.frequency_df.style.format({"Percentage": "{:.1f}%"}),
            use_container_width=True,
            hide_index=True
        )

    # Business Insights
    if analysis.insights:
        st.markdown("### 💡 Business Insights")
        for ins in analysis.insights:
            st.markdown(f"- {ins}")


# --- FOOTER ---
render_footer("Univariate Analysis - ReadyNest")
