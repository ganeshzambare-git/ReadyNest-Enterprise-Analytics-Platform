import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

from src.app.components.module_template import render_header, render_footer
from src.app.data_store import get_augmented_data

def apply_global_filters(df, filters):
    filtered = df.copy()
    if filters['region'] and 'All' not in filters['region']:
        filtered = filtered[filtered['Region'].isin(filters['region'])]
    if filters['product'] and 'All' not in filters['product']:
        filtered = filtered[filtered['Product_Category'].isin(filters['product'])]
    if filters['segment'] and 'All' not in filters['segment']:
        filtered = filtered[filtered['Customer_Segment'].isin(filters['segment'])]
    return filtered

def run():
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="color: #00EEFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">Interactive Command Center</h1>
        <p style="color: #94A3B8; font-size: 1.1rem; margin-bottom: 1rem;">Centralized executive dashboard with global filtering and multidimensional drill-down capabilities.</p>
    </div>
    """, unsafe_allow_html=True)

    df = get_augmented_data()
    
    if df.empty:
        st.warning("Insufficient data available.")
        return
        
    # Generate synthetic categorical dimensions if missing
    np.random.seed(42)
    if 'Region' not in df.columns:
        df['Region'] = np.random.choice(['North America', 'Europe', 'Asia Pacific', 'Latin America'], size=len(df), p=[0.4, 0.3, 0.2, 0.1])
    if 'Product_Category' not in df.columns:
        df['Product_Category'] = np.random.choice(['Hardware', 'Software', 'Services', 'Subscriptions'], size=len(df), p=[0.2, 0.4, 0.1, 0.3])
    if 'Customer_Segment' not in df.columns:
        df['Customer_Segment'] = np.random.choice(['Enterprise', 'Mid-Market', 'SMB', 'Startup'], size=len(df), p=[0.2, 0.3, 0.4, 0.1])

    # Global Filters Toolbar
    st.markdown("""
    <div style="background: rgba(10, 15, 36, 0.8); border: 1px solid rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-bottom: 20px;">
        <h4 style="color: #00EEFF; font-family: 'Orbitron', sans-serif; margin-top: 0;">Global Filters</h4>
    </div>
    """, unsafe_allow_html=True)
    
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    with f_col1:
        regions = ['All'] + list(df['Region'].unique())
        selected_regions = st.multiselect("Region", regions, default=['All'])
    with f_col2:
        products = ['All'] + list(df['Product_Category'].unique())
        selected_products = st.multiselect("Product Category", products, default=['All'])
    with f_col3:
        segments = ['All'] + list(df['Customer_Segment'].unique())
        selected_segments = st.multiselect("Customer Segment", segments, default=['All'])
    with f_col4:
        st.write("Date Range")
        date_range = st.date_input("Select Range", value=[], key='global_dates')

    # Apply Filters
    filters = {
        'region': selected_regions,
        'product': selected_products,
        'segment': selected_segments
    }
    
    filtered_df = apply_global_filters(df, filters)
    
    if filtered_df.empty:
        st.warning("No data matches the selected filters.")
        return

    # Dashboard Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Revenue Dashboard", "👥 Customer Dashboard", "📦 Product Dashboard", "🗺️ Geographic Dashboard"])

    chart_layout_config = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        title_font=dict(color='#00EEFF', family='Orbitron'),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # 1. REVENUE DASHBOARD
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        rc1, rc2, rc3, rc4 = st.columns(4)
        total_rev = filtered_df['Total_Spend_CLV'].sum()
        total_profit = filtered_df['Profit'].sum()
        margin = (total_profit / total_rev * 100) if total_rev > 0 else 0
        
        rc1.metric("Total Revenue", f"${total_rev:,.0f}")
        rc2.metric("Total Profit", f"${total_profit:,.0f}")
        rc3.metric("Profit Margin", f"{margin:.1f}%")
        rc4.metric("Avg Order Value", f"${filtered_df['Average_Order_Value'].mean():,.2f}")
        
        c1, c2 = st.columns(2)
        with c1:
            fig_rev = px.histogram(filtered_df, x='Total_Spend_CLV', title='Revenue Distribution', nbins=30, color_discrete_sequence=['#00EEFF'])
            fig_rev.update_layout(**chart_layout_config)
            st.plotly_chart(fig_rev, use_container_width=True)
        with c2:
            rev_by_segment = filtered_df.groupby('Customer_Segment')['Total_Spend_CLV'].sum().reset_index()
            fig_seg = px.pie(rev_by_segment, values='Total_Spend_CLV', names='Customer_Segment', hole=0.5, title='Revenue by Segment', color_discrete_sequence=px.colors.sequential.Mint)
            fig_seg.update_layout(**chart_layout_config)
            st.plotly_chart(fig_seg, use_container_width=True)

    # 2. CUSTOMER DASHBOARD
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        cc1, cc2, cc3 = st.columns(3)
        cc1.metric("Total Customers", f"{len(filtered_df):,}")
        cc2.metric("Repeat Purchasers", f"{filtered_df['Repeat_Purchaser'].sum():,}")
        cc3.metric("Avg Recency (Days)", f"{filtered_df['Recency_Days'].mean():.0f}")
        
        c1, c2 = st.columns(2)
        with c1:
            fig_scatter = px.scatter(filtered_df, x='Recency_Days', y='Total_Spend_CLV', color='Customer_Segment', title='Customer Recency vs Value', size='Purchase_Frequency')
            fig_scatter.update_layout(**chart_layout_config)
            st.plotly_chart(fig_scatter, use_container_width=True)
        with c2:
            fig_box = px.box(filtered_df, x='Customer_Segment', y='Total_Spend_CLV', color='Customer_Segment', title='Spend Distribution by Segment')
            fig_box.update_layout(**chart_layout_config)
            st.plotly_chart(fig_box, use_container_width=True)

    # 3. PRODUCT DASHBOARD
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        prod_perf = filtered_df.groupby('Product_Category').agg({'Total_Spend_CLV': 'sum', 'Profit': 'sum', 'Purchase_Frequency': 'sum'}).reset_index()
        
        c1, c2 = st.columns([2, 1])
        with c1:
            fig_prod = px.bar(prod_perf, x='Product_Category', y=['Total_Spend_CLV', 'Profit'], title='Revenue and Profit by Product Category', barmode='group', color_discrete_sequence=['#00EEFF', '#ec4899'])
            fig_prod.update_layout(**chart_layout_config)
            st.plotly_chart(fig_prod, use_container_width=True)
        with c2:
            st.dataframe(prod_perf, use_container_width=True, hide_index=True)

    # 4. GEOGRAPHIC DASHBOARD
    with tab4:
        st.markdown("<br>", unsafe_allow_html=True)
        reg_perf = filtered_df.groupby('Region')['Total_Spend_CLV'].sum().reset_index()
        fig_geo = px.treemap(reg_perf, path=['Region'], values='Total_Spend_CLV', title='Geographic Revenue Concentration', color='Total_Spend_CLV', color_continuous_scale='Purpor')
        fig_geo.update_layout(**chart_layout_config)
        st.plotly_chart(fig_geo, use_container_width=True)

    st.divider()
    
    # Global Export
    col1, col2, col3, col4 = st.columns([1, 1, 1, 5])
    with col1:
        st.button("📄 Export PDF", key="btn_pdf_interactive", use_container_width=True)
    with col2:
        st.button("📊 Export Excel", key="btn_excel_interactive", use_container_width=True)
    with col3:
        st.button("📑 Export PPT", key="btn_ppt_interactive", use_container_width=True)
        
    # Real-Time AI Insights Panel
    try:
        from src.reporting.insight_generator import InsightEngine
        insight_engine = InsightEngine()
        
        with st.spinner("Generating insights based on current filters..."):
            insights = insight_engine.extract_insights(filtered_df)
            
        if insights:
            st.markdown("""
            <div style="margin-top: 2rem; background: rgba(0, 238, 255, 0.05); border-left: 4px solid #00EEFF; padding: 1.5rem; border-radius: 4px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                    <div style="font-size: 1.5rem;">🤖</div>
                    <h3 style="color: #00EEFF; margin: 0; font-family: 'Orbitron', sans-serif;">Dynamic Command Center Insights</h3>
                </div>
                <ul style="color: #94A3B8; line-height: 1.6;">
            """, unsafe_allow_html=True)
            
            for ins in insights[:4]:
                color = "#ec4899" if ins.priority_level == "High" else "#00d084"
                st.markdown(f'<li><strong style="color: {color};">[{ins.priority_level} Priority] {ins.title}:</strong> {ins.business_impact} - {ins.recommendation}</li>', unsafe_allow_html=True)
                
            st.markdown("""
                </ul>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error generating dynamic insights: {e}")

if __name__ == "__main__":
    run()
