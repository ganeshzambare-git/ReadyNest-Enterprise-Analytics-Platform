import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
import os

# Add project root to path so we can import components
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from components.module_template import render_header, render_footer  # type: ignore
from data_store import get_augmented_data

@st.cache_data(show_spinner=False)
def compute_overview_segments(df):
    clv_75 = df['Total_Spend_CLV'].quantile(0.75)
    clv_25 = df['Total_Spend_CLV'].quantile(0.25)
    
    def determine_segment(clv):
        if clv >= clv_75:
            return 'VIP'
        elif clv <= clv_25:
            return 'At-Risk'
        else:
            return 'Loyal'
            
    df_out = df.copy()
    df_out['Customer_Segment'] = df_out['Total_Spend_CLV'].apply(determine_segment)
    return df_out

@st.cache_data(show_spinner=False)
def compute_kpis(df):
    total_customers = len(df)
    active_customers = len(df[df['Churn_Indicator'] == 0])
    churned_customers = len(df[df['Churn_Indicator'] == 1])
    
    recent_threshold = pd.to_datetime('today') - pd.Timedelta(days=90)
    new_customers = len(df[df['Join_Date'] >= recent_threshold])
    returning_customers = total_customers - new_customers
    
    vip_customers = len(df[df['Customer_Segment'] == 'VIP'])
    
    growth_rate = round((new_customers / max(returning_customers, 1)) * 100, 1)
    retention_rate = round((active_customers / max(total_customers, 1)) * 100, 1)
    churn_rate = round((churned_customers / max(total_customers, 1)) * 100, 1)
    avg_clv = df['Total_Spend_CLV'].mean()
    
    return {
        'total_customers': total_customers,
        'active_customers': active_customers,
        'returning_customers': returning_customers,
        'new_customers': new_customers,
        'vip_customers': vip_customers,
        'growth_rate': growth_rate,
        'retention_rate': retention_rate,
        'churn_rate': churn_rate,
        'avg_clv': avg_clv
    }

