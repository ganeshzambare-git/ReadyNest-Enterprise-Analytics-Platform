import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from src.app.components.module_template import render_header, render_footer
from src.app.data_store import get_augmented_data

def run():
    render_header(
        title="Data Quality Assessment",
        description="Identify missing values, outliers, and inconsistencies in your datasets.",
        business_value="Improves downstream model accuracy by catching dirty data early in the pipeline."
    )

    df = get_augmented_data()
    
    if df.empty:
        st.warning("No data available for quality assessment.")
        return

    # Dynamic KPI Calculations based on the actual dataset
    total_records = len(df)
    total_features = len(df.columns)
    
    # Calculate missing values percentage
    missing_cells = df.isnull().sum().sum()
    total_cells = total_records * total_features
    missing_percentage = (missing_cells / total_cells * 100) if total_cells > 0 else 0
    
    # Estimate duplicate rows
    duplicate_rows = df.duplicated().sum()
    duplicate_percentage = (duplicate_rows / total_records * 100) if total_records > 0 else 0

    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Data Quality KPIs</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", f"{total_records:,}")
    col2.metric("Total Features", f"{total_features}")
    col3.metric("Missing Data (%)", f"{missing_percentage:.2f}%")
    col4.metric("Duplicate Rows", f"{duplicate_percentage:.2f}%")

    st.divider()

    chart_layout_config = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        title_font=dict(color='#00EEFF', family='Orbitron'),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Completeness Analysis</h3>", unsafe_allow_html=True)
    
    col_viz1, col_viz2 = st.columns(2)
    
    with col_viz1:
        missing_by_col = df.isnull().sum().reset_index()
        missing_by_col.columns = ['Feature', 'Missing Count']
        missing_by_col = missing_by_col[missing_by_col['Missing Count'] > 0]
        
        if not missing_by_col.empty:
            fig_missing = px.bar(missing_by_col, x='Feature', y='Missing Count', title='Missing Values by Feature', color_discrete_sequence=['#ec4899'])
            fig_missing.update_layout(**chart_layout_config)
            st.plotly_chart(fig_missing, use_container_width=True)
        else:
            st.success("No missing values detected in the dataset.")
            
    with col_viz2:
        # Data Type Distribution
        dtypes = df.dtypes.astype(str).value_counts().reset_index()
        dtypes.columns = ['Data Type', 'Count']
        fig_dtypes = px.pie(dtypes, values='Count', names='Data Type', title='Data Type Distribution', hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
        fig_dtypes.update_layout(**chart_layout_config)
        st.plotly_chart(fig_dtypes, use_container_width=True)

    render_footer(title="Data Quality Assessment")

if __name__ == "__main__":
    run()
