"""
data_analysis/statistics.py — Descriptive Statistics Engine
=============================================================
Calculates comprehensive statistical summaries for numeric columns
and generates business insights based on the results.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd
from fpdf import FPDF

from src.core.logging_manager import get_logger

logger = get_logger("src.analytics.descriptive_statistics")


# ── Result Dataclasses ────────────────────────────────────────────────────────

@dataclass
class ColumnStatistics:
    """Descriptive statistics for a single numeric column."""
    column: str
    count: int
    mean: float
    median: float
    mode: Optional[float]
    variance: float
    std_dev: float
    min_val: float
    max_val: float
    q1: float
    q3: float
    range_val: float
    iqr: float
    skewness: float
    kurtosis: float


@dataclass
class StatisticalReport:
    """Comprehensive statistical report for multiple columns."""
    column_stats: dict[str, ColumnStatistics] = field(default_factory=dict)
    insights: dict[str, list[str]] = field(default_factory=dict)

    def to_dataframe(self) -> pd.DataFrame:
        """Convert all column statistics into a single DataFrame."""
        if not self.column_stats:
            return pd.DataFrame()
            
        rows = []
        for col, stats in self.column_stats.items():
            rows.append({
                "Metric": col,
                "Count": stats.count,
                "Mean": round(stats.mean, 2),
                "Median": round(stats.median, 2),
                "Mode": round(stats.mode, 2) if stats.mode is not None else None,
                "Std Dev": round(stats.std_dev, 2),
                "Variance": round(stats.variance, 2),
                "Min": round(stats.min_val, 2),
                "25% (Q1)": round(stats.q1, 2),
                "75% (Q3)": round(stats.q3, 2),
                "Max": round(stats.max_val, 2),
                "Range": round(stats.range_val, 2),
                "IQR": round(stats.iqr, 2),
            })
        return pd.DataFrame(rows)

    def to_pdf_bytes(self) -> bytes:
        """Convert the statistical report into a simple PDF format."""
        if not self.column_stats:
            return b""
            
        pdf = FPDF(orientation="landscape")
        pdf.add_page()
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, "ReadyNest Descriptive Statistics Report", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)
        
        pdf.set_font("helvetica", "B", 10)
        
        # Table Header
        headers = ["Metric", "Count", "Mean", "Median", "Min", "Max", "Std Dev"]
        col_widths = [45, 25, 30, 30, 30, 30, 30]
        
        for idx, h in enumerate(headers):
            pdf.cell(col_widths[idx], 8, h, border=1, align="C")
        pdf.ln()
        
        # Table Rows
        pdf.set_font("helvetica", "", 10)
        for col, stats in self.column_stats.items():
            row_data = [
                str(col)[:25],
                f"{stats.count:,}",
                f"{stats.mean:,.2f}",
                f"{stats.median:,.2f}",
                f"{stats.min_val:,.2f}",
                f"{stats.max_val:,.2f}",
                f"{stats.std_dev:,.2f}"
            ]
            for idx, data in enumerate(row_data):
                pdf.cell(col_widths[idx], 8, data, border=1, align="C")
            pdf.ln()
            
        pdf.ln(10)
        
        # Insights Section
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, "Business Insights", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        
        pdf.set_font("helvetica", "", 10)
        for col, insights in self.insights.items():
            if insights:
                pdf.set_font("helvetica", "B", 11)
                pdf.cell(0, 8, f"Metric: {col}", new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("helvetica", "", 10)
                for ins in insights:
                    # Clean up bold markdown formatting for text rendering
                    clean_ins = ins.replace("**", "")
                    pdf.multi_cell(0, 6, f"- {clean_ins}", new_x="LMARGIN", new_y="NEXT")
                pdf.ln(3)
                
        return bytes(pdf.output())


# ── Engine Class ──────────────────────────────────────────────────────────────

class DescriptiveStatsEngine:
    """
    Engine to calculate and interpret descriptive statistics.
    
    Example::
    
        engine = DescriptiveStatsEngine()
        report = engine.analyze(df, columns=["Revenue", "Quantity"])
    """
    
    def analyze(self, df: pd.DataFrame, columns: Optional[list[str]] = None) -> StatisticalReport:
        """
        Calculate statistics for the specified numeric columns.
        
        Args:
            df:      Input DataFrame.
            columns: List of numeric columns to analyze. If None, auto-selects.
            
        Returns:
            :class:`StatisticalReport` with metrics and insights.
        """
        report = StatisticalReport()
        
        target_cols = columns if columns else self._auto_select_columns(df)
        target_cols = [c for c in target_cols if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]
        
        if not target_cols:
            logger.warning("No valid numeric columns found for analysis.")
            return report
            
        for col in target_cols:
            series = df[col].dropna()
            if len(series) == 0:
                continue
                
            mode_series = series.mode()
            mode_val = mode_series.iloc[0] if not mode_series.empty else None
            
            stats = ColumnStatistics(
                column=col,
                count=len(series),
                mean=series.mean(),
                median=series.median(),
                mode=mode_val,
                variance=series.var() if len(series) > 1 else 0.0,
                std_dev=series.std() if len(series) > 1 else 0.0,
                min_val=series.min(),
                max_val=series.max(),
                q1=series.quantile(0.25),
                q3=series.quantile(0.75),
                range_val=series.max() - series.min(),
                iqr=series.quantile(0.75) - series.quantile(0.25),
                skewness=series.skew(),
                kurtosis=series.kurtosis()
            )
            
            report.column_stats[col] = stats
            report.insights[col] = self._generate_column_insights(col, stats)
            
        logger.info(f"Analyzed {len(target_cols)} columns for descriptive statistics.")
        return report

    def _auto_select_columns(self, df: pd.DataFrame) -> list[str]:
        """Automatically identify key business metrics from columns."""
        keywords = ["revenue", "sales", "profit", "quantity", "discount", "margin", "cost", "price", "customer"]
        selected = []
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                col_lower = col.lower()
                if any(kw in col_lower for kw in keywords):
                    selected.append(col)
                    
        # Fallback if no keywords matched
        if not selected:
            selected = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])][:5]
            
        return selected

    def _generate_column_insights(self, col: str, stats: ColumnStatistics) -> list[str]:
        """Generate human-readable business insights from raw statistics."""
        insights = []
        col_lower = col.lower()
        
        # Determine if higher is better (revenue) or worse (cost, discount sometimes)
        positive_metric = not any(kw in col_lower for kw in ["cost", "discount", "expense", "loss"])
        
        # 1. Central Tendency & Skewness Insight
        if stats.mean > stats.median * 1.1:
            insights.append(f"**Right Skewed:** The average (Mean: {stats.mean:,.2f}) is noticeably higher than the typical value (Median: {stats.median:,.2f}). This indicates a few very high {col} values are pulling the average up.")
        elif stats.median > stats.mean * 1.1:
            insights.append(f"**Left Skewed:** The typical value (Median: {stats.median:,.2f}) is higher than the average ({stats.mean:,.2f}), meaning a few very low values are dragging the average down.")
        else:
            insights.append(f"**Symmetrical Distribution:** The average ({stats.mean:,.2f}) and typical value (Median: {stats.median:,.2f}) are very close, indicating a balanced distribution of {col}.")
            
        # 2. Volatility / Dispersion Insight
        cv = (stats.std_dev / stats.mean) if stats.mean != 0 else 0
        if cv > 1.0:
            insights.append(f"**High Volatility:** The Standard Deviation ({stats.std_dev:,.2f}) is very high relative to the mean. {col} values fluctuate wildly.")
        elif cv < 0.2:
            insights.append(f"**High Consistency:** {col} is very stable across the dataset, with low variance from the mean.")
            
        # 3. Extremes Insight
        if stats.max_val > (stats.q3 + 3 * stats.iqr):
            insights.append(f"**Extreme Maximums:** The maximum value ({stats.max_val:,.2f}) is exceptionally high compared to the upper quartile ({stats.q3:,.2f}), suggesting massive outliers or special occurrences.")
            
        # 4. Contextual specific insights
        if "discount" in col_lower and stats.mean > 0.3:
            insights.append("⚠️ **High Average Discount:** Discounts are averaging over 30%, which could severely impact profit margins.")
        elif "profit" in col_lower and stats.min_val < 0:
            insights.append(f"⚠️ **Losses Detected:** The minimum profit is {stats.min_val:,.2f}, indicating that some transactions are resulting in a loss.")
            
        return insights
