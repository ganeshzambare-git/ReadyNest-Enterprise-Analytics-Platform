"""
data_analysis/bivariate.py — Bivariate Analysis Engine
======================================================
Calculates correlations, generates heatmaps, scatter plots,
and derives business insights for numerical variable relationships.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.core.logging_manager import get_logger

logger = get_logger("src.analytics.bivariate_analysis")


@dataclass
class RelationshipAnalysis:
    x_col: str
    y_col: str
    pearson_r: float
    spearman_rho: float
    insights: list[str]
    fig_scatter: plt.Figure


class BivariateEngine:
    """Engine for performing Bivariate EDA and correlation analysis."""

    def __init__(self) -> None:
        # Set clean aesthetic for seaborn
        sns.set_theme(style="whitegrid", palette="muted")

    def get_numerical_columns(self, df: pd.DataFrame) -> list[str]:
        """Returns a list of purely numerical columns suitable for correlation."""
        cols = []
        for c in df.columns:
            if pd.api.types.is_numeric_dtype(df[c]) and not c.endswith("_outlier") and not c.endswith("_was_null"):
                cols.append(c)
        return cols

    def generate_correlation_matrix(self, df: pd.DataFrame, method: str = "pearson") -> Optional[pd.DataFrame]:
        """Calculates the correlation matrix for all numeric columns."""
        num_cols = self.get_numerical_columns(df)
        if len(num_cols) < 2:
            return None
        
        corr_matrix = df[num_cols].corr(method=method)
        return corr_matrix

    def generate_heatmap(self, corr_matrix: pd.DataFrame, title: str) -> plt.Figure:
        """Generates a Seaborn heatmap from a correlation matrix."""
        # Calculate figure size based on number of columns
        n = len(corr_matrix.columns)
        fig_size = max(6, n * 0.8)
        
        fig, ax = plt.subplots(figsize=(fig_size, fig_size * 0.8))
        
        # Mask the upper triangle for a cleaner look
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        
        cmap = sns.diverging_palette(230, 20, as_cmap=True)
        
        sns.heatmap(
            corr_matrix, 
            mask=mask, 
            cmap=cmap, 
            vmax=1.0, 
            vmin=-1.0, 
            center=0,
            square=True, 
            linewidths=.5, 
            cbar_kws={"shrink": .5},
            annot=True if n <= 10 else False,
            fmt=".2f",
            ax=ax
        )
        
        ax.set_title(title, fontweight="bold", pad=20)
        fig.tight_layout()
        
        return fig

    def generate_pairplot(self, df: pd.DataFrame, max_cols: int = 5) -> Optional[plt.Figure]:
        """Generates a Pair Plot for the most highly correlated columns."""
        num_cols = self.get_numerical_columns(df)
        if len(num_cols) < 2:
            return None
            
        # If there are many columns, we only plot the top ones based on highest absolute correlation sum
        if len(num_cols) > max_cols:
            corr_matrix = df[num_cols].corr().abs()
            top_cols = corr_matrix.sum().sort_values(ascending=False).head(max_cols).index.tolist()
        else:
            top_cols = num_cols
            
        plot_df = df[top_cols].dropna()
        if plot_df.empty:
            return None

        # Seaborn pairplot returns a PairGrid, not a raw Figure
        pair_grid = sns.pairplot(plot_df, corner=True, diag_kind="kde", plot_kws={'alpha': 0.6, 's': 20, 'edgecolor': None})
        pair_grid.fig.suptitle(f"Pair Plot (Top {len(top_cols)} Correlated Variables)", y=1.02, fontweight="bold")
        
        return pair_grid.fig

    def generate_insights(self, r: float, x_col: str, y_col: str) -> list[str]:
        """Generates plain-English business insights from a correlation coefficient."""
        insights = []
        
        # Strength
        abs_r = abs(r)
        if abs_r >= 0.7:
            strength = "Strong"
        elif abs_r >= 0.4:
            strength = "Moderate"
        elif abs_r >= 0.2:
            strength = "Weak"
        else:
            strength = "Negligible"
            
        # Direction
        if r > 0:
            direction = "Positive"
            action = "tends to increase"
        else:
            direction = "Negative"
            action = "tends to decrease"
            
        if abs_r < 0.2:
            insights.append(f"No significant linear relationship detected between {x_col} and {y_col}.")
            return insights

        insights.append(f"**{strength} {direction} Correlation (r = {r:.2f})**")
        insights.append(f"As **{x_col}** increases, **{y_col}** {action}.")
        
        if abs_r >= 0.7:
            insights.append("This is a highly reliable trend. These two metrics are closely intertwined.")
        elif abs_r >= 0.4:
            insights.append("There is a noticeable trend, but there is still significant variance.")
            
        return insights

    def analyze_relationship(self, df: pd.DataFrame, x_col: str, y_col: str) -> Optional[RelationshipAnalysis]:
        """Analyzes the relationship between two specific numerical columns."""
        if x_col not in df.columns or y_col not in df.columns:
            return None
            
        plot_df = df[[x_col, y_col]].dropna()
        if plot_df.empty:
            return None

        pearson_r = plot_df[x_col].corr(plot_df[y_col], method="pearson")
        spearman_rho = plot_df[x_col].corr(plot_df[y_col], method="spearman")
        
        insights = self.generate_insights(pearson_r, x_col, y_col)

        # Generate Scatter Plot with Regression Line
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # Use regplot to automatically fit an OLS trendline
        sns.regplot(
            data=plot_df, 
            x=x_col, 
            y=y_col, 
            ax=ax,
            scatter_kws={'alpha':0.5, 's':30, 'color':'#3b82f6'}, 
            line_kws={'color':'#ef4444', 'linewidth': 2}
        )
        
        ax.set_title(f"Relationship: {x_col} vs {y_col}", fontweight="bold")
        sns.despine(fig)
        fig.tight_layout()

        return RelationshipAnalysis(
            x_col=x_col,
            y_col=y_col,
            pearson_r=pearson_r,
            spearman_rho=spearman_rho,
            insights=insights,
            fig_scatter=fig
        )
