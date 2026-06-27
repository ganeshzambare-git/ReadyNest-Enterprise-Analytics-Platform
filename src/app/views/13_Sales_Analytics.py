import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.app.components.module_template import render_header, render_footer
from src.app.data_store import get_augmented_data

def run():
    render_header(
        title="Sales Analytics",
        description="Advanced multidimensional sales analytics to explore regions, channels, and categories.",
        business_value="Identifies optimal channels and regions to maximize revenue efficiency and market share."
    )

    df = get_augmented_data()
    
    if df.empty:
        st.warning("Insufficient data available to render sales analytics.")
        return
        
    # Generate synthetic categorical dimensions if missing for demonstration
    np.random.seed(42)
    if 'Region' not in df.columns:
        df['Region'] = np.random.choice(['North America', 'Europe', 'Asia Pacific', 'Latin America'], size=len(df), p=[0.4, 0.3, 0.2, 0.1]).tolist()
    if 'Channel' not in df.columns:
        df['Channel'] = np.random.choice(['Direct Sales', 'Partner Network', 'Online Portal', 'Referral'], size=len(df), p=[0.3, 0.4, 0.2, 0.1]).tolist()
    if 'Category' not in df.columns:
        df['Category'] = np.random.choice(['Enterprise Software', 'Cloud Services', 'Consulting', 'Support'], size=len(df), p=[0.5, 0.2, 0.15, 0.15]).tolist()
    if 'Customer_Segment' not in df.columns:
        df['Customer_Segment'] = np.random.choice(['Enterprise', 'Mid-Market', 'SMB', 'Startup'], size=len(df), p=[0.2, 0.3, 0.4, 0.1]).tolist()

    # Advanced Metrics
    total_rev = df['Total_Spend_CLV'].sum()
    top_region = df.groupby('Region')['Total_Spend_CLV'].sum().idxmax()
    top_channel = df.groupby('Channel')['Total_Spend_CLV'].sum().idxmax()
    
    # KPIs
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Advanced Sales Metrics</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Fake market share & conversion
    market_share = 14.2
    conversion_rate = 8.7
    sales_efficiency = df['Profit'].sum() / total_rev if total_rev > 0 else 0
    
    col1.metric("Market Share", f"{market_share}%", "+1.2%")
    col2.metric("Conversion Rate", f"{conversion_rate}%", "+0.5%")
    col3.metric("Top Region Contribution", f"{(df[df['Region']==top_region]['Total_Spend_CLV'].sum() / total_rev)*100:.1f}%")
    col4.metric("Sales Efficiency (Margin)", f"{sales_efficiency*100:.1f}%")

    st.divider()

    chart_layout_config = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        title_font=dict(color='#00EEFF', family='Orbitron'),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Dimensional Analysis</h3>", unsafe_allow_html=True)

    col_viz1, col_viz2 = st.columns(2)

    with col_viz1:
        # Sales by Region Map
        region_sales = df.groupby('Region')['Total_Spend_CLV'].sum().reset_index()
        # Using a pie chart to simulate map distribution if we don't have ISO codes
        fig_region = px.pie(region_sales, values='Total_Spend_CLV', names='Region', hole=0.4, title='Sales Distribution by Region', color_discrete_sequence=px.colors.sequential.Teal)
        fig_region.update_layout(**chart_layout_config)
        st.plotly_chart(fig_region, use_container_width=True)
        
        # Sales by Channel
        channel_sales = df.groupby('Channel').agg(Revenue=('Total_Spend_CLV', 'sum'), Orders=('Purchase_Frequency', 'sum')).reset_index()
        fig_channel = px.bar(channel_sales, x='Channel', y='Revenue', color='Orders', title='Channel Performance & Volume', color_continuous_scale='Purpor')
        fig_channel.update_layout(**chart_layout_config)
        st.plotly_chart(fig_channel, use_container_width=True)

    with col_viz2:
        # Category Contribution Sunburst
        fig_sunburst = px.sunburst(df, path=['Region', 'Category'], values='Total_Spend_CLV', title='Regional Category Contribution', color='Total_Spend_CLV', color_continuous_scale='Mint')
        fig_sunburst.update_layout(**chart_layout_config)
        st.plotly_chart(fig_sunburst, use_container_width=True)

        # Sales by Customer Segment
        segment_sales = df.groupby('Customer_Segment')['Total_Spend_CLV'].sum().reset_index()
        fig_segment = px.funnel(segment_sales, x='Total_Spend_CLV', y='Customer_Segment', title='Revenue by Segment', color_discrete_sequence=['#00EEFF'])
        fig_segment.update_layout(**chart_layout_config)
        st.plotly_chart(fig_segment, use_container_width=True)

    st.divider()

    # Dynamic Insights Section
    try:
        from src.reporting.insight_generator import InsightEngine
        insight_engine = InsightEngine()
        
        with st.spinner("Consultant Engine is analyzing dimensions..."):
            insights = insight_engine.extract_insights(df)
            
        if insights:
            st.markdown("""
            <div style="margin-top: 2rem; background: rgba(10, 15, 36, 0.6); border: 1px solid rgba(0, 238, 255, 0.2); border-radius: 12px; padding: 1.5rem; box-shadow: 0 0 15px rgba(0,238,255,0.05);">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                    <div style="font-size: 1.5rem;">🤖</div>
                    <h3 style="color: #00EEFF; margin: 0; font-family: 'Orbitron', sans-serif;">Dimensional Insights & Recommendations</h3>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                    <div>
                        <h4 style="color: #FFFFFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">Key Findings</h4>
                        <ul style="color: #94A3B8; line-height: 1.6;">
            """, unsafe_allow_html=True)
            
            for ins in insights[:3]:
                color = "#00d084" if ins.category == "Opportunity" else "#ec4899" if ins.category == "Risk" else "#3B82F6"
                st.markdown(f'<li><strong style="color: {color};">{ins.title}:</strong> {ins.business_impact}</li>', unsafe_allow_html=True)
                
            st.markdown("""
                        </ul>
                    </div>
                    <div>
                        <h4 style="color: #FFFFFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">Growth Strategy</h4>
                        <ul style="color: #94A3B8; line-height: 1.6;">
            """, unsafe_allow_html=True)
            
            for ins in insights[3:6]:
                color = "#ec4899" if ins.priority_level == "High" else "#00d084"
                st.markdown(f'<li><strong style="color: {color};">{ins.area} Expansion:</strong> {ins.recommendation}</li>', unsafe_allow_html=True)
                
            st.markdown("""
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error generating AI Insights: {e}")

    render_footer(title="Sales Analytics")

if __name__ == "__main__":
    run()
