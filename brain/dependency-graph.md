# Dependency Graph

```mermaid
graph TD
    A[React SPA frontend-ui] -->|HTTP REST| B(FastAPI api)
    
    B --> C{Core Engine src}
    B --> DB[(SQLite users.db)]
    
    C --> D(analytics)
    C --> E(machine_learning)
    C --> F(preprocessing)
    C --> G(database postgres)
    
    E --> H[Scikit-Learn / XGBoost]
    D --> I[Pandas / Numpy]
    
    J[Streamlit App src/app] --> C
    J --> DB
```

## Internal Architecture Rules
1. `frontend-ui` must NEVER directly access the database. It must route entirely through `api/`.
2. `src/` modules should be stateless and callable by either FastAPI or Streamlit.
3. `api/` endpoints should primarily handle authentication, validation, and request routing, delegating heavy computation to `src/`.
