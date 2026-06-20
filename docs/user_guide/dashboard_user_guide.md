# ReadyNest Dashboard — User Guide

Welcome to the ReadyNest Enterprise Analytics Platform. This guide explains how to navigate the 8 core modules of the Streamlit dashboard.

## 1. Data Loading 📦
This is the entry point. Upload your raw `CSV` or `Excel` files here.
- **Data Lake Integration**: Once uploaded, the backend ETL pipeline automatically stores a physical `.parquet` copy in your hard drive's `data_lake/` folder.
- **SQL Connect**: You can also use the SQL Console tab to query your enterprise database directly.

## 2. Executive Home 🏠
The master 360-degree command center.
- Displays high-level KPIs (Total Revenue, Profit, Margin).
- Use the **Date Filter** in the sidebar to dynamically adjust all metrics across the page.
- Features top-selling categories and regional performance bar charts.

## 3. Data Visualization 📊 & Advanced Visuals 🌌
Where basic and complex charting happens.
- **Data Visualization**: Standard Line Charts, Bar Charts, and Scatter plots.
- **Advanced Visuals**: Use the **Plotly Sunburst** to click and drill down into product hierarchies, or view the **Waterfall Chart** to see how categories stack up to total revenue.

## 4. Geographic Intelligence 🗺️
Location-based analytics.
- If your dataset contains a "State" or "Country" column, the engine automatically renders a geographic heatmap, color-coding regions by revenue generation.

## 5. Predictive Modeling (ML) 🤖
The Machine Learning engine room.
- **Sales Prediction**: Trains a Random Forest Regressor to predict future sales based on historical data.
- **Churn Prediction**: Trains an XGBoost Classifier to identify which customers are at the highest risk of churning, outputting a Probability %.

## 6. A/B Testing & Experimentation 🧪
Stop guessing if marketing campaigns work.
- Input your Control Group and Treatment Group numbers.
- The system runs a `SciPy` Chi-Squared test to determine if the result is statistically significant (p-value < 0.05).

## 7. Automated Reporting ⏱️
- Configure automated job schedules (e.g., "Weekly Executive Summary").
- Test the system using the **Trigger Now** button to simulate generating a PDF/CSV and emailing it to stakeholders.

## 8. Data Governance (RLS) 🛡️
- View the **Business Glossary**.
- **RLS Simulator**: Select a role (e.g., "West Regional Manager") to securely lock down the dashboard. When active, all pages will automatically filter out data that does not belong to your region.
