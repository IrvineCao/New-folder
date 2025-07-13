import streamlit as st
from utils.ui_components import create_input_form, display_data_exporter
from utils.logic import handle_get_data_button
from utils.state import initialize_session_state
from utils.messaging import display_user_message 

initialize_session_state()

# --- KIỂM TRA ĐĂNG NHẬP ---
if not st.session_state.get('username'):
    st.warning("Please enter your name in the sidebar to start a session.")
    st.stop()

st.set_page_config(page_title="Keyword Lab", layout="wide")
st.title("Keyword Level Data Export")

# --- HIỂN THỊ THÔNG BÁO NGAY TẠI ĐÂY ---
display_user_message()

DATA_SOURCE_KEY = 'kwl'

# Hiển thị form nhập liệu
workspace_id, storefront_input, start_date, end_date, _ = create_input_form(DATA_SOURCE_KEY)

# Điều kiện để hiển thị nút "Preview Data"
# Nút sẽ hiển thị nếu:
# 1. Trạng thái là 'initial'
# 2. Hoặc, trạng thái không phải 'initial' NHƯNG nguồn dữ liệu đang xử lý không phải là của trang này.
show_button = (st.session_state.stage == 'initial' or 
               st.session_state.params.get('data_source') != DATA_SOURCE_KEY)

if show_button:
    if st.button("Preview Data", type="primary", use_container_width=True, key=f'get_data_{DATA_SOURCE_KEY}'):
        handle_get_data_button(workspace_id, storefront_input, start_date, end_date, DATA_SOURCE_KEY)

# Hiển thị phần kết quả chỉ khi nguồn dữ liệu khớp và không ở trạng thái ban đầu
if st.session_state.params.get('data_source') == DATA_SOURCE_KEY and st.session_state.stage != 'initial':
    display_data_exporter()