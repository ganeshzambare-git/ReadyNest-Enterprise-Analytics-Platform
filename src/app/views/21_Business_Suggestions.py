import streamlit as st
import sys
import os

# Add project root to path so we can import components
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from components.module_template import render_feature_module

st.set_page_config(page_title="Business Suggestions - ReadyNest", layout="wide")

render_feature_module(
    title="Business Suggestions",
    description="Prescriptive analytics recommending specific business actions.",
    business_value="Bridges the gap between knowing what happened and knowing what to do about it.",
    metrics=[
        {"label": "Total Volume", "value": "1.2M", "delta": "+15%"},
        {"label": "Active Users", "value": "45.2K", "delta": "2.4%"},
        {"label": "Processing Time", "value": "245ms", "delta": "-12ms"},
        {"label": "Error Rate", "value": "0.01%", "delta": "-0.05%"}
    ],
    chart_type="line"
)
