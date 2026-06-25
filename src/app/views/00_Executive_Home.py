"""
src/app/src/app/pages/00_Executive_Home.py — Master Executive Dashboard
========================================================
A centralized, dark-themed, glassmorphism "Command Center" that 
consolidates all analytics modules into a single, vertically scrolling page.
"""

import sys
import importlib
from datetime import datetime

import pandas as pd
import streamlit as st

# Force reload backend engines (updated for src architecture)
for module in ["insights", "bivariate", "forecasting"]:
    if f"data_analysis.{module}" in sys.modules:
        importlib.reload(sys.modules[f"data_analysis.{module}"])
if "src.reporting.pdf_generator" in sys.modules:
    importlib.reload(sys.modules["src.reporting.pdf_generator"])
if "src.visualization.chart_factory" in sys.modules:
    importlib.reload(sys.modules["src.visualization.chart_factory"])

from src.visualization.chart_factory import VisualizationEngine
from src.reporting.insight_generator import InsightEngine
from src.analytics.bivariate_analysis import BivariateEngine
from src.machine_learning.revenue_forecasting import ForecastingEngine
from src.config.config import APP_ICON, APP_TITLE

# ── 1. PAGE SETUP & CSS INJECTION ─────────────────────────────────────────────

st.set_page_config(
    page_title=f"Executive Home | {APP_TITLE}",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

    # CSS removed to allow global Streamlit config.toml theme to propagate.

# ── 2. DATA LOADING & ENGINES ─────────────────────────────────────────────────

from src.core.security import get_secured_df as get_current_df

raw_df = get_current_df()

if raw_df is None:
    st.error("⚠️ No dataset loaded. Please go to **Data Loading** to upload a file.")
    st.stop()

vis_engine = VisualizationEngine()
insight_engine = InsightEngine()
biv_engine = BivariateEngine()
forecast_engine = ForecastingEngine()

mapping = vis_engine.auto_map_columns(raw_df)

# ── 3. GLOBAL HEADER & FILTERS ────────────────────────────────────────────────

header_container = st.container()

st.markdown("<div class='filter-bar'>", unsafe_allow_html=True)
st.markdown("<h4 style='margin-top:0;'>Global Filter Panel</h4>", unsafe_allow_html=True)

# Build dynamic filters based on available categorical/date columns
filter_cols = st.columns(4)

df_filtered = raw_df.copy()

with filter_cols[0]:
    if mapping["category"]:
        cats = ["All"] + raw_df[mapping["category"]].dropna().drop_duplicates().tolist()
        sel_cat = st.selectbox("Category", cats)
        if sel_cat != "All":
            df_filtered = df_filtered[df_filtered[mapping["category"]] == sel_cat]
    else:
        st.selectbox("Category", ["N/A"], disabled=True)

with filter_cols[1]:
    if mapping["region"] or mapping["state"]:
        reg_col = mapping["region"] or mapping["state"]
        regs = ["All"] + raw_df[reg_col].dropna().drop_duplicates().tolist()
        sel_reg = st.selectbox("Region", regs)
        if sel_reg != "All":
            df_filtered = df_filtered[df_filtered[reg_col] == sel_reg]
    else:
        st.selectbox("Region", ["N/A"], disabled=True)

with filter_cols[2]:
    if mapping["date"]:
        try:
            valid_dates = pd.to_datetime(raw_df[mapping["date"]], errors="coerce").dropna()
            if not valid_dates.empty:
                min_d = valid_dates.min().date()
                max_d = valid_dates.max().date()
                date_range = st.date_input("Date Range", [min_d, max_d], min_value=min_d, max_value=max_d)
                if len(date_range) == 2:
                    mask = (pd.to_datetime(df_filtered[mapping["date"]], errors="coerce").dt.date >= date_range[0]) & \
                           (pd.to_datetime(df_filtered[mapping["date"]], errors="coerce").dt.date <= date_range[1])
                    df_filtered = df_filtered[mask]
            else:
                st.date_input("Date Range", disabled=True)
        except Exception as e:
            st.error(f"Date parsing error: {e}")
            st.date_input("Date Range", disabled=True)
    else:
        st.date_input("Date Range", disabled=True)
        
with filter_cols[3]:
    st.button("🔄 Reset All Filters", use_container_width=True, on_click=lambda: st.experimental_rerun())

st.markdown("</div>", unsafe_allow_html=True)

# Check if filtering resulted in empty DF
if df_filtered.empty:
    st.warning("Filters resulted in no data. Please adjust your selections.")
    st.stop()

with header_container:
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown("<h1 style='font-size: 2.5rem; margin-bottom: 0;'>ReadyNest Executive Dashboard</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #94A3B8; margin-top: 0;'>Last Refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Live Mode: Active</p>", unsafe_allow_html=True)

    with col_h2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚙️ Generate PDF Report", type="primary", use_container_width=True):
            with st.spinner("Compiling 60-Page Executive PDF... This may take up to 30 seconds."):
                try:
                    from src.reporting.pdf_generator import EnterpriseReportGenerator
                    generator = EnterpriseReportGenerator(df_filtered)
                    pdf_bytes = generator.generate()
                    st.session_state["pdf_bytes"] = pdf_bytes
                    st.success("Report Generated!")
                except Exception as e:
                    st.error(f"Failed to generate PDF: {e}")
                    
        if "pdf_bytes" in st.session_state:
            st.download_button(
                label="📄 Download Executive PDF Report",
                data=st.session_state["pdf_bytes"],
                file_name=f"ReadyNest_Executive_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )

# ── 4. EXECUTIVE KPI COMMAND CENTER ───────────────────────────────────────────

st.markdown("<div class='section-header'>EXECUTIVE KPI COMMAND CENTER</div>", unsafe_allow_html=True)

rev_col = mapping["revenue"]
prof_col = mapping["profit"]
qty_col = mapping["quantity"]
cust_col = mapping["customer"]

# Calculations
tot_rev = df_filtered[rev_col].sum() if rev_col else 0
tot_prof = df_filtered[prof_col].sum() if prof_col else 0
tot_orders = len(df_filtered)
tot_custs = df_filtered[cust_col].nunique() if cust_col else 0

margin = (tot_prof / tot_rev * 100) if tot_rev > 0 else 0
aov = (tot_rev / tot_orders) if tot_orders > 0 else 0

# Grid 1
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Revenue", f"${tot_rev:,.0f}", "Live")
kpi2.metric("Total Profit", f"${tot_prof:,.0f}", f"{margin:.1f}% Margin")
kpi3.metric("Total Orders", f"{tot_orders:,}")
kpi4.metric("Total Customers", f"{tot_custs:,}")

st.markdown("<br>", unsafe_allow_html=True)

# ── 5. SALES & PRODUCT OVERVIEW ───────────────────────────────────────────────

st.markdown("<div class='section-header'>SALES & PRODUCT PERFORMANCE</div>", unsafe_allow_html=True)

# Change Plotly template to dark globally for this run
vis_engine.template = "plotly_dark"

col_sp1, col_sp2 = st.columns([2, 1])

with col_sp1:
    if mapping["date"] and rev_col:
        st.markdown("**Monthly Revenue Trend**")
        metrics_to_plot = [m for m in [rev_col, prof_col] if m]
        try:
            fig_trend = vis_engine.plot_monthly_trend(df_filtered, mapping["date"], metrics_to_plot)
            st.plotly_chart(fig_trend, use_container_width=True)
        except Exception as e:
            st.error(f"Error rendering Monthly Revenue Trend: {e}")

with col_sp2:
    if mapping["category"] and rev_col:
        st.markdown("**Revenue by Category**")
        try:
            fig_cat = vis_engine.plot_category_performance(df_filtered, mapping["category"], rev_col)
            st.plotly_chart(fig_cat, use_container_width=True)
        except Exception as e:
            st.error(f"Error rendering Revenue by Category: {e}")


col_p1, col_p2 = st.columns(2)
with col_p1:
    if mapping["product"] and rev_col:
        st.markdown("**Top 10 Products (Revenue)**")
        try:
            fig_top = vis_engine.plot_top_products(df_filtered, mapping["product"], rev_col, top_n=10)
            st.plotly_chart(fig_top, use_container_width=True)
        except Exception as e:
            st.error(f"Error rendering Top 10 Products: {e}")

with col_p2:
    if mapping["product"] and prof_col:
        st.markdown("**Bottom 10 Products (Profit Risk)**")
        try:
            fig_bot = vis_engine.plot_top_products(df_filtered, mapping["product"], prof_col, top_n=10, bottom=True)
            st.plotly_chart(fig_bot, use_container_width=True)
        except Exception as e:
            st.error(f"Error rendering Bottom 10 Products: {e}")

# ── 6. REGIONAL & CUSTOMER ANALYTICS ──────────────────────────────────────────

st.markdown("<div class='section-header'>REGIONAL & CUSTOMER ANALYTICS</div>", unsafe_allow_html=True)

col_rc1, col_rc2 = st.columns(2)

with col_rc1:
    reg_col = mapping["region"] or mapping["state"]
    if reg_col and rev_col:
        st.markdown(f"**Regional Distribution ({reg_col})**")
        try:
            fig_reg = vis_engine.plot_regional_distribution(df_filtered, reg_col, rev_col)
            st.plotly_chart(fig_reg, use_container_width=True)
        except Exception as e:
            st.error(f"Error rendering Regional Distribution: {e}")

with col_rc2:
    if cust_col and rev_col and prof_col:
        st.markdown("**Customer Profitability Matrix**")
        try:
            fig_cust = vis_engine.plot_customer_scatter(df_filtered, cust_col, rev_col, prof_col)
            st.plotly_chart(fig_cust, use_container_width=True)
        except Exception as e:
            st.error(f"Error rendering Customer Matrix: {e}")

# ── 7. ADVANCED ANALYTICS (FORECASTING) ───────────────────────────────────────

st.markdown("<div class='section-header'>ADVANCED ANALYTICS (AI FORECASTING)</div>", unsafe_allow_html=True)

if mapping["date"] and rev_col:
    with st.spinner("Generating 6-Month Predictive Forecast..."):
        fig_forecast = forecast_engine.generate_forecast(df_filtered, mapping["date"], rev_col, periods=6)
        if fig_forecast:
            st.plotly_chart(fig_forecast, use_container_width=True)
        else:
            st.info("Not enough historical data points to generate a reliable mathematical forecast. Need at least 6 months.")
else:
    st.info("A 'Date' column and 'Revenue' column are required for predictive forecasting.")

# ── 8. AI INSIGHTS & ACTION CENTER ────────────────────────────────────────────

st.markdown("<div class='section-header'>AI BUSINESS INSIGHTS & ACTION CENTER</div>", unsafe_allow_html=True)

with st.spinner("BI Consultant Engine scanning for anomalies..."):
    insights = insight_engine.extract_insights(df_filtered)

if insights:
    col_i1, col_i2 = st.columns([2, 1])
    
    with col_i1:
        st.markdown("**Top Business Findings**")
        for ins in insights[:4]:
            color = "#EF4444" if ins.category == "Risk" else "#10B981" if ins.category == "Opportunity" else "#3B82F6"
            icon = "🚨" if ins.category == "Risk" else "🚀" if ins.category == "Opportunity" else "ℹ️"
            
            st.markdown(f"""
            <div style="background-color: rgba(30, 41, 59, 0.5); padding: 15px; border-left: 4px solid {color}; border-radius: 8px; margin-bottom: 10px;">
                <h4 style="margin:0;">{icon} {ins.title}</h4>
                <p style="margin:5px 0 0 0; color:#CBD5E1; font-size:0.9rem;">{ins.business_impact}</p>
            </div>
            """, unsafe_allow_html=True)
            
    with col_i2:
        st.markdown("**Executive Action Plan**")
        st.markdown("<div style='background-color: rgba(30, 41, 59, 0.5); padding: 15px; border-radius: 8px;'>", unsafe_allow_html=True)
        for ins in insights:
            if ins.priority_level == "High":
                st.markdown(f"🔴 **{ins.area}**: {ins.recommendation}")
            elif ins.priority_level == "Medium":
                st.markdown(f"🟡 **{ins.area}**: {ins.recommendation}")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No critical insights detected in the current filtered view.")

st.markdown("<br><br><p style='text-align:center; color:#64748B; font-size:0.8rem;'>ReadyNest Corporate Analytics | Secure Confidential Internal Document</p>", unsafe_allow_html=True)
