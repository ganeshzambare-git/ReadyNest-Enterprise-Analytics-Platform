"""
src/app/pages/08_Advanced_Visuals.py — Advanced Visualization Center
============================================================
Streamlit dashboard for Enterprise-grade visual analytics including
Sunburst, Waterfall, and Funnel charts.
"""

import sys
import importlib
import pandas as pd
import streamlit as st

if "src.visualization.chart_factory" in sys.modules:
    importlib.reload(sys.modules["src.visualization.chart_factory"])

from src.visualization.chart_factory import VisualizationEngine
from src.config.config import APP_ICON, APP_TITLE

# ── Setup ─────────────────────────────────────────────────────────────────────



def get_current_df() -> pd.DataFrame | None:
    if st.session_state.get("clean_df") is not None:
        return st.session_state["clean_df"]
    if st.session_state.get("df") is not None:
        return st.session_state["df"]
    return None

df = get_current_df()

st.title("🌌 Advanced Visualization Center")
st.markdown("Explore deep hierarchical patterns and cumulative contributions using enterprise-grade charting.")

if df is None:
    st.warning("⚠️ No dataset loaded. Please go to **Data Loading** to upload a file.")
    st.stop()

engine = VisualizationEngine()
mapping = engine.auto_map_columns(df)
rev_col = mapping["revenue"]
prof_col = mapping["profit"]

if not rev_col:
    st.error("No numerical Revenue/Sales column detected to build advanced charts.")
    st.stop()

# ── Tabs ──────────────────────────────────────────────────────────────────────

tab1, tab2, tab3 = st.tabs(["🎯 Waterfall Analysis", "☀️ Sunburst Hierarchy", "🔽 Funnel Drops"])

# ── Tab 1: Waterfall ──────────────────────────────────────────────────────────
with tab1:
    st.subheader("Cumulative Revenue Contribution")
    st.write("Understand how different categories incrementally build up your total revenue.")
    
    if mapping["category"]:
        fig_waterfall = engine.plot_waterfall(df, mapping["category"], rev_col)
        st.plotly_chart(fig_waterfall, use_container_width=True)
    else:
        st.info("No Category column detected for Waterfall chart.")

# ── Tab 2: Sunburst ───────────────────────────────────────────────────────────
with tab2:
    st.subheader("Hierarchical Drilldown")
    st.write("Click on any inner ring to drill down into sub-components.")
    
    if mapping["region"] and mapping["category"]:
        st.markdown(f"**Path:** Region ({mapping['region']}) → Category ({mapping['category']})")
        fig_sunburst = engine.plot_sunburst(df, [mapping["region"], mapping["category"]], rev_col)
        st.plotly_chart(fig_sunburst, use_container_width=True)
    else:
        st.info("Requires both a Region and a Category column for hierarchical drilldown.")

# ── Tab 3: Funnel ─────────────────────────────────────────────────────────────
with tab3:
    st.subheader("Categorical Funnel")
    st.write("Visualizes the size of categories in a descending funnel format.")
    
    if mapping["category"]:
        fig_funnel = engine.plot_funnel(df, mapping["category"], rev_col)
        st.plotly_chart(fig_funnel, use_container_width=True)
    else:
        st.info("No Category column detected for Funnel chart.")
