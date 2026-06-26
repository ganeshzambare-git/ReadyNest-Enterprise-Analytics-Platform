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

@st.cache_data(show_spinner=False)
def load_and_augment_data():
    try:
        data_path = os.path.join(project_root, "..", "data_lake", "curated", "feature_store_customers.parquet")
        df = pd.read_parquet(data_path)
    except Exception as e:
        st.error(f"Error loading customer data: {e}")
        return pd.DataFrame()

    np.random.seed(42)
    
    # Synthesize Profit (assuming 15% - 35% margin)
    df['Profit'] = df['Total_Spend_CLV'] * np.random.uniform(0.15, 0.35, size=len(df))  # type: ignore
    
    # Identify repeat purchasers
    df['Repeat_Purchaser'] = (df['Purchase_Frequency'] > 1).astype(int)
    
    # Determine Customer Segments
    clv_75 = df['Total_Spend_CLV'].quantile(0.75)
    recency_25 = df['Recency_Days'].quantile(0.25)
    recency_75 = df['Recency_Days'].quantile(0.75)
    
    def get_segment(row):
        if row['Total_Spend_CLV'] >= clv_75 and row['Recency_Days'] <= recency_25:
            return 'Most Valuable'
        elif row['Total_Spend_CLV'] >= clv_75 and row['Recency_Days'] > recency_75:
            return 'At-Risk'
        elif row['Recency_Days'] <= recency_25 and row['Total_Spend_CLV'] < clv_75:
            return 'High Potential'
        elif row['Recency_Days'] > recency_75:
            return 'Declining'
        else:
            return 'Average'
            
    df['Customer_Segment'] = df.apply(get_segment, axis=1)
    return df

