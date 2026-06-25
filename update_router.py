import os
import re

filepath = r"d:\Data Analytics Dashboard project\src\app\main.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace the entire 'else:' block for the authenticated router.
old_block_pattern = r"else:\s*# Authenticated Router with Structured Navigation\s*pg = st\.navigation\(\{[\s\S]*?\}\)"

new_block = """else:
    # Authenticated Router with Structured Navigation
    user_role = st.session_state.get("user_role", "Admin")
    nav_dict = {
        "Home": [
            st.Page("views/00_Home.py", title="Home", icon="🏠", default=True),
        ],
        "Platform Information": [
            st.Page("views/pricing_page.py", title="Pricing", icon="💳"),
            st.Page("views/resources_page.py", title="Resources", icon="📚"),
            st.Page("views/docs_page.py", title="Docs", icon="📖"),
            st.Page("views/about_page.py", title="About", icon="ℹ️"),
        ]
    }
    
    # Viewer sees Business Intelligence
    if user_role in ["Admin", "Executive", "Analyst", "Viewer"]:
        nav_dict["Business Intelligence"] = [
            st.Page("views/19_Interactive_Dashboard.py", title="Interactive Dashboard", icon="🎛️"),
            st.Page("views/20_Key_Insights.py", title="Key Insights", icon="💡"),
            st.Page("views/21_Business_Suggestions.py", title="Business Suggestions", icon="💼"),
            st.Page("views/26_Recommendations.py", title="Recommendations", icon="🎯"),
        ]
    
    # Executives & Analysts see core data and reporting
    if user_role in ["Admin", "Executive", "Analyst"]:
        nav_dict["Data Foundation"] = [
            st.Page("views/01_Data_Ingestion.py", title="Data Ingestion", icon="📥"),
            st.Page("views/02_Data_Quality_Assessment.py", title="Data Quality Assessment", icon="✅"),
            st.Page("views/03_Data_Cleaning.py", title="Data Cleaning", icon="🧹"),
            st.Page("views/04_Descriptive_Statistics.py", title="Descriptive Statistics", icon="📊"),
            st.Page("views/05_Univariate_Analysis.py", title="Univariate Analysis", icon="📈"),
            st.Page("views/06_Bivariate_Analysis.py", title="Bivariate Analysis", icon="🔗"),
        ]
        nav_dict["Customer Intelligence"] = [
            st.Page("views/08_Customer_Overview.py", title="Customer Overview", icon="👁️"),
            st.Page("views/07_Customer_Analysis.py", title="Customer Analysis", icon="👥"),
            st.Page("views/09_Customer_Segmentation.py", title="Customer Segmentation", icon="🎯"),
            st.Page("views/10_Behavior_Analysis.py", title="Behavior Analysis", icon="🧠"),
        ]
        nav_dict["Sales & Product Intelligence"] = [
            st.Page("views/11_Sales_Performance.py", title="Sales Performance", icon="💰"),
            st.Page("views/12_Product_Performance.py", title="Product Performance", icon="📦"),
            st.Page("views/13_Sales_Analytics.py", title="Sales Analytics", icon="📈"),
            st.Page("views/14_Product_Analytics.py", title="Product Analytics", icon="📊"),
        ]
        nav_dict["Reporting & Automation"] = [
            st.Page("views/22_Automated_Reporting.py", title="Automated Reporting", icon="📄"),
        ]
        
    # Analysts see advanced ML and geo tools
    if user_role in ["Admin", "Analyst"]:
        nav_dict["Geographic & Advanced Analytics"] = [
            st.Page("views/15_Geographic_Intelligence.py", title="Geographic Intelligence", icon="🗺️"),
            st.Page("views/16_Feature_Engineering.py", title="Feature Engineering", icon="⚙️"),
            st.Page("views/18_Advanced_Visual_Analytics.py", title="Advanced Visual Analytics", icon="🌌"),
        ]
        nav_dict["AI & Machine Learning"] = [
            st.Page("views/17_Predictive_Modeling_AI.py", title="Predictive Modeling & AI", icon="🤖"),
        ]
        
    # Only Admins see Governance & Cloud Integration
    if user_role == "Admin":
        nav_dict["Enterprise Platform"] = [
            st.Page("views/23_Governance_Security.py", title="Governance & Security", icon="🛡️"),
            st.Page("views/24_Monitoring_Observability.py", title="Monitoring & Observability", icon="🔍"),
            st.Page("views/25_Cloud_Enterprise_Integration.py", title="Cloud & Enterprise Integration", icon="☁️"),
        ]

    pg = st.navigation(nav_dict)"""

new_content = re.sub(old_block_pattern, new_block, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)
    
print("Updated RBAC in main.py")
