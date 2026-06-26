import streamlit as st
import sys
import os

from src.app.components.module_template import render_feature_module



render_feature_module(
    title="Product Performance",
    description="Analyze product adoption, usage metrics, and feature popularity.",
    business_value="Guides product roadmap decisions based on actual usage rather than intuition.",
    metrics=[
        {"label": "Total Volume", "value": "1.2M", "delta": "+15%"},
        {"label": "Active Users", "value": "45.2K", "delta": "2.4%"},
        {"label": "Processing Time", "value": "245ms", "delta": "-12ms"},
        {"label": "Error Rate", "value": "0.01%", "delta": "-0.05%"}
    ],
    chart_type="line"
)
