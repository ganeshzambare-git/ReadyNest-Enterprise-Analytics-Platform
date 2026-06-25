"""
data_loading/loader.py — Data Ingestion
========================================
DataLoader is the main entry point for loading data from CSV files,
Excel workbooks, SQL databases, and batch folder uploads.

All methods validate before loading, log every operation, and return
plain DataFrames — keeping I/O concerns separate from processing.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import pandas as pd

from src.config.config import MAX_PREVIEW_ROWS, SUPPORTED_EXTENSIONS
from src.database.connection import SQLConnector
from src.core.logging_manager import detect_file_type, get_logger, sanitize_column_names
from src.ingestion.schema_validator import FileValidator, ValidationResult
import streamlit as st

@st.cache_data(show_spinner=False)
def _cached_read_csv(path: str, encoding: str, sep: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(path, encoding=encoding, sep=sep, **kwargs)

@st.cache_data(show_spinner=False)
def _cached_read_excel(path: str, sheet_name, **kwargs) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name=sheet_name, **kwargs)

logger = get_logger("src.ingestion.csv_loader")


# ── LoadResult ────────────────────────────────────────────────────────────────

class LoadResult:
    """
    Container returned by every DataLoader.load_* method.

    Attributes:
        dataframe:        The loaded pandas DataFrame (or None on failure).
        validation:       The :class:`ValidationResult` from pre-load checks.
        source_name:      Human-readable label (filename / table name / query).
        success:          True if loading succeeded.
        error:            Error message string (populated on failure).
    """

    __slots__ = ("dataframe", "validation", "source_name", "success", "error")

    def __init__(
        self,
        dataframe: Optional[pd.DataFrame],
        validation: ValidationResult,
        source_name: str,
        success: bool = True,
        error: Optional[str] = None,
    ) -> None:
        self.dataframe = dataframe
        self.validation = validation
        self.source_name = source_name
        self.success = success
        self.error = error

    @property
    def preview(self) -> Optional[pd.DataFrame]:
        """Return first *MAX_PREVIEW_ROWS* rows, or None on failure."""
        if self.dataframe is None:
            return None
        return self.dataframe.head(MAX_PREVIEW_ROWS)

    def __repr__(self) -> str:
        status = "OK" if self.success else f"FAILED({self.error})"
        shape = (
            f"{len(self.dataframe):,}r × {len(self.dataframe.columns)}c"
            if self.dataframe is not None
            else "N/A"
        )
        return f"<LoadResult source={self.source_name!r} status={status} shape={shape}>"


# ── Main loader class ─────────────────────────────────────────────────────────

class DataLoader:
    """
    Multi-source data ingestion for the ReadyNest dashboard.

    Supported sources:
    - CSV files
    - Excel workbooks (.xlsx / .xls)
    - SQL databases (via :class:`SQLConnector`)
    - Folders containing multiple CSV/Excel files

    All methods:
    1. Validate inputs before I/O
    2. Log operations at INFO / ERROR level
    3. Return a :class:`LoadResult` — never raise silently

    Example::

        loader = DataLoader()
        result = loader.load_csv("data/sales_q3.csv")
        if result.success:
            df = result.dataframe
    """

    def __init__(
        self,
        expected_columns: Optional[list[str]] = None,
        sanitize_cols: bool = True,
    ) -> None:
        """
        Args:
            expected_columns: Optional schema reference passed to the validator.
            sanitize_cols:    If True, column names are lowercased and
                              special characters replaced with underscores.
        """
        self._validator = FileValidator(expected_columns=expected_columns)
        self._sanitize = sanitize_cols

    # ── CSV ───────────────────────────────────────────────────────────────────

    def load_csv(
        self,
        path: str | Path,
        encoding: str = "utf-8",
        separator: str = ",",
        **read_kwargs,
    ) -> LoadResult:
        """
        Load a CSV file into a DataFrame.

        Args:
            path:        Path to the .csv file.
            encoding:    File encoding (default ``'utf-8'``).
            separator:   Column delimiter (default ``','``).
            **read_kwargs: Extra keyword arguments forwarded to ``pd.read_csv``.

        Returns:
            :class:`LoadResult`
        """
        path = Path(path)
        logger.info(f"Loading CSV: {path.name}")

        validation = self._validator.validate(path)
        if not validation.is_valid:
            return LoadResult(
                dataframe=None,
                validation=validation,
                source_name=path.name,
                success=False,
                error="; ".join(validation.errors),
            )

        try:
            df = _cached_read_csv(
                str(path),
                encoding=encoding,
                sep=separator,
                **read_kwargs,
            )
            df = self._post_process(df)
            logger.info(f"CSV loaded: {len(df):,} rows × {len(df.columns)} cols.")
            return LoadResult(dataframe=df, validation=validation, source_name=path.name)

        except Exception as exc:
            msg = f"Failed to read CSV '{path.name}': {exc}"
            logger.error(msg)
            validation.add_error(msg)
            return LoadResult(
                dataframe=None,
                validation=validation,
                source_name=path.name,
                success=False,
                error=msg,
            )

    # ── Excel ─────────────────────────────────────────────────────────────────

    def load_excel(
        self,
        path: str | Path,
        sheet_name: str | int = 0,
        **read_kwargs,
    ) -> LoadResult:
        """
        Load a single sheet from an Excel workbook.

        Args:
            path:        Path to the .xlsx / .xls file.
            sheet_name:  Sheet name or index (default 0 = first sheet).
            **read_kwargs: Extra keyword arguments forwarded to ``pd.read_excel``.

        Returns:
            :class:`LoadResult`
        """
        path = Path(path)
        logger.info(f"Loading Excel: {path.name}, sheet={sheet_name!r}")

        validation = self._validator.validate(path)
        if not validation.is_valid:
            return LoadResult(
                dataframe=None,
                validation=validation,
                source_name=path.name,
                success=False,
                error="; ".join(validation.errors),
            )

        try:
            df = _cached_read_excel(str(path), sheet_name=sheet_name, **read_kwargs)
            df = self._post_process(df)
            logger.info(f"Excel loaded: {len(df):,} rows × {len(df.columns)} cols.")
            return LoadResult(dataframe=df, validation=validation, source_name=path.name)

        except Exception as exc:
            msg = f"Failed to read Excel '{path.name}': {exc}"
            logger.error(msg)
            validation.add_error(msg)
            return LoadResult(
                dataframe=None,
                validation=validation,
                source_name=path.name,
                success=False,
                error=msg,
            )

    def list_excel_sheets(self, path: str | Path) -> list[str]:
        """
        Return all sheet names in an Excel workbook without loading data.

        Args:
            path: Path to .xlsx / .xls file.

        Returns:
            List of sheet name strings.
        """
        try:
            xl = pd.ExcelFile(path)
            return xl.sheet_names
        except Exception as exc:
            logger.error(f"Cannot read sheets from '{path}': {exc}")
            return []

    # ── Folder ────────────────────────────────────────────────────────────────

    def load_folder(
        self,
        folder_path: str | Path,
        recursive: bool = False,
    ) -> dict[str, LoadResult]:
        """
        Load all supported files from a directory.

        Args:
            folder_path: Path to the folder.
            recursive:   If True, also search subdirectories.

        Returns:
            Dict mapping filename → :class:`LoadResult`.
            Files that fail to load have ``success=False`` in their result.
        """
        folder = Path(folder_path)
        if not folder.is_dir():
            raise NotADirectoryError(f"'{folder_path}' is not a valid directory.")

        pattern = "**/*" if recursive else "*"
        files = [
            f for f in folder.glob(pattern)
            if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
        ]

        logger.info(
            f"Folder load: found {len(files)} supported file(s) in '{folder.name}'."
        )

        results: dict[str, LoadResult] = {}
        for file_path in sorted(files):
            file_type = detect_file_type(file_path)
            if file_type == "csv":
                result = self.load_csv(file_path)
            elif file_type == "excel":
                result = self.load_excel(file_path)
            else:
                continue
            results[file_path.name] = result

        successes = sum(1 for r in results.values() if r.success)
        logger.info(
            f"Folder load complete: {successes}/{len(results)} files loaded successfully."
        )
        return results

    # ── SQL ───────────────────────────────────────────────────────────────────

    def load_from_sql(
        self,
        connector: SQLConnector,
        query: str,
        params: Optional[dict] = None,
    ) -> LoadResult:
        """
        Execute a SQL query and return results as a DataFrame.

        Args:
            connector: An initialised :class:`SQLConnector`.
            query:     SQL SELECT statement.
            params:    Optional query bind parameters.

        Returns:
            :class:`LoadResult`
        """
        if not query or not query.strip():
            raise ValueError("SQL query string cannot be empty.")

        logger.info(f"Loading from SQL: {query[:80]}...")

        from src.ingestion.schema_validator import ValidationResult as VR

        dummy_validation = VR(file_type="sql")

        try:
            df = connector.execute_query(query, params=params)
            df = self._post_process(df)

            col_validation = self._validator.validate_dataframe(df, name="SQL result")

            logger.info(f"SQL load: {len(df):,} rows × {len(df.columns)} cols.")
            return LoadResult(
                dataframe=df,
                validation=col_validation,
                source_name=f"SQL: {query[:60].strip()}",
            )

        except Exception as exc:
            msg = f"SQL load failed: {type(exc).__name__}: {exc}"
            logger.error(msg)
            dummy_validation.add_error(msg)
            return LoadResult(
                dataframe=None,
                validation=dummy_validation,
                source_name=f"SQL: {query[:60].strip()}",
                success=False,
                error=msg,
            )

    # ── Private helpers ───────────────────────────────────────────────────────

    def _post_process(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply standard post-load transformations:
        - Reset index
        - Optionally sanitise column names
        """
        df = df.reset_index(drop=True)
        if self._sanitize:
            df = sanitize_column_names(df)
        return df
