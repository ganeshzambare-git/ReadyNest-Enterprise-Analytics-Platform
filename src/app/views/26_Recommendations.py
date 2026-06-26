import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.app.components.module_template import render_header, render_footer
from src.app.data_store import get_augmented_data

def run():
    render_header(
        title="Executive Recommendations",
        description="Data-driven Decision Intelligence architecture with prioritized executive recommendations and ROI analysis.",
        business_value="Aligns executive leadership on strategic initiatives by quantifying effort vs. impact."
    )

    df = get_augmented_data()
    
    if df.empty:
        st.warning("Insufficient data available.")
        return

    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Decision Intelligence Matrices</h3>", unsafe_allow_html=True)

    chart_layout_config = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        title_font=dict(color='#00EEFF', family='Orbitron'),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # Generate synthetic recommendation initiatives for the matrices
    np.random.seed(42)
    initiatives = pd.DataFrame({
        'Initiative': [
            'Revamp Pricing Model', 'Expand into Europe', 'Automate Lead Scoring',
            'Reduce Cloud Hosting Costs', 'Loyalty Program Launch', 'Sunset Legacy Product',
            'Increase Ad Spend (LinkedIn)', 'Optimize Supply Chain'
        ],
        'Category': [
            'Revenue Optimization', 'Market Expansion', 'Sales Optimization',
            'Cost Reduction', 'Customer Retention', 'Product Optimization',
            'Marketing Optimization', 'Inventory Optimization'
        ],
        'Impact': np.random.randint(40, 100, 8),
        'Effort': np.random.randint(10, 90, 8),
        'ROI': np.random.uniform(50, 300, 8)
    })
    
    # Calculate Priority Zone
    def get_zone(row):
        if row['Impact'] > 70 and row['Effort'] < 50: return 'Quick Wins (High Priority)'
        elif row['Impact'] > 70 and row['Effort'] >= 50: return 'Major Projects'
        elif row['Impact'] <= 70 and row['Effort'] < 50: return 'Fill-ins'
        else: return 'Thankless Tasks'
        
    initiatives['Zone'] = initiatives.apply(get_zone, axis=1)

    col_viz1, col_viz2 = st.columns(2)

    with col_viz1:
        # Impact vs Effort Matrix
        fig_matrix = px.scatter(
            initiatives, x='Effort', y='Impact', color='Zone', size='ROI', 
            hover_name='Initiative', text='Initiative', title='Impact vs Effort Matrix',
            color_discrete_map={
                'Quick Wins (High Priority)': '#00d084',
                'Major Projects': '#3B82F6',
                'Fill-ins': '#f59e0b',
                'Thankless Tasks': '#ec4899'
            }
        )
        # Add quadrant lines
        fig_matrix.add_hline(y=70, line_dash="dash", line_color="rgba(255,255,255,0.2)")
        fig_matrix.add_vline(x=50, line_dash="dash", line_color="rgba(255,255,255,0.2)")
        fig_matrix.update_traces(textposition='top center')
        fig_matrix.update_layout(**chart_layout_config)
        st.plotly_chart(fig_matrix, use_container_width=True)

    with col_viz2:
        # ROI Analysis Chart
        roi_sorted = initiatives.sort_values('ROI', ascending=True)
        fig_roi = px.bar(roi_sorted, x='ROI', y='Initiative', orientation='h', 
                         color='Category', title='Estimated ROI by Initiative (%)', 
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_roi.update_layout(**chart_layout_config, xaxis_title="ROI (%)")
        st.plotly_chart(fig_roi, use_container_width=True)

    st.divider()

    # Strategic Roadmap & Department Plan
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Department-Wise Action Plan</h3>", unsafe_allow_html=True)
    
    try:
        from src.reporting.insight_generator import InsightEngine
        insight_engine = InsightEngine()
        
        with st.spinner("Compiling Department Strategies..."):
            insights = insight_engine.extract_insights(df)
            
        if insights:
            dept_cols = st.columns(3)
            
            # Map insights to departments
            depts = ['Sales & Revenue', 'Product & Inventory', 'Customer Success']
            
            for i, col in enumerate(dept_cols):
                with col:
                    st.markdown(f"""
                    <div style="background: rgba(10, 15, 36, 0.6); padding: 15px; border-radius: 8px; border-top: 3px solid #00EEFF; height: 100%;">
                        <h4 style="color: #00EEFF; margin-top: 0;">{depts[i]}</h4>
                        <ul style="color: #E2E8F0; padding-left: 15px; font-size: 0.9rem;">
                    """, unsafe_allow_html=True)
                    
                    # Distribute insights roughly
                    dept_insights = insights[i*2:(i*2)+2]
                    for ins in dept_insights:
                        st.markdown(f"<li style='margin-bottom: 10px;'><strong>{ins.title}:</strong> {ins.recommendation}</li>", unsafe_allow_html=True)
                        
                    st.markdown("</ul></div>", unsafe_allow_html=True)
                    
    except Exception as e:
        st.error(f"Error generating AI Recommendations: {e}")

    render_footer(title="Recommendations")

if __name__ == "__main__":
    run()
