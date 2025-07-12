# utils/logger.py
import streamlit as st
import traceback
from datetime import datetime

def log_error(exception: Exception):
    """
    Ghi lại thông tin chi tiết của một lỗi vào session_state.
    Bao gồm thời gian, loại lỗi, và toàn bộ traceback.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_type = type(exception).__name__
    full_traceback = traceback.format_exc()
    
    log_entry = {
        "timestamp": now,
        "error_type": error_type,
        "message": str(exception),
        "traceback": full_traceback
    }
    
    # Thêm log mới vào đầu danh sách để hiển thị lỗi mới nhất trước
    st.session_state.dev_logs.insert(0, log_entry)