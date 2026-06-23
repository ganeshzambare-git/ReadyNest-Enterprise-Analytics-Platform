# Core Memory: ReadyNest Insight Engine

## Current State
The project has evolved from a monolithic Streamlit application into a decoupled enterprise platform featuring a React frontend and a FastAPI backend, while still retaining the Streamlit app for complex data exploration and administrative views.

## Key Features
1. **Interactive Executive Dashboards:** KPIs, revenue forecasts, and geographic intelligence.
2. **Data Pipeline Engine:** Ingests CSV/Excel/SQL, cleans missing values, standardizes data, and scores quality.
3. **Statistical Analytics:** Descriptive, univariate, bivariate analysis, and correlation matrices.
4. **Machine Learning:** 
   - Customer Churn Prediction (Random Forest/XGBoost)
   - Revenue & Demand Forecasting (ARIMA/Regression)
   - Customer Segmentation
5. **A/B Testing Framework:** Statistical significance testing for campaigns and pricing.
6. **Data Governance:** Role-Based Access Control (RBAC), Row-Level Security (RLS), and secure authentication.
7. **Automated Reporting:** PDF and Excel enterprise report generation.

## Active Work
- Migrating core Streamlit visualizations to the React frontend.
- Connecting the React frontend (`frontend-ui`) to the FastAPI backend (`api`).
- Standardizing the REST API endpoints.
