import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.app.components.module_template import render_header, render_footer
from src.app.data_store import get_augmented_data

def run():
    render_header(
        title="Product Analytics",
        description="Deep dive into product categories, lifecycles, and demand forecasting.",
        business_value="Optimizes product portfolio and inventory planning to maximize margins and reduce holding costs."
    )

    df = get_augmented_data()
    
    if df.empty:
        st.warning("Insufficient data available to render product analytics.")
        return
        
    np.random.seed(42)
    if 'Product_Category' not in df.columns:
        df['Product_Category'] = np.random.choice(['Hardware', 'Software', 'Services', 'Subscriptions'], size=len(df), p=[0.2, 0.4, 0.1, 0.3]).tolist()
    if 'Product_Subcategory' not in df.columns:
        df['Product_Subcategory'] = np.random.choice(['Basic', 'Pro', 'Enterprise', 'Legacy'], size=len(df)).tolist()
    if 'Lifecycle_Stage' not in df.columns:
        df['Lifecycle_Stage'] = np.random.choice(['Introduction', 'Growth', 'Maturity', 'Decline'], size=len(df), p=[0.1, 0.3, 0.5, 0.1]).tolist()
    
    if 'Join_Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Join_Date'])
        df['Month'] = df['Date'].dt.to_period('M').astype(str)
    else:
        st.warning("Missing date information for forecasting.")
        return

    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Category Intelligence</h3>", unsafe_allow_html=True)

    chart_layout_config = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        title_font=dict(color='#00EEFF', family='Orbitron'),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    col_viz1, col_viz2 = st.columns(2)

    with col_viz1:
        # Category Sunburst
        fig_sunburst = px.sunburst(df, path=['Product_Category', 'Product_Subcategory', 'Lifecycle_Stage'], values='Total_Spend_CLV', title='Product Hierarchy & Lifecycle', color='Profit', color_continuous_scale='Purpor')
        fig_sunburst.update_layout(**chart_layout_config)
        st.plotly_chart(fig_sunburst, use_container_width=True)
        
        # Lifecycle Analysis
        lifecycle_sales = df.groupby('Lifecycle_Stage')['Total_Spend_CLV'].sum().reset_index()
        fig_lifecycle = px.bar(lifecycle_sales, x='Lifecycle_Stage', y='Total_Spend_CLV', title='Revenue by Lifecycle Stage', color='Lifecycle_Stage', color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_lifecycle.update_layout(**chart_layout_config, showlegend=False)
        st.plotly_chart(fig_lifecycle, use_container_width=True)

    with col_viz2:
        # Category Treemap
        fig_tree = px.treemap(df, path=['Product_Category', 'Product_Subcategory'], values='Purchase_Frequency', color='Profit', color_continuous_scale='Teal', title='Volume vs Profit Treemap')
        fig_tree.update_layout(**chart_layout_config)
        st.plotly_chart(fig_tree, use_container_width=True)

        # Inventory / Affinity Heatmap (Simulated)
        heatmap_data = df.groupby(['Product_Category', 'Lifecycle_Stage'])['Total_Spend_CLV'].sum().unstack().fillna(0)
        fig_heat = px.imshow(heatmap_data, text_auto=True, aspect="auto", title='Category Lifecycle Heatmap', color_continuous_scale='Mint')
        fig_heat.update_layout(**chart_layout_config)
        st.plotly_chart(fig_heat, use_container_width=True)

    st.divider()
    
    # Demand Forecast Section
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Demand Forecasting</h3>", unsafe_allow_html=True)
    
    demand_df = df.groupby('Month')['Purchase_Frequency'].sum().reset_index().sort_values('Month')
    
    if len(demand_df) > 3:
        demand_df['Forecast'] = demand_df['Purchase_Frequency'].rolling(window=3).mean().shift(-1)
        # Extend forecast
        last_month = pd.to_datetime(demand_df['Month'].iloc[-1])
        next_months = [(last_month + pd.DateOffset(months=i)).strftime('%Y-%m') for i in range(1, 4)]
        
        forecast_vals = [demand_df['Purchase_Frequency'].iloc[-3:].mean()]
        for i in range(2):
            forecast_vals.append(forecast_vals[-1] * np.random.uniform(0.95, 1.05))
            
        future_df = pd.DataFrame({'Month': next_months, 'Purchase_Frequency': [np.nan]*3, 'Forecast': forecast_vals})
        demand_df = pd.concat([demand_df, future_df], ignore_index=True)
        
        fig_forecast = go.Figure()
        fig_forecast.add_trace(go.Scatter(x=demand_df['Month'], y=demand_df['Purchase_Frequency'], name='Historical Demand', line=dict(color='#00EEFF', width=3)))
        fig_forecast.add_trace(go.Scatter(x=demand_df['Month'], y=demand_df['Forecast'], name='Demand Forecast (3 Months)', line=dict(color='#ec4899', width=2, dash='dash')))
        fig_forecast.update_layout(title='Aggregate Product Demand Forecast', **chart_layout_config)
        st.plotly_chart(fig_forecast, use_container_width=True)

    st.divider()

    # Dynamic Insights Section
    try:
        from src.reporting.insight_generator import InsightEngine
        insight_engine = InsightEngine()
        
        with st.spinner("Consultant Engine is analyzing product portfolio..."):
            insights = insight_engine.extract_insights(df)
            
        if insights:
            st.markdown("""
            <div style="margin-top: 2rem; background: rgba(10, 15, 36, 0.6); border: 1px solid rgba(0, 238, 255, 0.2); border-radius: 12px; padding: 1.5rem; box-shadow: 0 0 15px rgba(0,238,255,0.05);">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                    <div style="font-size: 1.5rem;">🤖</div>
                    <h3 style="color: #00EEFF; margin: 0; font-family: 'Orbitron', sans-serif;">Portfolio & Inventory Optimization</h3>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                    <div>
                        <h4 style="color: #FFFFFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">Trends & Risks</h4>
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
                st.markdown(f'<li><strong style="color: {color};">{ins.area} Optimization:</strong> {ins.recommendation}</li>', unsafe_allow_html=True)
                
            st.markdown("""
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error generating AI Insights: {e}")

    render_footer(title="Product Analytics")

if __name__ == "__main__":
    run()
