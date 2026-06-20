"""
data_analysis/security.py — Enterprise Security & RLS Enforcer
==============================================================
"""

import pandas as pd
import streamlit as st

def get_secured_df() -> pd.DataFrame | None:
    """
    Retrieves the dataset from session state and enforces any 
    active Row-Level Security (RLS) filters.
    """
    df = None
    if st.session_state.get("clean_df") is not None:
        df = st.session_state["clean_df"]
    elif st.session_state.get("df") is not None:
        df = st.session_state["df"]
        
    if df is None:
        return None
        
    # Enforce RLS
    rls = st.session_state.get("rls_filter")
    if rls:
        for col, val in rls.items():
            if col in df.columns:
                df = df[df[col] == val]
                
    return df
