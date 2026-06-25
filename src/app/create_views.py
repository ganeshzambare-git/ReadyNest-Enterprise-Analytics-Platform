import os

views_dir = r"d:\Data Analytics Dashboard project\src\app\views"

pages = {
    "Home": "00_Home.py",
    # Data Foundation
    "Data Ingestion": "01_Data_Ingestion.py",
    "Data Quality Assessment": "02_Data_Quality_Assessment.py",
    "Data Cleaning": "03_Data_Cleaning.py",
    "Descriptive Statistics": "04_Descriptive_Statistics.py",
    "Univariate Analysis": "05_Univariate_Analysis.py",
    "Bivariate Analysis": "06_Bivariate_Analysis.py",
    # Customer Intelligence
    "Customer Overview": "08_Customer_Overview.py",
    "Customer Analysis": "07_Customer_Analysis.py",
    "Customer Segmentation": "09_Customer_Segmentation.py",
    "Behavior Analysis": "10_Behavior_Analysis.py",
    # Sales & Product Intelligence
    "Sales Performance": "11_Sales_Performance.py",
    "Product Performance": "12_Product_Performance.py",
    "Sales Analytics": "13_Sales_Analytics.py",
    "Product Analytics": "14_Product_Analytics.py",
    # Business Intelligence
    "Interactive Dashboard": "19_Interactive_Dashboard.py",
    "Key Insights": "20_Key_Insights.py",
    "Business Suggestions": "21_Business_Suggestions.py",
    "Recommendations": "26_Recommendations.py",
    # Geographic & Advanced Analytics
    "Geographic Intelligence": "15_Geographic_Intelligence.py",
    "Feature Engineering": "16_Feature_Engineering.py",
    "Advanced Visual Analytics": "18_Advanced_Visual_Analytics.py",
    # AI & Machine Learning
    "Predictive Modeling & AI": "17_Predictive_Modeling_AI.py", # Can be reused for all AI sub-modules or we can keep it as a main hub for the 5 AI services
    # Reporting & Automation
    "Automated Reporting": "22_Automated_Reporting.py",
    # Enterprise Platform
    "Governance & Security": "23_Governance_Security.py",
    "Monitoring & Observability": "24_Monitoring_Observability.py",
    "Cloud & Enterprise Integration": "25_Cloud_Enterprise_Integration.py",
}

for title, filename in pages.items():
    filepath = os.path.join(views_dir, filename)
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            f.write(f"import streamlit as st\n\nst.title('{title}')\nst.write('This module is under development.')\n")
        print(f"Created {filename}")
    else:
        print(f"Exists {filename}")
