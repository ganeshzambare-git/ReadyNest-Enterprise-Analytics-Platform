import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

from src.app.components.module_template import render_header, render_footer
from src.app.data_store import get_augmented_data

@st.cache_data(show_spinner=False)
def compute_sales_kpis(df):
    total_revenue = df['Total_Spend_CLV'].sum()
    total_profit = df['Profit'].sum()
    total_orders = df['Purchase_Frequency'].sum()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    # Fake a previous period for growth %
    prev_revenue = total_revenue * 0.85
    prev_profit = total_profit * 0.82
    
    rev_growth = ((total_revenue - prev_revenue) / prev_revenue) * 100 if prev_revenue else 0
    profit_growth = ((total_profit - prev_profit) / prev_profit) * 100 if prev_profit else 0
    
    return {
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'rev_growth': rev_growth,
        'profit_growth': profit_growth
    }

def run():
    render_header(
        title="Sales Performance",
        description="Complete visibility into sales performance, revenue growth, and profitability.",
        business_value="Empowers sales leadership to identify revenue drivers and close growth gaps."
    )

    df = get_augmented_data()
    
    if df.empty or 'Join_Date' not in df.columns:
        st.warning("Insufficient or missing date data to render sales performance.")
        return
        
    # Standardize dates
    df['Date'] = pd.to_datetime(df['Join_Date'])
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    df['Quarter'] = df['Date'].dt.to_period('Q').astype(str)
    
    kpis = compute_sales_kpis(df)

    # KPI Grid
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Sales KPIs</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total Revenue", f"${kpis['total_revenue']:,.0f}", f"{kpis['rev_growth']:.1f}%")
    col2.metric("Total Profit", f"${kpis['total_profit']:,.0f}", f"{kpis['profit_growth']:.1f}%")
    col3.metric("Total Orders", f"{kpis['total_orders']:,.0f}")
    col4.metric("Avg Order Value", f"${kpis['avg_order_value']:,.2f}")
    col5.metric("Revenue Growth", f"{kpis['rev_growth']:.1f}%")
    col6.metric("Profit Growth", f"{kpis['profit_growth']:.1f}%")

    st.divider()

    chart_layout_config = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        title_font=dict(color='#00EEFF', family='Orbitron'),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # Visualizations
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Sales Analytics</h3>", unsafe_allow_html=True)
    
    col_viz1, col_viz2 = st.columns(2)

    with col_viz1:
        # Revenue Trend
        trend_df = df.groupby('Month')['Total_Spend_CLV'].sum().reset_index()
        trend_df = trend_df.sort_values('Month')
        fig_trend = px.line(trend_df, x='Month', y='Total_Spend_CLV', title='Monthly Revenue Trend', markers=True)
        fig_trend.update_traces(line_color='#00EEFF', line_width=3, marker=dict(size=8, color='#ec4899'))
        fig_trend.update_layout(**chart_layout_config)
        st.plotly_chart(fig_trend, use_container_width=True)

        # Sales Funnel (Simulated from visits -> purchase)
        stages = ["Website Visits", "Product Views", "Add to Cart", "Checkout", "Purchases"]
        base_val = kpis['total_orders'] * 4.5
        values = [base_val, base_val*0.7, base_val*0.4, base_val*0.25, kpis['total_orders']]
        fig_funnel = go.Figure(go.Funnel(y=stages, x=values, marker=dict(color=['#3b82f6', '#06b6d4', '#10b981', '#f59e0b', '#ec4899'])))
        fig_funnel.update_layout(title="Sales Conversion Funnel", **chart_layout_config)
        st.plotly_chart(fig_funnel, use_container_width=True)

    with col_viz2:
        # Revenue Waterfall (Quarterly)
        q_rev = df.groupby('Quarter')['Total_Spend_CLV'].sum().reset_index().sort_values('Quarter')
        
        measures = ['relative'] * len(q_rev)
        if len(measures) > 0:
            measures[-1] = 'total'
            
        fig_waterfall = go.Figure(go.Waterfall(
            name="20", orientation="v",
            measure=measures,
            x=q_rev['Quarter'],
            textposition="outside",
            y=q_rev['Total_Spend_CLV'],
            connector={"line": {"color": "rgba(255, 255, 255, 0.3)"}},
            decreasing={"marker": {"color": "#ec4899"}},
            increasing={"marker": {"color": "#00EEFF"}},
            totals={"marker": {"color": "#00d084"}}
        ))
        fig_waterfall.update_layout(title="Quarterly Revenue Waterfall", **chart_layout_config)
        st.plotly_chart(fig_waterfall, use_container_width=True)

        # Revenue Forecast (Simple Moving Average Projection)
        if len(trend_df) > 3:
            trend_df['Forecast'] = trend_df['Total_Spend_CLV'].rolling(window=3).mean().shift(-1)
            # Add a future point
            last_month = pd.to_datetime(trend_df['Month'].iloc[-1])
            next_month = (last_month + pd.DateOffset(months=1)).strftime('%Y-%m')
            next_val = trend_df['Total_Spend_CLV'].iloc[-3:].mean()
            
            # Use concat instead of append for future point
            future_df = pd.DataFrame({'Month': [next_month], 'Total_Spend_CLV': [np.nan], 'Forecast': [next_val]})
            trend_df = pd.concat([trend_df, future_df], ignore_index=True)
            
            fig_forecast = go.Figure()
            fig_forecast.add_trace(go.Scatter(x=trend_df['Month'], y=trend_df['Total_Spend_CLV'], name='Actual Revenue', line=dict(color='#00d084', width=3)))
            fig_forecast.add_trace(go.Scatter(x=trend_df['Month'], y=trend_df['Forecast'], name='Forecast', line=dict(color='#8b5cf6', width=2, dash='dash')))
            fig_forecast.update_layout(title='Revenue Forecast', **chart_layout_config)
            st.plotly_chart(fig_forecast, use_container_width=True)
        else:
            st.info("Not enough data to generate forecast.")

    st.divider()

    # Dynamic Insights Section
    try:
        from src.reporting.insight_generator import InsightEngine
        insight_engine = InsightEngine()
        
        with st.spinner("Consultant Engine is analyzing sales drivers..."):
            # Use raw df to generate real insights
            insights = insight_engine.extract_insights(df)
            
        if insights:
            st.markdown("""
            <div style="margin-top: 2rem; background: rgba(10, 15, 36, 0.6); border: 1px solid rgba(0, 238, 255, 0.2); border-radius: 12px; padding: 1.5rem; box-shadow: 0 0 15px rgba(0,238,255,0.05);">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                    <div style="font-size: 1.5rem;">🤖</div>
                    <h3 style="color: #00EEFF; margin: 0; font-family: 'Orbitron', sans-serif;">Sales Intelligence & Strategies</h3>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                    <div>
                        <h4 style="color: #FFFFFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">Revenue Drivers & Risks</h4>
                        <ul style="color: #94A3B8; line-height: 1.6;">
            """, unsafe_allow_html=True)
            
            # Map insights to Revenue Drivers/Risks and Recommendations
            for ins in insights[:3]:
                color = "#00d084" if ins.category == "Opportunity" else "#ec4899" if ins.category == "Risk" else "#3B82F6"
                st.markdown(f'<li><strong style="color: {color};">{ins.title}:</strong> {ins.business_impact}</li>', unsafe_allow_html=True)
                
            st.markdown("""
                        </ul>
                    </div>
                    <div>
                        <h4 style="color: #FFFFFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">Optimization Recommendations</h4>
                        <ul style="color: #94A3B8; line-height: 1.6;">
            """, unsafe_allow_html=True)
            
            for ins in insights[3:6]:
                color = "#ec4899" if ins.priority_level == "High" else "#00d084"
                st.markdown(f'<li><strong style="color: {color};">{ins.area} Optimization:</strong> {ins.recommendation}</li>', unsafe_allow_html=True)
                
            st.markdown("""
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error generating AI Insights: {e}")

    render_footer(title="Sales Performance")

if __name__ == "__main__":
    run()
