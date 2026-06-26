import streamlit as st
import pandas as pd
import numpy as np

from src.app.components.module_template import render_header, render_footer
from src.app.data_store import get_augmented_data

def run():
    render_header(
        title="Key Insights Engine",
        description="Automated business insights generation highlighting anomalies, trends, and growth opportunities.",
        business_value="Reduces time-to-insight from days to seconds, highlighting the most critical focus areas automatically."
    )

    df = get_augmented_data()
    
    if df.empty:
        st.warning("Insufficient data available.")
        return

    # Simulate Insight Extraction Engine
    st.markdown("""
    <div style="background: rgba(10, 15, 36, 0.8); border: 1px solid rgba(0,238,255,0.2); padding: 20px; border-radius: 12px; margin-bottom: 30px; text-align: center;">
        <h2 style="color: #00EEFF; font-family: 'Orbitron', sans-serif; margin: 0;">AI Insight Generation Engine Active</h2>
        <p style="color: #94A3B8; margin-top: 10px;">Scanning millions of data points across Revenue, Customers, Products, and Geography...</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        from src.reporting.insight_generator import InsightEngine
        insight_engine = InsightEngine()
        
        with st.spinner("Compiling Top 10 Executive Insights..."):
            insights = insight_engine.extract_insights(df)
            
        if insights:
            # We will render them as nice cards
            st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Top Insights & Anomalies</h3>", unsafe_allow_html=True)
            
            for i, ins in enumerate(insights[:10]): # Top 10
                # Determine styling based on category and priority
                border_color = "#ec4899" if ins.category == "Risk" else "#00d084" if ins.category == "Opportunity" else "#3B82F6"
                bg_color = "rgba(236, 72, 153, 0.05)" if ins.category == "Risk" else "rgba(0, 208, 132, 0.05)" if ins.category == "Opportunity" else "rgba(59, 130, 246, 0.05)"
                icon = "⚠️" if ins.category == "Risk" else "📈" if ins.category == "Opportunity" else "🔍"
                
                st.markdown(f"""
                <div style="background: {bg_color}; border-left: 5px solid {border_color}; padding: 20px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                        <h4 style="color: #FFFFFF; margin: 0; font-family: 'Orbitron', sans-serif;">{icon} {ins.title}</h4>
                        <span style="background: {border_color}; color: #FFF; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: bold;">{ins.priority_level} Priority</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;">
                        <div>
                            <span style="color: #94A3B8; font-size: 0.9rem; text-transform: uppercase;">Supporting Evidence</span>
                            <p style="color: #E2E8F0; margin-top: 5px;">{ins.evidence}</p>
                        </div>
                        <div>
                            <span style="color: #94A3B8; font-size: 0.9rem; text-transform: uppercase;">Business Impact</span>
                            <p style="color: #E2E8F0; margin-top: 5px;">{ins.business_impact}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            # Analysis Summary
            st.divider()
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Insights Generated", f"{len(insights)}")
            col2.metric("Critical Risks", f"{len([i for i in insights if i.category == 'Risk' and i.priority_level == 'High'])}")
            col3.metric("Growth Opportunities", f"{len([i for i in insights if i.category == 'Opportunity'])}")
            col4.metric("Anomalies Detected", f"{len([i for i in insights if i.category == 'Anomaly'])}")

    except Exception as e:
        st.error(f"Error generating AI Insights: {e}")

    # Export Section
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([1, 1, 1, 5])
    with col1:
        st.button("📄 Export Insights PDF", key="btn_pdf_insights", use_container_width=True)
    with col2:
        st.button("✉️ Email Exec Summary", key="btn_email_insights", use_container_width=True)

if __name__ == "__main__":
    run()
