import streamlit as st
from utils.state import initialize_session_state

initialize_session_state()

# --- KIỂM TRA ĐĂNG NHẬP ---
if not st.session_state.get('username'):
    st.warning("Please enter your name in the sidebar to start a session.")
    st.stop() # Dừng thực thi trang nếu chưa đăng nhập

st.title("Please Read")
try:
    # Giả định tệp help.md nằm ở thư mục gốc
    with open("help.md", "r", encoding="utf-8") as f:
        about = f.read()
    st.markdown(about)
except FileNotFoundError:
    st.error("File help.md not found.")