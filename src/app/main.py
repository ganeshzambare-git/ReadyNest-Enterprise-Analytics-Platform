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
        st.Page("pages/auth_page.py", title="Login / Sign Up", icon="🔐", default=True)
    ])
else:
    # Authenticated Router with Structured Navigation
    pg = st.navigation({
        "Executive Dashboard": [
            st.Page("pages/00_Executive_Home.py", title="Executive Home", icon="🏠", default=True),
        ],
        "Data Pipeline & Engineering": [
            st.Page("pages/0_Data_Loading.py", title="Data Loading", icon="📦"),
            st.Page("pages/1_Data_Cleaning.py", title="Data Cleaning", icon="🧹"),
        ],
        "Statistical Analytics": [
            st.Page("pages/2_Descriptive_Statistics.py", title="Descriptive Statistics", icon="📈"),
            st.Page("pages/3_Univariate_Analysis.py", title="Univariate Analysis", icon="🔬"),
            st.Page("pages/4_Bivariate_Analysis.py", title="Bivariate Analysis", icon="🔗"),
            st.Page("pages/5_Data_Visualization.py", title="Data Visualization", icon="📊"),
        ],
        "Machine Learning & AI": [
            st.Page("pages/6_Insight_Extraction.py", title="Insight Extraction", icon="💡"),
            st.Page("pages/07_Predictive_Modeling.py", title="Predictive Modeling (ML)", icon="🤖"),
            st.Page("pages/11_Experimentation.py", title="A/B Testing", icon="🧪"),
        ],
        "Enterprise Features": [
            st.Page("pages/08_Advanced_Visuals.py", title="Advanced Visuals", icon="🌌"),
            st.Page("pages/09_Geographic_Intelligence.py", title="Geographic Intelligence", icon="🗺️"),
            st.Page("pages/10_Automated_Reporting.py", title="Automated Reporting", icon="⏱️"),
            st.Page("pages/12_Data_Governance.py", title="Data Governance (RLS)", icon="🛡️"),
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

pg.run()
