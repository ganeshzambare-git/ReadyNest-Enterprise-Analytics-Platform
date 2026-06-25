import streamlit as st
import pandas as pd
import sys
import os
import tempfile
import time

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.ingestion.csv_loader import DataLoader
from src.core.security import get_secured_df

st.set_page_config(page_title="Data Ingestion - ReadyNest", page_icon="📥", layout="wide")

st.markdown("""
<div style="margin-bottom: 2rem;">
    <h1 style="color: #00EEFF; margin-bottom: 0.5rem; font-family: 'Orbitron', sans-serif;">Data Ingestion & Connection</h1>
    <p style="color: #94A3B8; font-size: 1.1rem; margin-bottom: 1rem;">Upload flat files or connect directly to enterprise databases.</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📄 Local File Upload", "☁️ Enterprise Database"])

with tab1:
    st.markdown("### Drag and Drop File Upload")
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel files", 
        type=["csv", "xlsx", "xls"],
        accept_multiple_files=False,
        help="Max file size 200MB."
    )
    
    if uploaded_file is not None:
        file_ext = uploaded_file.name.split('.')[-1].lower()
        
        with st.spinner(f"Loading {uploaded_file.name}..."):
            # Write to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
                
            loader = DataLoader()
            
            if file_ext == 'csv':
                result = loader.load_csv(tmp_path)
            else:
                result = loader.load_excel(tmp_path)
                
            # Cleanup temp file
            os.remove(tmp_path)
            
            if result.success:
                st.session_state["df"] = result.dataframe
                st.session_state["source_name"] = uploaded_file.name
                st.success(f"✅ Successfully loaded **{uploaded_file.name}** ({len(result.dataframe):,} rows × {len(result.dataframe.columns)} columns)")
                st.balloons()
            else:
                st.error(f"❌ Failed to load file: {result.error}")

with tab2:
    st.markdown("### Connect to Enterprise Data Warehouse")
    st.info("Cloud connectors (Snowflake, Databricks, PostgreSQL) are configured via the Enterprise Platform module.")
    st.button("Configure Connectors", disabled=True)

st.divider()

# Show the current loaded dataset
current_df = get_secured_df()
if current_df is not None:
    st.markdown(f"### Currently Loaded: `{st.session_state.get('source_name', 'Dataset')}`")
    st.dataframe(current_df.head(100), use_container_width=True)
    if st.button("🗑️ Clear Dataset", type="secondary"):
        if "df" in st.session_state: del st.session_state["df"]
        if "clean_df" in st.session_state: del st.session_state["clean_df"]
        if "source_name" in st.session_state: del st.session_state["source_name"]
        st.rerun()
else:
    st.info("No dataset currently loaded. Please upload a file to begin analysis.")
