# Engineering Decisions

## Decision: Dual Frontend Architecture (React + Streamlit)
**Reason:** Streamlit is excellent for data scientists to quickly prototype Python-heavy ML models, A/B testing frameworks, and deep statistical analysis (`src/app/`). However, for the primary executive dashboard, a React Single Page Application (`frontend-ui/`) provides a vastly superior user experience, faster client-side routing, and more customizable visual aesthetics.
**Alternatives Considered:** Monolithic Streamlit (poor UX) vs. Monolithic React (high overhead for data scientists).

## Decision: Exposing Python Logic via FastAPI
**Reason:** Since the core ML and data processing logic is written in Python (Pandas/Scikit-Learn), FastAPI provides a high-performance, asynchronous bridge to serve these Python results to the React frontend.
**Alternatives Considered:** Flask (slower, synchronous) or rewriting logic in Node.js (infeasible due to ML libraries).

## Decision: Renaming Streamlit `pages/` to `views/`
**Reason:** Streamlit automatically scans folders named `pages/` on startup and executes modules inside them. This caused `ModuleNotFoundError` during deployment on platforms like Render because `main.py` had not yet injected the root directory into `sys.path`. By renaming to `views/` and using `st.navigation`, we enforce explicit, safe loading.


## Update 2026-06-25: Static Link Rerouting
- **Decision:** We decided to keep the static links (Pricing, Docs, Resources) inside the Streamlit app instead of pushing to an external Next.js app that doesn't exist yet.
- **Reasoning:** It provides a better immediate user experience and avoids 'Connection Refused' errors. Next.js integration is delayed until the backend is fully stable.
