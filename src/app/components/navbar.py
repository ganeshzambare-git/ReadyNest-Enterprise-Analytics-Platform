import logging
from typing import Callable, Optional
import streamlit as st

logger = logging.getLogger(__name__)

class NavbarComponent:
    """
    Navbar component for Streamlit application.
    Handles user profile display, search, notifications, theme switching, and logout functionality.
    """
    
    def __init__(self, username: str, user_avatar: Optional[str] = None):
        """
        Initialize the navbar component.
        
        Args:
            username (str): The name of the currently logged-in user.
            user_avatar (Optional[str]): An optional emoji or URL for the user's avatar.
        """
        self.username = username
        self.user_avatar = user_avatar or "👤"
        logger.debug(f"NavbarComponent initialized for user: {self.username}")

    def render(
        self, 
        on_logout: Callable[[], None], 
        on_theme_toggle: Callable[[], None],
        on_search: Callable[[str], None]
    ) -> None:
        """
        Render the top navigation bar.
        
        Args:
            on_logout (Callable): Callback executed when the logout button is clicked.
            on_theme_toggle (Callable): Callback executed when theme switcher is clicked.
            on_search (Callable): Callback executed when a search query is submitted.
        """
        try:
            # Create a horizontal layout for the navbar using columns
            col1, col2, col3, col4, col5 = st.columns([4, 1, 1, 1, 1])
            
            with col1:
                # Search bar
                search_query = st.text_input("Search", placeholder="Search dashboards, reports, insights...", label_visibility="collapsed")
                if search_query:
                    on_search(search_query)

            with col2:
                # Notifications
                st.button("🔔 Notifications", key="nav_notifications", use_container_width=True)
                
            with col3:
                # Theme Switcher
                if st.button("🌓 Theme", key="nav_theme_toggle", use_container_width=True):
                    on_theme_toggle()
                    
            with col4:
                # User Profile display
                st.markdown(f"**{self.user_avatar} {self.username}**")
                
            with col5:
                # Logout Button
                if st.button("🚪 Logout", key="nav_logout", use_container_width=True):
                    logger.info(f"User {self.username} initiated logout.")
                    on_logout()
                    
            st.divider()
            
        except Exception as e:
            logger.error(f"Failed to render navbar component: {e}")
            st.error("Navbar rendering failed.")
