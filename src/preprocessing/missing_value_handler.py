"""
data_cleaning/imputers.py — Missing Value Handler
==================================================
Detects, reports and fills missing values using configurable strategies:
mean / median / mode / drop / flag.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional

import numpy as np
import pandas as pd

from src.core.logging_manager import get_logger

logger = get_logger("src.preprocessing.missing_value_handler")

Strategy = Literal["mean", "median", "mode", "drop", "flag", "none"]


# ── Result dataclass ──────────────────────────────────────────────────────────

@dataclass
class ImputationReport:
    """Summary produced after running imputation."""
    strategy_applied: dict[str, str] = field(default_factory=dict)
    nulls_before:     dict[str, int] = field(default_factory=dict)
    nulls_after:      dict[str, int] = field(default_factory=dict)
    rows_dropped:     int = 0
    flag_cols_added:  list[str] = field(default_factory=list)

    @property
    def total_filled(self) -> int:
        return sum(
            self.nulls_before.get(c, 0) - self.nulls_after.get(c, 0)
            for c in self.nulls_before
        )

    def to_dataframe(self) -> pd.DataFrame:
        rows = []
        for col in self.nulls_before:
            rows.append({
                "Column":     col,
                "Strategy":   self.strategy_applied.get(col, "none"),
                "Nulls Before": self.nulls_before[col],
                "Nulls After":  self.nulls_after.get(col, 0),
                "Filled":       self.nulls_before[col] - self.nulls_after.get(col, 0),
            })
        return pd.DataFrame(rows)


# ── Handler class ─────────────────────────────────────────────────────────────

class MissingValueHandler:
    """
    Detect and handle missing values in a DataFrame.

    Example::

        handler = MissingValueHandler()
        null_info = handler.detect(df)
        df_clean, report = handler.impute_mean(df, cols=["revenue", "quantity"])
    """

    # ── Detection ─────────────────────────────────────────────────────────────

    def detect(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Return a summary DataFrame with null counts and percentages per column.

        Args:
            df: Input DataFrame.

        Returns:
            DataFrame with columns: Column, Null Count, Null %, Has Nulls.
        """
        n = len(df)
        rows = []
        for col in df.columns:
            cnt = int(df[col].isna().sum())
            rows.append({
                "Column":     col,
                "Dtype":      str(df[col].dtype),
                "Null Count": cnt,
                "Null %":     round(cnt / n * 100, 2) if n > 0 else 0.0,
                "Has Nulls":  cnt > 0,
            })
        return pd.DataFrame(rows)

    def null_percentage(self, df: pd.DataFrame) -> dict[str, float]:
        """Return {column: null_percentage} for all columns."""
        n = len(df)
        return {
            col: round(df[col].isna().sum() / n * 100, 2) if n > 0 else 0.0
            for col in df.columns
        }

    # ── Imputation strategies ─────────────────────────────────────────────────

    def impute_mean(
        self, df: pd.DataFrame, cols: Optional[list[str]] = None
    ) -> tuple[pd.DataFrame, ImputationReport]:
        """Fill nulls in numeric columns with their column mean."""
        df, report = self._prepare(df, cols, strategy="mean")
        numeric_cols = [c for c in report.strategy_applied if pd.api.types.is_numeric_dtype(df[c])]
        for col in numeric_cols:
            fill_val = df[col].mean()
            df[col] = df[col].fillna(fill_val)
        self._finalize_report(df, report)
        logger.info(f"Mean imputation: filled {report.total_filled} nulls in {len(numeric_cols)} cols.")
        return df, report

    def impute_median(
        self, df: pd.DataFrame, cols: Optional[list[str]] = None
    ) -> tuple[pd.DataFrame, ImputationReport]:
        """Fill nulls in numeric columns with their column median."""
        df, report = self._prepare(df, cols, strategy="median")
        numeric_cols = [c for c in report.strategy_applied if pd.api.types.is_numeric_dtype(df[c])]
        for col in numeric_cols:
            fill_val = df[col].median()
            df[col] = df[col].fillna(fill_val)
        self._finalize_report(df, report)
        logger.info(f"Median imputation: filled {report.total_filled} nulls in {len(numeric_cols)} cols.")
        return df, report

    def impute_mode(
        self, df: pd.DataFrame, cols: Optional[list[str]] = None
    ) -> tuple[pd.DataFrame, ImputationReport]:
        """Fill nulls in any column with the column mode (most frequent value)."""
        df, report = self._prepare(df, cols, strategy="mode")
        for col in report.strategy_applied:
            mode_vals = df[col].mode()
            if not mode_vals.empty:
                df[col] = df[col].fillna(mode_vals.iloc[0])
        self._finalize_report(df, report)
        logger.info(f"Mode imputation: filled {report.total_filled} nulls.")
        return df, report

    def drop_nulls(
        self,
        df: pd.DataFrame,
        cols: Optional[list[str]] = None,
        how: Literal["any", "all"] = "any",
    ) -> tuple[pd.DataFrame, ImputationReport]:
        """
        Drop rows containing nulls.

        Args:
            df:   Input DataFrame.
            cols: Columns to consider (None = all columns).
            how:  ``'any'`` drops rows with at least one null;
                  ``'all'`` drops rows where all specified cols are null.

        Returns:
            Cleaned DataFrame and :class:`ImputationReport`.
        """
        df, report = self._prepare(df, cols, strategy="drop")
        before = len(df)
        subset = list(report.strategy_applied.keys()) if cols else None
        df = df.dropna(subset=subset, how=how).reset_index(drop=True)
        report.rows_dropped = before - len(df)
        self._finalize_report(df, report)
        logger.info(f"Drop nulls: removed {report.rows_dropped} rows (how='{how}').")
        return df, report

    def flag_nulls(
        self, df: pd.DataFrame, cols: Optional[list[str]] = None
    ) -> tuple[pd.DataFrame, ImputationReport]:
        """
        Add ``<col>_was_null`` boolean indicator columns, then mode-impute.

        Useful when downstream models need to distinguish imputed from
        originally observed values.
        """
        df, report = self._prepare(df, cols, strategy="flag")
        target_cols = list(report.strategy_applied.keys())
        for col in target_cols:
            flag_col = f"{col}_was_null"
            df[flag_col] = df[col].isna()
            report.flag_cols_added.append(flag_col)
            # Fill the original column with mode after flagging
            mode_vals = df[col].mode()
            if not mode_vals.empty:
                df[col] = df[col].fillna(mode_vals.iloc[0])
        self._finalize_report(df, report)
        logger.info(
            f"Flag nulls: added {len(report.flag_cols_added)} indicator cols, "
            f"filled {report.total_filled} nulls."
        )
        return df, report

    def apply_strategy(
        self,
        df: pd.DataFrame,
        col: str,
        strategy: Strategy,
    ) -> tuple[pd.DataFrame, str]:
        """
        Apply a single named strategy to a single column.

        Args:
            df:       Input DataFrame.
            col:      Target column name.
            strategy: Cleaning strategy string.

        Returns:
            (updated DataFrame, log message)
        """
        if strategy == "mean":
            df, _ = self.impute_mean(df, [col])
        elif strategy == "median":
            df, _ = self.impute_median(df, [col])
        elif strategy == "mode":
            df, _ = self.impute_mode(df, [col])
        elif strategy == "drop":
            df, _ = self.drop_nulls(df, [col])
        elif strategy == "flag":
            df, _ = self.flag_nulls(df, [col])
        else:
            return df, f"No imputation applied to '{col}' (strategy='none')."
        return df, f"Applied '{strategy}' to column '{col}'."

    # ── Private helpers ───────────────────────────────────────────────────────

    def _prepare(
        self, df: pd.DataFrame, cols: Optional[list[str]], strategy: str
    ) -> tuple[pd.DataFrame, ImputationReport]:
        df = df.copy()
        target = cols if cols else [c for c in df.columns if df[c].isna().any()]
        report = ImputationReport(
            strategy_applied={c: strategy for c in target},
            nulls_before={c: int(df[c].isna().sum()) for c in target},
        )
        return df, report

    def _finalize_report(self, df: pd.DataFrame, report: ImputationReport) -> None:
        for col in report.nulls_before:
            if col in df.columns:
                report.nulls_after[col] = int(df[col].isna().sum())
