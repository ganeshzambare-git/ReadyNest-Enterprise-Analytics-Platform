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
