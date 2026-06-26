"""
src/app/pages/11_Experimentation.py — A/B Testing Framework
===================================================
Prepares and calculates statistical significance for business experiments.
"""

import pandas as pd
import numpy as np
import streamlit as st

try:
    from scipy import stats
except ImportError:
    stats = None

from src.config.config import APP_ICON, APP_TITLE

# ── Setup ─────────────────────────────────────────────────────────────────────

st.title("🧪 A/B Testing Engine")
st.caption("Calculate statistical significance for your pricing, discount, and conversion experiments.")

if stats is None:
    st.error("Missing `scipy` library required for statistical calculations.")
    st.stop()

# ── Simulation UI ─────────────────────────────────────────────────────────────

st.info("Enter the results of your experiment below to determine if the Treatment group significantly outperformed the Control group.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔵 Control Group (A)")
    control_visitors = st.number_input("Total Visitors (Control)", min_value=1, value=1000)
    control_conversions = st.number_input("Total Conversions (Control)", min_value=0, value=100)
    control_revenue = st.number_input("Total Revenue (Control) $", min_value=0.0, value=5000.0)

with col2:
    st.markdown("### 🟢 Treatment Group (B)")
    treatment_visitors = st.number_input("Total Visitors (Treatment)", min_value=1, value=1000)
    treatment_conversions = st.number_input("Total Conversions (Treatment)", min_value=0, value=130)
    treatment_revenue = st.number_input("Total Revenue (Treatment) $", min_value=0.0, value=6800.0)

# ── Calculations ──────────────────────────────────────────────────────────────

st.markdown("---")
st.subheader("📊 Experiment Results")

if st.button("Calculate Significance", type="primary"):
    
    # Conversion Rates
    cr_control = control_conversions / control_visitors
    cr_treatment = treatment_conversions / treatment_visitors
    
    # Revenue Per Visitor (RPV)
    rpv_control = control_revenue / control_visitors
    rpv_treatment = treatment_revenue / treatment_visitors
    
    # Chi-Squared Test for Conversion Rate Significance
    # Contingency Table: [[Converted, Not Converted], ...]
    table = np.array([
        [control_conversions, control_visitors - control_conversions],
        [treatment_conversions, treatment_visitors - treatment_conversions]
    ])
    
    chi2_stat, p_val, dof, ex = stats.chi2_contingency(table)
    
    # Metric Display
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Control CR", f"{cr_control*100:.2f}%")
    c2.metric("Treatment CR", f"{cr_treatment*100:.2f}%", f"{(cr_treatment - cr_control)*100:.2f}%")
    
    c3.metric("Control RPV", f"${rpv_control:.2f}")
    c4.metric("Treatment RPV", f"${rpv_treatment:.2f}", f"${rpv_treatment - rpv_control:.2f}")
    
    # Significance Output
    st.markdown("#### 🔬 Statistical Analysis")
    
    alpha = 0.05
    if p_val < alpha:
        st.success(f"**Statistically Significant!** (p-value: {p_val:.4f})")
        st.write("The Treatment group performed significantly differently than the Control group. It is safe to roll out the winning variant.")
    else:
        st.warning(f"**Not Statistically Significant.** (p-value: {p_val:.4f})")
        st.write("The difference in performance could be due to random chance. You may need a larger sample size or a stronger treatment effect.")
