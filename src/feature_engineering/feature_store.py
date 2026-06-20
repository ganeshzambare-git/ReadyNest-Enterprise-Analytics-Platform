"""
data_analysis/feature_engineering.py — Feature Engineering Engine
================================================================
Generates business-ready analytical features from raw datasets to be used
in predictive modeling (CLV, Churn Prob, Profitability Scores).
"""

from __future__ import annotations

import pandas as pd
import numpy as np

from src.visualization.chart_factory import VisualizationEngine
from src.core.logging_manager import get_logger

logger = get_logger("src.feature_engineering.feature_store")


class FeatureEngineeringEngine:
    """Creates advanced analytical features from raw data."""

    def __init__(self):
        self.mapping_engine = VisualizationEngine()

    def engineer_customer_features(self, df: pd.DataFrame) -> pd.DataFrame | None:
        """
        Generates Customer-level features:
        - Total Spend (CLV Proxy)
        - Purchase Frequency
        - Average Order Value
        - Recency (Days since last purchase)
        - Churn Indicator (1 if Recency > 180 days, 0 otherwise)
        """
        mapping = self.mapping_engine.auto_map_columns(df)
        cust_col = mapping["customer"]
        rev_col = mapping["revenue"]
        date_col = mapping["date"]
        
        if not cust_col or not rev_col:
            return None
            
        # Group by customer
        agg_dict = {rev_col: ['sum', 'count', 'mean']}
        
        if date_col:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            agg_dict[date_col] = ['max']
            
        cust_df = df.groupby(cust_col).agg(agg_dict).reset_index()
        
        # Flatten MultiIndex columns
        cust_df.columns = [
            cust_col, 
            'Total_Spend_CLV', 
            'Purchase_Frequency', 
            'Average_Order_Value'
        ] + (['Last_Purchase_Date'] if date_col else [])
        
        # Calculate Recency and Churn if date exists
        if date_col:
            max_date = df[date_col].max()
            cust_df['Recency_Days'] = (max_date - cust_df['Last_Purchase_Date']).dt.days
            
            # Simple heuristic: If haven't purchased in 180 days, considered Churned (1)
            cust_df['Churn_Indicator'] = (cust_df['Recency_Days'] > 180).astype(int)
            
            # Retention Score (100 - (Recency / 365 * 100)), capped between 0 and 100
            cust_df['Retention_Score'] = np.clip(100 - (cust_df['Recency_Days'] / 365 * 100), 0, 100)
            
        return cust_df

    def engineer_product_features(self, df: pd.DataFrame) -> pd.DataFrame | None:
        """
        Generates Product-level features:
        - Product Popularity Score (Based on sales volume)
        - Profitability Score (Margin)
        """
        mapping = self.mapping_engine.auto_map_columns(df)
        prod_col = mapping["product"] or mapping["category"]
        rev_col = mapping["revenue"]
        prof_col = mapping["profit"]
        
        if not prod_col or not rev_col:
            return None
            
        agg_dict = {rev_col: 'sum'}
        if prof_col:
            agg_dict[prof_col] = 'sum'
            
        prod_df = df.groupby(prod_col).agg(agg_dict).reset_index()
        
        # Popularity Score (Min-Max scaled revenue * 100)
        max_rev = prod_df[rev_col].max()
        min_rev = prod_df[rev_col].min()
        if max_rev > min_rev:
            prod_df['Popularity_Score'] = ((prod_df[rev_col] - min_rev) / (max_rev - min_rev)) * 100
        else:
            prod_df['Popularity_Score'] = 100.0
            
        # Profitability Score (Margin %)
        if prof_col:
            prod_df['Profit_Margin_Pct'] = (prod_df[prof_col] / prod_df[rev_col]) * 100
            # Min-Max scaled profit
            max_prof = prod_df[prof_col].max()
            min_prof = prod_df[prof_col].min()
            if max_prof > min_prof:
                prod_df['Profitability_Score'] = ((prod_df[prof_col] - min_prof) / (max_prof - min_prof)) * 100
            else:
                prod_df['Profitability_Score'] = 100.0
                
        return prod_df
