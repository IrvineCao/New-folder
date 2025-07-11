import streamlit as st
from utils.ui_components import create_input_form, display_data_exporter
from utils.logic import handle_get_data_button
from utils.state import initialize_session_state

initialize_session_state()
# Đặt cấu hình cho trang
st.set_page_config(page_title="Digital Shelf Analytics", layout="wide")
st.title("Digital Shelf Analytics")

# Lấy trạng thái loading để vô hiệu hóa các nút khi cần
is_loading = st.session_state.stage in ['loading', 'waiting_confirmation']

# Tạo các tab
tab1, tab2, tab3 = st.tabs(["Keyword Performance", "Product Tracking", "Competition Landscape"])

with tab1:
    st.header("Keyword Performance Data Export")
    # Tạo form nhập liệu cho tab Keyword Performance
    workspace_id_kw_pfm, storefront_input_kw_pfm, start_date_kw_pfm, end_date_kw_pfm, pfm_options = create_input_form(
        'kw_pfm', show_kw_pfm_options=True
    )

    # Xử lý khi nhấn nút Get Data
    if st.button("Get Data", type="primary", use_container_width=True, key='get_data_kw_pfm', disabled=is_loading):
        handle_get_data_button(
            workspace_id_kw_pfm, storefront_input_kw_pfm, start_date_kw_pfm, end_date_kw_pfm, 'kw_pfm',
            **pfm_options
        )
    
    # Chỉ hiển thị kết quả nếu dữ liệu được tải cho tab này
    if st.session_state.params.get('data_source') == 'kw_pfm':
        display_data_exporter()

with tab2:
    st.header("Product Tracking Data Export")
    # Tạo form nhập liệu cho tab Product Tracking
    workspace_id_pt, storefront_input_pt, start_date_pt, end_date_pt, _ = create_input_form('pt')

    # Xử lý khi nhấn nút Get Data
    if st.button("Get Data", type="primary", use_container_width=True, key='get_data_pt', disabled=is_loading):
        handle_get_data_button(workspace_id_pt, storefront_input_pt, start_date_pt, end_date_pt, 'pt')

    # Chỉ hiển thị kết quả nếu dữ liệu được tải cho tab này
    if st.session_state.params.get('data_source') == 'pt':
        display_data_exporter()

with tab3:
    st.header("Competition Landscape Data Export")
    st.write("Coming soon...")