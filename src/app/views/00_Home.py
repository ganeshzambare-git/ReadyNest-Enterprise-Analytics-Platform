import streamlit as st

# Custom CSS for Dark Futuristic Theme
st.markdown("""
<style>
    /* Global Base */
    .stApp {
        background-color: #000814;
        color: #E2E8F0;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* Neon glow effects & Animations */
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 5px rgba(0,255,179,0.2); }
        50% { box-shadow: 0 0 20px rgba(0,255,179,0.5); }
        100% { box-shadow: 0 0 5px rgba(0,255,179,0.2); }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    /* Typography */
    h1, h2, h3, h4, h5 {
        color: #FFFFFF !important;
        font-family: 'Orbitron', 'Inter', sans-serif;
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00ffb3, #00d9ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-size: 1.8rem;
        color: #00d9ff;
        font-weight: 500;
        margin-bottom: 1.5rem;
    }
    
    .hero-desc {
        font-size: 1.2rem;
        line-height: 1.8;
        color: #94A3B8;
        margin-bottom: 2rem;
        max-width: 800px;
    }

    /* KPI Cards */
    .kpi-container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: center;
        margin-top: 3rem;
        margin-bottom: 4rem;
    }
    .kpi-card {
        background: rgba(4, 22, 51, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0,255,200,0.15);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        min-width: 200px;
        flex: 1;
        transition: all 0.3s ease;
        animation: float 6s ease-in-out infinite;
    }
    .kpi-card:hover {
        transform: translateY(-5px) scale(1.02);
        border-color: #00ffc8;
        box-shadow: 0 0 15px rgba(0,255,200,0.3);
    }
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #00ffb3;
        margin-bottom: 5px;
    }
    .kpi-label {
        font-size: 1rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Section Headers */
    .section-header {
        font-size: 2.5rem;
        text-align: center;
        margin: 4rem 0 2rem 0;
        border-bottom: 2px solid rgba(0,255,200,0.15);
        padding-bottom: 1rem;
        color: #00d9ff;
    }

    /* Service Cards (Streamlit native columns workaround) */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
        background: rgba(4, 22, 51, 0.7) !important;
        border: 1px solid rgba(0,255,200,0.15) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"]:hover {
        border-color: #00ffc8 !important;
        box-shadow: 0 0 15px rgba(0,255,200,0.3) !important;
        transform: translateY(-5px) !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, rgba(0,255,179,0.1), rgba(0,217,255,0.1)) !important;
        border: 1px solid #00ffb3 !important;
        color: #00ffb3 !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, rgba(0,255,179,0.3), rgba(0,217,255,0.3)) !important;
        box-shadow: 0 0 15px rgba(0,255,179,0.5) !important;
        color: #FFFFFF !important;
        border-color: #00ffc8 !important;
    }

    /* Tech Stack Tags */
    .tech-tag {
        display: inline-block;
        background: rgba(0, 217, 255, 0.1);
        border: 1px solid rgba(0, 217, 255, 0.3);
        color: #00d9ff;
        padding: 5px 12px;
        border-radius: 20px;
        margin: 5px;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    .tech-tag:hover {
        background: rgba(0, 217, 255, 0.2);
        border-color: #00d9ff;
        color: #FFFFFF;
    }

    /* Architecture Diagram */
    .arch-box {
        background: rgba(4, 22, 51, 0.9);
        border: 1px solid #00ffb3;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        color: #00ffb3;
        font-weight: bold;
        margin: 10px auto;
        width: 250px;
        box-shadow: 0 0 10px rgba(0,255,179,0.2);
    }
    .arch-arrow {
        text-align: center;
        color: #00d9ff;
        font-size: 1.5rem;
        margin: -5px 0;
    }

    /* Benefits Grid */
    .benefit-item {
        background: rgba(4, 22, 51, 0.5);
        border-left: 4px solid #00ffb3;
        padding: 15px 20px;
        margin-bottom: 15px;
        border-radius: 0 8px 8px 0;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        gap: 15px;
    }

    /* Footer */
    .enterprise-footer {
        margin-top: 5rem;
        border-top: 1px solid rgba(0,255,200,0.15);
        padding-top: 3rem;
        padding-bottom: 3rem;
        margin-bottom: 5rem;
    }
    .footer-heading {
        color: #00d9ff;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .footer-link {
        color: #94A3B8;
        display: block;
        margin-bottom: 0.5rem;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    .footer-link:hover {
        color: #00ffb3;
    }
</style>
""", unsafe_allow_html=True)

