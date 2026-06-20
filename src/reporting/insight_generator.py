"""
data_analysis/insights.py — Insight Extraction Engine
======================================================
An automated heuristic engine that scans datasets to uncover
actionable business insights, risks, and opportunities.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd

from src.visualization.chart_factory import VisualizationEngine
from src.core.logging_manager import get_logger

logger = get_logger("src.reporting.insight_generator")

@dataclass
class BusinessInsight:
    category: str       # 'Risk', 'Opportunity', 'Insight'
    area: str           # 'Product Performance', 'Regional Performance', etc.
    title: str
    insight: str
    evidence: str
    business_impact: str
    recommendation: str
    priority_level: str # 'High', 'Medium', 'Low'


class InsightEngine:
    """Heuristic engine that acts as a BI Consultant."""

    def __init__(self) -> None:
        self.mapping_engine = VisualizationEngine()
        self.insights: list[BusinessInsight] = []

    def extract_insights(self, df: pd.DataFrame) -> list[BusinessInsight]:
        """Runs all heuristic checks against the dataset."""
        self.insights = []
        mapping = self.mapping_engine.auto_map_columns(df)
        
        # If we don't have basic sales metrics, we can't do deep BI
        if not mapping["revenue"]:
            return self.insights

        # Run heuristic scanners
        self._check_profitability_risks(df, mapping)
        self._check_revenue_opportunities(df, mapping)
        self._check_regional_performance(df, mapping)
        
        # Sort insights by Priority: High -> Medium -> Low
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        self.insights.sort(key=lambda x: priority_map.get(x.priority_level, 4))
        
        return self.insights

    def _check_profitability_risks(self, df: pd.DataFrame, mapping: dict) -> None:
        """Scans for high-revenue but low/negative profit areas."""
        prof_col = mapping["profit"]
        rev_col = mapping["revenue"]
        cat_col = mapping["category"] or mapping["product"]
        
        if not prof_col or not rev_col or not cat_col:
            return

        grouped = df.groupby(cat_col)[[rev_col, prof_col]].sum()
        grouped["margin"] = grouped[prof_col] / grouped[rev_col]
        
        # Risk: Negative Margin on Top Sellers
        negative_margin = grouped[grouped["margin"] < 0].sort_values(by=rev_col, ascending=False)
        
        if not negative_margin.empty:
            worst = negative_margin.iloc[0]
            cat_name = negative_margin.index[0]
            
            self.insights.append(BusinessInsight(
                category="Risk",
                area="Profitability Drivers",
                title=f"Negative Margin on {cat_name}",
                insight=f"The category '{cat_name}' is driving significant revenue but operating at a loss.",
                evidence=f"Generated ${worst[rev_col]:,.2f} in sales but lost ${abs(worst[prof_col]):,.2f} (Margin: {worst['margin']:.1%}).",
                business_impact="Drains overall company profitability and wastes marketing/logistics resources on unprofitable volume.",
                recommendation=f"Immediately review pricing strategy, shipping costs, and discount structures for {cat_name}. Consider raising prices or discontinuing bottom-tier products.",
                priority_level="High"
            ))

        # Opportunity: High Margin Superstars
        high_margin = grouped[(grouped["margin"] > 0.20) & (grouped[rev_col] > grouped[rev_col].median())]
        if not high_margin.empty:
            best = high_margin.sort_values(by="margin", ascending=False).iloc[0]
            cat_name = high_margin.index[0]
            
            self.insights.append(BusinessInsight(
                category="Opportunity",
                area="Product Performance",
                title=f"High-Margin Superstar: {cat_name}",
                insight=f"'{cat_name}' produces an exceptionally high profit margin while maintaining above-average sales volume.",
                evidence=f"Margin of {best['margin']:.1%} on ${best[rev_col]:,.2f} in sales.",
                business_impact="Scaling this category offers the highest direct return on investment for the bottom line.",
                recommendation=f"Reallocate marketing spend to aggressively promote {cat_name}. Investigate upselling opportunities.",
                priority_level="High"
            ))

    def _check_revenue_opportunities(self, df: pd.DataFrame, mapping: dict) -> None:
        """Scans for pareto principles (80/20 rule) in revenue."""
        rev_col = mapping["revenue"]
        cust_col = mapping["customer"]
        
        if not rev_col or not cust_col:
            return
            
        grouped = df.groupby(cust_col)[rev_col].sum().sort_values(ascending=False)
        total_rev = grouped.sum()
        
        # Calculate Pareto
        cumulative = grouped.cumsum() / total_rev
        top_20_pct_customers = int(len(grouped) * 0.20)
        
        if top_20_pct_customers > 0:
            rev_from_top_20 = cumulative.iloc[top_20_pct_customers - 1]
            
            if rev_from_top_20 > 0.60:  # If top 20% drives more than 60% of revenue
                self.insights.append(BusinessInsight(
                    category="Insight",
                    area="Customer Trends",
                    title="High Customer Concentration",
                    insight="A small fraction of your customer base is driving the vast majority of your revenue.",
                    evidence=f"The top 20% of customers ({top_20_pct_customers:,} clients) generate {rev_from_top_20:.1%} of total revenue.",
                    business_impact="High risk of severe revenue drops if a few key accounts churn. However, it also presents an opportunity for VIP targeting.",
                    recommendation="Implement a VIP retention program for these top accounts. Diversify acquisition strategies to reduce dependency on whale clients.",
                    priority_level="Medium"
                ))

    def _check_regional_performance(self, df: pd.DataFrame, mapping: dict) -> None:
        """Identifies lagging or leading regions."""
        rev_col = mapping["revenue"]
        reg_col = mapping["region"] or mapping["state"]
        
        if not rev_col or not reg_col:
            return
            
        grouped = df.groupby(reg_col)[rev_col].sum()
        mean_rev = grouped.mean()
        
        lagging = grouped[grouped < (mean_rev * 0.5)]
        leading = grouped[grouped > (mean_rev * 2.0)]
        
        if not lagging.empty:
            worst = lagging.sort_values().index[0]
            self.insights.append(BusinessInsight(
                category="Risk",
                area="Regional Performance",
                title=f"Severely Underperforming Region: {worst}",
                insight=f"Sales in {worst} are significantly below the regional average.",
                evidence=f"{worst} generated ${lagging[worst]:,.2f}, which is less than half the average regional revenue (${mean_rev:,.2f}).",
                business_impact="Lost market share and inefficient allocation of regional resources/sales reps.",
                recommendation=f"Conduct a localized market analysis for {worst} to determine if the issue is pricing, competitor dominance, or lack of brand awareness.",
                priority_level="Medium"
            ))
            
        if not leading.empty:
            best = leading.sort_values(ascending=False).index[0]
            self.insights.append(BusinessInsight(
                category="Opportunity",
                area="Regional Performance",
                title=f"Booming Market: {best}",
                insight=f"{best} is vastly outperforming all other regions.",
                evidence=f"Generated ${leading[best]:,.2f}, more than double the average (${mean_rev:,.2f}).",
                business_impact="Proves strong product-market fit in this area.",
                recommendation="Analyze the successful sales strategies used in this region and attempt to replicate them in lagging markets.",
                priority_level="Low"
            ))
