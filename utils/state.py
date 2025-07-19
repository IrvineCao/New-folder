# utils/state.py
import streamlit as st

def initialize_session_state():
    """
    Initialize all necessary variables in st.session_state 
    if they don't already exist.
    """
    # Existing state variables
    if 'stage' not in st.session_state:
        st.session_state.stage = 'initial'
    if 'params' not in st.session_state:
        st.session_state.params = {}
    if 'df_preview' not in st.session_state:
        st.session_state.df_preview = None
    if 'query_duration' not in st.session_state:
        st.session_state.query_duration = 0
    if 'download_info' not in st.session_state:
        st.session_state.download_info = {}

    # --- NEW VARIABLE FOR USER NOTIFICATIONS ---
    if 'user_message' not in st.session_state:
        st.session_state.user_message = None
