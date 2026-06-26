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
    
    from src.app.data_store import get_augmented_data
    real_df = get_augmented_data()
    
    if not real_df.empty and 'Join_Date' in real_df.columns:
        real_df_dates = real_df.copy()
        real_df_dates['Date'] = pd.to_datetime(real_df_dates['Join_Date']).dt.date
        df = real_df_dates.groupby('Date').agg(
            Primary_Metric=('Total_Spend_CLV', 'sum'),
            Secondary_Metric=('Average_Order_Value', 'mean'),
            Tertiary_Metric=('Purchase_Frequency', 'sum')
        ).tail(20).fillna(0)
    else:
        df = pd.DataFrame(columns=['Primary Metric', 'Secondary Metric', 'Tertiary Metric'])
    
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
    try:
        from src.reporting.insight_generator import InsightEngine
        insight_engine = InsightEngine()
        
        with st.spinner("Consultant Engine is analyzing data..."):
            insights = insight_engine.extract_insights(real_df)
            
        if insights:
            st.markdown("""
            <div style="margin-top: 3rem; background: rgba(10, 15, 36, 0.6); border: 1px solid rgba(0, 238, 255, 0.2); border-radius: 12px; padding: 1.5rem; box-shadow: 0 0 15px rgba(0,238,255,0.05);">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                    <div style="font-size: 1.5rem;">💡</div>
                    <h3 style="color: #00EEFF; margin: 0; font-family: 'Orbitron', sans-serif;">AI Recommendations & Insights</h3>
                </div>
                <ul style="color: #94A3B8; line-height: 1.6;">
            """, unsafe_allow_html=True)
            
            for ins in insights[:3]:
                color = "#ec4899" if ins.priority_level == "High" else "#00d084"
                st.markdown(f'<li><strong style="color: {color};">{ins.area} Action:</strong> {ins.recommendation}</li>', unsafe_allow_html=True)
                
            st.markdown("""
                </ul>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error generating AI Insights: {e}")


def render_header(title: str, description: str, business_value: str):
    """Renders just the enterprise header for a feature module."""
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="color: #00EEFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">{title}</h1>
        <p style="color: #94A3B8; font-size: 1.1rem; margin-bottom: 1rem;">{description}</p>
        <div style="background: rgba(0, 208, 132, 0.1); border-left: 4px solid #00d084; padding: 1rem; border-radius: 4px;">
            <strong style="color: #00d084;">Business Value:</strong> <span style="color: #E2E8F0;">{business_value}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

def render_footer(title: str):
    """Renders just the enterprise footer (exports & AI insights)."""
    st.divider()
    
    # Export Section
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([1, 1, 1, 5])
    with col1:
        st.button("📄 Export PDF", key=f"btn_pdf_{title}_foot", use_container_width=True)
    with col2:
        st.button("📊 Export Excel", key=f"btn_excel_{title}_foot", use_container_width=True)
    with col3:
        st.button("📑 Export PPT", key=f"btn_ppt_{title}_foot", use_container_width=True)
        
    # AI Recommendations Section
    try:
        from src.app.data_store import get_augmented_data
        from src.reporting.insight_generator import InsightEngine
        
        real_df = get_augmented_data()
        insight_engine = InsightEngine()
        
        with st.spinner("Consultant Engine is analyzing data..."):
            insights = insight_engine.extract_insights(real_df)
            
        if insights:
            st.markdown("""
            <div style="margin-top: 3rem; background: rgba(10, 15, 36, 0.6); border: 1px solid rgba(0, 238, 255, 0.2); border-radius: 12px; padding: 1.5rem; box-shadow: 0 0 15px rgba(0,238,255,0.05);">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                    <div style="font-size: 1.5rem;">💡</div>
                    <h3 style="color: #00EEFF; margin: 0; font-family: 'Orbitron', sans-serif;">AI Recommendations & Insights</h3>
                </div>
                <ul style="color: #94A3B8; line-height: 1.6;">
            """, unsafe_allow_html=True)
            
            for ins in insights[:2]:
                color = "#00EEFF"
                st.markdown(f'<li><strong style="color: {color};">{ins.title}:</strong> {ins.business_impact}</li>', unsafe_allow_html=True)
                
            st.markdown("""
                </ul>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        pass
