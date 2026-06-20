"""
data_loading/validators.py — File Validation
=============================================
FileValidator performs structural and content-level checks before
any data is loaded into memory, preventing downstream errors.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import pandas as pd

from src.core.logging_manager import detect_file_type, get_logger

logger = get_logger("src.ingestion.schema_validator")


# ── Result dataclass ──────────────────────────────────────────────────────────

@dataclass
class ValidationResult:
    """Structured outcome of a file validation pass."""

    is_valid: bool = True
    file_type: str = "unknown"
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    file_size_bytes: int = 0
    detected_columns: list[str] = field(default_factory=list)
    row_estimate: Optional[int] = None

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)
        self.is_valid = False
        logger.error(msg)

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)
        logger.warning(msg)

    @property
    def summary(self) -> str:
        status = "✅ VALID" if self.is_valid else "❌ INVALID"
        parts = [f"{status} | Type: {self.file_type}"]
        if self.errors:
            parts.append(f"Errors: {'; '.join(self.errors)}")
        if self.warnings:
            parts.append(f"Warnings: {'; '.join(self.warnings)}")
        return " | ".join(parts)


# ── Validator class ───────────────────────────────────────────────────────────

class FileValidator:
    """
    Validate data files before ingestion.

    Checks performed:
    - File existence and non-zero size
    - Supported extension detection
    - Parse attempt (corruption check)
    - Header presence (missing/blank column names)
    - Optional schema consistency against a reference column list

    Example::

        validator = FileValidator()
        result = validator.validate("sales_data.csv")
        if not result.is_valid:
            print(result.errors)
    """

    SUPPORTED_TYPES = {"csv", "excel"}

    def __init__(self, expected_columns: Optional[list[str]] = None) -> None:
        """
        Args:
            expected_columns: Optional reference column list for schema checks.
        """
        self._expected_columns = (
            [c.lower().strip() for c in expected_columns]
            if expected_columns
            else None
        )

    # ── Public entry point ────────────────────────────────────────────────────

    def validate(self, path: str | Path) -> ValidationResult:
        """
        Run all validation checks on *path*.

        Args:
            path: Path to the file to validate.

        Returns:
            :class:`ValidationResult` with detailed findings.
        """
        path = Path(path)
        result = ValidationResult()

        logger.info(f"Validating file: {path.name}")

        self._check_exists(path, result)
        if not result.is_valid:
            return result

        self._check_extension(path, result)
        if not result.is_valid:
            return result

        self._check_size(path, result)
        if not result.is_valid:
            return result

        df = self._try_parse(path, result)
        if df is None:
            return result

        self._check_headers(df, result)
        self._check_schema(df, result)

        logger.info(f"Validation complete: {result.summary}")
        return result

    def validate_dataframe(self, df: pd.DataFrame, name: str = "DataFrame") -> ValidationResult:
        """
        Validate an already-loaded DataFrame (useful for SQL result sets).

        Args:
            df: The DataFrame to validate.
            name: Friendly label for logging.

        Returns:
            :class:`ValidationResult`.
        """
        result = ValidationResult(file_type="dataframe")
        logger.info(f"Validating DataFrame: {name}")

        if df is None or df.empty:
            result.add_error(f"'{name}' is empty or None.")
            return result

        self._check_headers(df, result)
        self._check_schema(df, result)

        logger.info(f"DataFrame validation: {result.summary}")
        return result

    # ── Private checks ────────────────────────────────────────────────────────

    def _check_exists(self, path: Path, result: ValidationResult) -> None:
        if not path.exists():
            result.add_error(f"File not found: '{path}'")
        elif not path.is_file():
            result.add_error(f"Path is a directory, not a file: '{path}'")

    def _check_extension(self, path: Path, result: ValidationResult) -> None:
        file_type = detect_file_type(path)
        result.file_type = file_type
        if file_type not in self.SUPPORTED_TYPES:
            result.add_error(
                f"Unsupported file type '{path.suffix}'. "
                f"Supported: .csv, .xlsx, .xls"
            )

    def _check_size(self, path: Path, result: ValidationResult) -> None:
        size = os.path.getsize(path)
        result.file_size_bytes = size
        if size == 0:
            result.add_error(f"File is empty (0 bytes): '{path.name}'")
        elif size > 500 * 1024 * 1024:  # 500 MB warning
            result.add_warning(
                f"Large file ({size / 1024**2:.1f} MB). "
                "Consider chunked loading for performance."
            )

    def _try_parse(
        self, path: Path, result: ValidationResult
    ) -> Optional[pd.DataFrame]:
        """Attempt to parse the file, catching corruption / encoding errors."""
        try:
            if result.file_type == "csv":
                df = pd.read_csv(path, nrows=5)
            else:
                df = pd.read_excel(path, nrows=5)

            result.detected_columns = list(df.columns)
            return df

        except Exception as exc:
            result.add_error(
                f"File appears corrupted or unreadable: {type(exc).__name__}: {exc}"
            )
            return None

    def _check_headers(self, df: pd.DataFrame, result: ValidationResult) -> None:
        """Detect blank, null, or 'Unnamed' column headers."""
        blank_cols = [
            str(c)
            for c in df.columns
            if not str(c).strip()
            or str(c).startswith("Unnamed:")
            or str(c).lower() in ("nan", "none")
        ]
        if blank_cols:
            result.add_warning(
                f"Detected {len(blank_cols)} blank/unnamed column(s): {blank_cols}"
            )

    def _check_schema(self, df: pd.DataFrame, result: ValidationResult) -> None:
        """Compare detected columns against the expected schema, if provided."""
        if not self._expected_columns:
            return

        actual = {c.lower().strip() for c in df.columns}
        expected = set(self._expected_columns)

        missing = expected - actual
        extra = actual - expected

        if missing:
            result.add_error(f"Missing expected columns: {sorted(missing)}")
        if extra:
            result.add_warning(f"Extra columns not in schema: {sorted(extra)}")
