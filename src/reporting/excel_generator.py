"""
data_loading/exporters.py — Data Export
=========================================
DataExporter handles writing cleaned DataFrames to CSV, Excel,
and SQL tables, and produces in-memory bytes for Streamlit
download buttons without writing temp files.
"""

from __future__ import annotations

import io
from pathlib import Path
from typing import Literal, Optional

import pandas as pd

from src.config.config import EXPORT_DIR
from src.database.connection import SQLConnector
from src.core.logging_manager import get_logger

logger = get_logger("src.reporting.excel_generator")

# Allowed export format literals
ExportFormat = Literal["csv", "excel"]


class DataExporter:
    """
    Export DataFrames to CSV, Excel, or SQL.

    All ``to_*`` methods write to the filesystem and log the result.
    ``get_download_bytes`` returns raw bytes for use with
    ``st.download_button`` in Streamlit — no temp files needed.

    Example::

        exporter = DataExporter()
        exporter.to_csv(cleaned_df, "exports/sales_clean.csv")
        bytes_data = exporter.get_download_bytes(df, fmt="excel")
    """

    def __init__(self, export_dir: Optional[Path] = None) -> None:
        """
        Args:
            export_dir: Base directory for all file exports.
                        Defaults to ``config.EXPORT_DIR``.
        """
        self._export_dir = Path(export_dir) if export_dir else EXPORT_DIR
        self._export_dir.mkdir(parents=True, exist_ok=True)

    # ── File exports ──────────────────────────────────────────────────────────

    def to_csv(
        self,
        df: pd.DataFrame,
        filename: str | Path,
        index: bool = False,
        encoding: str = "utf-8-sig",  # BOM for Excel compat
    ) -> Path:
        """
        Write *df* to a CSV file.

        Args:
            df:       DataFrame to export.
            filename: Filename (relative → placed in export_dir) or absolute path.
            index:    Whether to include the row index.
            encoding: File encoding. ``'utf-8-sig'`` adds a BOM so Excel
                      opens accented characters correctly.

        Returns:
            Absolute :class:`Path` of the written file.
        """
        self._guard(df, "CSV")
        out_path = self._resolve(filename, ".csv")
        df.to_csv(out_path, index=index, encoding=encoding)
        logger.info(f"CSV exported: {out_path}  ({len(df):,} rows)")
        return out_path

    def to_excel(
        self,
        df: pd.DataFrame,
        filename: str | Path,
        sheet_name: str = "Data",
        index: bool = False,
    ) -> Path:
        """
        Write *df* to an Excel workbook (.xlsx).

        Args:
            df:         DataFrame to export.
            filename:   Filename or absolute path.
            sheet_name: Target worksheet name.
            index:      Whether to include the row index.

        Returns:
            Absolute :class:`Path` of the written file.
        """
        self._guard(df, "Excel")
        out_path = self._resolve(filename, ".xlsx")
        with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=index)
        logger.info(f"Excel exported: {out_path}  ({len(df):,} rows)")
        return out_path

    # ── SQL export ────────────────────────────────────────────────────────────

    def to_sql(
        self,
        df: pd.DataFrame,
        connector: SQLConnector,
        table_name: str,
        if_exists: Literal["replace", "append", "fail"] = "replace",
        chunksize: int = 1000,
    ) -> None:
        """
        Write *df* to a SQL table via *connector*.

        Args:
            df:         DataFrame to write.
            connector:  Active :class:`SQLConnector` instance.
            table_name: Destination table.
            if_exists:  Behaviour if the table already exists.
            chunksize:  Rows per batch insert.
        """
        self._guard(df, "SQL")
        logger.info(
            f"Writing {len(df):,} rows → SQL table '{table_name}' "
            f"(if_exists='{if_exists}')"
        )
        connector.write_dataframe(
            df,
            table_name=table_name,
            if_exists=if_exists,
            chunksize=chunksize,
        )
        logger.info(f"SQL export complete: '{table_name}'")

    # ── In-memory bytes for Streamlit ─────────────────────────────────────────

    def get_download_bytes(
        self,
        df: pd.DataFrame,
        fmt: ExportFormat = "csv",
        sheet_name: str = "Data",
    ) -> bytes:
        """
        Serialise *df* to bytes without writing to disk.

        Use with ``st.download_button``::

            data = exporter.get_download_bytes(df, fmt="excel")
            st.download_button("⬇ Download Excel", data,
                               file_name="export.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        Args:
            df:         DataFrame to serialise.
            fmt:        ``'csv'`` or ``'excel'``.
            sheet_name: Excel sheet name (ignored for CSV).

        Returns:
            Raw bytes.
        """
        self._guard(df, fmt.upper())
        buf = io.BytesIO()

        if fmt == "csv":
            csv_str = df.to_csv(index=False, encoding="utf-8-sig")
            buf.write(csv_str.encode("utf-8-sig"))
        elif fmt == "excel":
            with pd.ExcelWriter(buf, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            raise ValueError(f"Unsupported export format: '{fmt}'. Use 'csv' or 'excel'.")

        buf.seek(0)
        logger.debug(f"get_download_bytes: {fmt}, {buf.getbuffer().nbytes:,} bytes")
        return buf.getvalue()

    # ── MIME type helper ──────────────────────────────────────────────────────

    @staticmethod
    def mime_type(fmt: ExportFormat) -> str:
        """Return the MIME type string for a given export format."""
        return {
            "csv":   "text/csv",
            "excel": (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
        }.get(fmt, "application/octet-stream")

    # ── Private helpers ───────────────────────────────────────────────────────

    def _guard(self, df: pd.DataFrame, label: str) -> None:
        if df is None or df.empty:
            raise ValueError(f"Cannot export an empty DataFrame as {label}.")

    def _resolve(self, filename: str | Path, suffix: str) -> Path:
        """
        If *filename* is a bare name (no parent dir), place it in export_dir.
        Ensure the correct extension is applied.
        """
        p = Path(filename)
        if not p.is_absolute() and not p.parent.name:
            p = self._export_dir / p
        if p.suffix.lower() != suffix:
            p = p.with_suffix(suffix)
        p.parent.mkdir(parents=True, exist_ok=True)
        return p
