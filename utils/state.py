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
        
    # --- BIẾN MỚI CHO VIỆC GHI LOG ---
    # Lưu trữ danh sách các lỗi kỹ thuật
    if 'dev_logs' not in st.session_state:
        st.session_state.dev_logs = []
        
    # Cờ để kiểm tra xem chế độ nhà phát triển đã được kích hoạt chưa
    if 'dev_mode_activated' not in st.session_state:
        st.session_state.dev_mode_activated = False
    
    # --- BIẾN MỚI CHO VIỆC ĐĂNG NHẬP ---
    if 'username' not in st.session_state:
        st.session_state.username = None