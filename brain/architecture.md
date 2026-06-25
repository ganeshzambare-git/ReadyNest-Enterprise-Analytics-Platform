# Architecture

## Multi-Layer Enterprise Architecture

### 1. Presentation Layer
- **Streamlit App (`src/app/`):** Python-based UI for complex data visualization and administrative tools.
  - Core entry point: `src/app/main.py`.
  - Pages located in `src/app/views/` (dynamically loaded via `st.navigation`).
- **React App (`frontend-ui/`):** Modern TypeScript + React Single Page Application (SPA) for the consumer-facing executive dashboard.

### 2. API Layer
- **FastAPI (`api/`):** RESTful interface connecting the React frontend to the backend logic.
  - Entry point: `api/main.py`.
  - Routes categorized in `api/routes/` (e.g., `auth.py`, `data.py`, `executive.py`).

### 3. Core Engine Layer (`src/`)
- **Analytics (`src/analytics/`):** Bivariate, univariate, and descriptive statistics.
- **Machine Learning (`src/machine_learning/`):** Churn prediction, revenue forecasting.
- **Preprocessing (`src/preprocessing/`):** Data cleaning, standardization, type conversion.
- **Reporting (`src/reporting/`):** PDF and Excel generators.
- **Visualization (`src/visualization/`):** Plotly chart factories.

### 4. Data Layer
- **Data Lake (`data_lake/`):** Storage for raw, clean, and curated datasets (CSV, Parquet).
- **Database (`src/database/`):** Connectors for PostgreSQL and SQLite.

## Deployment Architecture
- **Docker:** `deployment/docker/docker-compose.yml`
- **Kubernetes:** `deployment/kubernetes/deployment.yaml`
- **Cloud:** Render (Streamlit) & Vercel (React) supported.


## Update 2026-06-25: Production Routing & Module Template
- **Routing:** We completely abandoned hard-coded `localhost:3000` HTML links in `global_header.html` in favor of Streamlit's native `st.navigation` triggered via injected JS (`window.parent.document`).
- **Feature Modules:** Implemented a unified `module_template.py` architecture for all 26 feature modules, moving away from disparate hard-coded logic.
- **RBAC:** `main.py` is now the central authority for Role-Based Access Control, dynamically compiling the `st.navigation` dictionary based on `st.session_state.user_role`.
