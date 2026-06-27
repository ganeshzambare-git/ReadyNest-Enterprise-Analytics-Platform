import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
from sklearn.preprocessing import StandardScaler  # type: ignore
from sklearn.cluster import KMeans, AgglomerativeClustering  # type: ignore

from src.app.components.module_template import render_header, render_footer
from src.app.data_store import get_augmented_data

@st.cache_data(show_spinner=False)
def compute_kpis(df_final):
    return {
        'total_customers': len(df_final),
        'champions_count': len(df_final[df_final['Segment'] == 'Champions']),
        'at_risk_count': len(df_final[df_final['Segment'] == 'At Risk']),
        'total_rev': df_final['Total_Spend_CLV'].sum()
    }

@st.cache_data(show_spinner=False)
def calculate_rfm(df):
    # Ensure necessary columns exist
    cols = ['Recency_Days', 'Purchase_Frequency', 'Total_Spend_CLV']
    if not all(col in df.columns for col in cols):
        st.error("Missing required RFM columns in dataset.")
        return df

    # Calculate Quantiles
    r_labels = range(4, 0, -1) # Recency: lower is better
    f_labels = range(1, 5)     # Frequency: higher is better
    m_labels = range(1, 5)     # Monetary: higher is better

    # qcut can sometimes fail with duplicate edges if data is highly skewed, rank(method='first') fixes it
    r_quartiles = pd.qcut(df['Recency_Days'].rank(method='first'), q=4, labels=r_labels)
    f_quartiles = pd.qcut(df['Purchase_Frequency'].rank(method='first'), q=4, labels=f_labels)
    m_quartiles = pd.qcut(df['Total_Spend_CLV'].rank(method='first'), q=4, labels=m_labels)

    rfm = df.copy()
    rfm['R'] = r_quartiles.astype(int)
    rfm['F'] = f_quartiles.astype(int)
    rfm['M'] = m_quartiles.astype(int)
    
    rfm['RFM_Score'] = rfm['R'].map(str) + rfm['F'].map(str) + rfm['M'].map(str)
    
    # Segment definition function
    def segment_customer(row):
        score = int(row['RFM_Score'])
        r, f, m = row['R'], row['F'], row['M']
        if score >= 444:
            return 'Champions'
        elif score >= 333:
            return 'Loyal Customers'
        elif r >= 3 and f <= 2:
            return 'New Customers'
        elif r <= 2 and r >= 1 and f >= 3:
            return 'At Risk'
        elif r <= 2 and f <= 2:
            return 'Lost Customers'
        else:
            return 'Potential Loyalists'
            
    rfm['Segment'] = rfm.apply(segment_customer, axis=1)
    return rfm

@st.cache_data(show_spinner=False)
def ml_segmentation(df):
    cols = ['Recency_Days', 'Purchase_Frequency', 'Total_Spend_CLV']
    rfm_data = df[cols].copy()
    
    # Handling any potential NaNs or infs
    rfm_data = rfm_data.replace([np.inf, -np.inf], np.nan).dropna()
    
    # Scale Data
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(rfm_data)
    
    # KMeans Clustering
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    kmeans_labels = kmeans.fit_predict(scaled_features)
    
    # Hierarchical Clustering (Sampled if dataset is too large, but assume it's okay for now)
    # Using 4 clusters to compare with KMeans
    agglo = AgglomerativeClustering(n_clusters=4)
    agglo_labels = agglo.fit_predict(scaled_features)
    
    result_df = df.loc[rfm_data.index].copy()
    result_df['KMeans_Cluster'] = kmeans_labels
    result_df['Hierarchical_Cluster'] = agglo_labels
    
    # Map K-Means clusters to personas based on centroids
    centroids = scaler.inverse_transform(kmeans.cluster_centers_)
    centroid_df = pd.DataFrame(centroids, columns=cols)
    
    # Identify personas by sorting centroid attributes
    personas = {}
    for i in range(4):
        c = centroid_df.iloc[i]
        # High M, High F, Low R
        if c['Total_Spend_CLV'] >= centroid_df['Total_Spend_CLV'].median() and c['Recency_Days'] <= centroid_df['Recency_Days'].median():
            personas[i] = "Whales"
        elif c['Purchase_Frequency'] >= centroid_df['Purchase_Frequency'].median():
            personas[i] = "Frequent Buyers"
        elif c['Recency_Days'] > centroid_df['Recency_Days'].median():
            personas[i] = "Slipping Away"
        else:
            personas[i] = "Average Users"
            
    # Guarantee unique names if heuristic overlapped
    unique_personas = list(set(personas.values()))
    if len(unique_personas) < 4:
        personas = {0: "Cluster A", 1: "Cluster B", 2: "Cluster C", 3: "Cluster D"} # Fallback

    result_df['Persona'] = result_df['KMeans_Cluster'].map(personas)
    return result_df, centroid_df, personas

