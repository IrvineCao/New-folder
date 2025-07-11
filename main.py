import streamlit as st
from utils.state import initialize_session_state

initialize_session_state()

st.set_page_config(
    page_title="Data Exporter Home",
    page_icon="🏠",
)

st.title("Welcome to the Data Exporter! 👋")

st.markdown(
    """
    This is a centralized application for exporting various types of marketing and performance data.

    **👈 Please select a page from the navigation menu on the left to begin.**

    ### Available Pages:
    - **Keyword Lab**: For exporting keyword discovery and performance data.
    - **Digital Shelf Analytics**: For keyword performance and product tracking.
    - **Please Read**: Important notes and help documentation.
"""
)