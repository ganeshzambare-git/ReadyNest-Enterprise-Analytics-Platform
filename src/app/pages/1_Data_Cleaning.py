"""
src/app/pages/1_Data_Cleaning.py — ReadyNest Data Cleaning Module UI
=============================================================
6-tab Streamlit dashboard for data cleaning.
Reads from st.session_state["df"] if available.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.config.config import APP_ICON, APP_TITLE
from src.preprocessing.data_cleaner import DataCleaner
from src.preprocessing.standardization import DataStandardizer
from src.preprocessing.datatype_converter import DataTypeConverter
from src.preprocessing.duplicate_handler import DuplicateHandler
from src.preprocessing.missing_value_handler import MissingValueHandler
from src.preprocessing.outlier_detector import OutlierDetector
from src.preprocessing.quality_scorer import QualityScorer

# ── Setup & State ─────────────────────────────────────────────────────────────

if "clean_df" not in st.session_state:
    st.session_state["clean_df"] = None
if "cleaning_log" not in st.session_state:
    from src.preprocessing.data_cleaner import CleaningLog
    st.session_state["cleaning_log"] = CleaningLog()
if "original_quality" not in st.session_state:
    st.session_state["original_quality"] = None

def get_current_df() -> pd.DataFrame | None:
    if st.session_state["clean_df"] is not None:
        return st.session_state["clean_df"]
    if st.session_state.get("df") is not None:
        # Initialize from Data Loading module
        st.session_state["clean_df"] = st.session_state["df"].copy()
        # Compute baseline quality
        scorer = QualityScorer()
        st.session_state["original_quality"] = scorer.score(st.session_state["clean_df"])
        return st.session_state["clean_df"]
    return None

def update_df(new_df: pd.DataFrame, log_entry=None) -> None:
    st.session_state["clean_df"] = new_df
    if log_entry:
        # log_entry is typically the returned CleaningLog from a step, we just merge or store it
        # Actually, cleaner steps update their own log, we should just keep one master log in state
        pass

# Initialize helpers
imputer = MissingValueHandler()
dedup = DuplicateHandler()
converter = DataTypeConverter()
standardizer = DataStandardizer()
outlier_detector = OutlierDetector()
scorer = QualityScorer()

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        """
        <div style='text-align:center; padding: 12px 0 4px 0;'>
            <span style='font-size:2.4rem;'>🧹</span><br>
            <span style='font-size:1.1rem; font-weight:800;
                         letter-spacing:.08em; color:#14235F;'>
                READYNEST
            </span><br>
            <span style='font-size:.72rem; color:#6b7280; letter-spacing:.12em;'>
                DATA CLEANING MODULE
            </span>
        </div>
        <hr style='margin:12px 0;'>
        """,
        unsafe_allow_html=True,
    )
    
    st.info("💡 **Tip:** Load data in the **Data Loading** module first, then come here to clean it.")
    
    if st.button("🔄 Reset to Original Data"):
        if st.session_state.get("df") is not None:
            st.session_state["clean_df"] = st.session_state["df"].copy()
            from src.preprocessing.data_cleaner import CleaningLog
            st.session_state["cleaning_log"] = CleaningLog()
            st.success("Reset to original data!")
            st.rerun()
        else:
            st.warning("No original data found. Please load data first.")

# ── Main UI ───────────────────────────────────────────────────────────────────

st.title("🧹 Data Cleaning Engine")
st.caption("Automated data cleaning and quality scoring.")

df = get_current_df()

if df is None:
    st.warning("⚠️ No data found. Please go to the **Data Loading** module and load a dataset first.")
    st.stop()

# ── Tabs ──────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔍 Overview", 
    "🩹 Missing Values", 
    "♻️ Duplicates", 
    "🔄 Type & Format", 
    "📡 Outliers", 
    "📊 Quality Dashboard"
])

# ── Tab 1: Overview ───────────────────────────────────────────────────────────
with tab1:
    st.subheader("Dataset Overview")
    k1, k2, k3 = st.columns(3)
    k1.metric("Rows", f"{len(df):,}")
    k2.metric("Columns", len(df.columns))
    missing_cells = df.isna().sum().sum()
    k3.metric("Missing Cells", f"{missing_cells:,}")
    
    st.dataframe(df.head(100), use_container_width=True)
    
    if missing_cells > 0:
        st.subheader("Missing Value Heatmap")
        null_counts = df.isna().sum()
        null_df = pd.DataFrame({"Column": null_counts.index, "Missing Count": null_counts.values})
        null_df = null_df[null_df["Missing Count"] > 0]
        fig = px.bar(null_df, x="Column", y="Missing Count", title="Missing Values per Column")
        st.plotly_chart(fig, use_container_width=True)

# ── Tab 2: Missing Values ─────────────────────────────────────────────────────
with tab2:
    st.subheader("🩹 Handle Missing Values")
    null_info = imputer.detect(df)
    st.dataframe(null_info, use_container_width=True)
    
    cols_with_nulls = null_info[null_info["Has Nulls"]]["Column"].tolist()
    
    if not cols_with_nulls:
        st.success("No missing values detected!")
    else:
        with st.form("impute_form"):
            col_to_impute = st.selectbox("Select Column", cols_with_nulls)
            strategy = st.selectbox("Strategy", ["mean", "median", "mode", "drop", "flag"])
            apply_btn = st.form_submit_button("▶ Apply Imputation")
            
        if apply_btn:
            with st.spinner("Applying..."):
                new_df, msg = imputer.apply_strategy(df, col_to_impute, strategy)
                st.session_state["cleaning_log"].record("impute", msg, df, new_df)
                update_df(new_df)
                st.success(msg)
                st.rerun()

# ── Tab 3: Duplicates ─────────────────────────────────────────────────────────
with tab3:
    st.subheader("♻️ Handle Duplicates")
    dup_report = dedup.detect(df)
    
    d1, d2 = st.columns(2)
    d1.metric("Duplicate Rows", f"{dup_report.duplicate_count:,}")
    d2.metric("Duplicate %", f"{dup_report.duplicate_pct}%")
    
    if dup_report.is_clean:
        st.success("No duplicates detected!")
    else:
        st.warning(dup_report.summary_text())
        if dup_report.sample_rows is not None:
            st.write("Sample Duplicates:")
            st.dataframe(dup_report.sample_rows, use_container_width=True)
            
        with st.form("dedup_form"):
            keep_strat = st.selectbox("Keep Strategy", ["first", "last", "False (Drop All)"])
            keep_val = False if "False" in keep_strat else keep_strat
            rm_btn = st.form_submit_button("▶ Remove Duplicates")
            
        if rm_btn:
            with st.spinner("Removing..."):
                new_df, res_report = dedup.remove(df, keep=keep_val)
                msg = f"Removed {res_report.rows_removed} duplicate rows."
                st.session_state["cleaning_log"].record("deduplicate", msg, df, new_df)
                update_df(new_df)
                st.success(msg)
                st.rerun()

# ── Tab 4: Type & Format ──────────────────────────────────────────────────────
with tab4:
    st.subheader("🔄 Type & Format Standardization")
    
    c1, c2 = st.columns(2)
    with c1:
        st.write("Current Types:")
        type_df = pd.DataFrame({"Column": df.columns, "Type": df.dtypes.astype(str)})
        st.dataframe(type_df, use_container_width=True)
        
        if st.button("⚡ Auto-Convert Types"):
            with st.spinner("Converting..."):
                new_df, type_rep = converter.infer_and_convert(df)
                msg = f"Auto-converted {type_rep.success_count} columns."
                st.session_state["cleaning_log"].record("convert_types", msg, df, new_df)
                update_df(new_df)
                st.success(msg)
                st.rerun()
                
    with c2:
        st.write("Text Standardization")
        with st.form("std_form"):
            txt_cols = st.multiselect("Select Text Columns", df.select_dtypes(include=["object"]).columns)
            case_opt = st.selectbox("Case", ["lower", "upper", "title", "strip"])
            strip_spc = st.checkbox("Strip Special Characters", value=False)
            std_btn = st.form_submit_button("▶ Standardize Text")
            
        if std_btn and txt_cols:
            with st.spinner("Standardizing..."):
                new_df, std_rep = standardizer.normalize_text(df, txt_cols, case=case_opt, strip_special=strip_spc)
                msg = f"Standardized {len(txt_cols)} text columns."
                st.session_state["cleaning_log"].record("standardize", msg, df, new_df)
                update_df(new_df)
                st.success(msg)
                st.rerun()

# ── Tab 5: Outliers ───────────────────────────────────────────────────────────
with tab5:
    st.subheader("📡 Outlier Detection")
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    num_cols = [c for c in num_cols if not c.endswith("_outlier")]
    
    if not num_cols:
        st.info("No numeric columns available for outlier detection.")
    else:
        with st.form("outlier_form"):
            method = st.selectbox("Method", ["iqr", "zscore"])
            if method == "iqr":
                factor = st.slider("IQR Factor", 1.0, 5.0, 1.5, 0.5)
                thresh = 3.0
            else:
                factor = 1.5
                thresh = st.slider("Z-Score Threshold", 2.0, 5.0, 3.0, 0.5)
                
            action = st.selectbox("Action", ["Detect & Flag", "Cap (Winsorize)"])
            out_btn = st.form_submit_button("▶ Process Outliers")
            
        if out_btn:
            with st.spinner("Processing outliers..."):
                if action == "Detect & Flag":
                    if method == "iqr":
                        new_df, out_rep = outlier_detector.detect_iqr(df, factor=factor)
                    else:
                        new_df, out_rep = outlier_detector.detect_zscore(df, threshold=thresh)
                    msg = f"Flagged {out_rep.total_outliers} outliers."
                else:
                    new_df, out_rep = outlier_detector.cap_outliers(df, method=method, factor=factor, threshold=thresh)
                    msg = f"Capped {out_rep.total_outliers} outliers."
                    
                st.session_state["cleaning_log"].record("detect_outliers", msg, df, new_df)
                update_df(new_df)
                st.success(msg)
                st.rerun()

# ── Tab 6: Quality Dashboard ──────────────────────────────────────────────────
with tab6:
    st.subheader("📊 Data Quality Dashboard")
    
    current_quality = scorer.score(df)
    
    q1, q2 = st.columns(2)
    with q1:
        # Gauge Chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = current_quality.composite_score,
            title = {'text': f"Current Quality: {current_quality.composite_label}"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "red"},
                    {'range': [50, 75], 'color': "orange"},
                    {'range': [75, 90], 'color': "lightgreen"},
                    {'range': [90, 100], 'color': "green"}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
        
    with q2:
        # Radar Chart for Dimensions
        categories = [d.name for d in current_quality.dimensions]
        values = [d.score for d in current_quality.dimensions]
        
        orig_values = None
        if st.session_state["original_quality"]:
            orig_values = [d.score for d in st.session_state["original_quality"].dimensions]
            
        fig_radar = go.Figure()
        if orig_values:
            fig_radar.add_trace(go.Scatterpolar(
                r=orig_values, theta=categories, fill='toself', name='Original'
            ))
        fig_radar.add_trace(go.Scatterpolar(
            r=values, theta=categories, fill='toself', name='Current'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True)
        st.plotly_chart(fig_radar, use_container_width=True)
        
    st.dataframe(current_quality.to_dataframe(), use_container_width=True)
    
    st.markdown("---")
    st.subheader("⬇️ Export Cleaned Data")
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Clean CSV", data=csv_data, file_name="cleaned_data.csv", mime="text/csv", use_container_width=True)
    with col_dl2:
        log_df = st.session_state["cleaning_log"].to_dataframe()
        log_csv = log_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Cleaning Log", data=log_csv, file_name="cleaning_log.csv", mime="text/csv", use_container_width=True)