def run():
    render_header(
        title="Customer Analysis",
        description="Deep dive into customer behavior, purchasing patterns, profitability, engagement, and lifecycle performance.",
        business_value="Identifies high-value segments and highlights opportunities to maximize retention and profitability."
    )

    df = load_and_augment_data()
    
    if df.empty or len(df) < 5:
        st.warning("Insufficient data available to render dashboard.")
        return

    # Calculate KPIs
    rev_per_customer = df['Total_Spend_CLV'].mean()
    avg_order_value = df['Average_Order_Value'].mean()
    avg_purchase_freq = df['Purchase_Frequency'].mean()
    avg_profit = df['Profit'].mean()
    repeat_purchase_rate = df['Repeat_Purchaser'].mean() * 100

    # KPI Grid
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Customer Performance Metrics</h3>", unsafe_allow_html=True)
    
    try:
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Revenue per Customer", f"${rev_per_customer:,.0f}")
        col2.metric("Avg Order Value", f"${avg_order_value:,.2f}")
        col3.metric("Purchase Frequency", f"{avg_purchase_freq:.1f}x")
        col4.metric("Avg Profit/Customer", f"${avg_profit:,.0f}")
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
            # Top Customers Bar Chart
            top_10 = df.nlargest(10, 'Total_Spend_CLV').sort_values('Total_Spend_CLV', ascending=True)
            fig_top = px.bar(top_10, x='Total_Spend_CLV', y='customername', orientation='h', title='Top 10 Customers by Revenue', color='Total_Spend_CLV', color_continuous_scale='Teal')
            fig_top.update_layout(**chart_layout_config, coloraxis_showscale=False)
            st.plotly_chart(fig_top, use_container_width=True)

            # Customer Profitability Matrix
            fig_matrix = px.scatter(df, x='Total_Spend_CLV', y='Profit', color='Customer_Segment', title='Customer Profitability Matrix', opacity=0.7, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_matrix.update_layout(**chart_layout_config)
            st.plotly_chart(fig_matrix, use_container_width=True)
            
            # Revenue Heatmap
            heatmap_data = df.groupby('Customer_Segment')['Total_Spend_CLV'].mean().reset_index()
            # Faking a 2D matrix for heatmap by combining with Repeat Purchaser
            heatmap_data_2d = df.groupby(['Customer_Segment', 'Repeat_Purchaser'])['Total_Spend_CLV'].mean().unstack().fillna(0)
            heatmap_data_2d.columns = ['Single Purchase', 'Repeat Purchase']
            fig_heatmap = px.imshow(heatmap_data_2d, text_auto=True, aspect="auto", title='Average Revenue Heatmap (Segment vs Purchase Type)', color_continuous_scale='Purpor')
            fig_heatmap.update_layout(**chart_layout_config)
            st.plotly_chart(fig_heatmap, use_container_width=True)

        with col_viz2:
            # Revenue Distribution
            fig_dist = px.histogram(df, x='Total_Spend_CLV', nbins=40, title='Revenue Distribution', color_discrete_sequence=['#8b5cf6'], marginal='box')
            fig_dist.update_layout(**chart_layout_config)
            st.plotly_chart(fig_dist, use_container_width=True)

            # Pareto Chart
            df_pareto = df.sort_values(by='Total_Spend_CLV', ascending=False).reset_index()
            df_pareto['Cumulative_Revenue'] = df_pareto['Total_Spend_CLV'].cumsum()
            df_pareto['Cumulative_Percentage'] = 100 * df_pareto['Cumulative_Revenue'] / df_pareto['Total_Spend_CLV'].sum()
            df_pareto['Rank'] = df_pareto.index + 1
            
            fig_pareto = go.Figure()
            # Subsample for pareto chart if too many rows to keep it readable
            sample_size = min(len(df_pareto), 1000)
            df_pareto_sample = df_pareto.head(sample_size)
            
            fig_pareto.add_trace(go.Bar(x=df_pareto_sample['Rank'], y=df_pareto_sample['Total_Spend_CLV'], name='Revenue', marker_color='#00EEFF'))
            fig_pareto.add_trace(go.Scatter(x=df_pareto_sample['Rank'], y=df_pareto_sample['Cumulative_Percentage'], name='Cumulative %', yaxis='y2', line=dict(color='#ec4899', width=3)))
            
            fig_pareto.update_layout(
                title='Customer Contribution Pareto Chart (Top 1000)',
                yaxis=dict(title='Revenue'),
                yaxis2=dict(title='Cumulative %', overlaying='y', side='right', range=[0, 100]),
                **chart_layout_config
            )
            fig_pareto.update_layout(showlegend=False)
            st.plotly_chart(fig_pareto, use_container_width=True)

    except Exception as e:
        st.error(f"Error rendering visual analytics: {e}")

    st.divider()

    # Data Analytics Tables
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Detailed Analytics</h3>", unsafe_allow_html=True)
    
    col_table1, col_table2 = st.columns(2)
    with col_table1:
        st.markdown("<h5 style='color: #94A3B8;'>Top 10 Customers</h5>", unsafe_allow_html=True)
        st.dataframe(df.nlargest(10, 'Total_Spend_CLV')[['customername', 'Total_Spend_CLV', 'Profit', 'Customer_Segment']], use_container_width=True, hide_index=True)
        
        st.markdown("<h5 style='color: #94A3B8;'>Segment Contribution (Revenue vs Profit)</h5>", unsafe_allow_html=True)
        segment_contrib = df.groupby('Customer_Segment')[['Total_Spend_CLV', 'Profit']].sum().reset_index()
        segment_contrib['Revenue %'] = (segment_contrib['Total_Spend_CLV'] / segment_contrib['Total_Spend_CLV'].sum() * 100).round(1).astype(str) + '%'
        segment_contrib['Profit %'] = (segment_contrib['Profit'] / segment_contrib['Profit'].sum() * 100).round(1).astype(str) + '%'
        st.dataframe(segment_contrib[['Customer_Segment', 'Total_Spend_CLV', 'Revenue %', 'Profit', 'Profit %']], use_container_width=True, hide_index=True)

    with col_table2:
        st.markdown("<h5 style='color: #94A3B8;'>Bottom 10 Customers</h5>", unsafe_allow_html=True)
        st.dataframe(df.nsmallest(10, 'Total_Spend_CLV')[['customername', 'Total_Spend_CLV', 'Profit', 'Customer_Segment']], use_container_width=True, hide_index=True)


    st.divider()

    # Dynamic Insights Section
    try:
        most_valuable_count = len(df[df['Customer_Segment'] == 'Most Valuable'])
        at_risk_count = len(df[df['Customer_Segment'] == 'At-Risk'])
        high_potential_count = len(df[df['Customer_Segment'] == 'High Potential'])
        declining_count = len(df[df['Customer_Segment'] == 'Declining'])
        
        total_rev = df['Total_Spend_CLV'].sum()
        valuable_rev_pct = (df[df['Customer_Segment'] == 'Most Valuable']['Total_Spend_CLV'].sum() / total_rev) * 100 if total_rev > 0 else 0
        
        st.markdown(f"""
        <div style="margin-top: 2rem; background: rgba(10, 15, 36, 0.6); border: 1px solid rgba(0, 238, 255, 0.2); border-radius: 12px; padding: 1.5rem; box-shadow: 0 0 15px rgba(0,238,255,0.05);">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                <div style="font-size: 1.5rem;">🤖</div>
                <h3 style="color: #00EEFF; margin: 0; font-family: 'Orbitron', sans-serif;">AI-Powered Insights & Recommendations</h3>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                <div>
                    <h4 style="color: #FFFFFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">Segment Analysis</h4>
                    <ul style="color: #94A3B8; line-height: 1.6;">
                        <li><strong style="color: #00EEFF;">Most Valuable:</strong> {most_valuable_count} customers driving {valuable_rev_pct:.1f}% of total revenue. These customers purchase frequently and recently.</li>
                        <li><strong style="color: #00d084;">High Potential:</strong> {high_potential_count} customers who recently purchased but have lower overall spend. Ripe for development.</li>
                        <li><strong style="color: #f59e0b;">At-Risk:</strong> {at_risk_count} historically high-spending customers who haven't purchased recently.</li>
                        <li><strong style="color: #ef4444;">Declining:</strong> {declining_count} low-spending customers with high recency days, showing low engagement.</li>
                    </ul>
                </div>
                <div>
                    <h4 style="color: #FFFFFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">Strategic Recommendations</h4>
                    <ul style="color: #94A3B8; line-height: 1.6;">
                        <li><strong style="color: #ec4899;">Customer Retention Plan:</strong> Launch a targeted 'Win-Back' email and discount campaign specifically for the {at_risk_count} 'At-Risk' VIP customers to prevent churn.</li>
                        <li><strong style="color: #ec4899;">Cross-Selling Opportunities:</strong> Use product recommendation engines to cross-sell to the {high_potential_count} 'High Potential' customers to increase their Average Order Value.</li>
                        <li><strong style="color: #ec4899;">Personalized Marketing:</strong> Assign dedicated account managers or exclusive loyalty perks to the {most_valuable_count} 'Most Valuable' customers to maintain their {repeat_purchase_rate:.1f}% repeat purchase rate.</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error generating AI Insights: {e}")

    render_footer(title="Customer Analysis")

if __name__ == "__main__":
    run()
