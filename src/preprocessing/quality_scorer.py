"""
data_cleaning/quality_scorer.py — Data Quality Scorer
======================================================
Computes a composite 0–100 quality score across four dimensions:
Completeness, Consistency, Accuracy, and Validity.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd

from src.core.logging_manager import get_logger

logger = get_logger("src.preprocessing.quality_scorer")


# ── Score dataclasses ─────────────────────────────────────────────────────────

@dataclass
class DimensionScore:
    """Score for one quality dimension."""
    name:        str
    score:       float          # 0.0 – 100.0
    weight:      float          # contribution weight (0.0 – 1.0)
    issues:      list[str] = field(default_factory=list)
    details:     dict  = field(default_factory=dict)

    @property
    def weighted_score(self) -> float:
        return self.score * self.weight

    @property
    def label(self) -> str:
        if self.score >= 90: return "Excellent"
        if self.score >= 75: return "Good"
        if self.score >= 50: return "Fair"
        return "Poor"

    @property
    def color(self) -> str:
        if self.score >= 90: return "#22c55e"
        if self.score >= 75: return "#3b82f6"
        if self.score >= 50: return "#f59e0b"
        return "#ef4444"


@dataclass
class QualityReport:
    """Full quality assessment for a DataFrame."""
    composite_score:  float = 0.0
    composite_label:  str   = "Poor"
    dimensions:       list[DimensionScore] = field(default_factory=list)
    row_count:        int   = 0
    col_count:        int   = 0
    assessed_at:      str   = ""

    @property
    def dimension_map(self) -> dict[str, DimensionScore]:
        return {d.name: d for d in self.dimensions}

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([
            {
                "Dimension": d.name,
                "Score":     round(d.score, 1),
                "Weight":    f"{d.weight * 100:.0f}%",
                "Label":     d.label,
                "Issues":    len(d.issues),
            }
            for d in self.dimensions
        ])

    def delta(self, other: "QualityReport") -> float:
        """Return composite score improvement vs another report (+ve = better)."""
        return round(self.composite_score - other.composite_score, 2)


# ── Scorer class ──────────────────────────────────────────────────────────────

class QualityScorer:
    """
    Compute data quality across four dimensions with configurable weights.

    Dimensions:
    - **Completeness** — what fraction of cells are populated (non-null)
    - **Consistency**  — dtype uniformity; mixed-type object columns penalised
    - **Accuracy**     — outlier prevalence in numeric columns
    - **Validity**     — compliance with expected value ranges / domain rules

    Example::

        scorer = QualityScorer()
        report = scorer.score(df)
        print(report.composite_score)   # e.g. 83.5
        print(report.dimension_map["Completeness"].score)
    """

    def __init__(
        self,
        weights: Optional[dict[str, float]] = None,
        validity_ranges: Optional[dict[str, tuple]] = None,
        iqr_factor: float = 1.5,
    ) -> None:
        """
        Args:
            weights:         Dict of dimension weights. Must sum to ~1.0.
                             Default: completeness=.35, consistency=.25,
                             accuracy=.25, validity=.15
            validity_ranges: ``{col: (min, max)}`` for range validation.
            iqr_factor:      IQR multiplier used to detect outliers in accuracy scoring.
        """
        from src.config.cleaning_config import QUALITY_WEIGHTS, VALIDITY_RANGES
        self._weights = weights or QUALITY_WEIGHTS
        self._validity_ranges = validity_ranges or VALIDITY_RANGES
        self._iqr_factor = iqr_factor

    # ── Public API ────────────────────────────────────────────────────────────

    def score(self, df: pd.DataFrame) -> QualityReport:
        """
        Compute a full :class:`QualityReport` for *df*.

        Args:
            df: DataFrame to assess.

        Returns:
            :class:`QualityReport` with composite + per-dimension scores.
        """
        import datetime
        logger.info(f"Scoring quality: {len(df):,} rows × {len(df.columns)} cols")

        dims = [
            self._completeness(df),
            self._consistency(df),
            self._accuracy(df),
            self._validity(df),
        ]

        composite = round(sum(d.weighted_score for d in dims), 2)
        label = self._label(composite)

        report = QualityReport(
            composite_score=composite,
            composite_label=label,
            dimensions=dims,
            row_count=len(df),
            col_count=len(df.columns),
            assessed_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        logger.info(
            f"Quality score: {composite:.1f}/100 ({label}) | "
            + " | ".join(f"{d.name}={d.score:.1f}" for d in dims)
        )
        return report

    def compare(self, before: pd.DataFrame, after: pd.DataFrame) -> dict:
        """
        Score two DataFrames and return a delta summary.

        Args:
            before: Pre-cleaning DataFrame.
            after:  Post-cleaning DataFrame.

        Returns:
            Dict with before/after scores and improvement per dimension.
        """
        r_before = self.score(before)
        r_after  = self.score(after)
        result = {
            "composite_before": r_before.composite_score,
            "composite_after":  r_after.composite_score,
            "improvement":      r_after.delta(r_before),
            "dimensions": {
                d.name: {
                    "before": r_before.dimension_map[d.name].score,
                    "after":  d.score,
                    "delta":  round(d.score - r_before.dimension_map[d.name].score, 2),
                }
                for d in r_after.dimensions
            },
        }
        return result

    # ── Dimension scorers ─────────────────────────────────────────────────────

    def _completeness(self, df: pd.DataFrame) -> DimensionScore:
        """
        Score = (non-null cells) / (total cells) × 100
        """
        total = df.size
        non_null = df.notna().sum().sum()
        score = (non_null / total * 100) if total > 0 else 100.0

        issues = []
        per_col = {}
        for col in df.columns:
            null_pct = df[col].isna().mean() * 100
            per_col[col] = round(null_pct, 2)
            if null_pct > 50:
                issues.append(f"'{col}': {null_pct:.1f}% null (critical)")
            elif null_pct > 10:
                issues.append(f"'{col}': {null_pct:.1f}% null")

        return DimensionScore(
            name="Completeness",
            score=round(score, 2),
            weight=self._weights.get("completeness", 0.35),
            issues=issues,
            details={"null_pct_per_col": per_col},
        )

    def _consistency(self, df: pd.DataFrame) -> DimensionScore:
        """
        Score based on dtype regularity and uniform formatting.
        Penalises object columns that are mixtures of numeric / date / text.
        """
        issues = []
        penalties = 0
        checked = 0

        for col in df.columns:
            if df[col].dtype != object:
                continue
            checked += 1
            sample = df[col].dropna().head(500).astype(str)

            # Check if values look mixed (some numeric, some not)
            numeric_ratio = pd.to_numeric(sample, errors="coerce").notna().mean()
            if 0.1 < numeric_ratio < 0.9:
                issues.append(f"'{col}' has mixed numeric/text values ({numeric_ratio:.0%} numeric).")
                penalties += 20

            # Blank-string check
            blank_ratio = (sample.str.strip() == "").mean()
            if blank_ratio > 0.05:
                issues.append(f"'{col}' has {blank_ratio:.0%} blank strings.")
                penalties += 10

        score = max(0.0, 100.0 - penalties)
        return DimensionScore(
            name="Consistency",
            score=round(score, 2),
            weight=self._weights.get("consistency", 0.25),
            issues=issues,
            details={"columns_checked": checked, "total_penalty": penalties},
        )

    def _accuracy(self, df: pd.DataFrame) -> DimensionScore:
        """
        Score based on absence of outliers in numeric columns (IQR method).
        """
        issues = []
        numeric_cols = [
            c for c in df.columns
            if pd.api.types.is_numeric_dtype(df[c]) and not c.endswith("_outlier")
        ]

        if not numeric_cols:
            return DimensionScore(
                name="Accuracy",
                score=100.0,
                weight=self._weights.get("accuracy", 0.25),
                details={"note": "No numeric columns found."},
            )

        total_outliers = 0
        total_values = 0

        for col in numeric_cols:
            series = df[col].dropna()
            if len(series) < 4:
                continue
            q1, q3 = series.quantile(0.25), series.quantile(0.75)
            iqr = q3 - q1
            lower = q1 - self._iqr_factor * iqr
            upper = q3 + self._iqr_factor * iqr
            outliers = ((series < lower) | (series > upper)).sum()
            total_outliers += outliers
            total_values += len(series)
            if outliers > 0:
                pct = outliers / len(series) * 100
                issues.append(f"'{col}': {outliers} outliers ({pct:.1f}%)")

        outlier_ratio = total_outliers / total_values if total_values > 0 else 0
        score = max(0.0, 100.0 - outlier_ratio * 200)  # 0.5% outliers → −1 pt

        return DimensionScore(
            name="Accuracy",
            score=round(score, 2),
            weight=self._weights.get("accuracy", 0.25),
            issues=issues,
            details={"total_outliers": int(total_outliers), "total_values": total_values},
        )

    def _validity(self, df: pd.DataFrame) -> DimensionScore:
        """
        Score based on compliance with expected value ranges (from VALIDITY_RANGES config).
        If no ranges are configured, checks for negative values in obviously non-negative cols.
        """
        issues = []
        total_violations = 0
        total_checked = 0

        if self._validity_ranges:
            for col, (lo, hi) in self._validity_ranges.items():
                if col not in df.columns:
                    continue
                series = df[col].dropna()
                violations = ((series < lo) | (series > hi)).sum()
                total_violations += violations
                total_checked += len(series)
                if violations > 0:
                    issues.append(f"'{col}': {violations} values outside [{lo}, {hi}]")
        else:
            # Fallback: check for obviously invalid negatives in named cols
            neg_suspects = [
                c for c in df.columns
                if any(k in c.lower() for k in ("qty", "quantity", "count", "price", "amount", "revenue"))
                and pd.api.types.is_numeric_dtype(df[c])
            ]
            for col in neg_suspects:
                negs = (df[col] < 0).sum()
                if negs > 0:
                    issues.append(f"'{col}': {negs} negative values (expected ≥ 0).")
                    total_violations += negs
                    total_checked += len(df[col].dropna())

        if total_checked == 0:
            score = 100.0
        else:
            violation_rate = total_violations / total_checked
            score = max(0.0, 100.0 - violation_rate * 100)

        return DimensionScore(
            name="Validity",
            score=round(score, 2),
            weight=self._weights.get("validity", 0.15),
            issues=issues,
            details={"violations": total_violations, "checked": total_checked},
        )

    # ── Label helper ──────────────────────────────────────────────────────────

    @staticmethod
    def _label(score: float) -> str:
        if score >= 90: return "Excellent"
        if score >= 75: return "Good"
        if score >= 50: return "Fair"
        return "Poor"
