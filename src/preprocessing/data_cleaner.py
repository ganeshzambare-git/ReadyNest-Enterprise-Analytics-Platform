"""
data_cleaning/cleaner.py — DataCleaner Pipeline Orchestrator
=============================================================
DataCleaner chains all cleaning steps into a single configurable
pipeline and produces a timestamped CleaningLog of every operation.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any, Optional

import pandas as pd

from src.preprocessing.duplicate_handler import DuplicateHandler
from src.preprocessing.missing_value_handler import MissingValueHandler
from src.preprocessing.outlier_detector import OutlierDetector
from src.preprocessing.quality_scorer import QualityReport, QualityScorer
from src.preprocessing.standardization import DataStandardizer
from src.preprocessing.datatype_converter import DataTypeConverter
from src.core.logging_manager import get_logger

logger = get_logger("src.preprocessing.data_cleaner")


# ── Log entry ─────────────────────────────────────────────────────────────────

@dataclass
class LogEntry:
    timestamp:   str
    step:        str
    description: str
    rows_before: int
    rows_after:  int
    cols_before: int
    cols_after:  int
    details:     dict = field(default_factory=dict)

    @property
    def rows_changed(self) -> int:
        return self.rows_before - self.rows_after

    @property
    def cols_changed(self) -> int:
        return self.cols_after - self.cols_before


# ── Cleaning log ──────────────────────────────────────────────────────────────

class CleaningLog:
    """
    Chronological record of all cleaning operations applied to a DataFrame.
    Exportable as CSV for audit trails.
    """

    def __init__(self) -> None:
        self._entries: list[LogEntry] = []

    def record(
        self,
        step: str,
        description: str,
        df_before: pd.DataFrame,
        df_after: pd.DataFrame,
        details: Optional[dict] = None,
    ) -> None:
        entry = LogEntry(
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            step=step,
            description=description,
            rows_before=len(df_before),
            rows_after=len(df_after),
            cols_before=len(df_before.columns),
            cols_after=len(df_after.columns),
            details=details or {},
        )
        self._entries.append(entry)
        logger.info(
            f"[{step}] {description} | "
            f"rows: {entry.rows_before}→{entry.rows_after} "
            f"cols: {entry.cols_before}→{entry.cols_after}"
        )

    def to_dataframe(self) -> pd.DataFrame:
        if not self._entries:
            return pd.DataFrame(columns=[
                "Timestamp", "Step", "Description",
                "Rows Before", "Rows After", "Rows Changed",
                "Cols Before", "Cols After",
            ])
        return pd.DataFrame([
            {
                "Timestamp":    e.timestamp,
                "Step":         e.step,
                "Description":  e.description,
                "Rows Before":  e.rows_before,
                "Rows After":   e.rows_after,
                "Rows Changed": e.rows_changed,
                "Cols Before":  e.cols_before,
                "Cols After":   e.cols_after,
            }
            for e in self._entries
        ])

    def __len__(self) -> int:
        return len(self._entries)

    @property
    def entries(self) -> list[LogEntry]:
        return list(self._entries)


# ── Pipeline result ───────────────────────────────────────────────────────────

@dataclass
class CleaningResult:
    """Return value from DataCleaner.run_all()."""
    original_df:   pd.DataFrame
    cleaned_df:    pd.DataFrame
    log:           CleaningLog
    quality_before: QualityReport
    quality_after:  QualityReport

    @property
    def score_improvement(self) -> float:
        return round(
            self.quality_after.composite_score - self.quality_before.composite_score, 2
        )

    @property
    def rows_removed(self) -> int:
        return len(self.original_df) - len(self.cleaned_df)

    @property
    def summary(self) -> str:
        return (
            f"Rows: {len(self.original_df):,} → {len(self.cleaned_df):,} "
            f"(−{self.rows_removed:,}) | "
            f"Quality: {self.quality_before.composite_score:.1f} → "
            f"{self.quality_after.composite_score:.1f} "
            f"(+{self.score_improvement:.1f} pts)"
        )


# ── Orchestrator ──────────────────────────────────────────────────────────────

class DataCleaner:
    """
    Pipeline orchestrator that chains all cleaning steps in configurable order.

    Quick start::

        cleaner = DataCleaner()
        result = cleaner.run_all(df)
        cleaned_df = result.cleaned_df
        print(result.log.to_dataframe())

    Step-by-step::

        df, log = cleaner.run_step("impute", df, strategy="mean")
        df, log = cleaner.run_step("deduplicate", df)
    """

    def __init__(
        self,
        imputation_strategy: str = "mean",
        outlier_method: str = "iqr",
        iqr_factor: float = 1.5,
        zscore_threshold: float = 3.0,
        text_case: str = "lower",
        auto_convert_types: bool = True,
    ) -> None:
        self._imputer   = MissingValueHandler()
        self._dedup     = DuplicateHandler()
        self._converter = DataTypeConverter()
        self._std       = DataStandardizer()
        self._outlier   = OutlierDetector()
        self._scorer    = QualityScorer()

        self.imputation_strategy = imputation_strategy
        self.outlier_method      = outlier_method
        self.iqr_factor          = iqr_factor
        self.zscore_threshold    = zscore_threshold
        self.text_case           = text_case
        self.auto_convert_types  = auto_convert_types

    # ── Full pipeline ─────────────────────────────────────────────────────────

    def run_all(
        self,
        df: pd.DataFrame,
        steps: Optional[list[str]] = None,
    ) -> CleaningResult:
        """
        Execute the complete cleaning pipeline.

        Args:
            df:    Raw input DataFrame.
            steps: Optional list of step names to run. If None, runs all steps
                   in the order defined by ``cleaning_config.PIPELINE_ORDER``.

        Returns:
            :class:`CleaningResult` with cleaned df, log, and quality reports.
        """
        from src.config.cleaning_config import PIPELINE_ORDER
        step_order = steps or PIPELINE_ORDER

        log = CleaningLog()
        quality_before = self._scorer.score(df)
        current = df.copy()

        step_dispatch = {
            "impute":          self._step_impute,
            "deduplicate":     self._step_deduplicate,
            "convert_types":   self._step_convert_types,
            "standardize":     self._step_standardize,
            "detect_outliers": self._step_detect_outliers,
        }

        for step in step_order:
            if step not in step_dispatch:
                logger.warning(f"Unknown pipeline step: '{step}' — skipped.")
                continue
            prev = current.copy()
            current = step_dispatch[step](current, log)
            logger.info(f"Step '{step}' complete. Rows: {len(prev)} → {len(current)}")

        quality_after = self._scorer.score(current)

        return CleaningResult(
            original_df=df,
            cleaned_df=current,
            log=log,
            quality_before=quality_before,
            quality_after=quality_after,
        )

    def run_step(
        self,
        step: str,
        df: pd.DataFrame,
        **kwargs: Any,
    ) -> tuple[pd.DataFrame, CleaningLog]:
        """
        Execute a single named cleaning step.

        Args:
            step: One of ``'impute'``, ``'deduplicate'``, ``'convert_types'``,
                  ``'standardize'``, ``'detect_outliers'``.
            df:   Input DataFrame.
            **kwargs: Step-specific overrides (e.g. ``strategy='median'``).

        Returns:
            Tuple of (processed DataFrame, single-entry CleaningLog).
        """
        log = CleaningLog()
        prev = df.copy()
        step_dispatch = {
            "impute":          self._step_impute,
            "deduplicate":     self._step_deduplicate,
            "convert_types":   self._step_convert_types,
            "standardize":     self._step_standardize,
            "detect_outliers": self._step_detect_outliers,
        }
        if step not in step_dispatch:
            raise ValueError(f"Unknown step '{step}'. Valid: {list(step_dispatch)}")

        df = step_dispatch[step](df, log)
        return df, log

    # ── Private step implementations ──────────────────────────────────────────

    def _step_impute(self, df: pd.DataFrame, log: CleaningLog) -> pd.DataFrame:
        strategy = self.imputation_strategy
        prev = df.copy()
        if strategy == "mean":
            df, report = self._imputer.impute_mean(df)
        elif strategy == "median":
            df, report = self._imputer.impute_median(df)
        elif strategy == "mode":
            df, report = self._imputer.impute_mode(df)
        elif strategy == "drop":
            df, report = self._imputer.drop_nulls(df)
        elif strategy == "flag":
            df, report = self._imputer.flag_nulls(df)
        else:
            return df

        log.record(
            "impute", f"Strategy: {strategy}. Filled {report.total_filled} nulls.",
            prev, df, {"total_filled": report.total_filled}
        )
        return df

    def _step_deduplicate(self, df: pd.DataFrame, log: CleaningLog) -> pd.DataFrame:
        prev = df.copy()
        df, report = self._dedup.remove(df)
        log.record(
            "deduplicate", f"Removed {report.rows_removed:,} duplicate rows.",
            prev, df, {"rows_removed": report.rows_removed}
        )
        return df

    def _step_convert_types(self, df: pd.DataFrame, log: CleaningLog) -> pd.DataFrame:
        if not self.auto_convert_types:
            return df
        prev = df.copy()
        df, report = self._converter.infer_and_convert(df)
        log.record(
            "convert_types",
            f"Auto-converted {report.success_count} columns.",
            prev, df,
            {"converted": report.success_count, "failed": report.failure_count}
        )
        return df

    def _step_standardize(self, df: pd.DataFrame, log: CleaningLog) -> pd.DataFrame:
        from src.config.cleaning_config import STANDARDIZATION_RULES
        prev = df.copy()
        text_cols = STANDARDIZATION_RULES.get("text_columns", [])
        text_cols = [c for c in text_cols if c in df.columns]
        if text_cols:
            df, report = self._std.normalize_text(
                df, text_cols, case=STANDARDIZATION_RULES.get("text_case", "lower")
            )
            log.record(
                "standardize",
                f"Normalized text in {len(text_cols)} columns.",
                prev, df, {"columns": text_cols}
            )
        return df

    def _step_detect_outliers(self, df: pd.DataFrame, log: CleaningLog) -> pd.DataFrame:
        prev = df.copy()
        if self.outlier_method == "iqr":
            df, report = self._outlier.detect_iqr(df, factor=self.iqr_factor)
        else:
            df, report = self._outlier.detect_zscore(df, threshold=self.zscore_threshold)

        log.record(
            "detect_outliers",
            f"Method: {self.outlier_method}. "
            f"Flagged {report.total_outliers} outliers in "
            f"{len(report.affected_columns)} columns.",
            prev, df,
            {"total_outliers": report.total_outliers, "method": self.outlier_method}
        )
        return df
