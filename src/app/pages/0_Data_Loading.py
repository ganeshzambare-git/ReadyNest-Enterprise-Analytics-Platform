"""
streamlit_app.py — ReadyNest Data Loading Module UI
====================================================
Five-tab Streamlit dashboard for data ingestion, preview,
metadata analysis, SQL console, and export.

Run:
    streamlit run streamlit_app.py
"""

from __future__ import annotations

import traceback
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.config.config import APP_ICON, APP_TITLE, MAX_PREVIEW_ROWS, SAMPLE_DATA_DIR
from data_loading import (
    DataExporter,
    DataLoader,
    MetadataGenerator,
    SQLConnector,
)

# ── Shared helpers ────────────────────────────────────────────────────────────

loader   = DataLoader(sanitize_cols=True)
meta_gen = MetadataGenerator()
exporter = DataExporter()


def _quality_color(score: int) -> str:
    if score >= 90:
        return "#22c55e"   # green
    if score >= 75:
        return "#3b82f6"   # blue
    if score >= 50:
        return "#f59e0b"   # amber
    return "#ef4444"       # red


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style='text-align:center; padding: 12px 0 4px 0;'>
            <span style='font-size:2.4rem;'>📦</span><br>
            <span style='font-size:1.1rem; font-weight:800;
                         letter-spacing:.08em; color:#14235F;'>
                READYNEST
            </span><br>
            <span style='font-size:.72rem; color:#6b7280; letter-spacing:.12em;'>
                DATA LOADING MODULE
            </span>
        </div>
        <hr style='margin:12px 0;'>
        """,
        unsafe_allow_html=True,
    )

    source = st.radio(
        "**Select Data Source**",
        ["📄 CSV File", "📊 Excel File", "🗄️ SQL Database", "📁 Folder Upload"],
        index=0,
    )

    st.markdown("---")
    with st.expander("ℹ️ Quick Guide", expanded=False):
        st.markdown(
            """
            1. **Pick a source** above
            2. Upload your file (or enter SQL creds)
            3. Browse the **Preview**, **Summary**, and **Quality** tabs
            4. Connect to a database in the **SQL Console** tab
            5. Download your processed dataset from **Export**
            """
        )

# ── State ─────────────────────────────────────────────────────────────────────
if "df" not in st.session_state:
    st.session_state["df"] = None
if "source_name" not in st.session_state:
    st.session_state["source_name"] = None
if "report" not in st.session_state:
    st.session_state["report"] = None


def _store(df: pd.DataFrame, name: str) -> None:
    st.session_state["df"] = df
    st.session_state["source_name"] = name
    st.session_state["report"] = meta_gen.generate(df, file_name=name)


# ── Load panel ────────────────────────────────────────────────────────────────
st.title(f"{APP_ICON} ReadyNest — Data Loading Module")
st.caption("Ingest, validate, preview, and export your product sales data.")

load_col, _ = st.columns([3, 1])

with load_col:
    # ── CSV Upload ────────────────────────────────────────────────────────────
    if source == "📄 CSV File":
        col1, col2 = st.columns([2, 1])
        with col1:
            uploaded = st.file_uploader(
                "Upload a CSV file", type=["csv"], key="csv_upload"
            )
        with col2:
            sep = st.selectbox("Delimiter", [",", ";", "\t", "|"], index=0)
            enc = st.selectbox("Encoding", ["utf-8", "latin-1", "utf-8-sig"], index=0)

        btn_col, sample_col = st.columns([1, 1])
        with btn_col:
            if uploaded and st.button("▶ Load CSV", type="primary"):
                with st.spinner("Loading…"):
                    tmp = Path("_tmp_upload.csv")
                    tmp.write_bytes(uploaded.read())
                    result = loader.load_csv(tmp, encoding=enc, separator=sep)
                    
                    if result.success:
                        try:
                            from src.ingestion.folder_loader import DataLakePipeline
                            dlp = DataLakePipeline()
                            dlp.run_pipeline(tmp, uploaded.name)
                        except Exception as e:
                            st.warning(f"Data Lake Warning: {e}")
                    
                    tmp.unlink(missing_ok=True)
                if result.success:
                    st.info("🌊 Routed data through Enterprise Data Lake (Raw -> Clean -> Curated).")
                    _store(result.dataframe, uploaded.name)
                    st.success(f"✅ Loaded **{uploaded.name}** — {len(result.dataframe):,} rows")
                else:
                    st.error(f"❌ {result.error}")
        with sample_col:
            sample_file = SAMPLE_DATA_DIR / "readynest_sales_sample.csv"
            if sample_file.exists() and st.button("🧪 Load Sample Data"):
                result = loader.load_csv(sample_file)
                if result.success:
                    _store(result.dataframe, "readynest_sales_sample.csv")
                    st.success(f"✅ Sample data loaded — {len(result.dataframe):,} rows")

    # ── Excel Upload ──────────────────────────────────────────────────────────
    elif source == "📊 Excel File":
        uploaded = st.file_uploader(
            "Upload an Excel file", type=["xlsx", "xls"], key="excel_upload"
        )
        if uploaded:
            tmp = Path("_tmp_upload.xlsx")
            tmp.write_bytes(uploaded.getvalue())
            sheets = loader.list_excel_sheets(tmp)
            sheet = st.selectbox("Select Sheet", sheets) if sheets else None

            if sheet and st.button("▶ Load Excel", type="primary"):
                with st.spinner("Loading…"):
                    result = loader.load_excel(tmp, sheet_name=sheet)
                tmp.unlink(missing_ok=True)
                if result.success:
                    _store(result.dataframe, f"{uploaded.name} [{sheet}]")
                    st.success(
                        f"✅ Loaded **{uploaded.name}** / **{sheet}** — "
                        f"{len(result.dataframe):,} rows"
                    )
                else:
                    st.error(f"❌ {result.error}")

    # ── Folder Upload ─────────────────────────────────────────────────────────
    elif source == "📁 Folder Upload":
        st.info(
            "Upload multiple CSV/Excel files at once. "
            "Each file will be validated and loaded independently."
        )
        files = st.file_uploader(
            "Upload files (CSV or Excel)",
            type=["csv", "xlsx", "xls"],
            accept_multiple_files=True,
            key="folder_upload",
        )
        if files and st.button("▶ Load All Files", type="primary"):
            tmp_dir = Path("_tmp_folder")
            tmp_dir.mkdir(exist_ok=True)
            for f in files:
                (tmp_dir / f.name).write_bytes(f.read())

            with st.spinner(f"Loading {len(files)} file(s)…"):
                batch = loader.load_folder(tmp_dir)

            # Display results table
            summary_rows = []
            for fname, res in batch.items():
                summary_rows.append(
                    {
                        "File": fname,
                        "Status": "✅ OK" if res.success else "❌ Failed",
                        "Rows": f"{len(res.dataframe):,}" if res.success else "—",
                        "Columns": len(res.dataframe.columns) if res.success else "—",
                        "Error": res.error or "",
                    }
                )
            st.dataframe(pd.DataFrame(summary_rows), use_container_width=True)

            # Merge all successful loads
            good = [r.dataframe for r in batch.values() if r.success]
            if good:
                merged = pd.concat(good, ignore_index=True)
                _store(merged, f"Batch ({len(good)} files merged)")
                st.success(f"✅ Merged {len(good)} files → {len(merged):,} total rows")

            # Cleanup
            import shutil
            shutil.rmtree(tmp_dir, ignore_errors=True)

    # ── SQL Database ──────────────────────────────────────────────────────────
    elif source == "🗄️ SQL Database":
        st.markdown("#### 🗄️ Database Connection")
        c1, c2 = st.columns(2)
        with c1:
            db_type = st.selectbox("Database Type", ["postgresql", "mysql"])
            db_host = st.text_input("Host", value="localhost")
            db_port = st.number_input(
                "Port", value=5432 if db_type == "postgresql" else 3306,
                min_value=1, max_value=65535
            )
        with c2:
            db_name = st.text_input("Database Name", value="readynest_db")
            db_user = st.text_input("Username", value="postgres")
            db_pass = st.text_input("Password", type="password")

        if st.button("🔌 Test Connection"):
            with st.spinner("Connecting…"):
                try:
                    conn = SQLConnector(
                        db_type=db_type, host=db_host, port=int(db_port),
                        database=db_name, user=db_user, password=db_pass
                    )
                    result = conn.test_connection()
                    conn.close()
                    if result.success:
                        st.success(result.summary)
                    else:
                        st.error(result.summary)
                except Exception as exc:
                    st.error(f"❌ {exc}")

        st.markdown("#### ▶ Execute Query")
        query = st.text_area(
            "SQL Query",
            value="SELECT * FROM sales LIMIT 100;",
            height=120,
        )
        if st.button("Run Query", type="primary"):
            with st.spinner("Executing…"):
                try:
                    conn = SQLConnector(
                        db_type=db_type, host=db_host, port=int(db_port),
                        database=db_name, user=db_user, password=db_pass
                    )
                    res = loader.load_from_sql(conn, query)
                    conn.close()
                    if res.success:
                        _store(res.dataframe, f"SQL: {query[:40]}…")
                        st.success(f"✅ {len(res.dataframe):,} rows returned.")
                    else:
                        st.error(f"❌ {res.error}")
                except Exception as exc:
                    st.error(f"❌ {exc}")


# ── Tabs ──────────────────────────────────────────────────────────────────────
st.markdown("---")

df: pd.DataFrame | None = st.session_state.get("df")
report = st.session_state.get("report")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🔍 Data Preview", "📋 Dataset Summary", "🩺 Quality Report",
     "🗄️ SQL Console", "⬇ Export"]
)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1: DATA PREVIEW
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    if df is None:
        st.info("⬆ Load a dataset using the panel above to see a preview here.")
    else:
        src_name = st.session_state.get("source_name", "Dataset")
        st.subheader(f"Preview — *{src_name}*")
        st.caption(
            f"Showing first **{min(MAX_PREVIEW_ROWS, len(df))}** of "
            f"**{len(df):,}** rows · **{len(df.columns)}** columns"
        )

        # Row-count selector
        n_rows = st.slider("Rows to preview", 5, min(100, len(df)), MAX_PREVIEW_ROWS)
        st.dataframe(df.head(n_rows), use_container_width=True, height=340)

        # Column info table
        st.subheader("Column Details")
        col_info = pd.DataFrame(
            {
                "Column":    df.columns.tolist(),
                "Data Type": [str(dt) for dt in df.dtypes],
                "Non-Null":  df.notna().sum().values,
                "Null Count": df.isna().sum().values,
                "Unique":    [df[c].nunique() for c in df.columns],
            }
        )
        st.dataframe(col_info, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: DATASET SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    if report is None:
        st.info("⬆ Load a dataset to see summary statistics.")
    else:
        st.subheader("📋 Dataset Summary")

        # KPI cards
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Rows", f"{report.row_count:,}")
        k2.metric("Columns", report.col_count)
        k3.metric("Memory", report.memory_human)
        k4.metric("Duplicate Rows", f"{report.duplicate_rows:,}",
                  delta=f"{report.duplicate_pct:.1f}%",
                  delta_color="inverse")
        k5.metric("Total Nulls", f"{report.total_nulls:,}")

        st.markdown("---")

        # Column-level stats table
        st.subheader("Column Statistics")
        col_df = meta_gen.column_summary_df(report)
        st.dataframe(col_df, use_container_width=True)

        st.markdown("---")

        # Dtypes distribution
        if df is not None:
            st.subheader("Data Type Distribution")
            dtype_counts = df.dtypes.astype(str).value_counts().reset_index()
            dtype_counts.columns = ["Data Type", "Count"]
            fig = px.pie(
                dtype_counts, names="Data Type", values="Count",
                color_discrete_sequence=px.colors.qualitative.Set2,
                hole=0.45,
            )
            fig.update_layout(margin=dict(t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: QUALITY REPORT
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    if report is None:
        st.info("⬆ Load a dataset to generate a quality report.")
    else:
        st.subheader("🩺 Data Quality Report")

        q_color = _quality_color(report.quality_score)

        # Quality score gauge
        gauge_fig = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=report.quality_score,
                delta={"reference": 100, "valueformat": ".0f"},
                title={"text": f"Quality Score: <b>{report.quality_label}</b>",
                       "font": {"size": 18}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1},
                    "bar":  {"color": q_color},
                    "steps": [
                        {"range": [0,  50], "color": "#fee2e2"},
                        {"range": [50, 75], "color": "#fef9c3"},
                        {"range": [75, 90], "color": "#dbeafe"},
                        {"range": [90, 100],"color": "#dcfce7"},
                    ],
                    "threshold": {
                        "line": {"color": "#111827", "width": 3},
                        "thickness": 0.8,
                        "value": report.quality_score,
                    },
                },
            )
        )
        gauge_fig.update_layout(height=280, margin=dict(t=20, b=10, l=20, r=20))
        st.plotly_chart(gauge_fig, use_container_width=True)

        # Issues list
        if report.quality_issues:
            st.warning("**Quality Issues Detected:**")
            for issue in report.quality_issues:
                st.markdown(f"- ⚠️ {issue}")
        else:
            st.success("🎉 No quality issues detected — dataset looks clean!")

        st.markdown("---")

        # Null count bar chart
        st.subheader("Null Count by Column")
        null_data = pd.DataFrame(
            [{"Column": c.name, "Null Count": c.null_count, "Null %": c.null_pct}
             for c in report.columns if c.null_count > 0]
        )
        if null_data.empty:
            st.success("✅ No null values detected in any column.")
        else:
            fig_null = px.bar(
                null_data.sort_values("Null Count", ascending=False),
                x="Column", y="Null Count",
                color="Null %",
                color_continuous_scale=["#86efac", "#f59e0b", "#ef4444"],
                text="Null %",
                labels={"Null Count": "Null Count"},
            )
            fig_null.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_null.update_layout(margin=dict(t=10, b=10), height=350)
            st.plotly_chart(fig_null, use_container_width=True)

        # Duplicate analysis
        st.markdown("---")
        st.subheader("Duplicate Analysis")
        d1, d2 = st.columns(2)
        d1.metric("Duplicate Rows", f"{report.duplicate_rows:,}")
        d2.metric("Duplicate %", f"{report.duplicate_pct:.2f}%")

        if report.duplicate_rows > 0 and df is not None:
            if st.checkbox("Show duplicate rows"):
                st.dataframe(df[df.duplicated(keep=False)].head(50),
                             use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4: SQL CONSOLE
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.subheader("🗄️ SQL Console")
    st.caption("Connect to PostgreSQL or MySQL and run ad-hoc queries.")

    with st.form("sql_console_form"):
        fc1, fc2 = st.columns(2)
        with fc1:
            c_type = st.selectbox("Database", ["postgresql", "mysql"], key="console_db")
            c_host = st.text_input("Host", value="localhost", key="console_host")
            c_port = st.number_input("Port", value=5432, min_value=1,
                                     max_value=65535, key="console_port")
        with fc2:
            c_name = st.text_input("Database Name", value="readynest_db", key="console_name")
            c_user = st.text_input("User", value="postgres", key="console_user")
            c_pass = st.text_input("Password", type="password", key="console_pass")

        c_query = st.text_area(
            "SQL Query",
            value="SELECT table_name FROM information_schema.tables "
                  "WHERE table_schema = 'public';",
            height=130,
            key="console_query",
        )

        col_test, col_run = st.columns(2)
        test_btn = col_test.form_submit_button("🔌 Test Connection")
        run_btn  = col_run.form_submit_button("▶ Run Query", type="primary")

    if test_btn or run_btn:
        try:
            sql_conn = SQLConnector(
                db_type=c_type, host=c_host, port=int(c_port),
                database=c_name, user=c_user, password=c_pass,
            )
            if test_btn:
                with st.spinner("Testing…"):
                    cr = sql_conn.test_connection()
                st.success(cr.summary) if cr.success else st.error(cr.summary)
                # Show tables if connected
                if cr.success:
                    try:
                        tables = sql_conn.list_tables()
                        if tables:
                            st.info(f"Tables in `{c_name}`: **{', '.join(tables[:20])}**")
                    except Exception:
                        pass

            if run_btn:
                with st.spinner("Running query…"):
                    qr = loader.load_from_sql(sql_conn, c_query)
                if qr.success:
                    _store(qr.dataframe, f"SQL: {c_query[:40]}")
                    st.success(f"✅ Returned **{len(qr.dataframe):,}** rows.")
                    st.dataframe(qr.dataframe.head(100), use_container_width=True)
                else:
                    st.error(f"❌ {qr.error}")

            sql_conn.close()
        except Exception as exc:
            st.error(f"❌ {exc}")
            with st.expander("Traceback"):
                st.code(traceback.format_exc())

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5: EXPORT
# ─────────────────────────────────────────────────────────────────────────────
with tab5:
    st.subheader("⬇ Export Processed Dataset")

    if df is None:
        st.info("⬆ Load a dataset first, then come back here to export it.")
    else:
        st.markdown(
            f"**Ready to export:** `{st.session_state.get('source_name', 'Dataset')}` "
            f"— **{len(df):,}** rows × **{len(df.columns)}** columns"
        )

        ex1, ex2 = st.columns(2)

        with ex1:
            st.markdown("#### 📄 Download as CSV")
            csv_bytes = exporter.get_download_bytes(df, fmt="csv")
            st.download_button(
                label="⬇ Download CSV",
                data=csv_bytes,
                file_name="readynest_export.csv",
                mime=DataExporter.mime_type("csv"),
                use_container_width=True,
            )

        with ex2:
            st.markdown("#### 📊 Download as Excel")
            xl_bytes = exporter.get_download_bytes(df, fmt="excel", sheet_name="Data")
            st.download_button(
                label="⬇ Download Excel",
                data=xl_bytes,
                file_name="readynest_export.xlsx",
                mime=DataExporter.mime_type("excel"),
                use_container_width=True,
            )

        st.markdown("---")
        st.markdown("#### 🗄️ Save to SQL Table")
        with st.form("export_sql_form"):
            es1, es2 = st.columns(2)
            with es1:
                e_type = st.selectbox("Database", ["postgresql", "mysql"])
                e_host = st.text_input("Host", value="localhost")
                e_port = st.number_input("Port", value=5432, min_value=1, max_value=65535)
            with es2:
                e_name = st.text_input("Database Name", value="readynest_db")
                e_user = st.text_input("User", value="postgres")
                e_pass = st.text_input("Password", type="password")

            e_table = st.text_input("Target Table Name", value="readynest_sales")
            e_mode  = st.selectbox("If Table Exists", ["replace", "append", "fail"])
            export_btn = st.form_submit_button("📤 Export to SQL", type="primary")

        if export_btn:
            with st.spinner("Writing to database…"):
                try:
                    sql_exp = SQLConnector(
                        db_type=e_type, host=e_host, port=int(e_port),
                        database=e_name, user=e_user, password=e_pass,
                    )
                    exporter.to_sql(df, sql_exp, e_table, if_exists=e_mode)
                    sql_exp.close()
                    st.success(
                        f"✅ {len(df):,} rows written to **{e_name}.{e_table}**."
                    )
                except Exception as exc:
                    st.error(f"❌ {exc}")
                    with st.expander("Traceback"):
                        st.code(traceback.format_exc())
