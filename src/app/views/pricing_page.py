import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pricing - ReadyNest", page_icon="💳", layout="wide")

st.markdown("""
<style>
    .pricing-header {
        text-align: center;
        margin-bottom: 3rem;
    }
    .pricing-header h1 {
        color: #00EEFF !important;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    .pricing-header p {
        color: #94A3B8;
        font-size: 1.2rem;
    }
    .tier-card {
        background: rgba(10, 15, 36, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        height: 100%;
        transition: transform 0.3s;
    }
    .tier-card:hover {
        transform: translateY(-5px);
        border-color: #00EEFF;
        box-shadow: 0 0 20px rgba(0, 238, 255, 0.2);
    }
    .tier-card.popular {
        border-color: #00d084;
        position: relative;
    }
    .tier-card.popular::before {
        content: 'MOST POPULAR';
        position: absolute;
        top: -12px;
        left: 50%;
        transform: translateX(-50%);
        background: #00d084;
        color: #03142e;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .tier-name {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .tier-price {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FFFFFF;
        margin-bottom: 1rem;
    }
    .tier-price span {
        font-size: 1rem;
        color: #94A3B8;
    }
    .tier-features {
        list-style: none;
        padding: 0;
        margin: 0 0 2rem 0;
        text-align: left;
    }
    .tier-features li {
        margin-bottom: 0.8rem;
        color: #E2E8F0;
        display: flex;
        align-items: center;
    }
    .tier-features li::before {
        content: '✓';
        color: #00EEFF;
        margin-right: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="pricing-header">
    <h1>Simple, transparent pricing</h1>
    <p>Choose the plan that best fits your enterprise data needs.</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="tier-card">
        <div class="tier-name">Free Plan</div>
        <div class="tier-price">$0<span>/month</span></div>
        <p style="color: #94A3B8; margin-bottom: 2rem;">Perfect for exploring basic analytics.</p>
        <ul class="tier-features">
            <li>Up to 1GB Data Storage</li>
            <li>Basic Descriptive Statistics</li>
            <li>Standard Dashboards</li>
            <li>Community Support</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.button("Get Started", key="btn_free", use_container_width=True)

with col2:
    st.markdown("""
    <div class="tier-card popular">
        <div class="tier-name">Professional</div>
        <div class="tier-price">$499<span>/month</span></div>
        <p style="color: #94A3B8; margin-bottom: 2rem;">For growing data-driven teams.</p>
        <ul class="tier-features">
            <li>Up to 50GB Data Storage</li>
            <li>Advanced Visual Analytics</li>
            <li>Predictive Modeling</li>
            <li>Priority Email Support</li>
            <li>Custom Reporting</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.button("Start Free Trial", key="btn_pro", type="primary", use_container_width=True)

with col3:
    st.markdown("""
    <div class="tier-card">
        <div class="tier-name">Enterprise</div>
        <div class="tier-price">Custom</div>
        <p style="color: #94A3B8; margin-bottom: 2rem;">For large-scale enterprise deployments.</p>
        <ul class="tier-features">
            <li>Unlimited Data Storage</li>
            <li>Full AI & ML Suite</li>
            <li>Dedicated Account Manager</li>
            <li>On-Premise Deployment Options</li>
            <li>Advanced Governance & Security</li>
            <li>24/7 Phone Support</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.button("Contact Sales", key="btn_ent", use_container_width=True)

st.markdown("<br><br><br><h2 style='text-align: center; color: #00EEFF;'>Feature Comparison</h2><br>", unsafe_allow_html=True)

features_df = pd.DataFrame({
    "Feature": [
        "Data Connectors", "Storage Limit", "Advanced Analytics", 
        "Predictive Modeling", "Custom Dashboards", "API Access", "Support"
    ],
    "Free Plan": ["Basic (CSV, Excel)", "1 GB", "❌", "❌", "3 max", "❌", "Community"],
    "Professional": ["Standard (SQL, APIs)", "50 GB", "✅", "✅", "Unlimited", "✅", "Priority Email"],
    "Enterprise": ["All + Custom", "Unlimited", "✅", "✅", "Unlimited", "✅", "24/7 Dedicated"]
})

st.dataframe(features_df, use_container_width=True, hide_index=True)
