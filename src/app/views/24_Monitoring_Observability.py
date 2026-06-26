import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

from src.app.components.module_template import render_header, render_footer
from src.app.data_store import get_augmented_data

def run():
    render_header(
        title="Monitoring & Observability",
        description="Real-time system health, pipeline metrics, and data processing throughput.",
        business_value="Ensures SLA compliance and 99.99% uptime for mission-critical enterprise analytics pipelines."
    )

    df = get_augmented_data()
    
    # Simulate telemetry based on the dataset size and current time
    data_points = len(df) if not df.empty else 0
    throughput = max((data_points / 24), 1200) # Fake requests/sec
    latency = max(245 - (data_points / 1000), 45) # Fake ms
    error_rate = min(0.01 + (data_points / 1000000), 0.5) # Fake error rate
    
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>System Health KPIs</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pipeline Throughput", f"{throughput:,.0f} req/s", "+12.4%")
    col2.metric("P99 Latency", f"{latency:.0f} ms", f"{-2.1} ms")
    col3.metric("Error Rate", f"{error_rate:.2f}%", f"{-0.01}%")
    col4.metric("Active Nodes", "24", "+2")

    st.divider()

    chart_layout_config = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        title_font=dict(color='#00EEFF', family='Orbitron'),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Live Telemetry</h3>", unsafe_allow_html=True)
    
    col_viz1, col_viz2 = st.columns(2)
    
    with col_viz1:
        # Simulate time series telemetry
        np.random.seed(int(time.time() % 100))
        times = pd.date_range(end=pd.Timestamp.now(), periods=60, freq='min')
        throughput_vals = np.random.normal(throughput, throughput*0.1, 60)
        telemetry_df = pd.DataFrame({'Time': times, 'Throughput': throughput_vals})
        
        fig_telemetry = px.line(telemetry_df, x='Time', y='Throughput', title='Pipeline Throughput (Last Hour)')
        fig_telemetry.update_traces(line_color='#00d084', fill='tozeroy', fillcolor='rgba(0, 208, 132, 0.2)')
        fig_telemetry.update_layout(**chart_layout_config)
        st.plotly_chart(fig_telemetry, use_container_width=True)

    with col_viz2:
        # Simulate Error Distribution
        errors = pd.DataFrame({
            'Service': ['Data Ingestion', 'Model Inference', 'API Gateway', 'Database'],
            'Errors': [int(error_rate * 1000 * 0.4), int(error_rate * 1000 * 0.3), int(error_rate * 1000 * 0.2), int(error_rate * 1000 * 0.1)]
        })
        fig_errors = px.bar(errors, x='Errors', y='Service', orientation='h', title='Error Distribution by Service', color='Errors', color_continuous_scale='Purpor')
        fig_errors.update_layout(**chart_layout_config, coloraxis_showscale=False)
        st.plotly_chart(fig_errors, use_container_width=True)

    render_footer(title="Monitoring & Observability")

if __name__ == "__main__":
    run()
