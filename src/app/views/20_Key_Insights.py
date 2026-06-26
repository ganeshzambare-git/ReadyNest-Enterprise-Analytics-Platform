"""
src/app/pages/6_Insight_Extraction.py — Insight Extraction UI
======================================================
Streamlit dashboard that acts as an automated BI consultant,
presenting heuristic-driven business insights in a structured format.
"""

import sys
import importlib
import pandas as pd
import streamlit as st

# Force reload the insights backend to fix caching issues
if "src.reporting.insight_generator" in sys.modules:
    importlib.reload(sys.modules["src.reporting.insight_generator"])
from src.reporting.insight_generator import InsightEngine
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
            <span style='font-size:2.4rem;'>💡</span><br>
            <span style='font-size:1.1rem; font-weight:800;
                         letter-spacing:.08em; color:#14235F;'>
                READYNEST
            </span><br>
            <span style='font-size:.72rem; color:#6b7280; letter-spacing:.12em;'>
                INSIGHT ENGINE
            </span>
        </div>
        <hr style='margin:12px 0;'>
        """,
        unsafe_allow_html=True,
    )
    
    st.info("💡 **Tip:** This module uses heuristic algorithms to find mathematical risks and opportunities in your dataset.")

# ── Main UI ───────────────────────────────────────────────────────────────────

st.title("💡 Automated Insight Extraction")
st.markdown("*\"Data will talk to you if you're willing to listen.\" — Jim Bergeson*")

if df is None:
    st.warning("⚠️ No dataset loaded. Please go to **Data Loading** to upload a file.")
    st.stop()

engine = InsightEngine()

with st.spinner("Consultant Engine is scanning the dataset for patterns..."):
    insights = engine.extract_insights(df)

if not insights:
    st.warning("The engine could not extract any insights. This usually happens if the dataset lacks distinct 'Sales', 'Profit', or 'Category' columns.")
    st.info("Try going to **Data Cleaning** -> **Type & Format** to auto-convert your columns, or ensure your CSV has financial metrics.")
    st.stop()

# ── Metrics Pre-computation ───────────────────────────────────────────────────

risks = [i for i in insights if i.category == "Risk"]
opps = [i for i in insights if i.category == "Opportunity"]
neutrals = [i for i in insights if i.category == "Insight"]

high_pri = len([i for i in insights if i.priority_level == "High"])

# ── Tabs ──────────────────────────────────────────────────────────────────────

tab1, tab2, tab3 = st.tabs(["📋 Executive Summary", "🔍 Comprehensive Insight Report", "✅ Action Plan"])

# ── Tab 1: Executive Summary ──────────────────────────────────────────────────

with tab1:
    st.subheader("High-Level Diagnostic")
    
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    col_k1.metric("Total Findings", len(insights))
    col_k2.metric("Critical Risks 🚨", len(risks))
    col_k3.metric("Growth Opportunities 🚀", len(opps))
    col_k4.metric("High Priority Actions ⚠️", high_pri)
    
    st.markdown("---")
    st.subheader("🏆 Top 3 Critical Insights")
    
    for idx, insight in enumerate(insights[:3]):
        icon = "🚨" if insight.category == "Risk" else "🚀" if insight.category == "Opportunity" else "ℹ️"
        st.markdown(f"#### {icon} {insight.title}")
        st.markdown(f"**Impact:** {insight.business_impact}")
        st.markdown(f"**Action:** {insight.recommendation}")
        st.markdown("<br>", unsafe_allow_html=True)


# ── Tab 2: Insight Report ─────────────────────────────────────────────────────

with tab2:
    st.subheader("Detailed Findings")
    st.write("A deep dive into the mathematical evidence behind each business recommendation.")
    
    for idx, insight in enumerate(insights):
        color = "red" if insight.category == "Risk" else "green" if insight.category == "Opportunity" else "blue"
        icon = "🚨" if insight.category == "Risk" else "🚀" if insight.category == "Opportunity" else "ℹ️"
        
        with st.expander(f"{icon} {insight.title} ({insight.area})", expanded=(idx==0)):
            st.markdown(f"""
            <div style="padding: 10px; border-left: 5px solid {color}; background-color: #f8fafc;">
                <p><strong>Priority Level:</strong> {insight.priority_level}</p>
                <p><strong>Insight:</strong> {insight.insight}</p>
                <p><strong>Evidence:</strong> {insight.evidence}</p>
                <p><strong>Business Impact:</strong> {insight.business_impact}</p>
                <p><strong>Recommendation:</strong> {insight.recommendation}</p>
            </div>
            """, unsafe_allow_html=True)


# ── Tab 3: Action Plan ────────────────────────────────────────────────────────

with tab3:
    st.subheader("Prioritized Action Plan")
    st.write("Checklist of recommended actions sorted by urgency.")
    
    # High Priority
    if high_pri > 0:
        st.markdown("### 🛑 Immediate Action Required (High Priority)")
        for insight in [i for i in insights if i.priority_level == "High"]:
            st.checkbox(f"**{insight.area}**: {insight.recommendation}", key=f"high_{insight.title}")
            
    # Medium Priority
    med_pri = [i for i in insights if i.priority_level == "Medium"]
    if med_pri:
        st.markdown("### ⚠️ Short-Term Goals (Medium Priority)")
        for insight in med_pri:
            st.checkbox(f"**{insight.area}**: {insight.recommendation}", key=f"med_{insight.title}")
            
    # Low Priority
    low_pri = [i for i in insights if i.priority_level == "Low"]
    if low_pri:
        st.markdown("### 🟢 Long-Term Strategy (Low Priority)")
        for insight in low_pri:
            st.checkbox(f"**{insight.area}**: {insight.recommendation}", key=f"low_{insight.title}")
