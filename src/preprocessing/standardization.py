"""
data_cleaning/standardizer.py — Data Standardizer
==================================================
Normalises text case, formats currency strings, standardises
date representations, and strips unwanted special characters.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Literal, Optional

import pandas as pd

from src.core.logging_manager import get_logger

logger = get_logger("src.preprocessing.standardization")

CaseOption = Literal["lower", "upper", "title", "strip"]


# ── Result dataclass ──────────────────────────────────────────────────────────

@dataclass
class StandardizationReport:
    """Summary of all standardization operations applied."""
    operations: list[dict] = field(default_factory=list)

    def add(self, col: str, operation: str, detail: str = "") -> None:
        self.operations.append({"column": col, "operation": operation, "detail": detail})
        logger.info(f"Standardize '{col}' | {operation} | {detail}")

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.operations) if self.operations else pd.DataFrame(
            columns=["column", "operation", "detail"]
        )


# ── Standardizer class ────────────────────────────────────────────────────────

class DataStandardizer:
    """
    Standardise text, currency, and date columns.

    Example::

        std = DataStandardizer()
        df, report = std.normalize_text(df, ["region", "channel"], case="title")
        df, report = std.format_currency(df, ["revenue"], symbol="$", decimals=2)
        df, report = std.format_dates(df, ["order_date"], output_fmt="%Y-%m-%d")
    """

    # ── Text normalization ────────────────────────────────────────────────────

    def normalize_text(
        self,
        df: pd.DataFrame,
        cols: list[str],
        case: CaseOption = "lower",
        strip_whitespace: bool = True,
        strip_special: bool = False,
        special_pattern: str = r"[^\w\s]",
    ) -> tuple[pd.DataFrame, StandardizationReport]:
        """
        Normalise text columns: strip whitespace, change case, remove special chars.

        Args:
            df:              Input DataFrame.
            cols:            Text columns to normalise.
            case:            ``'lower'``, ``'upper'``, ``'title'``, or ``'strip'``.
            strip_whitespace: Strip leading/trailing whitespace.
            strip_special:   Remove non-word characters (punctuation, symbols).
            special_pattern: Regex pattern for special-char removal.

        Returns:
            (updated DataFrame, :class:`StandardizationReport`)
        """
        df = df.copy()
        report = StandardizationReport()

        for col in cols:
            if col not in df.columns:
                report.add(col, "SKIP", f"Column '{col}' not found.")
                continue

            try:
                series = df[col].astype(str)

                if strip_whitespace:
                    series = series.str.strip()

                case_map = {
                    "lower": series.str.lower,
                    "upper": series.str.upper,
                    "title": series.str.title,
                    "strip": lambda: series,  # already stripped
                }
                series = case_map.get(case, lambda: series)()

                if strip_special:
                    series = series.str.replace(special_pattern, " ", regex=True)
                    series = series.str.replace(r"\s+", " ", regex=True).str.strip()

                # Restore original NaN positions
                series = series.where(df[col].notna(), other=pd.NA)
                df[col] = series

                detail = f"case={case}, strip_special={strip_special}"
                report.add(col, "text_normalize", detail)

            except Exception as exc:
                report.add(col, "ERROR", str(exc))
                logger.error(f"Text normalize failed for '{col}': {exc}")

        return df, report

    # ── Currency formatting ───────────────────────────────────────────────────

    def format_currency(
        self,
        df: pd.DataFrame,
        cols: list[str],
        symbol: str = "$",
        decimals: int = 2,
        thousands_sep: str = ",",
    ) -> tuple[pd.DataFrame, StandardizationReport]:
        """
        Clean and reformat currency columns.

        Steps:
        1. Strip existing currency symbols, commas, spaces.
        2. Convert to float.
        3. Re-format as ``{symbol}{value:,.{decimals}f}``.

        Args:
            df:            Input DataFrame.
            cols:          Currency columns to reformat.
            symbol:        Currency prefix (e.g. ``'$'``, ``'€'``, ``'₹'``).
            decimals:      Decimal places.
            thousands_sep: Thousands separator character.

        Returns:
            (updated DataFrame, :class:`StandardizationReport`)
        """
        df = df.copy()
        report = StandardizationReport()

        for col in cols:
            if col not in df.columns:
                report.add(col, "SKIP", f"Column '{col}' not found.")
                continue

            try:
                # Strip non-numeric chars (keep decimal point and minus)
                cleaned = (
                    df[col]
                    .astype(str)
                    .str.replace(r"[^\d.\-]", "", regex=True)
                    .replace("", float("nan"))
                )
                numeric = pd.to_numeric(cleaned, errors="coerce")

                # Format as currency string
                fmt = f"{{:,.{decimals}f}}"
                df[col] = numeric.apply(
                    lambda v: f"{symbol}{fmt.format(v)}" if pd.notna(v) else pd.NA
                )
                report.add(col, "currency_format", f"symbol={symbol}, decimals={decimals}")

            except Exception as exc:
                report.add(col, "ERROR", str(exc))
                logger.error(f"Currency format failed for '{col}': {exc}")

        return df, report

    # ── Date formatting ───────────────────────────────────────────────────────

    def format_dates(
        self,
        df: pd.DataFrame,
        cols: list[str],
        output_fmt: str = "%Y-%m-%d",
        input_fmt: Optional[str] = None,
    ) -> tuple[pd.DataFrame, StandardizationReport]:
        """
        Standardise date columns to a consistent string format.

        Args:
            df:         Input DataFrame.
            cols:       Date columns to reformat.
            output_fmt: Target strftime format (default ``'%Y-%m-%d'``).
            input_fmt:  Optional input format string (None = auto-detect).

        Returns:
            (updated DataFrame, :class:`StandardizationReport`)
        """
        df = df.copy()
        report = StandardizationReport()

        for col in cols:
            if col not in df.columns:
                report.add(col, "SKIP", f"Column '{col}' not found.")
                continue

            try:
                parsed = pd.to_datetime(df[col], format=input_fmt, errors="coerce")
                df[col] = parsed.dt.strftime(output_fmt)
                report.add(col, "date_format", f"output_fmt={output_fmt}")
            except Exception as exc:
                report.add(col, "ERROR", str(exc))
                logger.error(f"Date format failed for '{col}': {exc}")

        return df, report

    # ── Special character removal ─────────────────────────────────────────────

    def remove_special_chars(
        self,
        df: pd.DataFrame,
        cols: list[str],
        pattern: str = r"[^\w\s]",
        replacement: str = "",
    ) -> tuple[pd.DataFrame, StandardizationReport]:
        """
        Remove characters matching *pattern* from text columns.

        Args:
            df:          Input DataFrame.
            cols:        Columns to clean.
            pattern:     Regex pattern for unwanted characters.
            replacement: String to replace matches with (default ``''``).

        Returns:
            (updated DataFrame, :class:`StandardizationReport`)
        """
        df = df.copy()
        report = StandardizationReport()

        for col in cols:
            if col not in df.columns:
                report.add(col, "SKIP", f"Column '{col}' not found.")
                continue

            try:
                original_na = df[col].isna()
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace(pattern, replacement, regex=True)
                    .str.strip()
                )
                df.loc[original_na, col] = pd.NA
                report.add(col, "remove_special_chars", f"pattern={pattern!r}")
            except Exception as exc:
                report.add(col, "ERROR", str(exc))
                logger.error(f"Special char removal failed for '{col}': {exc}")

        return df, report
