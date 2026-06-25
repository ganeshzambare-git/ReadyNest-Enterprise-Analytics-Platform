import os

modules = [
    ("01_Data_Ingestion.py", "Data Ingestion", "Automate the collection of raw data from multiple sources into a centralized lake.", "Ensures a single source of truth for all enterprise analytics, reducing data silos by 80%."),
    ("02_Data_Quality_Assessment.py", "Data Quality Assessment", "Identify missing values, outliers, and inconsistencies in your datasets.", "Improves downstream model accuracy by catching dirty data early in the pipeline."),
    ("03_Data_Cleaning.py", "Data Cleaning", "Apply transformations, imputations, and standardizations to raw data.", "Reduces manual data preparation time by 60%, allowing analysts to focus on insights."),
    ("04_Descriptive_Statistics.py", "Descriptive Statistics", "Calculate central tendencies, dispersions, and distribution shapes.", "Provides immediate high-level understanding of data distributions and baselines."),
    ("05_Univariate_Analysis.py", "Univariate Analysis", "Analyze single variables in isolation to understand their distributions.", "Critical for identifying highly skewed metrics that require transformation."),
    ("06_Bivariate_Analysis.py", "Bivariate Analysis", "Analyze relationships and correlations between two variables.", "Discovers hidden correlations that drive key business metrics like conversion rates."),
    ("07_Customer_Analysis.py", "Customer Analysis", "Deep dive into customer demographics, firmographics, and behaviors.", "Increases marketing ROI by targeting the right demographics with precision."),
    ("08_Customer_Overview.py", "Customer Overview", "High-level summary of the entire customer base and key demographics.", "Provides executive alignment on who the core customer base is today."),
    ("09_Customer_Segmentation.py", "Customer Segmentation", "Group customers using k-means and RFM modeling techniques.", "Allows hyper-personalized marketing campaigns, lifting conversion by up to 25%."),
    ("10_Behavior_Analysis.py", "Behavior Analysis", "Track and analyze how users interact with your product or service.", "Identifies friction points in the user journey, improving retention rates."),
    ("11_Sales_Performance.py", "Sales Performance", "Track revenue, deal sizes, win rates, and sales velocity.", "Empowers sales leadership to identify coaching opportunities and close gaps."),
    ("12_Product_Performance.py", "Product Performance", "Analyze product adoption, usage metrics, and feature popularity.", "Guides product roadmap decisions based on actual usage rather than intuition."),
    ("13_Sales_Analytics.py", "Sales Analytics", "Advanced forecasting and pipeline health analysis.", "Improves quarterly revenue forecast accuracy to within 5% margin of error."),
    ("14_Product_Analytics.py", "Product Analytics", "Cohort analysis, retention curves, and stickiness metrics.", "Identifies the 'Aha!' moment that turns free users into paying subscribers."),
    ("15_Geographic_Intelligence.py", "Geographic Intelligence", "Spatial analysis and mapping of revenue, customers, and operations.", "Optimizes supply chain routing and identifies under-served regional markets."),
    ("16_Feature_Engineering.py", "Feature Engineering", "Create new predictive signals from raw data columns.", "Can improve machine learning model performance by an order of magnitude."),
    ("17_Predictive_Modeling_AI.py", "Predictive Modeling & AI", "Train and deploy ML models to predict future outcomes.", "Transitions the business from reactive reporting to proactive decision making."),
    ("18_Advanced_Visual_Analytics.py", "Advanced Visual Analytics", "Multi-dimensional plotting, network graphs, and heatmaps.", "Uncovers complex multi-variable relationships invisible in standard charts."),
    ("19_Interactive_Dashboard.py", "Interactive Dashboard", "Customizable drag-and-drop analytics canvas.", "Democratizes data access by allowing non-technical users to build their own views."),
    ("20_Key_Insights.py", "Key Insights", "AI-generated summaries of the most important metrics changes.", "Saves executives hours of manual dashboard scanning every week."),
    ("21_Business_Suggestions.py", "Business Suggestions", "Prescriptive analytics recommending specific business actions.", "Bridges the gap between knowing what happened and knowing what to do about it."),
    ("22_Automated_Reporting.py", "Automated Reporting", "Schedule and distribute PDF/Excel reports to stakeholders.", "Eliminates the manual weekly reporting grind for data analysts."),
    ("23_Governance_Security.py", "Governance & Security", "Manage roles, access logs, PII masking, and audit trails.", "Ensures compliance with GDPR, CCPA, and enterprise infosec policies."),
    ("24_Monitoring_Observability.py", "Monitoring & Observability", "Track pipeline health, data freshness, and system uptime.", "Reduces mean-time-to-resolution (MTTR) for data pipeline failures."),
    ("25_Cloud_Enterprise_Integration.py", "Cloud Integration", "Connect to AWS, Azure, GCP, Snowflake, and Databricks.", "Seamlessly fits into your existing enterprise data stack without migration."),
    ("26_Recommendations.py", "Recommendations", "Collaborative and content-based filtering algorithms.", "Increases cross-sell and up-sell revenue through personalized suggestions.")
]

template = """import streamlit as st
import sys
import os

# Add project root to path so we can import components
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from components.module_template import render_feature_module

st.set_page_config(page_title="{title} - ReadyNest", layout="wide")

render_feature_module(
    title="{title}",
    description="{desc}",
    business_value="{value}",
    metrics=[
        {{"label": "Total Volume", "value": "1.2M", "delta": "+15%"}},
        {{"label": "Active Users", "value": "45.2K", "delta": "2.4%"}},
        {{"label": "Processing Time", "value": "245ms", "delta": "-12ms"}},
        {{"label": "Error Rate", "value": "0.01%", "delta": "-0.05%"}}
    ],
    chart_type="line"
)
"""

base_dir = r"d:\Data Analytics Dashboard project\src\app\views"

for filename, title, desc, value in modules:
    filepath = os.path.join(base_dir, filename)
    content = template.format(title=title, desc=desc, value=value)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Successfully updated 26 modules!")
