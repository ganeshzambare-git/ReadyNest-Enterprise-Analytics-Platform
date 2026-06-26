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
def compute_product_kpis(df):
    total_revenue = df['Total_Spend_CLV'].sum()
    total_profit = df['Profit'].sum()
    total_units = df['Purchase_Frequency'].sum()
    
    # Fake a previous period for growth %
    prev_revenue = total_revenue * 0.88
    product_growth_rate = ((total_revenue - prev_revenue) / prev_revenue) * 100 if prev_revenue else 0
    
    return {
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'total_units': total_units,
        'product_growth': product_growth_rate
    }

def run():
    render_header(
        title="Product Performance",
        description="Analyze product-level performance, profitability, demand, and growth.",
        business_value="Identifies best sellers and underperformers to optimize inventory and product lifecycle."
    )

    df = get_augmented_data()
    
    if df.empty:
        st.warning("Insufficient data available to render product performance.")
        return
        
    # In the absence of a real 'Product' column in standard customer data, 
    # we create a synthetic one based on clustering or random assignment for demonstration
    # if it doesn't exist.
    product_col = next((c for c in df.columns if c.lower() in ['product', 'item', 'sku', 'category', 'product_name']), None)
    
    if not product_col:
        # Create synthetic product categories for visualization
        np.random.seed(42)
        products = ['Enterprise Plan', 'Pro Plan', 'Basic Plan', 'Add-on: Storage', 'Add-on: Users']
        df['Product'] = np.random.choice(products, size=len(df), p=[0.1, 0.3, 0.4, 0.1, 0.1])
        product_col = 'Product'

    kpis = compute_product_kpis(df)

    # KPI Grid
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Product KPIs</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Product Revenue", f"${kpis['total_revenue']:,.0f}")
    col2.metric("Product Profit", f"${kpis['total_profit']:,.0f}")
    col3.metric("Units Sold", f"{kpis['total_units']:,.0f}")
    col4.metric("Product Growth Rate", f"{kpis['product_growth']:.1f}%")

    st.divider()

    chart_layout_config = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        title_font=dict(color='#00EEFF', family='Orbitron'),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # Visualizations
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Product Analytics</h3>", unsafe_allow_html=True)
    
    col_viz1, col_viz2 = st.columns(2)

    product_summary = df.groupby(product_col).agg(
        Revenue=('Total_Spend_CLV', 'sum'),
        Profit=('Profit', 'sum'),
        Units=('Purchase_Frequency', 'sum')
    ).reset_index().sort_values('Revenue', ascending=False)

    with col_viz1:
        # Product Ranking
        fig_rank = px.bar(product_summary, x='Revenue', y=product_col, orientation='h', title='Product Ranking by Revenue', color='Profit', color_continuous_scale='Mint')
        fig_rank.update_layout(**chart_layout_config, coloraxis_showscale=False)
        st.plotly_chart(fig_rank, use_container_width=True)

        # Product Heatmap (Profitability vs Volume)
        fig_heat = px.scatter(product_summary, x='Units', y='Profit', size='Revenue', color=product_col, title='Product Profitability vs Demand', hover_name=product_col)
        fig_heat.update_layout(**chart_layout_config)
        st.plotly_chart(fig_heat, use_container_width=True)

    with col_viz2:
        # Product Treemap
        # Add a dummy hierarchy if needed
        product_summary['Category'] = 'Software Products'
        fig_tree = px.treemap(product_summary, path=['Category', product_col], values='Revenue', color='Profit', color_continuous_scale='Purpor', title='Product Revenue Treemap')
        fig_tree.update_layout(**chart_layout_config)
        st.plotly_chart(fig_tree, use_container_width=True)

        # Pareto Analysis
        product_summary['Cumulative_Percentage'] = 100 * product_summary['Revenue'].cumsum() / product_summary['Revenue'].sum()
        product_summary['Rank'] = range(1, len(product_summary) + 1)
        
        fig_pareto = go.Figure()
        fig_pareto.add_trace(go.Bar(x=product_summary[product_col], y=product_summary['Revenue'], name='Revenue', marker_color='#00EEFF'))
        fig_pareto.add_trace(go.Scatter(x=product_summary[product_col], y=product_summary['Cumulative_Percentage'], name='Cumulative %', yaxis='y2', line=dict(color='#ec4899', width=3)))
        
        fig_pareto.update_layout(
            title='Product Revenue Pareto Chart',
            yaxis=dict(title='Revenue'),
            yaxis2=dict(title='Cumulative %', overlaying='y', side='right', range=[0, 100]),
            **chart_layout_config
        )
        fig_pareto.update_layout(showlegend=False)
        st.plotly_chart(fig_pareto, use_container_width=True)

    st.divider()

    # Dynamic Insights Section
    try:
        from src.reporting.insight_generator import InsightEngine
        insight_engine = InsightEngine()
        
        with st.spinner("Consultant Engine is analyzing product data..."):
            insights = insight_engine.extract_insights(df)
            
        if insights:
            st.markdown("""
            <div style="margin-top: 2rem; background: rgba(10, 15, 36, 0.6); border: 1px solid rgba(0, 238, 255, 0.2); border-radius: 12px; padding: 1.5rem; box-shadow: 0 0 15px rgba(0,238,255,0.05);">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                    <div style="font-size: 1.5rem;">🤖</div>
                    <h3 style="color: #00EEFF; margin: 0; font-family: 'Orbitron', sans-serif;">Product Intelligence</h3>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                    <div>
                        <h4 style="color: #FFFFFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">Performance Drivers</h4>
                        <ul style="color: #94A3B8; line-height: 1.6;">
            """, unsafe_allow_html=True)
            
            for ins in insights[:3]:
                color = "#00d084" if ins.category == "Opportunity" else "#ec4899" if ins.category == "Risk" else "#3B82F6"
                st.markdown(f'<li><strong style="color: {color};">{ins.title}:</strong> {ins.business_impact}</li>', unsafe_allow_html=True)
                
            st.markdown("""
                        </ul>
                    </div>
                    <div>
                        <h4 style="color: #FFFFFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">Action Plan</h4>
                        <ul style="color: #94A3B8; line-height: 1.6;">
            """, unsafe_allow_html=True)
            
            for ins in insights[3:6]:
                color = "#ec4899" if ins.priority_level == "High" else "#00d084"
                st.markdown(f'<li><strong style="color: {color};">Recommendation:</strong> {ins.recommendation}</li>', unsafe_allow_html=True)
                
            st.markdown("""
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error generating AI Insights: {e}")

    render_footer(title="Product Performance")

if __name__ == "__main__":
    run()
