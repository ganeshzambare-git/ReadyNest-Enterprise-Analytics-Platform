"""
src/app/pages/5_Data_Visualization.py — Executive Data Visualization UI
===============================================================
Streamlit dashboard providing Power BI / Tableau style interactive reports.
"""

import sys
import importlib
import pandas as pd
import streamlit as st

# Force reload the visualization backend to fix caching issues
if "src.visualization.chart_factory" in sys.modules:
    importlib.reload(sys.modules["src.visualization.chart_factory"])
from src.visualization.chart_factory import VisualizationEngine
from src.config.config import APP_ICON, APP_TITLE


# ── Setup & State ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title=f"{APP_TITLE} - Data Visualization",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
            <span style='font-size:2.4rem;'>📊</span><br>
            <span style='font-size:1.1rem; font-weight:800;
                         letter-spacing:.08em; color:#14235F;'>
                READYNEST
            </span><br>
            <span style='font-size:.72rem; color:#6b7280; letter-spacing:.12em;'>
                EXECUTIVE DASHBOARD
            </span>
        </div>
        <hr style='margin:12px 0;'>
        """,
        unsafe_allow_html=True,
    )
    
    st.info("💡 **Tip:** Hover over charts to see precise data points. Click legend items to filter.")

# ── Main UI ───────────────────────────────────────────────────────────────────

st.title("📊 Executive Dashboard")
st.markdown("Interactive visual storytelling for Sales, Products, and Regional performance.")

if df is None:
    st.warning("⚠️ No dataset loaded. Please go to **Data Loading** to upload a file.")
    st.stop()

engine = VisualizationEngine()

with st.spinner("Auto-detecting dataset schema..."):
    mapping = engine.auto_map_columns(df)

# If auto-mapping completely fails for essential revenue metric, allow manual override.
if mapping["revenue"] is None:
    st.error("❌ Could not auto-detect a Revenue/Sales column.")
    st.stop()

# ── KPI Header ────────────────────────────────────────────────────────────────

rev_col = mapping["revenue"]
prof_col = mapping["profit"]
qty_col = mapping["quantity"]

total_rev = df[rev_col].sum() if rev_col else 0
total_prof = df[prof_col].sum() if prof_col else 0
total_qty = df[qty_col].sum() if qty_col else 0
margin = (total_prof / total_rev * 100) if total_rev > 0 else 0

st.markdown("""
<style>
div[data-testid="metric-container"] {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 15px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Revenue", f"${total_rev:,.2f}")
if prof_col: kpi2.metric("Total Profit", f"${total_prof:,.2f}")
if prof_col: kpi3.metric("Overall Margin", f"{margin:.1f}%")
if qty_col: kpi4.metric("Total Quantity", f"{total_qty:,.0f}")

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────

tab1, tab2, tab3 = st.tabs(["💰 Sales Analysis", "📦 Product Analysis", "🗺️ Regional Analysis"])

# ── Tab 1: Sales Analysis ─────────────────────────────────────────────────────

with tab1:
    if mapping["date"]:
        st.subheader("Time Series Trends")
        metrics_to_plot = [m for m in [rev_col, prof_col] if m]
        fig_trend = engine.plot_monthly_trend(df, mapping["date"], metrics_to_plot)
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("A 'Date' column is required for Time Series Trends.")

# ── Tab 2: Product Analysis ───────────────────────────────────────────────────

with tab2:
    if mapping["product"] or mapping["category"]:
        col_p1, col_p2 = st.columns([1, 1])
        
        with col_p1:
            if mapping["category"]:
                st.subheader("Category Breakdown")
                fig_cat = engine.plot_category_performance(df, mapping["category"], rev_col)
                st.plotly_chart(fig_cat, use_container_width=True)
            elif mapping["product"]:
                st.subheader("Top Products")
                fig_top = engine.plot_top_products(df, mapping["product"], rev_col, top_n=10)
                st.plotly_chart(fig_top, use_container_width=True)

        with col_p2:
            if mapping["product"]:
                st.subheader("Products Requiring Attention")
                fig_bot = engine.plot_top_products(df, mapping["product"], rev_col, top_n=10, bottom=True)
                st.plotly_chart(fig_bot, use_container_width=True)
    else:
        st.info("A 'Category' or 'Product' column is required for Product Analysis.")

# ── Tab 3: Regional Analysis ──────────────────────────────────────────────────

with tab3:
    if mapping["region"] or mapping["state"]:
        col_r1, col_r2 = st.columns([1, 1])
        
        with col_r1:
            reg_col = mapping["region"] or mapping["state"]
            st.subheader(f"Sales by {reg_col.capitalize()}")
            fig_map = engine.plot_regional_distribution(df, reg_col, rev_col)
            st.plotly_chart(fig_map, use_container_width=True)
            
        with col_r2:
            if mapping["customer"] and prof_col:
                st.subheader("Customer Profitability Matrix")
                fig_cust = engine.plot_customer_scatter(df, mapping["customer"], rev_col, prof_col)
                st.plotly_chart(fig_cust, use_container_width=True)
            else:
                st.info("A 'Customer' and 'Profit' column is required for the Profitability Matrix.")
    else:
        st.info("A 'Region' or 'State' column is required for Regional Analysis.")
