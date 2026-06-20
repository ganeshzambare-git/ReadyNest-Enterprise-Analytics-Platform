"""
data_loading/metadata.py — Metadata & Quality Reporting
========================================================
MetadataGenerator produces rich statistics and a 0–100 quality
score for any DataFrame, suitable for Streamlit dashboard cards
and standalone CLI reporting.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd

from src.core.logging_manager import df_memory_mb, get_logger

logger = get_logger("src.ingestion.metadata_extractor")


# ── Dataclasses ───────────────────────────────────────────────────────────────

@dataclass
class ColumnStats:
    """Per-column statistics."""
    name: str
    dtype: str
    null_count: int
    null_pct: float          # 0.0 – 100.0
    unique_count: int
    unique_pct: float
    sample_values: list      # up to 5 representative values


@dataclass
class MetadataReport:
    """
    Full metadata snapshot for a loaded DataFrame.

    All attributes are JSON-serialisable so the report can be
    cached, logged, or sent to a REST endpoint.
    """
    # Shape
    row_count: int
    col_count: int

    # Memory
    memory_mb: float
    memory_human: str

    # File info (optional — populated when loading from disk)
    file_name: Optional[str] = None
    file_size_bytes: Optional[int] = None

    # Duplicate analysis
    duplicate_rows: int = 0
    duplicate_pct: float = 0.0

    # Column-level stats
    columns: list[ColumnStats] = field(default_factory=list)

    # Quality
    quality_score: int = 100          # 0 – 100
    quality_label: str = "Excellent"  # Excellent / Good / Fair / Poor
    quality_issues: list[str] = field(default_factory=list)

    # ── Convenience properties ────────────────────────────────────────────────

    @property
    def total_nulls(self) -> int:
        return sum(c.null_count for c in self.columns)

    @property
    def null_summary(self) -> dict[str, int]:
        return {c.name: c.null_count for c in self.columns if c.null_count > 0}

    def to_dict(self) -> dict:
        return {
            "rows": self.row_count,
            "columns": self.col_count,
            "memory_mb": round(self.memory_mb, 4),
            "duplicate_rows": self.duplicate_rows,
            "duplicate_pct": round(self.duplicate_pct, 2),
            "total_nulls": self.total_nulls,
            "quality_score": self.quality_score,
            "quality_label": self.quality_label,
            "file_name": self.file_name,
        }


# ── Quality scoring ───────────────────────────────────────────────────────────

_QUALITY_LABELS = [
    (90, "Excellent"),
    (75, "Good"),
    (50, "Fair"),
    (0,  "Poor"),
]


def _score_to_label(score: int) -> str:
    for threshold, label in _QUALITY_LABELS:
        if score >= threshold:
            return label
    return "Poor"


# ── Generator class ───────────────────────────────────────────────────────────

class MetadataGenerator:
    """
    Compute metadata and data-quality metrics for a pandas DataFrame.

    Example::

        gen = MetadataGenerator()
        report = gen.generate(df, file_name="sales_q3.csv")
        print(report.quality_score)       # e.g. 87
        print(report.null_summary)        # {'revenue': 12, 'region': 0}
    """

    def __init__(
        self,
        null_warn_threshold: float = 0.10,
        null_error_threshold: float = 0.50,
        dup_warn_threshold: float = 0.05,
    ) -> None:
        """
        Args:
            null_warn_threshold:  Fraction of nulls that triggers a warning penalty.
            null_error_threshold: Fraction of nulls that triggers an error penalty.
            dup_warn_threshold:   Fraction of duplicates that triggers a penalty.
        """
        self._null_warn = null_warn_threshold
        self._null_error = null_error_threshold
        self._dup_warn = dup_warn_threshold

    # ── Public API ────────────────────────────────────────────────────────────

    def generate(
        self,
        df: pd.DataFrame,
        file_name: Optional[str] = None,
        file_size_bytes: Optional[int] = None,
    ) -> MetadataReport:
        """
        Generate a full :class:`MetadataReport` for *df*.

        Args:
            df:               Source DataFrame.
            file_name:        Optional original filename.
            file_size_bytes:  Optional on-disk size.

        Returns:
            :class:`MetadataReport` instance.
        """
        if df is None:
            raise ValueError("Cannot generate metadata for None.")

        logger.info(
            f"Generating metadata for "
            f"{'`' + file_name + '`' if file_name else 'DataFrame'} "
            f"({len(df):,} rows × {len(df.columns)} cols)"
        )

        mem_mb = df_memory_mb(df)
        dup_count = int(df.duplicated().sum())
        dup_pct = (dup_count / len(df) * 100) if len(df) > 0 else 0.0

        col_stats = [self._column_stats(df, col) for col in df.columns]

        report = MetadataReport(
            row_count=len(df),
            col_count=len(df.columns),
            memory_mb=mem_mb,
            memory_human=f"{mem_mb:.3f} MB",
            file_name=file_name,
            file_size_bytes=file_size_bytes,
            duplicate_rows=dup_count,
            duplicate_pct=round(dup_pct, 2),
            columns=col_stats,
        )

        self._compute_quality(report)
        logger.info(
            f"Metadata done | Quality: {report.quality_score}/100 "
            f"({report.quality_label}) | Issues: {len(report.quality_issues)}"
        )
        return report

    def column_summary_df(self, report: MetadataReport) -> pd.DataFrame:
        """
        Convert column-level stats into a tidy DataFrame for display.

        Args:
            report: Previously generated :class:`MetadataReport`.

        Returns:
            DataFrame with one row per column.
        """
        rows = []
        for c in report.columns:
            rows.append(
                {
                    "Column":       c.name,
                    "Data Type":    c.dtype,
                    "Null Count":   c.null_count,
                    "Null %":       f"{c.null_pct:.1f}%",
                    "Unique Count": c.unique_count,
                    "Unique %":     f"{c.unique_pct:.1f}%",
                    "Sample Values": ", ".join(str(v) for v in c.sample_values),
                }
            )
        return pd.DataFrame(rows)

    # ── Private helpers ───────────────────────────────────────────────────────

    def _column_stats(self, df: pd.DataFrame, col: str) -> ColumnStats:
        series = df[col]
        n = len(series)
        null_count = int(series.isna().sum())
        null_pct = (null_count / n * 100) if n > 0 else 0.0
        unique_count = int(series.nunique(dropna=True))
        unique_pct = (unique_count / n * 100) if n > 0 else 0.0

        # Sample up to 5 non-null distinct values
        sample = (
            series.dropna()
            .unique()[:5]
            .tolist()
        )

        return ColumnStats(
            name=col,
            dtype=str(series.dtype),
            null_count=null_count,
            null_pct=round(null_pct, 2),
            unique_count=unique_count,
            unique_pct=round(unique_pct, 2),
            sample_values=sample,
        )

    def _compute_quality(self, report: MetadataReport) -> None:
        """
        Assign a 0–100 quality score based on null and duplicate prevalence.

        Scoring model:
        - Start at 100
        - Each column with null % > warn threshold → −5 points
        - Each column with null % > error threshold → −15 points
        - Duplicate % > warn threshold → −10 points
        - Empty DataFrame → score = 0
        """
        if report.row_count == 0:
            report.quality_score = 0
            report.quality_label = "Poor"
            report.quality_issues.append("Dataset is empty.")
            return

        score = 100
        issues = []

        for cs in report.columns:
            frac = cs.null_pct / 100.0
            if frac >= self._null_error:
                score -= 15
                issues.append(
                    f"Column '{cs.name}' has {cs.null_pct:.1f}% nulls (critical)."
                )
            elif frac >= self._null_warn:
                score -= 5
                issues.append(
                    f"Column '{cs.name}' has {cs.null_pct:.1f}% nulls."
                )

        dup_frac = report.duplicate_pct / 100.0
        if dup_frac >= self._dup_warn:
            score -= 10
            issues.append(
                f"{report.duplicate_rows:,} duplicate rows "
                f"({report.duplicate_pct:.1f}%)."
            )

        report.quality_score = max(0, score)
        report.quality_label = _score_to_label(report.quality_score)
        report.quality_issues = issues
