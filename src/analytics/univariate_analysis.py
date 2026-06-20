"""
data_analysis/univariate.py — Univariate Analysis Engine
=========================================================
Generates descriptive metrics, business insights, and Seaborn/Matplotlib
visualizations for individual numerical and categorical columns.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.core.logging_manager import get_logger

logger = get_logger("src.analytics.univariate_analysis")


@dataclass
class NumericalAnalysis:
    column: str
    count: int
    missing: int
    mean: float
    median: float
    std_dev: float
    skewness: float
    kurtosis: float
    min_val: float
    max_val: float
    outlier_count: int
    insights: list[str]
    fig_dist: plt.Figure
    fig_box: plt.Figure


@dataclass
class CategoricalAnalysis:
    column: str
    count: int
    missing: int
    unique_categories: int
    mode: str
    frequency_df: pd.DataFrame
    insights: list[str]
    fig_count: plt.Figure


class UnivariateEngine:
    """Engine for performing Univariate EDA."""

    def __init__(self) -> None:
        # Set clean aesthetic for seaborn
        sns.set_theme(style="whitegrid", palette="muted")

    def analyze_numerical(self, df: pd.DataFrame, column: str) -> Optional[NumericalAnalysis]:
        """Performs EDA on a single numerical column."""
        if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
            logger.error(f"Cannot analyze '{column}' as numerical.")
            return None

        series = df[column]
        clean_series = series.dropna()
        if clean_series.empty:
            return None

        # Base Stats
        q1 = clean_series.quantile(0.25)
        q3 = clean_series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = clean_series[(clean_series < lower_bound) | (clean_series > upper_bound)]

        skew = clean_series.skew()
        kurt = clean_series.kurtosis()

        # Generate Insights
        insights = []
        if abs(skew) > 1:
            direction = "Right (Positive)" if skew > 0 else "Left (Negative)"
            insights.append(f"Highly Skewed: {direction} skew. The distribution has a long tail.")
        elif abs(skew) > 0.5:
            insights.append("Moderately Skewed.")
        else:
            insights.append("Symmetrical Distribution (Normal-like bell curve).")

        if kurt > 3:
            insights.append("Leptokurtic (Heavy Tails): Prone to extreme outliers.")
        elif kurt < -1:
            insights.append("Platykurtic (Light Tails): Very flat distribution.")

        if len(outliers) > 0:
            pct = (len(outliers) / len(clean_series)) * 100
            insights.append(f"Outliers Detected: {len(outliers):,} records ({pct:.1f}%) fall outside standard IQR bounds.")

        # Plot 1: Histogram + KDE
        fig_dist, ax_dist = plt.subplots(figsize=(8, 4))
        sns.histplot(clean_series, kde=True, ax=ax_dist, color="#3b82f6", bins=30)
        ax_dist.set_title(f"Distribution of {column}", fontweight="bold")
        ax_dist.set_xlabel(column)
        ax_dist.set_ylabel("Frequency")
        sns.despine(fig_dist)
        fig_dist.tight_layout()

        # Plot 2: Box Plot
        fig_box, ax_box = plt.subplots(figsize=(8, 2))
        sns.boxplot(x=clean_series, ax=ax_box, color="#10b981", fliersize=3)
        ax_box.set_title(f"Box Plot of {column} (Outlier Detection)", fontweight="bold")
        ax_box.set_xlabel(column)
        sns.despine(fig_box)
        fig_box.tight_layout()

        return NumericalAnalysis(
            column=column,
            count=len(series),
            missing=series.isna().sum(),
            mean=clean_series.mean(),
            median=clean_series.median(),
            std_dev=clean_series.std() if len(clean_series) > 1 else 0.0,
            skewness=skew,
            kurtosis=kurt,
            min_val=clean_series.min(),
            max_val=clean_series.max(),
            outlier_count=len(outliers),
            insights=insights,
            fig_dist=fig_dist,
            fig_box=fig_box,
        )

    def analyze_categorical(self, df: pd.DataFrame, column: str, max_categories: int = 15) -> Optional[CategoricalAnalysis]:
        """Performs EDA on a single categorical column."""
        if column not in df.columns:
            return None

        series = df[column].astype(str).replace("nan", np.nan)
        clean_series = series.dropna()
        if clean_series.empty:
            return None

        val_counts = clean_series.value_counts()
        freq_df = val_counts.reset_index()
        freq_df.columns = ["Category", "Count"]
        freq_df["Percentage"] = (freq_df["Count"] / len(clean_series)) * 100

        unique_count = len(val_counts)
        mode_val = val_counts.index[0]

        # Generate Insights
        insights = []
        insights.append(f"Dominant Category: '{mode_val}' makes up {freq_df['Percentage'].iloc[0]:.1f}% of the data.")
        
        if unique_count > max_categories:
            insights.append(f"High Cardinality: {unique_count} distinct categories found. Displaying top {max_categories} in chart.")
        elif unique_count == 1:
            insights.append("Zero Variance: Every row has the exact same value for this column.")
            
        if unique_count == len(clean_series):
            insights.append("Unique Identifier: Every row has a distinct value (like an ID column).")

        # Plot: Count Plot
        plot_data = freq_df.head(max_categories)
        fig_count, ax_count = plt.subplots(figsize=(8, max_categories * 0.4 + 2))
        
        sns.barplot(
            data=plot_data, 
            y="Category", 
            x="Count", 
            ax=ax_count, 
            palette="viridis",
            hue="Category",
            legend=False
        )
        
        ax_count.set_title(f"Frequency Count of {column}", fontweight="bold")
        ax_count.set_xlabel("Count")
        ax_count.set_ylabel("")
        sns.despine(fig_count)
        fig_count.tight_layout()

        return CategoricalAnalysis(
            column=column,
            count=len(series),
            missing=series.isna().sum(),
            unique_categories=unique_count,
            mode=mode_val,
            frequency_df=freq_df,
            insights=insights,
            fig_count=fig_count,
        )
