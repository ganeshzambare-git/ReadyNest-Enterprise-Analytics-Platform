import logging
from typing import Callable, Optional
import streamlit as st

logger = logging.getLogger(__name__)

class ExportButtonsComponent:
    """
    Component for rendering export buttons (PDF, Excel, PPT).
    Handles UI layout and trigger callbacks for export generation.
    """
    
    @classmethod
    def render(
        cls, 
        on_export_pdf: Optional[Callable[[], None]] = None,
        on_export_excel: Optional[Callable[[], None]] = None,
        on_export_ppt: Optional[Callable[[], None]] = None
    ) -> None:
        """
        Render export buttons. Only renders buttons that have an associated callback.
        
        Args:
            on_export_pdf (Callable): Callback to trigger PDF generation/download.
            on_export_excel (Callable): Callback to trigger Excel generation/download.
            on_export_ppt (Callable): Callback to trigger PPT generation/download.
        """
        try:
            st.markdown("### 📥 Export Options")
            
            # Determine how many buttons to render for dynamic column sizing
            callbacks = [on_export_pdf, on_export_excel, on_export_ppt]
            active_buttons = sum(1 for cb in callbacks if cb is not None)
            
            if active_buttons == 0:
                st.info("No export options available for this view.")
                return
                
            cols = st.columns(active_buttons)
            col_idx = 0
            
            if on_export_pdf:
                with cols[col_idx]:
                    if st.button("📄 Export PDF", key="btn_export_pdf", use_container_width=True):
                        logger.info("PDF Export requested by user.")
                        on_export_pdf()
                col_idx += 1
                
            if on_export_excel:
                with cols[col_idx]:
                    if st.button("📊 Export Excel", key="btn_export_excel", use_container_width=True):
                        logger.info("Excel Export requested by user.")
                        on_export_excel()
                col_idx += 1
                
            if on_export_ppt:
                with cols[col_idx]:
                    if st.button("📽️ Export PPT", key="btn_export_ppt", use_container_width=True):
                        logger.info("PowerPoint Export requested by user.")
                        on_export_ppt()
                        
        except Exception as e:
            logger.error(f"Failed to render export buttons: {e}")
            st.error("Error displaying export options.")