# ── 1. HERO SECTION ─────────────────────────────────────────────────────────────

col_hero1, col_hero2 = st.columns([3, 2])

with col_hero1:
    st.markdown('<div class="hero-title">READYNEST</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Enterprise Data Analytics Platform</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #FFFFFF; font-size: 2.2rem; font-weight: 300; margin-bottom: 1rem;">Transform Raw Data Into Enterprise Intelligence</h2>', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="hero-desc">
    ReadyNest Insight Engine is an enterprise-grade end-to-end analytics platform that combines:<br><br>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <div>✅ Business Intelligence</div>
        <div>✅ Data Analytics</div>
        <div>✅ Data Engineering</div>
        <div>✅ Machine Learning</div>
        <div>✅ Predictive Analytics</div>
        <div>✅ Executive Reporting</div>
        <div>✅ Governance</div>
        <div>✅ Cloud Analytics</div>
        <div>✅ AI-driven Recommendations</div>
    </div><br>
    The platform enables organizations to ingest, clean, analyze, visualize, forecast, govern, and operationalize business data using one unified analytics workspace.
    </div>
    ''', unsafe_allow_html=True)

    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    with col_btn1: st.button("🚀 Get Started", key="btn_hero_1", use_container_width=True)
    with col_btn2: st.button("🔍 Explore Platform", key="btn_hero_2", use_container_width=True)
    with col_btn3: st.button("📺 Watch Demo", key="btn_hero_3", use_container_width=True)
    with col_btn4: st.button("📚 Documentation", key="btn_hero_4", use_container_width=True)

with col_hero2:
    # Stylized Data Visual / Logo Replacement
    st.markdown("""
    <div style="height: 100%; display: flex; align-items: center; justify-content: center; flex-direction: column;">
        <div style="width: 300px; height: 300px; border-radius: 50%; border: 2px dashed #00ffb3; animation: spin 20s linear infinite; display: flex; align-items: center; justify-content: center; position: relative;">
            <div style="width: 250px; height: 250px; border-radius: 50%; border: 2px solid #00d9ff; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 30px rgba(0,217,255,0.3);">
                <div style="font-size: 5rem; animation: float 4s ease-in-out infinite;">📦</div>
            </div>
            <div style="position: absolute; top: -10px; left: 140px; background: #000814; color: #00ffb3; padding: 0 10px;">DATA</div>
            <div style="position: absolute; bottom: -10px; left: 140px; background: #000814; color: #00ffb3; padding: 0 10px;">AI</div>
        </div>
    </div>
    <style>@keyframes spin { 100% { transform: rotate(360deg); } }</style>
    """, unsafe_allow_html=True)

# ── 2. PLATFORM STATISTICS ──────────────────────────────────────────────────────

st.markdown("""
<div class="kpi-container">
    <div class="kpi-card" style="animation-delay: 0.1s;">
        <div class="kpi-value">25+</div>
        <div class="kpi-label">Analytics Modules</div>
    </div>
    <div class="kpi-card" style="animation-delay: 0.2s;">
        <div class="kpi-value">100+</div>
        <div class="kpi-label">Interactive Visualizations</div>
    </div>
    <div class="kpi-card" style="animation-delay: 0.3s;">
        <div class="kpi-value">50+</div>
        <div class="kpi-label">Enterprise KPIs</div>
    </div>
    <div class="kpi-card" style="animation-delay: 0.4s;">
        <div class="kpi-value">15+</div>
        <div class="kpi-label">Analytics Engines</div>
    </div>
    <div class="kpi-card" style="animation-delay: 0.5s;">
        <div class="kpi-value">10+</div>
        <div class="kpi-label">ML Algorithms</div>
    </div>
    <div class="kpi-card" style="animation-delay: 0.6s;">
        <div class="kpi-value">5</div>
        <div class="kpi-label">Cloud Integrations</div>
    </div>
    <div class="kpi-card" style="animation-delay: 0.7s;">
        <div class="kpi-value">99.9%</div>
        <div class="kpi-label">Availability</div>
    </div>
    <div class="kpi-card" style="animation-delay: 0.8s;">
        <div class="kpi-value">🔐</div>
        <div class="kpi-label">Enterprise Security</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── 3. ENTERPRISE PLATFORM OVERVIEW ───────────────────────────────────────────

st.markdown('<div class="section-header">What is ReadyNest?</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; color: #94A3B8; font-size: 1.2rem; margin-bottom: 3rem; max-width: 900px; margin-left: auto; margin-right: auto;">
ReadyNest is an enterprise-scale analytics platform designed to provide an integrated workspace for 
Data Analytics, Business Intelligence, Data Science, Data Engineering, Cloud Analytics, Executive Reporting, Governance, and Machine Learning.
</div>
""", unsafe_allow_html=True)

# ── 4. SERVICES SECTION ───────────────────────────────────────────────────────
st.markdown('<div class="section-header">Platform Services</div>', unsafe_allow_html=True)

def render_service_card(icon, title, desc, features, target_page):
    with st.container():
        st.markdown(f"""
        <div style="padding: 10px 0;">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">{icon}</div>
            <h3 style="color: #00ffb3; margin: 0 0 10px 0; font-size: 1.3rem;">{title}</h3>
            <p style="color: #94A3B8; font-size: 0.9rem; line-height: 1.5; min-height: 60px;">{desc}</p>
            <div style="color: #00d9ff; font-size: 0.8rem; margin-bottom: 15px; font-weight: bold;">
                <span style="background: rgba(0, 217, 255, 0.1); padding: 4px 8px; border-radius: 12px;">{len(features)} Features</span>
            </div>
            <ul style="color: #E2E8F0; font-size: 0.85rem; padding-left: 20px; min-height: 120px;">
                {"".join([f"<li>{f}</li>" for f in features])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Service", key=f"btn_{title.replace(' ', '_')}", use_container_width=True):
            st.switch_page(target_page)

st.markdown("### 🗄️ DATA FOUNDATION")
c1, c2, c3 = st.columns(3)
with c1: render_service_card("📥", "Data Ingestion", "Import and validate external data", ["CSV Import", "Excel Import", "SQL Import", "API Import", "Folder Import", "Schema Validation", "Metadata Extraction"], "views/01_Data_Ingestion.py")
with c2: render_service_card("✅", "Data Quality Assessment", "Audit data integrity", ["Completeness Score", "Accuracy Score", "Validity Score", "Consistency Score", "Data Profiling", "Quality Dashboard"], "views/02_Data_Quality_Assessment.py")
with c3: render_service_card("🧹", "Data Cleaning", "Automated preprocessing", ["Missing Values", "Duplicate Detection", "Outlier Detection", "Standardization", "Encoding", "Transformation"], "views/03_Data_Cleaning.py")

st.markdown("<br>", unsafe_allow_html=True)
c4, c5, c6 = st.columns(3)
with c4: render_service_card("📊", "Descriptive Statistics", "Core statistical properties", ["Mean", "Median", "Mode", "Variance", "Distribution", "Summary Statistics"], "views/04_Descriptive_Statistics.py")
with c5: render_service_card("📈", "Univariate Analysis", "Single variable distributions", ["Histograms", "Boxplots", "KDE", "Frequency Analysis"], "views/05_Univariate_Analysis.py")
with c6: render_service_card("🔗", "Bivariate Analysis", "Cross-variable relationships", ["Correlation", "Scatterplots", "Regression", "Heatmaps"], "views/06_Bivariate_Analysis.py")

st.markdown("<br><hr style='border-color: rgba(0,255,200,0.1);'><br>", unsafe_allow_html=True)

st.markdown("### 👥 CUSTOMER INTELLIGENCE")
c7, c8, c9, c10 = st.columns(4)
with c7: render_service_card("👁️", "Customer Overview", "High-level customer KPIs", ["Customer KPIs", "Customer Growth", "Customer Lifetime Value", "Customer Retention", "Customer Churn"], "views/08_Customer_Overview.py")
with c8: render_service_card("👥", "Customer Analysis", "Deep dive customer metrics", ["RFM Analysis", "Customer Value Analysis", "Revenue Contribution", "Purchase Analysis"], "views/07_Customer_Analysis.py")
with c9: render_service_card("🎯", "Customer Segmentation", "AI-driven clustering", ["KMeans", "Clustering", "VIP Detection", "Segment Profiling"], "views/09_Customer_Segmentation.py")
with c10: render_service_card("🧠", "Behavior Analysis", "Session and journey mapping", ["Session Analysis", "Purchase Behavior", "Funnel Analysis", "Journey Mapping"], "views/10_Behavior_Analysis.py")

st.markdown("<br><hr style='border-color: rgba(0,255,200,0.1);'><br>", unsafe_allow_html=True)

st.markdown("### 💰 SALES & PRODUCT INTELLIGENCE")
c11, c12, c13, c14 = st.columns(4)
with c11: render_service_card("💹", "Sales Performance", "Revenue dashboards", ["Revenue KPIs", "Sales Trends", "Targets", "Forecasts"], "views/11_Sales_Performance.py")
with c12: render_service_card("📦", "Product Performance", "Product portfolio health", ["Product Ranking", "Revenue Contribution", "Profitability", "Category Analysis"], "views/12_Product_Performance.py")
with c13: render_service_card("📈", "Sales Analytics", "Deep regional & temporal sales", ["Time Series", "Sales Growth", "Profit Analysis", "Regional Sales"], "views/13_Sales_Analytics.py")
with c14: render_service_card("📊", "Product Analytics", "Inventory & demand mapping", ["Product Mix", "Demand", "Inventory", "Lifecycle"], "views/14_Product_Analytics.py")

st.markdown("<br><hr style='border-color: rgba(0,255,200,0.1);'><br>", unsafe_allow_html=True)

st.markdown("### 💡 BUSINESS INTELLIGENCE")
c15, c16, c17, c18 = st.columns(4)
with c15: render_service_card("🎛️", "Interactive Dashboard", "Command center", ["Dynamic Filters", "Drilldown", "Cross-filtering", "Real-time KPIs"], "views/19_Interactive_Dashboard.py")
with c16: render_service_card("💡", "Key Insights", "AI text extraction", ["AI Insight Engine", "Trend Detection", "Anomaly Detection", "Opportunity Discovery"], "views/20_Key_Insights.py")
with c17: render_service_card("💼", "Business Suggestions", "Strategic guidance", ["Recommendation Engine", "Revenue Optimization", "Retention Improvement", "Product Strategy"], "views/21_Business_Suggestions.py")
with c18: render_service_card("🎯", "Recommendations", "Actionable next steps", ["Customer Recommendations", "Product Recommendations", "Marketing Recommendations", "Sales Recommendations"], "views/26_Recommendations.py")

st.markdown("<br><hr style='border-color: rgba(0,255,200,0.1);'><br>", unsafe_allow_html=True)

st.markdown("### 🔬 ADVANCED ANALYTICS")
c19, c20, c21, c21b = st.columns(4)
with c19: render_service_card("⚙️", "Feature Engineering", "Data prep for ML", ["Feature Store", "Feature Importance", "Feature Pipeline"], "views/16_Feature_Engineering.py")
with c20: render_service_card("🤖", "Predictive Modeling", "AI Forecasting & Churn", ["Revenue Forecasting", "Churn Prediction", "Demand Forecasting", "Recommendation Engine"], "views/17_Predictive_Modeling_AI.py")
with c21: render_service_card("🌌", "Advanced Visual Analytics", "Complex charts", ["Sankey", "Treemap", "Heatmaps", "Radar", "Waterfall", "Pareto", "Funnel"], "views/18_Advanced_Visual_Analytics.py")
with c21b: render_service_card("🗺️", "Geographic Intelligence", "Spatial Data", ["Choropleth", "Heatmaps", "Drilldowns", "Top Locations"], "views/15_Geographic_Intelligence.py")

st.markdown("<br><hr style='border-color: rgba(0,255,200,0.1);'><br>", unsafe_allow_html=True)

st.markdown("### 🏢 ENTERPRISE OPERATIONS")
c22, c23, c24, c25 = st.columns(4)
with c22: render_service_card("📄", "Automated Reporting", "Export & Email", ["PDF", "Excel", "PowerPoint", "Executive Reports", "Scheduling"], "views/22_Automated_Reporting.py")
with c23: render_service_card("🛡️", "Governance & Security", "Data Protection", ["RBAC", "Row Level Security", "Audit Logs", "Data Lineage", "Compliance"], "views/23_Governance_Security.py")
with c24: render_service_card("🔍", "Monitoring", "System Health", ["Performance", "Health Checks", "Error Tracking", "Usage Analytics", "Metrics"], "views/24_Monitoring_Observability.py")
with c25: render_service_card("☁️", "Cloud Integration", "Data Lake Sync", ["AWS S3", "BigQuery", "PostgreSQL", "MySQL", "Data Lake"], "views/25_Cloud_Enterprise_Integration.py")


# ── 5. ENTERPRISE ARCHITECTURE SECTION ────────────────────────────────────────

st.markdown('<div class="section-header">Enterprise Architecture</div>', unsafe_allow_html=True)

st.markdown("""
<div style="display: flex; flex-direction: column; align-items: center;">
    <div class="arch-box">Data Sources</div>
    <div class="arch-arrow">↓</div>
    <div class="arch-box">Data Ingestion</div>
    <div class="arch-arrow">↓</div>
    <div class="arch-box">Data Cleaning</div>
    <div class="arch-arrow">↓</div>
    <div class="arch-box">Analytics Engine</div>
    <div class="arch-arrow">↓</div>
    <div class="arch-box">Feature Engineering</div>
    <div class="arch-arrow">↓</div>
    <div class="arch-box">Machine Learning</div>
    <div class="arch-arrow">↓</div>
    <div class="arch-box">Visualization</div>
    <div class="arch-arrow">↓</div>
    <div class="arch-box">Reporting</div>
    <div class="arch-arrow">↓</div>
    <div class="arch-box">Governance</div>
    <div class="arch-arrow">↓</div>
    <div class="arch-box">Cloud Layer</div>
</div>
""", unsafe_allow_html=True)


# ── 6. TECHNOLOGY STACK SECTION ───────────────────────────────────────────────

st.markdown('<div class="section-header">Technology Stack</div>', unsafe_allow_html=True)

tech_data = {
    "Programming": ["Python", "Pandas", "NumPy", "SciPy", "StatsModels"],
    "Machine Learning": ["Scikit-Learn", "XGBoost"],
    "Visualization": ["Streamlit", "Plotly", "Matplotlib", "Seaborn", "Power BI", "Tableau"],
    "Database": ["PostgreSQL", "MySQL", "SQLAlchemy"],
    "Cloud": ["AWS S3", "Google BigQuery", "Data Lake", "Parquet"],
    "Reporting": ["ReportLab", "OpenPyXL", "Python PPTX", "FPDF2"],
    "APIs": ["PostgreSQL API", "MySQL API", "AWS API", "BigQuery API", "Kaleido API", "FPDF2 API"],
    "DevOps": ["Git", "GitHub", "GitHub Actions", "Docker", "Kubernetes", "Terraform", "Nginx"],
    "Security": ["RBAC", "RLS", "Audit Logging", "Compliance"]
}

for category, tags in tech_data.items():
    st.markdown(f"<h4 style='color: #00ffb3; margin-top: 1rem;'>{category}</h4>", unsafe_allow_html=True)
    tags_html = "".join([f"<span class='tech-tag'>{t}</span>" for t in tags])
    st.markdown(f"<div>{tags_html}</div>", unsafe_allow_html=True)


# ── 7. BUSINESS BENEFITS SECTION ──────────────────────────────────────────────

st.markdown('<div class="section-header">Business Benefits</div>', unsafe_allow_html=True)

benefits = [
    "Improve Data Quality", "Increase Revenue", "Reduce Churn", "Improve Decision Making",
    "Automate Reporting", "Enhance Governance", "Reduce Operational Cost", "Scale Analytics"
]

b_col1, b_col2 = st.columns(2)
for i, benefit in enumerate(benefits):
    target = b_col1 if i % 2 == 0 else b_col2
    target.markdown(f"""
    <div class="benefit-item">
        <span style="color: #00ffb3; font-size: 1.5rem;">✅</span> {benefit}
    </div>
    """, unsafe_allow_html=True)


# ── 8. DATA FLOW VISUALIZATION ────────────────────────────────────────────────

st.markdown('<div class="section-header">Data Flow Pipeline</div>', unsafe_allow_html=True)

st.markdown("""
<div style="background: rgba(4, 22, 51, 0.5); border: 1px solid rgba(0,255,200,0.15); border-radius: 12px; padding: 30px; overflow-x: auto;">
    <div style="display: flex; justify-content: space-between; align-items: center; min-width: 800px;">
        <div style="text-align: center; color: #E2E8F0;">
            <div style="font-size: 2rem; margin-bottom: 10px;">📄</div>
            <div>CSV / Excel<br>SQL / API</div>
        </div>
        <div style="color: #00ffb3; font-size: 1.5rem;">→</div>
        <div style="text-align: center; color: #E2E8F0;">
            <div style="font-size: 2rem; margin-bottom: 10px;">🗄️</div>
            <div>Data Lake</div>
        </div>
        <div style="color: #00ffb3; font-size: 1.5rem;">→</div>
        <div style="text-align: center; color: #E2E8F0;">
            <div style="font-size: 2rem; margin-bottom: 10px;">🧹</div>
            <div>Cleaning</div>
        </div>
        <div style="color: #00ffb3; font-size: 1.5rem;">→</div>
        <div style="text-align: center; color: #E2E8F0;">
            <div style="font-size: 2rem; margin-bottom: 10px;">⚙️</div>
            <div>Analytics</div>
        </div>
        <div style="color: #00ffb3; font-size: 1.5rem;">→</div>
        <div style="text-align: center; color: #E2E8F0;">
            <div style="font-size: 2rem; margin-bottom: 10px;">🤖</div>
            <div>Machine Learning</div>
        </div>
        <div style="color: #00ffb3; font-size: 1.5rem;">→</div>
        <div style="text-align: center; color: #E2E8F0;">
            <div style="font-size: 2rem; margin-bottom: 10px;">📊</div>
            <div>Dashboards</div>
        </div>
        <div style="color: #00ffb3; font-size: 1.5rem;">→</div>
        <div style="text-align: center; color: #E2E8F0;">
            <div style="font-size: 2rem; margin-bottom: 10px;">📑</div>
            <div>Executive Reports</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── 10. FOOTER ────────────────────────────────────────────────────────────────

st.markdown("""
<div class="enterprise-footer">
<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 30px;">
<div style="flex: 1; min-width: 250px;">
<div style="font-size: 1.5rem; font-weight: 800; color: #00ffb3; font-family: 'Orbitron', sans-serif; margin-bottom: 1rem;">READYNEST</div>
<p style="color: #94A3B8; font-size: 0.9rem; line-height: 1.6;">
Enterprise Data Analytics Platform.<br>
Transform Raw Data Into Enterprise Intelligence.
</p>
</div>

<div style="flex: 1; min-width: 150px;">
<div class="footer-heading">Platform</div>
<a href="#" class="footer-link">Products</a>
<a href="#" class="footer-link">Services</a>
<a href="#" class="footer-link">Pricing</a>
<a href="#" class="footer-link">Documentation</a>
</div>

<div style="flex: 1; min-width: 150px;">
<div class="footer-heading">Company</div>
<a href="#" class="footer-link">About</a>
<a href="#" class="footer-link">Careers</a>
<a href="#" class="footer-link">Contact</a>
<a href="#" class="footer-link">Resources</a>
</div>

<div style="flex: 1; min-width: 150px;">
<div class="footer-heading">Capabilities</div>
<a href="#" class="footer-link">Technology</a>
<a href="#" class="footer-link">Cloud</a>
<a href="#" class="footer-link">Machine Learning</a>
<a href="#" class="footer-link">Security</a>
<a href="#" class="footer-link">Reporting</a>
<a href="#" class="footer-link">Analytics</a>
</div>

<div style="flex: 1; min-width: 150px;">
<div class="footer-heading">Social</div>
<a href="https://github.com/ganeshzambare-git" target="_blank" class="footer-link">GitHub</a>
<a href="https://www.linkedin.com/in/ganesh-zambare-10369a313/" target="_blank" class="footer-link">LinkedIn</a>
<a href="#" class="footer-link">YouTube</a>
<a href="#" class="footer-link">Twitter</a>
</div>
</div>

<div style="margin-top: 4rem; text-align: center; color: #64748B; font-size: 0.8rem; border-top: 1px solid rgba(0,255,200,0.1); padding-top: 2rem;">
&copy; 2026 ReadyNest Enterprise Analytics. All rights reserved.
</div>
</div>
""", unsafe_allow_html=True)
