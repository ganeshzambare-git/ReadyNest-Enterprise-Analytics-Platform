# Feature Map

## Authentication & Authorization
- **Logic:** `src/app/authentication.py`
- **React Context:** `frontend-ui/src/context/AuthContext.tsx`
- **FastAPI Endpoint:** `api/routes/auth.py`
- **Streamlit View:** `src/app/views/auth_page.py`

## Executive Dashboard
- **React Component:** `frontend-ui/src/pages/ExecutiveHome.tsx`
- **FastAPI Endpoint:** `api/routes/executive.py`
- **Streamlit View:** `src/app/views/00_Executive_Home.py`

## Data Ingestion & Cleaning
- **Core Logic:** `src/ingestion/` and `src/preprocessing/`
- **Streamlit Views:** `src/app/views/0_Data_Loading.py` and `1_Data_Cleaning.py`

## Predictive Modeling & ML
- **Core Logic:** `src/machine_learning/`
- **Streamlit View:** `src/app/views/07_Predictive_Modeling.py`

## Database Management
- **SQLite / DB connections:** `src/database/postgres_manager.py` & `automation/auth.py`
