import streamlit as st
from utils.page_config import render_page
from utils.page_config import PAGES
from utils.helpers import initialize_session_state, display_user_message
import os

initialize_session_state()
display_user_message()

script_name = os.path.basename(__file__)

page_config = PAGES.get(script_name)

if page_config:
    render_page(page_config)
else:
    st.error(f"Page configuration for {script_name} not found.")