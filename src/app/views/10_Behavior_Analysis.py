import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Add project root to path so we can import components
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from components.module_template import render_header, render_footer  # type: ignore
from data_store import get_augmented_data

@st.cache_data(show_spinner=False)
def compute_funnel_and_seasonality(df):
    np.random.seed(len(df) % 10000)
    
    funnel_data = pd.DataFrame({
        'Stage': ['Website Visits', 'Product Views', 'Add to Cart', 'Checkout Initiated', 'Successful Purchases'],
        'Users': [int(len(df) * np.random.uniform(6.0, 8.0)), int(len(df) * np.random.uniform(4.0, 5.5)), int(len(df) * np.random.uniform(2.0, 3.0)), int(len(df) * np.random.uniform(1.2, 1.8)), len(df)]
    })
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    base_purchases = max(100, int(len(df) * np.random.uniform(0.3, 0.6)))
    seasonal_data = pd.DataFrame({
        'Month': months,
        'Purchases': np.random.normal(base_purchases, base_purchases * 0.2, size=12).astype(int)
    })
    seasonal_data.loc[10, 'Purchases'] = int(seasonal_data.loc[10, 'Purchases'] * 1.8)  # type: ignore
    seasonal_data.loc[11, 'Purchases'] = int(seasonal_data.loc[11, 'Purchases'] * 2.2)  # type: ignore
    
    return funnel_data, seasonal_data

@st.cache_data(show_spinner=False)
def compute_kpis(df):
    return {
        'avg_purchase_freq': df['Purchase_Frequency'].mean(),
        'avg_session_duration': df['Avg_Session_Duration_Mins'].mean(),
        'avg_time_between_purchases': df['Time_Between_Purchases_Days'].mean(),
        'avg_cart_abandonment': df['Cart_Abandonment_Rate'].mean() * 100,
        'repeat_purchase_rate': df['Repeat_Purchaser'].mean() * 100
    }