def render_visualizations(df, chart_layout_config):
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Visual Analytics</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # 1. Segment Distribution
    with col1:
        segment_counts = df['Segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Count']
        fig_dist = px.pie(
            segment_counts, 
            values='Count', 
            names='Segment', 
            hole=0.4,
            title='RFM Segment Distribution',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_dist.update_layout(**chart_layout_config)
        st.plotly_chart(fig_dist, use_container_width=True)

    # 2. Revenue Contribution by Segment
    with col2:
        rev_by_seg = df.groupby('Segment')['Total_Spend_CLV'].sum().reset_index()
        fig_rev = px.bar(
            rev_by_seg, 
            x='Segment', 
            y='Total_Spend_CLV',
            title='Revenue Contribution by Segment',
            text_auto='.2s',
            color='Segment',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_rev.update_layout(**chart_layout_config, showlegend=False)
        fig_rev.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(fig_rev, use_container_width=True)
        
    col3, col4 = st.columns(2)
    
    # 3. Cluster Scatter Plot (ML Segments)
    with col3:
        # Taking a sample if dataset is too large for 3D scatter
        sample_df = df.sample(n=min(100000, len(df)), random_state=42) if len(df) > 100000 else df
        fig_scatter = px.scatter_3d(
            sample_df,
            x='Recency_Days',
            y='Purchase_Frequency',
            z='Total_Spend_CLV',
            color='Persona',
            title='ML Customer Clusters (K-Means)',
            opacity=0.7,
            size_max=10,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_scatter.update_layout(
            **chart_layout_config,
            scene=dict(
                xaxis_title='Recency (Days)',
                yaxis_title='Frequency',
                zaxis_title='Monetary (CLV)',
                bgcolor='rgba(0,0,0,0)'
            ),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # 4. Customer Value Matrix
    with col4:
        fig_matrix = px.scatter(
            sample_df,
            x='Recency_Days',
            y='Purchase_Frequency',
            size='Total_Spend_CLV',
            color='Segment',
            title='Customer Value Matrix (Bubble Size = Value)',
            hover_name='customername' if 'customername' in sample_df.columns else None,
            opacity=0.7,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        # Recency is better when smaller, so we reverse the x-axis
        fig_matrix.update_layout(**chart_layout_config)
        fig_matrix.update_xaxes(autorange="reversed", title='Recency (Days - Reversed)')
        fig_matrix.update_yaxes(title='Purchase Frequency')
        st.plotly_chart(fig_matrix, use_container_width=True)

def render_insights_and_recommendations(df):
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px; margin-top: 30px;'>Strategic Insights & Recommendations</h3>", unsafe_allow_html=True)
    
    # Calculate Insights
    rev_by_seg = df.groupby('Segment')['Total_Spend_CLV'].sum()
    most_profitable = rev_by_seg.idxmax()
    
    # Highest growth potential (New Customers or Potential Loyalists usually)
    growth_seg = 'Potential Loyalists' if 'Potential Loyalists' in df['Segment'].values else most_profitable
    
    churn_risk = 'At Risk' if 'At Risk' in df['Segment'].values else 'Lost Customers'
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style='background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10B981; padding: 15px; border-radius: 4px;'>
            <h4 style='color: #10B981; margin:0 0 10px 0;'>🏆 Most Profitable</h4>
            <h2 style='color: white; margin: 0;'>{most_profitable}</h2>
            <p style='color: #94A3B8; font-size: 0.9em; margin-top: 10px;'>Generates the highest overall revenue. Focus on premium rewards and VIP experiences to retain these champions.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style='background: rgba(59, 130, 246, 0.1); border-left: 4px solid #3B82F6; padding: 15px; border-radius: 4px;'>
            <h4 style='color: #3B82F6; margin:0 0 10px 0;'>🚀 Highest Growth</h4>
            <h2 style='color: white; margin: 0;'>{growth_seg}</h2>
            <p style='color: #94A3B8; font-size: 0.9em; margin-top: 10px;'>Recent engagements show promise. Target with cross-sell campaigns to convert them into loyalists.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style='background: rgba(239, 68, 68, 0.1); border-left: 4px solid #EF4444; padding: 15px; border-radius: 4px;'>
            <h4 style='color: #EF4444; margin:0 0 10px 0;'>⚠️ Churn Risk</h4>
            <h2 style='color: white; margin: 0;'>{churn_risk}</h2>
            <p style='color: #94A3B8; font-size: 0.9em; margin-top: 10px;'>High past value but declining frequency. Deploy immediate win-back campaigns and personalized discounts.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h4 style='color: #00EEFF; margin-top: 30px;'>AI-Powered Marketing Strategies</h4>", unsafe_allow_html=True)
    
    try:
        from src.reporting.insight_generator import InsightEngine
        insight_engine = InsightEngine()
        
        with st.spinner("Consultant Engine is analyzing segmentation clusters..."):
            insights = insight_engine.extract_insights(df)
            
        if insights:
            st.markdown("""
            <div style="background: rgba(10, 15, 36, 0.6); border: 1px solid rgba(0, 238, 255, 0.2); border-radius: 12px; padding: 1.5rem; box-shadow: 0 0 15px rgba(0,238,255,0.05);">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                    <div>
                        <h4 style="color: #FFFFFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">Segment Analysis</h4>
                        <ul style="color: #94A3B8; line-height: 1.6;">
            """, unsafe_allow_html=True)
            
            for ins in insights[:4]:
                color = "#00d084" if ins.category == "Opportunity" else "#ec4899" if ins.category == "Risk" else "#3B82F6"
                st.markdown(f'<li><strong style="color: {color};">{ins.title}:</strong> {ins.business_impact}</li>', unsafe_allow_html=True)
                
            st.markdown("""
                        </ul>
                    </div>
                    <div>
                        <h4 style="color: #FFFFFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">Actionable Strategies</h4>
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


def run():
    render_header(
        title="Customer Segmentation",
        description="Automatically segment customers into meaningful groups for business decision-making using RFM heuristics and ML clustering.",
        business_value="Enables hyper-personalized marketing campaigns, lifting conversion by up to 25% and reducing churn through targeted interventions."
    )

    df_raw = get_augmented_data()
    
    if df_raw.empty:
        st.warning("No customer data available to segment.")
        render_footer(title="Customer Segmentation")
        return

    with st.spinner("Running segmentation models..."):
        # Run RFM
        df_rfm = calculate_rfm(df_raw)
        
        # Run ML Segmentation
        df_final, centroids, personas = ml_segmentation(df_rfm)

    # KPI Summary Row
    st.markdown("<h3 style='color: #FFFFFF; font-family: \"Orbitron\", sans-serif; margin-bottom: 20px;'>Segmentation Overview</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    kpis = compute_kpis(df_final)
    total_customers = kpis['total_customers']
    champions_count = kpis['champions_count']
    at_risk_count = kpis['at_risk_count']
    total_rev = kpis['total_rev']
    
    col1.metric("Total Customers Segmented", f"{total_customers:,}")
    col2.metric("Champions", f"{champions_count:,}", f"{(champions_count/total_customers)*100:.1f}% of base")
    col3.metric("At-Risk Customers", f"{at_risk_count:,}", f"{(at_risk_count/total_customers)*100:.1f}% of base", delta_color="inverse")
    col4.metric("Total Customer Value", f"${total_rev:,.0f}")

    st.divider()

    chart_layout_config = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        title_font=dict(color='#00EEFF', family='Orbitron'),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    render_visualizations(df_final, chart_layout_config)
    
    render_insights_and_recommendations(df_final)
    
    render_footer(title="Customer Segmentation")

if __name__ == "__main__":
    run()
