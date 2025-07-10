import streamlit as st
from utils.ui_components import create_input_form, display_data_exporter
from utils.logic import handle_get_data_button

# Đặt tiêu đề cho trang
st.set_page_config(page_title="Keyword Lab", layout="wide")
st.title("Keyword Level Data Export")

# Lấy trạng thái loading
is_loading = st.session_state.stage in ['loading', 'waiting_confirmation']

# Tạo form nhập liệu
workspace_id, storefront_input, start_date, end_date, _ = create_input_form('kwl')

# Xử lý khi nhấn nút
if st.button("Get Data", type="primary", use_container_width=True, key='get_data_kwl', disabled=is_loading):
    handle_get_data_button(workspace_id, storefront_input, start_date, end_date, 'kwl')

# Luôn kiểm tra và hiển thị kết quả nếu data source khớp
if st.session_state.params.get('data_source') == 'kwl':
    display_data_exporter()