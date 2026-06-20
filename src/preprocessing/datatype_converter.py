"""
data_cleaning/type_converter.py — Data Type Converter
======================================================
Converts DataFrame columns to their correct dtypes with
full error logging and conversion success reporting.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import pandas as pd

from src.core.logging_manager import get_logger

logger = get_logger("src.preprocessing.datatype_converter")


# ── Result dataclass ──────────────────────────────────────────────────────────

@dataclass
class ConversionResult:
    """Per-column conversion outcome."""
    column:       str = ""
    target_dtype: str = ""
    success:      bool = True
    before_dtype: str = ""
    after_dtype:  str = ""
    coerced_nulls: int = 0    # values that became NaN during conversion
    error:        Optional[str] = None


@dataclass
class TypeConversionReport:
    """Full report of all type conversion operations."""
    results: list[ConversionResult] = field(default_factory=list)

    @property
    def success_count(self) -> int:
        return sum(1 for r in self.results if r.success)

    @property
    def failure_count(self) -> int:
        return sum(1 for r in self.results if not r.success)

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([
            {
                "Column":        r.column,
                "Target Type":   r.target_dtype,
                "Before":        r.before_dtype,
                "After":         r.after_dtype,
                "Status":        "✅ OK" if r.success else "❌ Failed",
                "Coerced Nulls": r.coerced_nulls,
                "Error":         r.error or "",
            }
            for r in self.results
        ])


# ── Converter class ───────────────────────────────────────────────────────────

class DataTypeConverter:
    """
    Convert DataFrame columns to correct dtypes.

    Example::

        converter = DataTypeConverter()
        df, report = converter.convert_dates(df, ["order_date", "ship_date"])
        df, report = converter.convert_numeric(df, ["revenue", "quantity"])
    """

    # ── Date conversion ───────────────────────────────────────────────────────

    def convert_dates(
        self,
        df: pd.DataFrame,
        cols: list[str],
        fmt: Optional[str] = None,
        utc: bool = False,
    ) -> tuple[pd.DataFrame, TypeConversionReport]:
        """
        Parse string/object columns to ``datetime64``.

        Args:
            df:   Input DataFrame.
            cols: Columns to convert.
            fmt:  Optional explicit strptime format string.
            utc:  If True, localise to UTC.

        Returns:
            (updated DataFrame, :class:`TypeConversionReport`)
        """
        df = df.copy()
        report = TypeConversionReport()

        for col in cols:
            if col not in df.columns:
                report.results.append(ConversionResult(
                    column=col, target_dtype="datetime",
                    success=False, error=f"Column '{col}' not found."
                ))
                continue

            before = str(df[col].dtype)
            nulls_before = df[col].isna().sum()

            try:
                df[col] = pd.to_datetime(df[col], format=fmt, utc=utc, errors="coerce")
                nulls_after = df[col].isna().sum()
                coerced = int(nulls_after - nulls_before)
                report.results.append(ConversionResult(
                    column=col, target_dtype="datetime",
                    before_dtype=before, after_dtype=str(df[col].dtype),
                    coerced_nulls=max(0, coerced),
                ))
                logger.info(f"Date convert '{col}': {before} → {df[col].dtype}, coerced={coerced}")
            except Exception as exc:
                report.results.append(ConversionResult(
                    column=col, target_dtype="datetime",
                    before_dtype=before, success=False, error=str(exc)
                ))
                logger.error(f"Date convert failed for '{col}': {exc}")

        return df, report

    # ── Numeric conversion ────────────────────────────────────────────────────

    def convert_numeric(
        self,
        df: pd.DataFrame,
        cols: list[str],
        target: str = "float",
    ) -> tuple[pd.DataFrame, TypeConversionReport]:
        """
        Convert columns to numeric dtype (float or int).

        Non-parseable values are coerced to ``NaN``.

        Args:
            df:     Input DataFrame.
            cols:   Columns to convert.
            target: ``'float'`` or ``'int'``.
        """
        df = df.copy()
        report = TypeConversionReport()

        for col in cols:
            if col not in df.columns:
                report.results.append(ConversionResult(
                    column=col, target_dtype=target,
                    success=False, error=f"Column '{col}' not found."
                ))
                continue

            before = str(df[col].dtype)
            nulls_before = df[col].isna().sum()

            try:
                # Strip currency symbols / commas first
                if df[col].dtype == object:
                    df[col] = (
                        df[col]
                        .astype(str)
                        .str.replace(r"[^\d.\-]", "", regex=True)
                        .replace("", float("nan"))
                    )

                df[col] = pd.to_numeric(df[col], errors="coerce")

                if target == "int":
                    df[col] = df[col].round(0).astype("Int64")  # nullable int

                nulls_after = df[col].isna().sum()
                coerced = int(nulls_after - nulls_before)
                report.results.append(ConversionResult(
                    column=col, target_dtype=target,
                    before_dtype=before, after_dtype=str(df[col].dtype),
                    coerced_nulls=max(0, coerced),
                ))
                logger.info(f"Numeric convert '{col}': {before} → {df[col].dtype}")
            except Exception as exc:
                report.results.append(ConversionResult(
                    column=col, target_dtype=target,
                    before_dtype=before, success=False, error=str(exc)
                ))
                logger.error(f"Numeric convert failed for '{col}': {exc}")

        return df, report

    # ── Categorical conversion ────────────────────────────────────────────────

    def convert_categorical(
        self,
        df: pd.DataFrame,
        cols: list[str],
    ) -> tuple[pd.DataFrame, TypeConversionReport]:
        """
        Convert columns to ``pd.Categorical`` dtype (saves memory for low-cardinality cols).

        Args:
            df:   Input DataFrame.
            cols: Columns to convert.
        """
        df = df.copy()
        report = TypeConversionReport()

        for col in cols:
            if col not in df.columns:
                report.results.append(ConversionResult(
                    column=col, target_dtype="category",
                    success=False, error=f"Column '{col}' not found."
                ))
                continue

            before = str(df[col].dtype)
            try:
                df[col] = df[col].astype("category")
                report.results.append(ConversionResult(
                    column=col, target_dtype="category",
                    before_dtype=before, after_dtype="category",
                ))
                logger.info(f"Category convert '{col}': {before} → category")
            except Exception as exc:
                report.results.append(ConversionResult(
                    column=col, target_dtype="category",
                    before_dtype=before, success=False, error=str(exc)
                ))
                logger.error(f"Category convert failed for '{col}': {exc}")

        return df, report

    # ── Auto-detect and convert ───────────────────────────────────────────────

    def infer_and_convert(self, df: pd.DataFrame) -> tuple[pd.DataFrame, TypeConversionReport]:
        """
        Attempt to infer and convert dtypes for all object columns.

        - Columns that look like dates → datetime
        - Columns that look like numbers → float
        - Low-cardinality columns (< 10 % unique) → category

        Args:
            df: Input DataFrame.

        Returns:
            (updated DataFrame, :class:`TypeConversionReport`)
        """
        df = df.copy()
        report = TypeConversionReport()
        n = len(df)

        for col in df.columns:
            if df[col].dtype != object:
                continue

            sample = df[col].dropna().head(200).astype(str)

            # Try numeric: strip currency symbols / commas first for the test
            sample_stripped = sample.str.replace(r"[^\d.\-]", "", regex=True).replace("", float("nan"))
            numeric_attempt = pd.to_numeric(sample_stripped, errors="coerce")
            if numeric_attempt.notna().mean() > 0.8:
                df, sub = self.convert_numeric(df, [col])
                report.results.extend(sub.results)
                continue

            # Try datetime
            try:
                pd.to_datetime(sample, errors="raise")
                df, sub = self.convert_dates(df, [col])
                report.results.extend(sub.results)
                continue
            except Exception:
                pass

            # Low-cardinality → category
            cardinality = df[col].nunique(dropna=True) / n if n > 0 else 1
            if cardinality < 0.10:
                df, sub = self.convert_categorical(df, [col])
                report.results.extend(sub.results)

        logger.info(f"Infer & convert: processed {len(report.results)} columns.")
        return df, report
