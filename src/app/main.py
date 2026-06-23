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
        st.Page("views/auth_page.py", title="Login / Sign Up", icon="🔐", default=True)
    ])
else:
    # Authenticated Router with Structured Navigation
    pg = st.navigation({
        "Executive Dashboard": [
            st.Page("views/00_Executive_Home.py", title="Executive Home", icon="🏠", default=True),
        ],
        "Data Pipeline & Engineering": [
            st.Page("views/0_Data_Loading.py", title="Data Loading", icon="📦"),
            st.Page("views/1_Data_Cleaning.py", title="Data Cleaning", icon="🧹"),
        ],
        "Statistical Analytics": [
            st.Page("views/2_Descriptive_Statistics.py", title="Descriptive Statistics", icon="📈"),
            st.Page("views/3_Univariate_Analysis.py", title="Univariate Analysis", icon="🔬"),
            st.Page("views/4_Bivariate_Analysis.py", title="Bivariate Analysis", icon="🔗"),
            st.Page("views/5_Data_Visualization.py", title="Data Visualization", icon="📊"),
        ],
        "Machine Learning & AI": [
            st.Page("views/6_Insight_Extraction.py", title="Insight Extraction", icon="💡"),
            st.Page("views/07_Predictive_Modeling.py", title="Predictive Modeling (ML)", icon="🤖"),
            st.Page("views/11_Experimentation.py", title="A/B Testing", icon="🧪"),
        ],
        "Enterprise Features": [
            st.Page("views/08_Advanced_Visuals.py", title="Advanced Visuals", icon="🌌"),
            st.Page("views/09_Geographic_Intelligence.py", title="Geographic Intelligence", icon="🗺️"),
            st.Page("views/10_Automated_Reporting.py", title="Automated Reporting", icon="⏱️"),
            st.Page("views/12_Data_Governance.py", title="Data Governance (RLS)", icon="🛡️"),
        ]
    })
    
    # Inject secure logout button into the sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"**Logged in as:** {st.session_state.user_name} ({st.session_state.user_role})")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            for key in ["user_name", "user_email", "user_role"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# Apply DarkStore UI Theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Orbitron:wght@400;500;700;900&display=swap');

/* Main Backgrounds */
.stApp {
    background-color: #070B19 !important;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stSidebar"] {
    background-color: rgba(7, 11, 25, 0.9) !important;
    border-right: 1px solid rgba(0, 238, 255, 0.2) !important;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Orbitron', sans-serif !important;
}
h1 {
    color: #FFFFFF !important;
}
h2, h3 {
    color: #00EEFF !important;
    text-shadow: 0 0 10px rgba(0, 238, 255, 0.4);
}

/* Buttons */
.stButton > button {
    background-color: transparent !important;
    border: 1px solid #00EEFF !important;
    color: #00EEFF !important;
    border-radius: 50px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    box-shadow: 0 0 10px rgba(0, 238, 255, 0.2) !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    background-color: #00EEFF !important;
    color: #070B19 !important;
    box-shadow: 0 0 20px rgba(0, 238, 255, 0.6) !important;
}

/* Metrics Dashboard Styling */
[data-testid="stMetricValue"] {
    font-family: 'Orbitron', sans-serif !important;
    color: #00FF9D !important;
    text-shadow: 0 0 10px rgba(0, 255, 157, 0.4);
}
[data-testid="stMetricLabel"] {
    color: #94A3B8 !important;
    font-family: 'Inter', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.8rem !important;
}
[data-testid="stMetricDelta"] {
    color: #00EEFF !important;
}
[data-testid="stMetric"] {
    background: rgba(10, 15, 36, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 15px;
    box-shadow: inset 0 0 20px rgba(0, 238, 255, 0.05);
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0, 238, 255, 0.2) !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

pg.run()
