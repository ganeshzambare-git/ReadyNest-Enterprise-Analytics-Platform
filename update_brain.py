import os
import datetime

brain_dir = r"d:\Data Analytics Dashboard project\brain"
now = datetime.datetime.now().strftime("%Y-%m-%d")

# 1. Update Architecture
with open(os.path.join(brain_dir, "architecture.md"), "a", encoding="utf-8") as f:
    f.write(f"\n\n## Update {now}: Production Routing & Module Template\n")
    f.write("- **Routing:** We completely abandoned hard-coded `localhost:3000` HTML links in `global_header.html` in favor of Streamlit's native `st.navigation` triggered via injected JS (`window.parent.document`).\n")
    f.write("- **Feature Modules:** Implemented a unified `module_template.py` architecture for all 26 feature modules, moving away from disparate hard-coded logic.\n")
    f.write("- **RBAC:** `main.py` is now the central authority for Role-Based Access Control, dynamically compiling the `st.navigation` dictionary based on `st.session_state.user_role`.\n")

# 2. Update Patterns
with open(os.path.join(brain_dir, "patterns.md"), "a", encoding="utf-8") as f:
    f.write(f"\n\n## Update {now}: Error Boundaries and Caching\n")
    f.write("- **Error Boundaries:** Complex UI grids (like Plotly charts in Executive Home) must be wrapped in `try/except` blocks returning `st.error()` so that a single bad chart doesn't crash the page.\n")
    f.write("- **Caching:** Core data IO (`pd.read_csv`, `pd.read_excel`) should be wrapped in `@st.cache_data(show_spinner=False)` to heavily optimize dashboard loading times.\n")

# 3. Update Decisions
with open(os.path.join(brain_dir, "decisions.md"), "a", encoding="utf-8") as f:
    f.write(f"\n\n## Update {now}: Static Link Rerouting\n")
    f.write("- **Decision:** We decided to keep the static links (Pricing, Docs, Resources) inside the Streamlit app instead of pushing to an external Next.js app that doesn't exist yet.\n")
    f.write("- **Reasoning:** It provides a better immediate user experience and avoids 'Connection Refused' errors. Next.js integration is delayed until the backend is fully stable.\n")

# 4. Update Mistakes
with open(os.path.join(brain_dir, "mistakes.md"), "a", encoding="utf-8") as f:
    f.write(f"\n\n## Update {now}: Cross-Origin IFrames & CSS Stripping\n")
    f.write("- **Mistake:** Attempting to inject `header_script.html` with hard-coded Python multiline strings caused CSS line comments (`//`) to break the entire layout when whitespace was stripped.\n")
    f.write("- **Fix:** We now read HTML/JS/CSS assets directly from separate files (e.g., `ui_styles.html`) using Python's `open().read()` and `unsafe_allow_html=True`.\n")

# 5. Update Master Memory
with open(os.path.join(brain_dir, "master-memory.md"), "a", encoding="utf-8") as f:
    f.write(f"\n\n### {now} - Production Overhaul (Phase 1-4)\n")
    f.write("Successfully executed a massive platform audit. Fixed all routing issues, created responsive static pages (Pricing, About), implemented a unified feature templating engine for 26 modules, enforced RBAC authentication, and cleaned up legacy orphaned files. The Streamlit prototype is now production-ready.\n")

print("Successfully updated brain/")
