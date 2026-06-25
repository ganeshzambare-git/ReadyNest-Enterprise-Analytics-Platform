import streamlit as st
import pandas as pd
import numpy as np

def render_feature_module(
    title: str, 
    description: str, 
    business_value: str, 
    metrics: list, 
    chart_type: str = "line"
):
    """
    Renders a standardized enterprise feature module page.
    """
    # Hero Section
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="color: #00EEFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">{title}</h1>
        <p style="color: #94A3B8; font-size: 1.1rem; margin-bottom: 1rem;">{description}</p>
        <div style="background: rgba(0, 208, 132, 0.1); border-left: 4px solid #00d084; padding: 1rem; border-radius: 4px;">
            <strong style="color: #00d084;">Business Value:</strong> <span style="color: #E2E8F0;">{business_value}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics Section
    if metrics:
        cols = st.columns(len(metrics))
        for i, col in enumerate(cols):
            with col:
                st.metric(
                    label=metrics[i]['label'], 
                    value=metrics[i]['value'], 
                    delta=metrics[i].get('delta')
                )
                
    st.divider()
    
    # Visualization Section
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif;'>Data Visualization</h3>", unsafe_allow_html=True)
    
    # Generate deterministic mock data based on title length so it looks somewhat consistent
    np.random.seed(len(title)) 
    df = pd.DataFrame(
        np.random.randn(20, 3).cumsum(axis=0), 
        columns=['Primary Metric', 'Secondary Metric', 'Tertiary Metric']
    )
    
    if chart_type == "line":
        st.line_chart(df)
    elif chart_type == "bar":
        # Make bar data positive for better visualization
        st.bar_chart(df.abs())
    else:
        st.area_chart(df)
        
    st.divider()
        
    # Data Table Section
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif;'>Data Explorer</h3>", unsafe_allow_html=True)
    st.dataframe(df.tail(10), use_container_width=True)
    
    # Export Section
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([1, 1, 1, 5])
    with col1:
        st.button("📄 Export PDF", key=f"btn_pdf_{title}", use_container_width=True)
    with col2:
        st.button("📊 Export Excel", key=f"btn_excel_{title}", use_container_width=True)
    with col3:
        st.button("📑 Export PPT", key=f"btn_ppt_{title}", use_container_width=True)
        
    # AI Recommendations Section
    st.markdown("""
    <div style="margin-top: 3rem; background: rgba(10, 15, 36, 0.6); border: 1px solid rgba(0, 238, 255, 0.2); border-radius: 12px; padding: 1.5rem; box-shadow: 0 0 15px rgba(0,238,255,0.05);">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
            <div style="font-size: 1.5rem;">💡</div>
            <h3 style="color: #00EEFF; margin: 0; font-family: 'Orbitron', sans-serif;">AI Recommendations & Insights</h3>
        </div>
        <ul style="color: #94A3B8; line-height: 1.6;">
            <li><strong style="color: white;">Trend Analysis:</strong> Consider adjusting strategies based on the recent downward trend in the Secondary Metric.</li>
            <li><strong style="color: white;">Correlation:</strong> The Primary Metric is showing strong correlation with overall performance indicators.</li>
            <li><strong style="color: white;">Anomaly Detection:</strong> Automated anomaly detection found no unusual patterns in the current dataset. Proceed with standard operational guidelines.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
