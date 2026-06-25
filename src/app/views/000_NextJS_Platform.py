import streamlit as st
import streamlit.components.v1 as components

# Hide Streamlit's default margins, padding, and top decoration to allow Next.js to take over
st.markdown("""
<style>
    /* Remove padding around the main block */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    
    /* Hide the top header decoration */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Make the iframe container take full height */
    iframe {
        width: 100% !important;
        height: 100vh !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Embed the Next.js app running on port 3000
components.iframe("http://localhost:3000", height=900, scrolling=True)
