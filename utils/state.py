# utils/state.py
import streamlit as st

def initialize_session_state():
    """
    Khởi tạo tất cả các biến cần thiết trong st.session_state 
    nếu chúng chưa tồn tại.
    """
    # Các biến trạng thái hiện có
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

    # Biến để lưu trữ thông tin người dùng
    if 'username' not in st.session_state:
        st.session_state.username = None

    # --- BIẾN MỚI CHO THÔNG BÁO NGƯỜI DÙNG ---
    if 'user_message' not in st.session_state:
        st.session_state.user_message = None
