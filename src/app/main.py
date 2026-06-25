import sys
import os

# Add the project root to sys.path so 'src' can be imported globally
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st

st.set_page_config(
    page_title="ReadyNest Analytics",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Unauthenticated Router
    pg = st.navigation([
        st.Page("views/000_NextJS_Platform.py", title="Next.js Platform", icon="🚀", default=True),
        st.Page("views/auth_page.py", title="Legacy Login", icon="🔐")
    ])
else:
    # Authenticated Router with Structured Navigation
    pg = st.navigation({
        "Home": [
            st.Page("views/00_Home.py", title="Home", icon="🏠", default=True),
        ],
        "Data Foundation": [
            st.Page("views/01_Data_Ingestion.py", title="Data Ingestion", icon="📥"),
            st.Page("views/02_Data_Quality_Assessment.py", title="Data Quality Assessment", icon="✅"),
            st.Page("views/03_Data_Cleaning.py", title="Data Cleaning", icon="🧹"),
            st.Page("views/04_Descriptive_Statistics.py", title="Descriptive Statistics", icon="📊"),
            st.Page("views/05_Univariate_Analysis.py", title="Univariate Analysis", icon="📈"),
            st.Page("views/06_Bivariate_Analysis.py", title="Bivariate Analysis", icon="🔗"),
        ],
        "Customer Intelligence": [
            st.Page("views/08_Customer_Overview.py", title="Customer Overview", icon="👁️"),
            st.Page("views/07_Customer_Analysis.py", title="Customer Analysis", icon="👥"),
            st.Page("views/09_Customer_Segmentation.py", title="Customer Segmentation", icon="🎯"),
            st.Page("views/10_Behavior_Analysis.py", title="Behavior Analysis", icon="🧠"),
        ],
        "Sales & Product Intelligence": [
            st.Page("views/11_Sales_Performance.py", title="Sales Performance", icon="💰"),
            st.Page("views/12_Product_Performance.py", title="Product Performance", icon="📦"),
            st.Page("views/13_Sales_Analytics.py", title="Sales Analytics", icon="📈"),
            st.Page("views/14_Product_Analytics.py", title="Product Analytics", icon="📊"),
        ],
        "Business Intelligence": [
            st.Page("views/19_Interactive_Dashboard.py", title="Interactive Dashboard", icon="🎛️"),
            st.Page("views/20_Key_Insights.py", title="Key Insights", icon="💡"),
            st.Page("views/21_Business_Suggestions.py", title="Business Suggestions", icon="💼"),
            st.Page("views/26_Recommendations.py", title="Recommendations", icon="🎯"),
        ],
        "Geographic & Advanced Analytics": [
            st.Page("views/15_Geographic_Intelligence.py", title="Geographic Intelligence", icon="🗺️"),
            st.Page("views/16_Feature_Engineering.py", title="Feature Engineering", icon="⚙️"),
            st.Page("views/18_Advanced_Visual_Analytics.py", title="Advanced Visual Analytics", icon="🌌"),
        ],
        "AI & Machine Learning": [
            st.Page("views/17_Predictive_Modeling_AI.py", title="Predictive Modeling & AI", icon="🤖"),
        ],
        "Reporting & Automation": [
            st.Page("views/22_Automated_Reporting.py", title="Automated Reporting", icon="📄"),
        ],
        "Enterprise Platform": [
            st.Page("views/23_Governance_Security.py", title="Governance & Security", icon="🛡️"),
            st.Page("views/24_Monitoring_Observability.py", title="Monitoring & Observability", icon="🔍"),
            st.Page("views/25_Cloud_Enterprise_Integration.py", title="Cloud & Enterprise Integration", icon="☁️"),
        ]
    })

# Load UI assets from external files to prevent IDE parsing errors
components_dir = os.path.join(os.path.dirname(__file__), 'components')

# Apply DarkStore UI Theme
try:
    with open(os.path.join(components_dir, 'ui_styles.html'), 'r', encoding='utf-8') as f:
        st.markdown(f.read(), unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Global Header Injection
try:
    with open(os.path.join(components_dir, 'global_header.html'), 'r', encoding='utf-8') as f:
        st.markdown(f.read(), unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Inject JS to route navigation via the hidden sidebar
import streamlit.components.v1 as components
try:
    with open(os.path.join(components_dir, 'header_script.html'), 'r', encoding='utf-8') as f:
        components.html(f.read(), height=0, width=0)
except FileNotFoundError:
    pass

pg.run()
