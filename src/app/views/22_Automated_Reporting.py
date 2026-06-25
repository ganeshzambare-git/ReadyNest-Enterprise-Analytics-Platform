import streamlit as st
import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from components.module_template import render_header, render_footer

st.set_page_config(page_title="Automated Reporting - ReadyNest - ReadyNest", layout="wide")

render_header(
    title="Automated Reporting - ReadyNest",
    description="Schedule and distribute PDF/Excel reports to stakeholders.",
    business_value="Eliminates the manual weekly reporting grind for data analysts."
)

# --- RESTORED LEGACY LOGIC ---
"""
src/app/pages/10_Automated_Reporting.py — Automated Reporting Engine UI
===============================================================
Dashboard to configure and manage automated report distribution.
"""

import sys
import importlib
import pandas as pd
import streamlit as st

if "src.reporting.report_scheduler" in sys.modules:
    importlib.reload(sys.modules["src.reporting.report_scheduler"])

from src.reporting.report_scheduler import ReportScheduler
from src.config.config import APP_ICON, APP_TITLE

# ── Setup ─────────────────────────────────────────────────────────────────────




st.markdown("Configure enterprise schedules to automatically generate and email reports to stakeholders.")

scheduler = ReportScheduler()

# ── Create Schedule Form ──────────────────────────────────────────────────────

with st.expander("➕ Create New Automated Report", expanded=True):
    with st.form("new_schedule_form"):
        col1, col2 = st.columns(2)
        with col1:
            r_name = st.text_input("Report Name", placeholder="e.g. Weekly Executive Summary")
            r_freq = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly", "Quarterly"])
        with col2:
            r_format = st.selectbox("Export Format", ["PDF", "Excel", "CSV", "PowerPoint"])
            r_emails = st.text_input("Recipient Emails (comma separated)", placeholder="ceo@company.com, sales@company.com")
            
        submit = st.form_submit_button("💾 Save Schedule", type="primary")
        
        if submit:
            if r_name and r_emails:
                res = scheduler.add_schedule(r_name, r_freq, r_format, r_emails)
                if res["success"]:
                    st.success(f"Successfully scheduled '{r_name}'!")
                else:
                    st.error(f"Failed: {res.get('error')}")
            else:
                st.error("Report Name and Recipient Emails are required.")

# ── Active Schedules List ─────────────────────────────────────────────────────

st.markdown("### 📋 Active Schedules")

schedules = scheduler.get_schedules()

if not schedules:
    st.info("No active schedules found. Create one above.")
else:
    for job in schedules:
        with st.container():
            col_info, col_action = st.columns([4, 1])
            with col_info:
                st.markdown(f"**{job['name']}**")
                st.caption(f"⏱️ **{job['frequency']}** | 📄 Format: **{job['format']}** | 📧 To: **{job['emails']}** | Status: 🟢 {job['status']}")
            
            with col_action:
                if st.button("▶ Trigger Now", key=f"run_{job['id']}", use_container_width=True):
                    with st.spinner("Generating and sending..."):
                        res = scheduler.trigger_report_now(job["id"])
                        if res["success"]:
                            st.success("Sent!")
                        else:
                            st.error("Failed")
                
                if st.button("🗑️ Delete", key=f"del_{job['id']}", use_container_width=True):
                    scheduler.delete_schedule(job["id"])
                    st.rerun()
            
            st.markdown("---")


# --- FOOTER ---
render_footer("Automated Reporting - ReadyNest")
