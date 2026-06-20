import logging
from typing import Optional, List
import streamlit as st
from pydantic import BaseModel, Field
import plotly.graph_objects as go

logger = logging.getLogger(__name__)

class KPIData(BaseModel):
    """Data transfer object representing the data for a single KPI card."""
    title: str = Field(..., description="The title of the KPI (e.g., 'Total Revenue')")
    value: str = Field(..., description="The main formatted value (e.g., '$1.2M')")
    growth_percentage: Optional[float] = Field(None, description="Growth compared to previous period")
    sparkline_data: Optional[List[float]] = Field(None, description="Data points for mini trend chart")
    is_positive_trend: Optional[bool] = Field(None, description="Indicates if trend is good (True) or bad (False)")

class KPICardComponent:
    """
    Component for rendering KPI cards with growth indicators and sparklines.
    """
    
    @staticmethod
    def _create_sparkline(data: List[float], is_positive: bool) -> go.Figure:
        """Helper to create a mini sparkline chart using Plotly."""
        color = "green" if is_positive else "red"
        fig = go.Figure(go.Scatter(y=data, mode='lines', line=dict(color=color, width=2)))
        fig.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            height=40,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        return fig

    @classmethod
    def render(cls, kpi_data: KPIData) -> None:
        """
        Render a single KPI card in the current Streamlit container.
        
        Args:
            kpi_data (KPIData): The data to render.
        """
        try:
            with st.container():
                # Apply custom CSS-like logic via markdown or native metrics
                # Streamlit's native st.metric supports basic growth indicators out of the box
                delta_str = None
                delta_color = "normal"
                
                if kpi_data.growth_percentage is not None:
                    delta_str = f"{kpi_data.growth_percentage:+.2f}%"
                    if kpi_data.is_positive_trend is not None:
                        delta_color = "normal" if kpi_data.is_positive_trend else "inverse"

                st.metric(
                    label=kpi_data.title,
                    value=kpi_data.value,
                    delta=delta_str,
                    delta_color=delta_color
                )
                
                # Render Sparkline if data is provided
                if kpi_data.sparkline_data and len(kpi_data.sparkline_data) > 1:
                    trend_flag = kpi_data.is_positive_trend if kpi_data.is_positive_trend is not None else True
                    fig = cls._create_sparkline(kpi_data.sparkline_data, trend_flag)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                    
            logger.debug(f"Rendered KPI Card: {kpi_data.title}")
            
        except Exception as e:
            logger.error(f"Failed to render KPI card '{kpi_data.title}': {e}")
            st.error("KPI rendering failed.")
