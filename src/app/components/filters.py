import logging
from typing import Dict, List, Any, Optional
import streamlit as st
from pydantic import BaseModel, Field
import datetime

logger = logging.getLogger(__name__)

class FilterState(BaseModel):
    """Data transfer object for the current state of filters."""
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    selected_products: List[str] = Field(default_factory=list)
    selected_regions: List[str] = Field(default_factory=list)
    selected_categories: List[str] = Field(default_factory=list)

class FilterComponent:
    """
    Component for rendering and managing dynamic cascading filters.
    Includes date, product, region, and category filters.
    """
    
    def __init__(self, available_data: Dict[str, List[Any]]):
        """
        Initialize the filter component with available options.
        
        Args:
            available_data (Dict): Dictionary containing lists of available options
                                   for 'products', 'regions', and 'categories'.
        """
        self.available_data = available_data
        logger.debug("FilterComponent initialized with available data keys: %s", list(available_data.keys()))

    def render(self) -> FilterState:
        """
        Render the filter component and return the selected filter state.
        Cascading logic is applied (e.g., selecting a region could ideally 
        filter available products, though here we demonstrate the UI foundation).
        
        Returns:
            FilterState: An object containing the currently selected filter values.
        """
        try:
            st.markdown("### 🔍 Global Filters")
            
            with st.expander("Adjust Filters", expanded=True):
                # Date Range Filter
                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input("Start Date", value=None, key="filter_start_date")
                with col2:
                    end_date = st.date_input("End Date", value=None, key="filter_end_date")
                
                # Dynamic Cascading Selects
                # In a full implementation, `available_categories` would be filtered by `selected_regions` etc.
                regions = self.available_data.get("regions", [])
                selected_regions = st.multiselect(
                    "Region",
                    options=regions,
                    default=[],
                    key="filter_regions",
                    help="Select one or more regions"
                )
                
                categories = self.available_data.get("categories", [])
                selected_categories = st.multiselect(
                    "Category",
                    options=categories,
                    default=[],
                    key="filter_categories",
                    help="Select product categories"
                )
                
                products = self.available_data.get("products", [])
                selected_products = st.multiselect(
                    "Product",
                    options=products,
                    default=[],
                    key="filter_products",
                    help="Select specific products"
                )
                
                # Compile state
                state = FilterState(
                    start_date=start_date,
                    end_date=end_date,
                    selected_products=selected_products,
                    selected_regions=selected_regions,
                    selected_categories=selected_categories
                )
                
                logger.info(f"FilterState updated: {state}")
                return state
                
        except Exception as e:
            logger.error(f"Failed to render filter component: {e}")
            st.error("Filter rendering failed.")
            return FilterState()