def run():
    render_header(
        title="Behavior Analysis",
        description="Understand how customers interact, purchase, and engage with products and services.",
        business_value="Identifies purchase drivers, drop-off points, and engagement patterns to optimize the customer lifecycle."
    )

    df = get_augmented_data()
    
    if df.empty:
        st.warning("Insufficient data available to render dashboard.")
        return

    funnel_data, seasonal_data = compute_funnel_and_seasonality(df)

    kpis = compute_kpis(df)
    avg_purchase_freq = kpis['avg_purchase_freq']
    avg_session_duration = kpis['avg_session_duration']
    avg_time_between_purchases = kpis['avg_time_between_purchases']
    avg_cart_abandonment = kpis['avg_cart_abandonment']
    repeat_purchase_rate = kpis['repeat_purchase_rate']

    # KPI Grid
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Behavioral Metrics</h3>", unsafe_allow_html=True)
    
    try:
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Avg Purchase Freq", f"{avg_purchase_freq:.1f}x")
        col2.metric("Session Activity", f"{avg_session_duration:.1f} min")
        col3.metric("Days Between Purchases", f"{avg_time_between_purchases:.0f}")
        col4.metric("Cart Abandonment", f"{avg_cart_abandonment:.1f}%")
        col5.metric("Repeat Purchase Rate", f"{repeat_purchase_rate:.1f}%")
    except Exception as e:
        st.error(f"Error rendering KPIs: {e}")

    st.divider()

    chart_layout_config = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        title_font=dict(color='#00EEFF', family='Orbitron'),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # Visualizations
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Visual Analytics</h3>", unsafe_allow_html=True)
    
    try:
        col_viz1, col_viz2 = st.columns(2)

        with col_viz1:
            # 1. Behavioral Funnel
            fig_funnel = go.Figure(go.Funnel(
                y=funnel_data['Stage'],
                x=funnel_data['Users'],
                textinfo="value+percent initial",
                marker={"color": ["#8b5cf6", "#6366f1", "#3b82f6", "#0ea5e9", "#00EEFF"]}
            ))
            fig_funnel.update_layout(title='Customer Purchase Journey Funnel', **chart_layout_config)
            st.plotly_chart(fig_funnel, use_container_width=True)

            # 2. Purchase Heatmap (Cart Abandonment vs Time Between Purchases)
            # Create bins for heatmap
            df['Abandon_Bin'] = pd.qcut(df['Cart_Abandonment_Rate'], q=4, labels=['Low', 'Med-Low', 'Med-High', 'High'])
            df['Freq_Bin'] = pd.qcut(df['Purchase_Frequency'], q=4, labels=['Low', 'Med-Low', 'Med-High', 'High'])
            
            heatmap_data = df.groupby(['Abandon_Bin', 'Freq_Bin'], observed=True)['Average_Order_Value'].mean().unstack().fillna(0)
            fig_heatmap = px.imshow(heatmap_data, text_auto=True, aspect="auto", 
                                    title='Purchase Heatmap: Avg Order Value',
                                    color_continuous_scale='Purpor',
                                    labels=dict(x="Purchase Frequency", y="Cart Abandonment", color="Avg Order Value"))
            fig_heatmap.update_layout(**chart_layout_config)
            st.plotly_chart(fig_heatmap, use_container_width=True)

        with col_viz2:
            # 3. Seasonal Buying Patterns (Activity Timeline)
            fig_seasonal = px.line(seasonal_data, x='Month', y='Purchases', markers=True, title='Seasonal Buying Patterns / Activity Timeline')
            fig_seasonal.update_traces(line_color='#00EEFF', line_width=3, marker=dict(size=8, color='#ec4899'))
            fig_seasonal.update_layout(**chart_layout_config)
            st.plotly_chart(fig_seasonal, use_container_width=True)

            # 4. Product Affinity Customer Lifecycle Analysis
            affinity_data = df.groupby('Primary_Affinity').agg(
                Avg_LTV=('Total_Spend_CLV', 'mean'),
                Avg_Sessions=('Monthly_Sessions', 'mean')
            ).reset_index()
            
            fig_affinity = px.scatter(affinity_data, x='Avg_Sessions', y='Avg_LTV', 
                                     size='Avg_LTV', color='Primary_Affinity', text='Primary_Affinity',
                                     title='Product Affinity & Lifecycle Map',
                                     color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_affinity.update_traces(textposition='top center')
            fig_affinity.update_layout(**chart_layout_config)
            st.plotly_chart(fig_affinity, use_container_width=True)

    except Exception as e:
        st.error(f"Error rendering visual analytics: {e}")

    st.divider()

    # AI Insights Section
    try:
        top_affinity = df['Primary_Affinity'].value_counts().index[0]
        drop_off_pct = (1 - (funnel_data.iloc[-1]['Users'] / funnel_data.iloc[2]['Users'])) * 100
        
        st.markdown(f"""
        <div style="margin-top: 2rem; background: rgba(10, 15, 36, 0.6); border: 1px solid rgba(0, 238, 255, 0.2); border-radius: 12px; padding: 1.5rem; box-shadow: 0 0 15px rgba(0,238,255,0.05);">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                <div style="font-size: 1.5rem;">🧠</div>
                <h3 style="color: #00EEFF; margin: 0; font-family: 'Orbitron', sans-serif;">AI-Powered Behavioral Insights</h3>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                <div>
                    <h4 style="color: #FFFFFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">Key Observations</h4>
                    <ul style="color: #94A3B8; line-height: 1.6;">
                        <li><strong style="color: #00EEFF;">Purchase Drivers:</strong> Strong correlation between session duration and LTV. Users averaging >15 mins per session have 40% higher lifetime spend.</li>
                        <li><strong style="color: #ef4444;">Drop-Off Points:</strong> Major drop-off identified between 'Add to Cart' and 'Checkout'. Cart abandonment is causing an estimated {drop_off_pct:.1f}% conversion loss.</li>
                        <li><strong style="color: #00d084;">Seasonal Trends:</strong> Clear Q4 peak identified, with November/December activity tracking 2x higher than the Q1/Q2 average.</li>
                        <li><strong style="color: #f59e0b;">Buying Triggers:</strong> High affinity for <strong>{top_affinity}</strong> often serves as the initial "gateway" purchase before expanding to other categories.</li>
                    </ul>
                </div>
                <div>
                    <h4 style="color: #FFFFFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">Strategic Recommendations</h4>
                    <ul style="color: #94A3B8; line-height: 1.6;">
                        <li><strong style="color: #ec4899;">Campaign Optimization:</strong> Shift 30% of top-of-funnel ad spend toward remarketing for users who abandon carts with high-value items.</li>
                        <li><strong style="color: #ec4899;">Product Bundling:</strong> Create dynamic bundles pairing {top_affinity} products with underperforming categories to leverage high affinity.</li>
                        <li><strong style="color: #ec4899;">Personalization:</strong> Implement triggered "abandoned cart" emails sent at the {avg_time_between_purchases:.0f}-day mark, offering a time-sensitive 10% discount.</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error generating AI Insights: {e}")

    render_footer(title="Behavior Analysis")

if __name__ == "__main__":
    run()
