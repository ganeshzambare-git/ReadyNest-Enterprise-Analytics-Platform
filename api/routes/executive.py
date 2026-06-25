from fastapi import APIRouter
from typing import Dict, Any
import json

router = APIRouter()

# In a full implementation, these would query the dataframe using 
# src.visualization.chart_factory and return the plotly JSON.

@router.get("/kpis")
def get_kpis() -> Dict[str, Any]:
    return {
        "revenue": {"value": 8420000, "formatted": "$8.42M", "trend": "+12.4%", "positive": True},
        "aov": {"value": 56.32, "formatted": "$56.32", "trend": "+8.7%", "positive": True},
        "margin": {"value": 0.286, "formatted": "28.6%", "trend": "+4.1%", "positive": True},
        "delivery": {"value": 0.967, "formatted": "96.7%", "trend": "+2.2%", "positive": True}
    }

@router.get("/insights")
def get_insights() -> Dict[str, Any]:
    return {
        "insights": [
            {"title": "Revenue Spike", "description": "Electronics category up 22% this month.", "type": "positive"},
            {"title": "Delivery Delay", "description": "West region experiencing 2-day delays.", "type": "negative"},
            {"title": "New Trend", "description": "High correlation between discount and volume in Q3.", "type": "neutral"}
        ]
    }
