"""
data_analysis/visualization.py — Data Visualization Engine
==========================================================
Generates interactive Plotly charts for Executive Dashboards.
Includes semantic column mapping heuristics to auto-detect
Dates, Regions, Categories, and Financial Metrics.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.core.logging_manager import get_logger

logger = get_logger("src.visualization.chart_factory")

class VisualizationEngine:
    """Engine for building interactive BI visualizations."""

    def __init__(self):
        # Default Plotly template for clean UI
        self.template = "plotly_dark"
        self.colors = ["#E6007E", "#00E5FF", "#8C52FF", "#4A69FF", "#FF2A85"]

    # ── Semantic Column Mapping ───────────────────────────────────────────────

    def auto_map_columns(self, df: pd.DataFrame) -> dict[str, str | list[str] | None]:
        """Heuristically auto-detects column roles for charting."""
        mapping = {
            "date": None,
            "category": None,
            "product": None,
            "region": None,
            "state": None,
            "revenue": None,
            "profit": None,
            "quantity": None,
            "customer": None,
        }
        
        cols = [c.lower() for c in df.columns]
        
        for idx, col in enumerate(cols):
            orig_col = df.columns[idx]
            dtype = df[orig_col].dtype
            
            # Dates
            if "date" in col or pd.api.types.is_datetime64_any_dtype(dtype):
                if mapping["date"] is None: mapping["date"] = orig_col
                
            # Categories
            if any(k in col for k in ["category", "segment", "type"]):
                if mapping["category"] is None: mapping["category"] = orig_col
                
            # Products
            if any(k in col for k in ["product", "item", "sku"]):
                if mapping["product"] is None: mapping["product"] = orig_col
                
            # Regions
            if "region" in col or "country" in col:
                if mapping["region"] is None: mapping["region"] = orig_col
            if "state" in col or "province" in col:
                if mapping["state"] is None: mapping["state"] = orig_col
                
            # Customers
            if "customer" in col or "client" in col:
                if mapping["customer"] is None: mapping["customer"] = orig_col

            # Financial Metrics (Requires Numeric)
            if pd.api.types.is_numeric_dtype(dtype) and not col.endswith("_outlier"):
                if any(k in col for k in ["sales", "revenue", "total"]):
                    if mapping["revenue"] is None: mapping["revenue"] = orig_col
                if "profit" in col or "margin" in col:
                    if mapping["profit"] is None: mapping["profit"] = orig_col
                if "quantity" in col or "qty" in col or "count" in col:
                    if mapping["quantity"] is None: mapping["quantity"] = orig_col

        # Fallbacks for numerics if names don't match
        num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and not c.endswith("_outlier")]
        if not mapping["revenue"] and num_cols: mapping["revenue"] = num_cols[0]
        if not mapping["profit"] and len(num_cols) > 1: mapping["profit"] = num_cols[1]
        
        # Fallbacks for categoricals
        cat_cols = [c for c in df.columns if df[c].dtype == object or str(df[c].dtype) == "category"]
        if not mapping["category"] and cat_cols: mapping["category"] = cat_cols[0]
        if not mapping["product"] and len(cat_cols) > 1: mapping["product"] = cat_cols[1]

        return mapping

    # ── Sales Analysis Charts ─────────────────────────────────────────────────

    def plot_monthly_trend(self, df: pd.DataFrame, date_col: str, metric_cols: list[str]) -> go.Figure:
        """Plots an Area/Line chart for metrics over time."""
        # Ensure date type
        df = df.copy()
        if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            
        df = df.dropna(subset=[date_col])
        if df.empty:
            return go.Figure()

        # Group by Month-Year
        df["Month"] = df[date_col].dt.to_period("M").dt.to_timestamp()
        trend_df = df.groupby("Month")[metric_cols].sum().reset_index()

        fig = px.area(
            trend_df, 
            x="Month", 
            y=metric_cols, 
            title="Monthly Trend Analysis",
            template=self.template,
            color_discrete_sequence=self.colors
        )
        fig.update_layout(hovermode="x unified", legend_title="Metrics")
        return fig

    # ── Product Analysis Charts ───────────────────────────────────────────────

    def plot_category_performance(self, df: pd.DataFrame, category_col: str, metric_col: str) -> go.Figure:
        """Plots a Donut chart of metric by category."""
        grouped = df.groupby(category_col)[metric_col].sum().reset_index()
        fig = px.pie(
            grouped, 
            names=category_col, 
            values=metric_col, 
            hole=0.4,
            title=f"{metric_col} by {category_col}",
            template=self.template,
            color_discrete_sequence=self.colors
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig

    def plot_top_products(self, df: pd.DataFrame, product_col: str, metric_col: str, top_n: int = 10, bottom: bool = False) -> go.Figure:
        """Plots a horizontal bar chart of top/bottom products."""
        grouped = df.groupby(product_col)[metric_col].sum().reset_index()
        grouped = grouped.sort_values(by=metric_col, ascending=bottom).head(top_n)
        
        # Sort back descending for horizontal bar display
        grouped = grouped.sort_values(by=metric_col, ascending=True)

        title = f"Bottom {top_n} {product_col}s by {metric_col}" if bottom else f"Top {top_n} {product_col}s by {metric_col}"
        
        fig = px.bar(
            grouped, 
            x=metric_col, 
            y=product_col, 
            orientation="h",
            title=title,
            template=self.template,
            color=metric_col,
            color_continuous_scale="Reds" if bottom else "Blues"
        )
        fig.update_layout(coloraxis_showscale=False)
        return fig

    # ── Regional Analysis Charts ──────────────────────────────────────────────

    def plot_regional_distribution(self, df: pd.DataFrame, region_col: str, metric_col: str) -> go.Figure:
        """Plots a Treemap or Bar chart for regional sales."""
        grouped = df.groupby(region_col)[metric_col].sum().reset_index()
        
        fig = px.treemap(
            grouped, 
            path=[px.Constant("All Regions"), region_col], 
            values=metric_col,
            title=f"Regional Distribution of {metric_col}",
            color=metric_col,
            color_continuous_scale="Viridis"
        )
        fig.update_traces(root_color="lightgrey")
        fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
        return fig

    def plot_customer_scatter(self, df: pd.DataFrame, customer_col: str, metric_x: str, metric_y: str) -> go.Figure:
        """Plots a scatterplot of customers based on two metrics (e.g. Sales vs Profit)."""
        grouped = df.groupby(customer_col)[[metric_x, metric_y]].sum().reset_index()
        
        fig = px.scatter(
            grouped, 
            x=metric_x, 
            y=metric_y, 
            hover_data=[customer_col],
            title=f"Customer Analysis: {metric_x} vs {metric_y}",
            template=self.template,
            color=metric_y,
            color_continuous_scale="RdYlGn"
        )
        # Add zero lines
        fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="black")
        fig.add_vline(x=0, line_width=1, line_dash="dash", line_color="black")
        return fig

    # ── Advanced Visualization Charts (Phase 2) ───────────────────────────────

    def plot_sunburst(self, df: pd.DataFrame, path_cols: list[str], metric_col: str) -> go.Figure:
        """Plots an advanced Sunburst chart for hierarchical data."""
        df_clean = df.dropna(subset=path_cols + [metric_col]).copy()
        
        # Ensure positive values only for sunburst
        df_clean = df_clean[df_clean[metric_col] > 0]
        
        if df_clean.empty:
            return go.Figure()
            
        fig = px.sunburst(
            df_clean,
            path=path_cols,
            values=metric_col,
            title=f"Hierarchical View of {metric_col}",
            template=self.template,
            color=metric_col,
            color_continuous_scale="Blues"
        )
        return fig

    def plot_waterfall(self, df: pd.DataFrame, category_col: str, metric_col: str) -> go.Figure:
        """Plots a Waterfall chart showing cumulative contribution of categories."""
        grouped = df.groupby(category_col)[metric_col].sum().reset_index()
        grouped = grouped.sort_values(metric_col, ascending=False)
        
        fig = go.Figure(go.Waterfall(
            name="Cumulative",
            orientation="v",
            measure=["relative"] * len(grouped),
            x=grouped[category_col],
            y=grouped[metric_col],
            textposition="outside",
            text=[f"${v:,.0f}" for v in grouped[metric_col]],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "#EF4444"}},
            increasing={"marker": {"color": "#10B981"}},
            totals={"marker": {"color": "#3B82F6"}}
        ))
        fig.update_layout(
            title=f"{metric_col} Contribution by {category_col}",
            template=self.template,
            showlegend=False
        )
        return fig

    def plot_funnel(self, df: pd.DataFrame, stage_col: str, metric_col: str) -> go.Figure:
        """Plots a Funnel chart (useful for sales stages or aggregated categorical drops)."""
        grouped = df.groupby(stage_col)[metric_col].sum().reset_index()
        grouped = grouped.sort_values(metric_col, ascending=False)
        
        fig = px.funnel(
            grouped,
            x=metric_col,
            y=stage_col,
            title=f"Funnel Analysis: {metric_col} by {stage_col}",
            template=self.template,
            color_discrete_sequence=self.colors
        )
        return fig

    def plot_geographic_map(self, df: pd.DataFrame, location_col: str, metric_col: str, location_mode: str = "USA-states") -> go.Figure:
        """
        Plots a Choropleth Map. 
        Note: location_mode determines if it's world countries or US states.
        """
        grouped = df.groupby(location_col)[metric_col].sum().reset_index()
        
        fig = px.choropleth(
            grouped,
            locations=location_col,
            locationmode=location_mode,
            color=metric_col,
            scope="usa" if location_mode == "USA-states" else "world",
            title=f"Geographic Heatmap: {metric_col}",
            color_continuous_scale="Viridis",
            template=self.template
        )
        fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'))
        return fig
