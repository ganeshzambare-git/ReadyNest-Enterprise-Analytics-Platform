from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter()

# In a real scenario, this would load the global dataset from src.core.security
# For Phase 1 demonstration, we return mock metadata about the dataset

@router.get("/status")
def get_data_status() -> Dict[str, Any]:
    return {
        "loaded": True,
        "filename": "mock_sales_data.csv",
        "rows": 15000,
        "columns": 24,
        "last_updated": "2026-06-23T08:00:00Z"
    }

@router.get("/sample")
def get_data_sample() -> Dict[str, Any]:
    # Mock returning the first 5 rows
    return {
        "data": [
            {"id": 1, "date": "2023-01-01", "region": "North", "revenue": 1500, "category": "Electronics"},
            {"id": 2, "date": "2023-01-02", "region": "South", "revenue": 2200, "category": "Furniture"},
            {"id": 3, "date": "2023-01-03", "region": "East", "revenue": 1800, "category": "Office Supplies"},
            {"id": 4, "date": "2023-01-04", "region": "West", "revenue": 3400, "category": "Electronics"},
            {"id": 5, "date": "2023-01-05", "region": "North", "revenue": 900, "category": "Furniture"},
        ]
    }
