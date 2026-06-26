# Master Memory: ReadyNest Insight Engine

## 🧠 What is this?
This is the **Compressed Project Intelligence** file. Every AI agent must read this file before beginning any task.

## 🚀 Project Overview
**ReadyNest Insight Engine** is an enterprise-grade Data Analytics, Business Intelligence, and Predictive Analytics platform. It transforms raw business data into actionable insights through Data Engineering, Machine Learning, and Interactive Dashboards.

## 🏗️ High-Level Architecture
- **V1 Frontend (Legacy/Data Exploration):** Streamlit (`src/app/views/`)
- **V2 Frontend (Modern UI):** React + TypeScript + Vite (`frontend-ui/`)
- **Backend API:** FastAPI (`api/main.py`)
- **Data Engineering & ML Core:** Python / Pandas / Scikit-Learn (`src/`)
- **Database:** SQLite (`automation/users.db`) / PostgreSQL
- **Deployment:** Render / Vercel / Docker

## 🔑 Key Patterns
- **API Routing:** FastAPI routers located in `api/routes/`.
- **Streamlit Routing:** `st.navigation` pointing to `views/` (not `pages/`).
- **Data Architecture:** Raw → Clean → Curated Data Lake architecture.
- **Authentication:** PBKDF2 hashing stored in SQLite database. React UI uses Context API (`AuthContext.tsx`).

## ⚠️ Important Context / Known Issues
- **Streamlit Deployment:** Do not use `pages/` directory for Streamlit multipage routing. We renamed it to `views/` to prevent Streamlit V1 auto-discovery from causing `ModuleNotFoundError` on Render.
- **Backend API:** FastAPI must be started explicitly. The React frontend depends on it at `http://localhost:8000`.

## 🗺️ Quick Links
- Full Architecture: `architecture.md`
- Code Patterns: `patterns.md`
- Engineering Decisions: `decisions.md`
- Terminology: `glossary.md`


### 2026-06-25 - Production Overhaul (Phase 1-4)
Successfully executed a massive platform audit. Fixed all routing issues, created responsive static pages (Pricing, About), implemented a unified feature templating engine for 26 modules, enforced RBAC authentication, and cleaned up legacy orphaned files. The Streamlit prototype is now production-ready.

### 2026-06-26 - Feature Implementation: Customer Analysis
Successfully implemented the Customer Analysis dashboard (`07_Customer_Analysis.py`). The module now features advanced data augmentation (Profit, Segments, Repeat Rates), KPI metrics grids, and interactive visual analytics using Plotly. Dynamic AI Insights are generated based on calculated segments.

### 2026-06-26 - Feature Implementation: Customer Segmentation
Successfully implemented the Customer Segmentation engine (`09_Customer_Segmentation.py`). Added automated RFM heuristics (Champions, At-Risk, etc.) alongside K-Means and Hierarchical Clustering for behavioral ML segmentation. Added interactive 3D cluster visualizations and dynamic marketing strategy recommendations based on segmented cohorts.

### 2026-06-26 - Feature Implementation: Behavior Analysis
Successfully implemented the Behavior Analysis dashboard (`10_Behavior_Analysis.py`). Synthesized behavioral metrics (session activity, cart abandonment, time between purchases) and integrated interactive visual analytics (Funnel, Heatmap, Activity Timeline). Included dynamic AI Insights to identify drop-off points, seasonal trends, and recommend product bundling and personalization strategies.