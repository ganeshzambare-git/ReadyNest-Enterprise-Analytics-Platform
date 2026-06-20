import logging
from typing import List, Optional
import streamlit as st
from pydantic import BaseModel, Field

# Configure logging
logger = logging.getLogger(__name__)

class MenuItem(BaseModel):
    """Data transfer object for a sidebar menu item."""
    title: str = Field(..., description="Display title of the menu item")
    icon: str = Field(..., description="Icon identifier (e.g., Streamlit emoji or custom icon name)")
    page_id: str = Field(..., description="Internal identifier for routing")
    roles: List[str] = Field(default_factory=lambda: ["*"], description="Roles allowed to see this item. '*' means all roles.")

class SidebarComponent:
    """
    Sidebar component for Streamlit application.
    Handles dynamic navigation, role-based visibility, and active state.
    """
    
    def __init__(self, menu_items: List[MenuItem], user_role: str = "guest"):
        """
        Initialize the sidebar component.
        
        Args:
            menu_items (List[MenuItem]): The complete list of available menu items.
            user_role (str): The current user's role, used for filtering menu visibility.
        """
        self.menu_items = menu_items
        self.user_role = user_role
        logger.debug(f"SidebarComponent initialized for role: {self.user_role}")

    def _filter_items_by_role(self) -> List[MenuItem]:
        """
        Filter menu items based on the current user's role.
        """
        filtered = []
        for item in self.menu_items:
            if "*" in item.roles or self.user_role in item.roles:
                filtered.append(item)
        return filtered

    def render(self, active_page_id: str, expanded: bool = True) -> Optional[str]:
        """
        Render the sidebar in Streamlit.
        
        Args:
            active_page_id (str): The ID of the currently active page.
            expanded (bool): Whether the sidebar should be expanded by default.
            
        Returns:
            Optional[str]: The ID of the clicked page, or None if no click occurred.
        """
        try:
            # Note: Streamlit's sidebar state is often controlled globally, 
            # but we use native st.sidebar context.
            with st.sidebar:
                st.markdown("### 🧭 Navigation")
                
                visible_items = self._filter_items_by_role()
                
                selected_page = None
                
                for item in visible_items:
                    # Active page indicator logic
                    is_active = (item.page_id == active_page_id)
                    button_style = "primary" if is_active else "secondary"
                    
                    # Display the menu item
                    label = f"{item.icon} {item.title}"
                    if st.button(label, key=f"nav_{item.page_id}", type=button_style, use_container_width=True):
                        selected_page = item.page_id
                        logger.info(f"User navigated to: {item.page_id}")
                
                return selected_page
                
        except Exception as e:
            logger.error(f"Failed to render sidebar component: {e}")
            st.sidebar.error("Navigation rendering failed.")
            return None