def run():
    render_header(
        title="Customer Overview",
        description="A complete executive snapshot of customer activity, growth, retention, acquisition, and engagement.",
        business_value="Identifies key demographic shifts and highlights opportunities to maximize Customer Lifetime Value (CLV)."
    )

    df = get_augmented_data()
    
    if df.empty or len(df) < 5:
        st.warning("Insufficient data available to render dashboard.")
        return

    df = compute_overview_segments(df)
    
    kpis = compute_kpis(df)
    total_customers = kpis['total_customers']
    active_customers = kpis['active_customers']
    returning_customers = kpis['returning_customers']
    new_customers = kpis['new_customers']
    vip_customers = kpis['vip_customers']
    growth_rate = kpis['growth_rate']
    retention_rate = kpis['retention_rate']
    churn_rate = kpis['churn_rate']
    avg_clv = kpis['avg_clv']

    # KPI Grid layout
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Key Performance Indicators</h3>", unsafe_allow_html=True)
    
    # To handle potential Streamlit errors, wrap in try/except (as per patterns.md)
    try:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Customers", f"{total_customers:,}", None)
            st.metric("Returning Customers", f"{returning_customers:,}", None)
            st.metric("Customer Retention Rate", f"{retention_rate}%", None)
        with col2:
            st.metric("Active Customers", f"{active_customers:,}", None)
            st.metric("VIP Customers", f"{vip_customers:,}", None)
            st.metric("Customer Churn Rate", f"{churn_rate}%", None)
        with col3:
            st.metric("New Customers (Last 90d)", f"{new_customers:,}", None)
            st.metric("Avg. Customer Lifetime Value", f"${avg_clv:,.2f}", None)
            st.metric("Customer Growth Rate", f"{growth_rate}%", None)
    except Exception as e:
        st.error(f"Error rendering KPIs: {e}")

    st.divider()

    # Visualizations
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Visual Analytics</h3>", unsafe_allow_html=True)
    
    chart_layout_config = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        title_font=dict(color='#00EEFF', family='Orbitron'),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    geo_counts = pd.DataFrame(columns=['Region', 'Count'])
    try:
        col_viz1, col_viz2 = st.columns(2)

        with col_viz1:
            # Customer Growth Trend
            df_growth = df.set_index('Join_Date').resample('ME').size().reset_index(name='New_Customers').sort_values('Join_Date')
            df_growth['Cumulative_Customers'] = df_growth['New_Customers'].cumsum()
            fig_growth = px.line(df_growth, x='Join_Date', y='Cumulative_Customers', title='Customer Growth Trend', line_shape='spline', color_discrete_sequence=['#00d084'])
            fig_growth.update_layout(**chart_layout_config)
            st.plotly_chart(fig_growth, use_container_width=True)
            
            # Monthly New Customers
            df_monthly = df.copy()
            df_monthly['Month'] = pd.to_datetime(df_monthly['Join_Date']).dt.to_period('M').astype(str)
            df_new = df_monthly.groupby('Month').size().reset_index(name='Count')
            df_new['Type'] = 'New'
            
            fig_new_return = px.bar(df_new.tail(6), x='Month', y='Count', color='Type', title='Monthly New Customers', color_discrete_map={'New': '#00EEFF'})
            fig_new_return.update_layout(**chart_layout_config)
            st.plotly_chart(fig_new_return, use_container_width=True)

            # Customer Value Distribution
            fig_value = px.histogram(df, x='Total_Spend_CLV', nbins=30, title='Customer Value Distribution', color_discrete_sequence=['#8b5cf6'], marginal='box')
            fig_value.update_layout(**chart_layout_config)
            st.plotly_chart(fig_value, use_container_width=True)

        with col_viz2:
            # Customer Acquisition Trend
            fig_acq = px.area(df_growth.tail(12), x='Join_Date', y='New_Customers', title='Customer Acquisition Trend (Last 12 Months)', color_discrete_sequence=['#ec4899'])
            fig_acq.update_layout(**chart_layout_config)
            st.plotly_chart(fig_acq, use_container_width=True)

            # Customer Distribution by Segment
            seg_counts = df['Customer_Segment'].value_counts().reset_index()
            seg_counts.columns = ['Segment', 'Count']
            fig_segment = px.pie(seg_counts, values='Count', names='Segment', title='Customer Distribution by Segment', hole=0.6, color_discrete_sequence=['#00EEFF', '#00d084', '#ef4444'])
            fig_segment.update_layout(**chart_layout_config)
            st.plotly_chart(fig_segment, use_container_width=True)

            # Customer Geographic Distribution
            geo_counts = df['Region'].value_counts().reset_index()
            geo_counts.columns = ['Region', 'Count']
            fig_geo = px.bar(geo_counts, y='Region', x='Count', orientation='h', title='Customer Geographic Distribution', color='Count', color_continuous_scale='Teal')
            fig_geo.update_layout(**chart_layout_config)
            fig_geo.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_geo, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error rendering visual analytics: {e}")

    st.divider()

    # Dynamic Insights Section
    try:
        from src.reporting.insight_generator import InsightEngine
        insight_engine = InsightEngine()
        
        with st.spinner("Consultant Engine is analyzing customer data..."):
            insights = insight_engine.extract_insights(df)
            
        if insights:
            st.markdown("""
            <div style="margin-top: 2rem; background: rgba(10, 15, 36, 0.6); border: 1px solid rgba(0, 238, 255, 0.2); border-radius: 12px; padding: 1.5rem; box-shadow: 0 0 15px rgba(0,238,255,0.05);">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                    <div style="font-size: 1.5rem;">🤖</div>
                    <h3 style="color: #00EEFF; margin: 0; font-family: 'Orbitron', sans-serif;">AI-Powered Insights</h3>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                    <div>
                        <h4 style="color: #FFFFFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">Key Findings</h4>
                        <ul style="color: #94A3B8; line-height: 1.6;">
            """, unsafe_allow_html=True)
            
            for ins in insights[:4]:
                color = "#00d084" if ins.category == "Opportunity" else "#ec4899" if ins.category == "Risk" else "#3B82F6"
                st.markdown(f'<li><strong style="color: {color};">{ins.title}:</strong> {ins.business_impact}</li>', unsafe_allow_html=True)
                
            st.markdown("""
                        </ul>
                    </div>
                    <div>
                        <h4 style="color: #FFFFFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">Business Recommendations</h4>
                        <ul style="color: #94A3B8; line-height: 1.6;">
            """, unsafe_allow_html=True)
            
            for ins in insights[:4]:
                color = "#ec4899" if ins.priority_level == "High" else "#00d084"
                st.markdown(f'<li><strong style="color: {color};">{ins.area} Action:</strong> {ins.recommendation}</li>', unsafe_allow_html=True)
                
            st.markdown("""
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error generating AI Insights: {e}")

    render_footer(title="Customer Overview")

if __name__ == "__main__":
    run()
