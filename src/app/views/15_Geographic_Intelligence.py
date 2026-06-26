"""
src/app/pages/09_Geographic_Intelligence.py — Location-Based Analytics
==============================================================
Streamlit dashboard for plotting geographic choropleth heatmaps.
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

st.title("🗺️ Geographic Intelligence")
st.markdown("Analyze business performance through location-based heatmaps and spatial drilldowns.")

if df is None:
    st.warning("⚠️ No dataset loaded. Please go to **Data Loading** to upload a file.")
    st.stop()

engine = VisualizationEngine()
mapping = engine.auto_map_columns(df)
rev_col = mapping["revenue"]
state_col = mapping["state"]

if not rev_col:
    st.error("No numerical Revenue column detected.")
    st.stop()

if not state_col:
    st.warning("⚠️ No State/Location column detected in your dataset. The mapping engine looks for column names containing 'state' or 'province'.")
    st.stop()

# ── Map Configuration ─────────────────────────────────────────────────────────

st.sidebar.markdown("## 🗺️ Map Controls")
map_scope = st.sidebar.radio("Map Scope", ["USA (States)", "Global (Countries)"])
location_mode = "USA-states" if map_scope == "USA (States)" else "country names"

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader(f"Revenue Heatmap by {state_col}")
    with st.spinner("Generating Geographic Heatmap..."):
        fig_map = engine.plot_geographic_map(df, state_col, rev_col, location_mode=location_mode)
        st.plotly_chart(fig_map, use_container_width=True, height=600)

with col2:
    st.subheader("Top Locations")
    grouped = df.groupby(state_col)[rev_col].sum().sort_values(ascending=False).head(10).reset_index()
    st.dataframe(grouped, use_container_width=True)
