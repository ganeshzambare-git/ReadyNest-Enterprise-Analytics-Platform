"""
src/app/pages/2_Descriptive_Statistics.py — ReadyNest Statistics Module UI
===================================================================
Streamlit dashboard for Descriptive Statistics.
Reads from st.session_state["clean_df"] (or "df") if available.
"""

import importlib
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Force reload the statistics backend to fix caching issues
if "src.analytics.descriptive_statistics" in sys.modules:
    importlib.reload(sys.modules["src.analytics.descriptive_statistics"])
from src.analytics.descriptive_statistics import DescriptiveStatsEngine
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
            <span style='font-size:2.4rem;'>📈</span><br>
            <span style='font-size:1.1rem; font-weight:800;
                         letter-spacing:.08em; color:#14235F;'>
                READYNEST
            </span><br>
            <span style='font-size:.72rem; color:#6b7280; letter-spacing:.12em;'>
                STATISTICS MODULE
            </span>
        </div>
        <hr style='margin:12px 0;'>
        """,
        unsafe_allow_html=True,
    )
    
    st.info("💡 **Tip:** This module automatically analyzes numeric columns to provide business insights.")

# ── Main UI ───────────────────────────────────────────────────────────────────

st.title("📈 Descriptive Statistics & Insights")
st.caption("Comprehensive statistical summaries and automated business insights.")

if df is None:
    st.warning("⚠️ No data found. Please go to the **Data Loading** module and load a dataset first.")
    st.stop()

# Identify numeric columns for the user to optionally filter
all_numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and not c.endswith("_outlier") and not c.endswith("_was_null")]

if not all_numeric_cols:
    st.error("❌ No numeric columns available for statistical analysis.")
    st.warning("💡 **Tip:** Your numerical columns (like Sales or Profit) might be currently formatted as text because they contain currency symbols ($), percentages (%), or commas.")
    
    if st.button("⚡ Auto-Convert Types Now"):
        with st.spinner("Converting types..."):
            from src.preprocessing.datatype_converter import DataTypeConverter
            converter = DataTypeConverter()
            new_df, _ = converter.infer_and_convert(df)
            if st.session_state.get("clean_df") is not None:
                st.session_state["clean_df"] = new_df
            else:
                st.session_state["df"] = new_df
            st.rerun()
            
    st.stop()

selected_cols = st.multiselect(
    "Select metrics to analyze (leave empty to auto-detect key metrics):", 
    options=all_numeric_cols, 
    default=[]
)

# Run the engine
engine = DescriptiveStatsEngine()
report = engine.analyze(df, columns=selected_cols if selected_cols else None)

if not report.column_stats:
    st.warning("No relevant columns found for analysis. Try selecting them manually above.")
    st.stop()

# ── Tabs ──────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 KPI Dashboard", 
    "📈 Summary Tables", 
    "💡 Business Insights", 
    "⬇️ Export Report"
])

# ── Tab 1: KPI Dashboard ──────────────────────────────────────────────────────
with tab1:
    st.subheader("High-Level KPIs")
    
    # Display top 4 metrics as KPI cards
    metrics = list(report.column_stats.values())[:4]
    cols = st.columns(len(metrics))
    
    for i, m in enumerate(metrics):
        with cols[i]:
            st.metric(
                label=f"Average {m.column}", 
                value=f"{m.mean:,.2f}",
                delta=f"Max: {m.max_val:,.2f}",
                delta_color="off"
            )
            
    st.markdown("---")
    
    # Generate some quick distribution charts
    st.subheader("Metric Distributions")
    chart_col = st.selectbox("Select metric for distribution view:", list(report.column_stats.keys()), key="kpi_dist")
    if chart_col:
        fig = px.histogram(
            df, x=chart_col, 
            marginal="box", 
            nbins=50, 
            title=f"Distribution of {chart_col}",
            color_discrete_sequence=["#3b82f6"]
        )
        st.plotly_chart(fig, use_container_width=True)

# ── Tab 2: Summary Tables ─────────────────────────────────────────────────────
with tab2:
    st.subheader("Detailed Statistical Summary")
    
    summary_df = report.to_dataframe()
    st.dataframe(summary_df, use_container_width=True)
    
    st.markdown("""
    **Metrics Explained:**
    - **Mean / Median / Mode**: Measures of central tendency.
    - **Std Dev / Variance**: Measures of data spread and volatility.
    - **Min / Max / Range**: The absolute limits and span of the data.
    - **25% (Q1) / 75% (Q3) / IQR**: Quartiles showing where the middle 50% of your data lies.
    """)

# ── Tab 3: Business Insights ──────────────────────────────────────────────────
with tab3:
    st.subheader("Automated Business Insights")
    st.caption("AI-generated insights based on statistical distributions.")
    
    for col, stats in report.column_stats.items():
        with st.expander(f"Insights for: **{col}**", expanded=True):
            col_insights = report.insights.get(col, [])
            if not col_insights:
                st.write("No extreme or notable insights detected for this metric.")
            else:
                for ins in col_insights:
                    st.markdown(f"- {ins}")
            
            # Show a mini box plot for visual context
            fig = px.box(df, x=col, points="outliers", height=200, title=f"{col} Spread")
            fig.update_layout(margin=dict(t=30, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

# ── Tab 4: Export Report ──────────────────────────────────────────────────────
with tab4:
    st.subheader("⬇️ Download Statistical Report")
    
    st.write("Export the comprehensive statistical summary table and insights for external reporting or presentations.")
    
    try:
        pdf_bytes = report.to_pdf_bytes()
        st.download_button(
            label="Descriptive Statistics Report (PDF)", 
            data=pdf_bytes, 
            file_name="descriptive_statistics_summary.pdf", 
            mime="application/pdf", 
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Could not generate PDF: {e}")
    
    st.markdown("---")
    st.info("💡 **Note:** The export includes all statistical metrics (Mean, Median, Standard Deviation, etc.) as well as the AI-generated business insights.")
