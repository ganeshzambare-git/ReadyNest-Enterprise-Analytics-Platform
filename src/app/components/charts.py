import logging
from typing import Optional
import streamlit as st
import plotly.graph_objects as go

logger = logging.getLogger(__name__)

class ChartComponent:
    """
    Reusable wrapper for Plotly charts to ensure consistent theming,
    error handling, and layout within the Streamlit application.
    """
    
    @classmethod
    def apply_theme(cls, fig: go.Figure, theme_name: str = "plotly_white") -> go.Figure:
        """
        Apply global application theme to a Plotly figure.
        
        Args:
            fig (go.Figure): The plotly figure to style.
            theme_name (str): The name of the theme to apply.
            
        Returns:
            go.Figure: The styled figure.
        """
        fig.update_layout(
            template=theme_name,
            margin=dict(l=20, r=20, t=40, b=20),
            title_x=0.5, # Center title
            paper_bgcolor="rgba(0,0,0,0)", # Transparent background
            plot_bgcolor="rgba(0,0,0,0)",
        )
        return fig

    @classmethod
    def render(
        cls, 
        fig: go.Figure, 
        title: Optional[str] = None, 
        height: int = 400,
        use_container_width: bool = True
    ) -> None:
        """
        Render a chart safely in Streamlit.
        
        Args:
            fig (go.Figure): The chart to render.
            title (Optional[str]): Optional title to display above the chart.
            height (int): Height of the chart in pixels.
            use_container_width (bool): Whether to expand to fill the column width.
        """
        try:
            if title:
                st.markdown(f"#### {title}")
                
            # Apply standard theme before rendering
            fig = cls.apply_theme(fig)
            fig.update_layout(height=height)
            
            # Render using Streamlit's plotly integration
            st.plotly_chart(
                fig, 
                use_container_width=use_container_width, 
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['lasso2d', 'select2d']
                }
            )
            logger.debug(f"Rendered chart: {title if title else 'Untitled'}")
            
        except Exception as e:
            logger.error(f"Failed to render chart component: {e}")
            st.error("Error displaying chart.")
