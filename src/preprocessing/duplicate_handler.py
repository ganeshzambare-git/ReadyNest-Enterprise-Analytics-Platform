"""
data_cleaning/deduplicator.py — Duplicate Handler
==================================================
Detects, reports and removes duplicate rows from DataFrames.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional

import pandas as pd

from src.core.logging_manager import get_logger

logger = get_logger("src.preprocessing.duplicate_handler")

KeepStrategy = Literal["first", "last", False]


# ── Result dataclass ──────────────────────────────────────────────────────────

@dataclass
class DuplicateReport:
    """Summary of duplicate detection and removal."""
    total_rows:       int = 0
    duplicate_count:  int = 0
    duplicate_pct:    float = 0.0
    rows_removed:     int = 0
    subset_used:      Optional[list[str]] = None
    keep_strategy:    str = "first"
    sample_rows:      Optional[pd.DataFrame] = None   # up to 20 example dups

    @property
    def is_clean(self) -> bool:
        return self.duplicate_count == 0

    def summary_text(self) -> str:
        if self.is_clean:
            return "✅ No duplicates detected."
        return (
            f"⚠️ {self.duplicate_count:,} duplicate rows "
            f"({self.duplicate_pct:.2f}% of {self.total_rows:,} total rows). "
            f"{self.rows_removed:,} removed."
        )


# ── Handler class ─────────────────────────────────────────────────────────────

class DuplicateHandler:
    """
    Identify and remove duplicate rows.

    Example::

        handler = DuplicateHandler()
        report  = handler.detect(df)
        df_clean, report = handler.remove(df, keep="first")
    """

    # ── Detection ─────────────────────────────────────────────────────────────

    def detect(
        self,
        df: pd.DataFrame,
        subset: Optional[list[str]] = None,
    ) -> DuplicateReport:
        """
        Detect duplicate rows without modifying the DataFrame.

        Args:
            df:     Input DataFrame.
            subset: Columns to consider for duplicate detection.
                    ``None`` = use all columns.

        Returns:
            :class:`DuplicateReport` with count, percentage, and sample rows.
        """
        n = len(df)
        dup_mask = df.duplicated(subset=subset, keep=False)
        dup_count = int(df.duplicated(subset=subset, keep="first").sum())
        dup_pct = round(dup_count / n * 100, 2) if n > 0 else 0.0

        sample = df[dup_mask].head(20) if dup_count > 0 else None

        report = DuplicateReport(
            total_rows=n,
            duplicate_count=dup_count,
            duplicate_pct=dup_pct,
            subset_used=subset,
            sample_rows=sample,
        )
        logger.info(
            f"Duplicate detection: {dup_count:,} dups ({dup_pct:.2f}%) "
            f"in {n:,} rows. Subset: {subset or 'all columns'}"
        )
        return report

    # ── Removal ───────────────────────────────────────────────────────────────

    def remove(
        self,
        df: pd.DataFrame,
        subset: Optional[list[str]] = None,
        keep: KeepStrategy = "first",
    ) -> tuple[pd.DataFrame, DuplicateReport]:
        """
        Remove duplicate rows from *df*.

        Args:
            df:     Input DataFrame.
            subset: Columns to consider for deduplication.
            keep:   ``'first'`` keep first occurrence, ``'last'`` keep last,
                    ``False`` drop all duplicates (even originals).

        Returns:
            Tuple of (cleaned DataFrame, :class:`DuplicateReport`).
        """
        report = self.detect(df, subset=subset)
        report.keep_strategy = str(keep)

        before = len(df)
        df = df.drop_duplicates(subset=subset, keep=keep).reset_index(drop=True)
        report.rows_removed = before - len(df)

        logger.info(
            f"Duplicate removal: removed {report.rows_removed:,} rows "
            f"(keep='{keep}'). Remaining: {len(df):,}."
        )
        return df, report

    # ── Detailed report ───────────────────────────────────────────────────────

    def generate_report(
        self,
        df: pd.DataFrame,
        subset: Optional[list[str]] = None,
    ) -> pd.DataFrame:
        """
        Return a DataFrame showing each duplicate group with occurrence count.

        Args:
            df:     Input DataFrame.
            subset: Columns to group by for duplicate detection.

        Returns:
            DataFrame sorted by occurrence count (descending).
        """
        cols = subset if subset else list(df.columns)
        # Keep only columns that exist
        cols = [c for c in cols if c in df.columns]

        try:
            report_df = (
                df[cols]
                .groupby(cols, dropna=False)
                .size()
                .reset_index(name="occurrences")
                .query("occurrences > 1")
                .sort_values("occurrences", ascending=False)
                .reset_index(drop=True)
            )
        except Exception:
            # Fallback for unhashable dtypes
            report_df = pd.DataFrame({"info": ["Unable to group — contains unhashable column types."]})

        logger.info(f"Duplicate report: {len(report_df)} duplicate groups identified.")
        return report_df
