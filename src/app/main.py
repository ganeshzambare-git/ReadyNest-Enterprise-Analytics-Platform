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
        "New Platform Experience": [
            st.Page("views/000_NextJS_Platform.py", title="Next.js Platform", icon="🚀", default=True),
        ],
        "Executive Dashboard": [
            st.Page("views/00_Executive_Home.py", title="Executive Home", icon="🏠"),
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

# Global Header Injection (matches Next.js React App Header)
global_header_html = """
<div style="
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 64px;
    background-color: rgba(3, 20, 46, 0.95);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid rgba(226, 232, 240, 0.1);
    z-index: 999999;
    display: flex;
    align-items: center;
    padding: 0 2rem;
    font-family: 'Inter', sans-serif;
    color: white;
">
    <div style="display: flex; align-items: center; gap: 0.5rem; text-decoration: none; color: white;">
        <div style="height: 32px; width: 32px; border-radius: 6px; background-color: #00d084; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #03142e;">R</div>
        <div style="display: flex; flex-direction: column; line-height: 1;">
            <span style="font-weight: bold; font-size: 1.125rem; letter-spacing: -0.025em; color: white;">ReadyNest</span>
            <span style="font-size: 0.65rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600;">Insight Engine</span>
        </div>
    </div>
    <div style="flex: 1;"></div>
    <div style="display: flex; gap: 1.5rem; align-items: center;">
        <a href="http://localhost:3000/platform" style="color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.875rem; font-weight: 500; transition: color 0.2s;" onmouseover="this.style.color='white'" onmouseout="this.style.color='rgba(255,255,255,0.8)'">Platform</a>
        <a href="http://localhost:3000/resources" style="color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.875rem; font-weight: 500; transition: color 0.2s;" onmouseover="this.style.color='white'" onmouseout="this.style.color='rgba(255,255,255,0.8)'">Resources</a>
        <a href="http://localhost:3000/pricing" style="color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.875rem; font-weight: 500; transition: color 0.2s;" onmouseover="this.style.color='white'" onmouseout="this.style.color='rgba(255,255,255,0.8)'">Pricing</a>
        <a href="http://localhost:3000/docs" style="color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.875rem; font-weight: 500; transition: color 0.2s;" onmouseover="this.style.color='white'" onmouseout="this.style.color='rgba(255,255,255,0.8)'">Docs</a>
    </div>
    <div style="margin-left: 2rem; display: flex; gap: 0.5rem; align-items: center;">
        <a href="http://localhost:3000/login" style="padding: 0.5rem 1rem; color: white; text-decoration: none; font-size: 0.875rem; font-weight: 500; border-radius: 6px; transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.1)'" onmouseout="this.style.background='transparent'">Sign In</a>
        <a href="http://localhost:3000/register" style="padding: 0.5rem 1rem; background-color: #00d084; color: #03142e; text-decoration: none; font-size: 0.875rem; font-weight: 600; border-radius: 6px; box-shadow: 0 0 20px 0px rgba(0, 208, 132, 0.3); transition: opacity 0.2s;" onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">Get Started</a>
    </div>
</div>
<style>
    /* Push the main Streamlit content down so it's not hidden by our fixed header */
    .stApp > header {
        top: 64px !important;
        background: transparent !important;
    }
    .stApp > div:first-child {
        margin-top: 64px;
    }
    /* Streamlit sidebar push down */
    section[data-testid="stSidebar"] {
        top: 64px !important;
        height: calc(100vh - 64px) !important;
    }
</style>
"""
st.markdown(global_header_html, unsafe_allow_html=True)

pg.run()
