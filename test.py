import streamlit as st
from ui import display_main_ui

# --- App State Initialization ---
if 'stage' not in st.session_state:
    st.session_state.stage = 'initial'  # States: initial, waiting_confirmation, loading
if 'params' not in st.session_state:
    st.session_state.params = {}

# --- Run the main application ---
display_main_ui()
