"""
cleaning_config.py — Data Cleaning Configuration
=================================================
Central config-driven rules for the DataCleaner pipeline.
Override these defaults in the UI or subclass for project-specific rules.
No code changes needed to adjust cleaning behaviour — just edit this file.
"""

# ── Missing value imputation rules ────────────────────────────────────────────
# Strategy per column: "mean" | "median" | "mode" | "drop" | "flag" | "none"
# "flag" adds a <col>_was_null boolean indicator and fills with mode/mean.
IMPUTATION_RULES: dict[str, str] = {
    # numeric columns default
    "_default_numeric":     "mean",
    # categorical / object columns default
    "_default_categorical": "mode",
}

# ── Type conversion rules ─────────────────────────────────────────────────────
# Target dtype per column: "datetime" | "float" | "int" | "category" | "str"
TYPE_RULES: dict[str, str] = {
    # Example: "order_date": "datetime", "revenue": "float"
}

# ── Standardization rules ─────────────────────────────────────────────────────
STANDARDIZATION_RULES: dict = {
    "text_columns":      [],        # columns to apply text normalization
    "currency_columns":  [],        # columns containing currency strings
    "date_columns":      [],        # columns to reformat date strings
    "text_case":         "lower",   # "lower" | "upper" | "title"
    "date_input_format": None,      # None = auto-detect via pd.to_datetime
    "date_output_format": "%Y-%m-%d",
    "currency_symbol":   "$",
    "currency_decimals": 2,
    "strip_special_chars": False,   # strip non-alphanumeric from text cols
}

# ── Outlier detection ─────────────────────────────────────────────────────────
OUTLIER_CONFIG: dict = {
    "default_method":   "iqr",   # "iqr" | "zscore"
    "iqr_factor":       1.5,     # multiplier for IQR fences (common: 1.5 or 3.0)
    "zscore_threshold": 3.0,     # abs z-score above which a value is an outlier
}

# ── Quality score dimension weights ───────────────────────────────────────────
# Must sum to 1.0
QUALITY_WEIGHTS: dict[str, float] = {
    "completeness": 0.35,
    "consistency":  0.25,
    "accuracy":     0.25,
    "validity":     0.15,
}

# ── Validity rules ────────────────────────────────────────────────────────────
# Value-range expectations for numeric columns: {col: (min, max)}
# Rows outside range are flagged as invalid.
VALIDITY_RANGES: dict[str, tuple] = {
    # Example: "quantity": (0, 10000), "discount": (0.0, 1.0)
}

# ── Duplicate detection ───────────────────────────────────────────────────────
DUPLICATE_CONFIG: dict = {
    "subset":   None,   # None = use all columns; or list of column names
    "keep":     "first",  # "first" | "last" | False (remove all)
}

# ── Pipeline step order ───────────────────────────────────────────────────────
# Controls the sequence of cleaning operations in DataCleaner.run_all()
PIPELINE_ORDER: list[str] = [
    "impute",
    "deduplicate",
    "convert_types",
    "standardize",
    "detect_outliers",
]
