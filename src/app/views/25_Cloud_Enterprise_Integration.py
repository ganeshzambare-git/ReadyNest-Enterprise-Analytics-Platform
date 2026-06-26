import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.app.components.module_template import render_header, render_footer
from src.app.data_store import get_augmented_data

def run():
    render_header(
        title="Cloud & Enterprise Integration",
        description="Seamlessly integrate with modern data stacks: Snowflake, Databricks, AWS, Azure, and GCP.",
        business_value="Prevents vendor lock-in and scales elastically with organizational data demands."
    )

    df = get_augmented_data()
    
    # Simulate integration metrics dynamically based on the dataset
    data_volume_gb = len(df) * 0.005 if not df.empty else 0
    total_syncs = int(len(df) / 100) if not df.empty else 0
    active_connectors = 5
    avg_sync_time = max(0.5, data_volume_gb * 2.1)
    
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Integration KPIs</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Data Synced (24h)", f"{data_volume_gb:,.2f} GB", "+5.2%")
    col2.metric("Total Syncs", f"{total_syncs:,}")
    col3.metric("Avg Sync Time", f"{avg_sync_time:.1f}s")
    col4.metric("Active Connectors", f"{active_connectors}")

    st.divider()

    chart_layout_config = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        title_font=dict(color='#00EEFF', family='Orbitron'),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Connector Health & Throughput</h3>", unsafe_allow_html=True)
    
    col_viz1, col_viz2 = st.columns(2)
    
    with col_viz1:
        # Connector Status
        connectors = pd.DataFrame({
            'Connector': ['Snowflake', 'AWS S3', 'PostgreSQL', 'Salesforce', 'Databricks'],
            'Status': ['Healthy', 'Healthy', 'Healthy', 'Warning', 'Healthy'],
            'Volume (GB)': [data_volume_gb*0.4, data_volume_gb*0.3, data_volume_gb*0.15, data_volume_gb*0.05, data_volume_gb*0.1]
        })
        
        fig_connectors = px.pie(connectors, values='Volume (GB)', names='Connector', hole=0.5, title='Data Volume by Connector', color_discrete_sequence=px.colors.sequential.Mint)
        fig_connectors.update_layout(**chart_layout_config)
        st.plotly_chart(fig_connectors, use_container_width=True)

    with col_viz2:
        # Architecture Diagram
        st.markdown("""
        <div style="background: rgba(10, 15, 36, 0.6); padding: 20px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); height: 100%;">
            <h4 style="color: #00EEFF; font-family: 'Orbitron', sans-serif; margin-top: 0; text-align: center;">Active Integrations</h4>
            <div style="display: flex; flex-direction: column; gap: 15px; margin-top: 20px;">
        """, unsafe_allow_html=True)
        
        for index, row in connectors.iterrows():
            color = "#00d084" if row['Status'] == 'Healthy' else "#f59e0b"
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.02); padding: 10px 15px; border-left: 4px solid {color}; border-radius: 4px;">
                <strong style="color: #E2E8F0;">{row['Connector']}</strong>
                <span style="color: #94A3B8; font-size: 0.9rem;">{row['Status']}</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div></div>", unsafe_allow_html=True)

    render_footer(title="Cloud & Enterprise Integration")

if __name__ == "__main__":
    run()
