# Mistakes & Lessons Learned

## Problem: Streamlit V1 Multipage Import Failure on Deployment
**Cause:** We originally placed Streamlit multipage files inside a folder named `pages/`. Streamlit's V1 legacy auto-discovery mechanism scans this folder on startup. These files contained absolute imports like `from src.app.authentication`. Because they were executed before `src/app/main.py` could modify `sys.path` to include the root directory, deployments failed with `ModuleNotFoundError`.
**Fix:** We renamed the directory from `pages/` to `views/`. This disabled Streamlit's implicit loading. We updated `src/app/main.py` to use `st.navigation(["views/file.py"])` ensuring files are only loaded explicitly after `sys.path` is initialized.
**Status:** Resolved.

## Problem: Subprocess Not Inheriting `PYTHONPATH`
**Cause:** The `app.py` wrapper used `subprocess.run(["streamlit", "run", "src/app/main.py"])` but didn't pass the root directory to the Streamlit process.
**Fix:** Modified `app.py` to read `os.environ`, explicitly inject `os.path.dirname(__file__)` into `PYTHONPATH`, and pass `env=env` to the subprocess.
**Status:** Resolved.
