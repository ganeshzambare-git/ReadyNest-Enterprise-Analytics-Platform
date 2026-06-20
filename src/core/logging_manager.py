"""
data_loading/utils.py — Shared Utilities
=========================================
Logger factory, file-type detection, size formatting, and
column-name sanitisation helpers used across the package.
"""

from __future__ import annotations

import logging
import re
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pandas as pd

# ── Logger factory ────────────────────────────────────────────────────────────

_loggers: dict[str, logging.Logger] = {}


def get_logger(name: str = "data_loading") -> logging.Logger:
    """
    Return a module-level logger with both console and rotating-file handlers.
    Subsequent calls with the same *name* return the cached instance.
    """
    if name in _loggers:
        return _loggers[name]

    # Lazy import to avoid circular dependency with config
    from src.config.config import LOG_FILE, LOG_LEVEL, LOG_MAX_BYTES, LOG_BACKUP_COUNT

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    ch.setLevel(logging.DEBUG)

    # Rotating file handler
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    fh = RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    fh.setFormatter(fmt)

    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.propagate = False

    _loggers[name] = logger
    return logger


# ── File-type detection ───────────────────────────────────────────────────────

EXTENSION_MAP: dict[str, str] = {
    ".csv":  "csv",
    ".xlsx": "excel",
    ".xls":  "excel",
}


def detect_file_type(path: str | Path) -> str:
    """
    Return ``'csv'``, ``'excel'``, or ``'unknown'`` based on file extension.

    Args:
        path: Filesystem path to the file.

    Returns:
        Lowercase string identifying the file type.
    """
    ext = Path(path).suffix.lower()
    return EXTENSION_MAP.get(ext, "unknown")


# ── Human-readable sizes ──────────────────────────────────────────────────────

def human_readable_size(num_bytes: int) -> str:
    """
    Convert *num_bytes* to a human-readable string (KB / MB / GB).

    Args:
        num_bytes: Size in bytes.

    Returns:
        Formatted string, e.g. ``'3.14 MB'``.
    """
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:,.2f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:,.2f} PB"


# ── Column name sanitisation ──────────────────────────────────────────────────

def sanitize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalise DataFrame column names:
    - Strip leading/trailing whitespace
    - Replace spaces and special characters with underscores
    - Convert to lowercase

    Args:
        df: Input DataFrame (mutated in-place copy).

    Returns:
        DataFrame with sanitised column names.
    """
    df = df.copy()
    df.columns = [
        re.sub(r"[^\w]+", "_", str(col).strip()).lower().strip("_")
        for col in df.columns
    ]
    return df


# ── DataFrame memory usage ────────────────────────────────────────────────────

def df_memory_mb(df: pd.DataFrame) -> float:
    """Return memory usage of *df* in megabytes (deep inspection)."""
    return df.memory_usage(deep=True).sum() / (1024 ** 2)
