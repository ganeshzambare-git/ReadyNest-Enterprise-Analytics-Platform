"""
data_cleaning/outlier_detector.py — Outlier Detection
======================================================
Detects statistical anomalies using IQR fences and Z-score methods.
Returns flagged DataFrames and per-column outlier summaries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional

import numpy as np
import pandas as pd

from src.core.logging_manager import get_logger

logger = get_logger("src.preprocessing.outlier_detector")

OutlierMethod = Literal["iqr", "zscore"]


# ── Result dataclasses ────────────────────────────────────────────────────────

@dataclass
class ColumnOutlierResult:
    """Outlier statistics for a single column."""
    column:        str
    method:        str
    outlier_count: int
    outlier_pct:   float
    lower_bound:   Optional[float] = None
    upper_bound:   Optional[float] = None
    threshold:     Optional[float] = None   # Z-score threshold used

    @property
    def has_outliers(self) -> bool:
        return self.outlier_count > 0


@dataclass
class OutlierReport:
    """Combined outlier detection results across all inspected columns."""
    method:         str = "iqr"
    column_results: list[ColumnOutlierResult] = field(default_factory=list)

    @property
    def total_outliers(self) -> int:
        return sum(r.outlier_count for r in self.column_results)

    @property
    def affected_columns(self) -> list[str]:
        return [r.column for r in self.column_results if r.has_outliers]

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([
            {
                "Column":        r.column,
                "Method":        r.method,
                "Outliers":      r.outlier_count,
                "Outlier %":     f"{r.outlier_pct:.2f}%",
                "Lower Bound":   f"{r.lower_bound:.4f}" if r.lower_bound is not None else "—",
                "Upper Bound":   f"{r.upper_bound:.4f}" if r.upper_bound is not None else "—",
            }
            for r in self.column_results
        ])


# ── Detector class ────────────────────────────────────────────────────────────

class OutlierDetector:
    """
    Detect outliers using IQR fences or Z-score thresholds.

    Both methods add a boolean ``<col>_outlier`` flag column so anomalies
    can be highlighted without losing original data.

    Example::

        detector = OutlierDetector()
        df_flagged, report = detector.detect_iqr(df, ["revenue", "quantity"])
        df_flagged, report = detector.detect_zscore(df, ["revenue"], threshold=3.0)
    """

    # ── IQR Method ────────────────────────────────────────────────────────────

    def detect_iqr(
        self,
        df: pd.DataFrame,
        cols: Optional[list[str]] = None,
        factor: float = 1.5,
        add_flags: bool = True,
    ) -> tuple[pd.DataFrame, OutlierReport]:
        """
        Detect outliers using the Interquartile Range (IQR) method.

        Fences:
        - Lower = Q1 − factor × IQR
        - Upper = Q3 + factor × IQR

        Args:
            df:        Input DataFrame.
            cols:      Numeric columns to inspect (None = all numeric cols).
            factor:    IQR multiplier. Common values: 1.5 (mild), 3.0 (extreme).
            add_flags: If True, add ``<col>_outlier`` boolean columns.

        Returns:
            (DataFrame with optional flag columns, :class:`OutlierReport`)
        """
        df = df.copy()
        target = cols or self._numeric_cols(df)
        report = OutlierReport(method="iqr")

        for col in target:
            if col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
                continue

            series = df[col].dropna()
            q1, q3 = series.quantile(0.25), series.quantile(0.75)
            iqr = q3 - q1
            lower = q1 - factor * iqr
            upper = q3 + factor * iqr

            mask = (df[col] < lower) | (df[col] > upper)
            cnt = int(mask.sum())
            pct = round(cnt / len(df) * 100, 2) if len(df) > 0 else 0.0

            if add_flags:
                df[f"{col}_outlier"] = mask

            report.column_results.append(ColumnOutlierResult(
                column=col, method="iqr",
                outlier_count=cnt, outlier_pct=pct,
                lower_bound=round(lower, 4), upper_bound=round(upper, 4),
            ))
            logger.info(
                f"IQR '{col}': bounds=[{lower:.2f}, {upper:.2f}], "
                f"outliers={cnt} ({pct:.1f}%)"
            )

        return df, report

    # ── Z-score Method ────────────────────────────────────────────────────────

    def detect_zscore(
        self,
        df: pd.DataFrame,
        cols: Optional[list[str]] = None,
        threshold: float = 3.0,
        add_flags: bool = True,
    ) -> tuple[pd.DataFrame, OutlierReport]:
        """
        Detect outliers where |Z-score| > threshold.

        Z-score = (value − column mean) / column std

        Args:
            df:        Input DataFrame.
            cols:      Numeric columns to inspect (None = all numeric).
            threshold: Absolute Z-score cutoff (common: 2.5, 3.0, 3.5).
            add_flags: If True, add ``<col>_outlier`` boolean columns.

        Returns:
            (DataFrame with optional flag columns, :class:`OutlierReport`)
        """
        df = df.copy()
        target = cols or self._numeric_cols(df)
        report = OutlierReport(method="zscore")

        for col in target:
            if col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
                continue

            mean = df[col].mean()
            std  = df[col].std()

            if std == 0:
                # All values identical — no outliers possible
                report.column_results.append(ColumnOutlierResult(
                    column=col, method="zscore",
                    outlier_count=0, outlier_pct=0.0,
                    threshold=threshold,
                ))
                continue

            z = (df[col] - mean) / std
            mask = z.abs() > threshold
            cnt = int(mask.sum())
            pct = round(cnt / len(df) * 100, 2) if len(df) > 0 else 0.0

            if add_flags:
                df[f"{col}_outlier"] = mask

            report.column_results.append(ColumnOutlierResult(
                column=col, method="zscore",
                outlier_count=cnt, outlier_pct=pct,
                threshold=threshold,
            ))
            logger.info(
                f"Z-score '{col}': threshold={threshold}, "
                f"outliers={cnt} ({pct:.1f}%)"
            )

        return df, report

    # ── Highlight / cap outliers ──────────────────────────────────────────────

    def cap_outliers(
        self,
        df: pd.DataFrame,
        cols: Optional[list[str]] = None,
        method: OutlierMethod = "iqr",
        factor: float = 1.5,
        threshold: float = 3.0,
    ) -> tuple[pd.DataFrame, OutlierReport]:
        """
        Winsorise (cap) outliers to the fence values rather than removing them.

        Args:
            df:        Input DataFrame.
            cols:      Numeric columns to cap.
            method:    ``'iqr'`` or ``'zscore'``.
            factor:    IQR multiplier (used when method='iqr').
            threshold: Z-score cutoff (used when method='zscore').

        Returns:
            (capped DataFrame, :class:`OutlierReport`)
        """
        df = df.copy()
        target = cols or self._numeric_cols(df)
        report = OutlierReport(method=method)

        for col in target:
            if col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
                continue

            if method == "iqr":
                series = df[col].dropna()
                q1, q3 = series.quantile(0.25), series.quantile(0.75)
                iqr = q3 - q1
                lower = q1 - factor * iqr
                upper = q3 + factor * iqr
            else:
                mean, std = df[col].mean(), df[col].std()
                lower = mean - threshold * std
                upper = mean + threshold * std

            before_outliers = ((df[col] < lower) | (df[col] > upper)).sum()
            df[col] = df[col].clip(lower=lower, upper=upper)

            report.column_results.append(ColumnOutlierResult(
                column=col, method=method,
                outlier_count=int(before_outliers),
                outlier_pct=round(before_outliers / len(df) * 100, 2),
                lower_bound=round(lower, 4),
                upper_bound=round(upper, 4),
            ))
            logger.info(f"Capped '{col}': [{lower:.2f}, {upper:.2f}], capped={before_outliers}")

        return df, report

    # ── Private helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _numeric_cols(df: pd.DataFrame) -> list[str]:
        return [
            c for c in df.columns
            if pd.api.types.is_numeric_dtype(df[c])
            and not c.endswith("_outlier")
        ]
