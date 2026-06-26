import streamlit as st

st.markdown("""
<style>
    /* Shared CSS for Platform Pages */
    .stApp { background-color: #000814; color: #E2E8F0; font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4 { color: #FFFFFF !important; font-family: 'Orbitron', sans-serif; }
    
    .hero-title {
        font-size: 3.5rem; font-weight: 900;
        background: linear-gradient(90deg, #00ffb3, #00d9ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-top: 2rem; margin-bottom: 1rem;
    }
    .hero-subtitle {
        font-size: 1.2rem; color: #94A3B8; text-align: center; max-width: 800px; margin: 0 auto 3rem auto; line-height: 1.6;
    }

    .search-box {
        background: rgba(4, 22, 51, 0.8); border: 2px solid #00d9ff; border-radius: 50px;
        padding: 15px 30px; font-size: 1.2rem; color: white; width: 100%; max-width: 600px;
        margin: 0 auto 4rem auto; display: block; text-align: left;
    }

    .doc-card {
        background: rgba(4, 22, 51, 0.7); border: 1px solid rgba(0,255,200,0.15);
        border-radius: 12px; padding: 25px; transition: all 0.3s ease; height: 100%;
        cursor: pointer;
    }
    .doc-card:hover { transform: translateX(10px); border-color: #00ffc8; box-shadow: -5px 0 15px rgba(0,255,200,0.2); }
    .doc-title { color: #00ffb3; font-size: 1.3rem; margin-bottom: 10px; }

    .step-box { background: rgba(0, 217, 255, 0.1); border-left: 4px solid #00d9ff; padding: 20px; margin-bottom: 20px; }

    .enterprise-footer { margin-top: 5rem; border-top: 1px solid rgba(0,255,200,0.15); padding-top: 3rem; padding-bottom: 3rem; margin-bottom: 5rem; }
    .footer-heading { color: #00d9ff; font-weight: bold; margin-bottom: 1rem; }
    .footer-link { color: #94A3B8; display: block; margin-bottom: 0.5rem; text-decoration: none; transition: color 0.3s ease; }
    .footer-link:hover { color: #00ffb3; }
</style>
""", unsafe_allow_html=True)

# ── HERO ────────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Platform Documentation</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Learn how to connect data, build dashboards, configure ML pipelines, and extract insights.</div>', unsafe_allow_html=True)

st.markdown('<div class="search-box">🔍 Search documentation, API references, tutorials...</div>', unsafe_allow_html=True)

# ── QUICK START ─────────────────────────────────────────────────────────────────
st.markdown("## 🚀 Quick Start Guide")
st.markdown("""
<div class="step-box">
    <h3 style="color: #00d9ff; margin:0;">1. Connect Your Data</h3>
    <p style="color: #94A3B8; margin: 5px 0 0 0;">Navigate to the <b>Data Ingestion</b> module. Upload a CSV, Excel, or connect directly to PostgreSQL/AWS S3. The system will auto-infer schemas.</p>
</div>
<div class="step-box">
    <h3 style="color: #00d9ff; margin:0;">2. Let AI Analyze</h3>
    <p style="color: #94A3B8; margin: 5px 0 0 0;">Navigate to <b>Key Insights</b>. The AI consultant will immediately scan your data for anomalies, revenue risks, and business opportunities.</p>
</div>
<div class="step-box">
    <h3 style="color: #00d9ff; margin:0;">3. Generate Executive Reports</h3>
    <p style="color: #94A3B8; margin: 5px 0 0 0;">Go to <b>Automated Reporting</b>. Select your KPIs and instantly download a comprehensive 60-page PDF report.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ── CATEGORIES ──────────────────────────────────────────────────────────────────
st.markdown("## 📚 Documentation Categories")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="doc-card">
        <div class="doc-title">⚙️ Platform Setup</div>
        <ul style="color:#94A3B8; line-height: 1.8; font-size: 0.9rem;">
            <li>Role-Based Access Control (RBAC)</li>
            <li>Cloud Data Lake Integration</li>
            <li>Environment Configuration</li>
            <li>Audit Log Monitoring</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
with c2:
    st.markdown("""
    <div class="doc-card">
        <div class="doc-title">🤖 Machine Learning</div>
        <ul style="color:#94A3B8; line-height: 1.8; font-size: 0.9rem;">
            <li>AutoML Pipeline Configuration</li>
            <li>Customer Churn Prediction</li>
            <li>Time-Series Revenue Forecasting</li>
            <li>Feature Engineering Store</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
with c3:
    st.markdown("""
    <div class="doc-card">
        <div class="doc-title">🔌 API References</div>
        <ul style="color:#94A3B8; line-height: 1.8; font-size: 0.9rem;">
            <li>REST API Authentication</li>
            <li>Headless BI Querying</li>
            <li>Webhook Integrations</li>
            <li>GraphQL Schemas</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="enterprise-footer">
    <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 30px;">
        <div style="flex: 1; min-width: 250px;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #00ffb3; font-family: 'Orbitron', sans-serif; margin-bottom: 1rem;">READYNEST</div>
            <p style="color: #94A3B8; font-size: 0.9rem; line-height: 1.6;">Enterprise Data Analytics Platform.<br>Transform Raw Data Into Enterprise Intelligence.</p>
        </div>
        <div style="flex: 1; min-width: 150px;">
            <div class="footer-heading">Platform</div>
            <a href="#" class="footer-link">Documentation</a><a href="#" class="footer-link">API Reference</a><a href="#" class="footer-link">System Status</a>
        </div>
    </div>
    <div style="margin-top: 4rem; text-align: center; color: #64748B; font-size: 0.8rem; border-top: 1px solid rgba(0,255,200,0.1); padding-top: 2rem;">
        &copy; 2026 ReadyNest Enterprise Analytics. All rights reserved.
    </div>
</div>
""", unsafe_allow_html=True)
