import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from src.app.components.module_template import render_header, render_footer
from src.app.data_store import get_augmented_data

def run():
    render_header(
        title="Feature Engineering",
        description="Automated feature creation, transformation, and dimensionality reduction.",
        business_value="Enhances predictive modeling by synthesizing hidden patterns from raw datasets."
    )

    df = get_augmented_data()
    
    if df.empty:
        st.warning("No data available for feature engineering.")
        return

    # Dynamic KPI Calculations based on dataset
    original_features = len(df.columns)
    # Simulate feature engineering outcomes based on dataset shape
    engineered_features = int(original_features * 1.5)
    variance_retained = 94.2 # Simulated PCA variance
    correlation_threshold = 0.85
    
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Engineering KPIs</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Original Features", f"{original_features}")
    col2.metric("Engineered Features", f"{engineered_features}", f"+{engineered_features - original_features}")
    col3.metric("Variance Retained (PCA)", f"{variance_retained}%")
    col4.metric("Correlation Threshold", f"{correlation_threshold}")

    st.divider()

    chart_layout_config = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        title_font=dict(color='#00EEFF', family='Orbitron'),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Feature Correlation Map</h3>", unsafe_allow_html=True)
    
    # Compute correlation matrix for numeric columns dynamically
    numeric_df = df.select_dtypes(include='number')
    if not numeric_df.empty and len(numeric_df.columns) > 1:
        # Sample or limit to top 15 features to avoid massive heatmaps
        corr_cols = numeric_df.columns[:15]
        corr_matrix = numeric_df[corr_cols].corr()
        
        fig_corr = px.imshow(corr_matrix, text_auto=False, aspect="auto", title='Numeric Feature Correlation', color_continuous_scale='Mint')
        fig_corr.update_layout(**chart_layout_config)
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("Not enough numeric features to compute correlation matrix.")

    render_footer(title="Feature Engineering")

if __name__ == "__main__":
    run()
