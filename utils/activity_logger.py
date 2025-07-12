# utils/activity_logger.py
import streamlit as st
import csv
from datetime import datetime
import os
import threading

# Sử dụng một "khóa" (lock) để ngăn ngừa xung đột khi nhiều phiên ghi file cùng lúc
_lock = threading.Lock()
LOG_FILE = 'activity_log.csv'

def log_activity(action: str, details: dict = None):
    """
    Ghi lại một hành động của người dùng vào tệp CSV.

    Args:
        action (str): Tên của hành động (ví dụ: 'LOGIN', 'PREVIEW_DATA').
        details (dict, optional): Một từ điển chứa các thông tin chi tiết.
    """
    # Chỉ ghi log nếu người dùng đã đăng nhập
    username = st.session_state.get('username')
    if not username:
        return

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    details_str = str(details) if details is not None else ''
    
    log_entry = [timestamp, username, action, details_str]
    
    with _lock:
        # Kiểm tra xem tệp đã tồn tại chưa để quyết định có ghi header không
        file_exists = os.path.isfile(LOG_FILE)
        
        with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Nếu tệp mới được tạo, ghi dòng header
            if not file_exists:
                writer.writerow(['Timestamp', 'Username', 'Action', 'Details'])
            
            # Ghi lại hành động
            writer.writerow(log_entry)