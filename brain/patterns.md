# Approved Implementation Patterns

## 1. Authentication Pattern
- **Backend:** Passwords must be hashed using PBKDF2 HMAC with SHA-256 and salted. Logic resides in `src/app/authentication.py`.
- **Database:** SQLite `users.db` is currently used to store user credentials.
- **Frontend (React):** Use the Context API (`AuthContext.tsx`) to manage session state globally.

## 2. API Pattern
- **Framework:** FastAPI.
- **Routing:** Use `APIRouter` to compartmentalize routes inside `api/routes/`.
- **CORS:** Must be configured in `api/main.py` to allow origins like `http://localhost:5173`.

## 3. Data Lake Pattern
- Datasets must transition through three states:
  1. **Raw:** Immutable source datasets.
  2. **Clean:** Missing values handled, duplicates removed, standardized.
  3. **Curated:** Business-ready with calculated KPIs (e.g., CLV, Churn).

## 4. Frontend Routing Pattern
- **Streamlit:** Use `st.navigation` and explicitly link to `views/` files. Do NOT use Streamlit's implicit V1 `pages/` auto-discovery.
- **React:** Standard `react-router-dom` configuration.

## 5. UI Component Pattern
- **CSS:** Use standard modular or vanilla CSS (e.g., `Hero.css`, `PipelineCards.css`). Tailwind is not used by default unless specified.
- **Design System:** Prioritize glassmorphism, dynamic animations, and premium data visualizations.
