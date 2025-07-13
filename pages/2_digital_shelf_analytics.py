import streamlit as st
from utils.ui_components import create_input_form, display_data_exporter
from utils.logic import handle_get_data_button
from utils.state import initialize_session_state
from utils.messaging import display_user_message # <-- Import hàm mới

initialize_session_state()

# --- HIỂN THỊ THÔNG BÁO NGAY TẠI ĐÂY ---
display_user_message()

# --- KIỂM TRA ĐĂNG NHẬP ---
if not st.session_state.get('username'):
    st.warning("Please enter your name in the sidebar to start a session.")
    st.stop() # Dừng thực thi trang nếu chưa đăng nhập

st.set_page_config(page_title="Digital Shelf Analytics", layout="wide")
st.title("Digital Shelf Analytics")

tab1, tab2, tab3 = st.tabs(["Keyword Performance", "Product Tracking", "Competition Landscape"])

# Keyword Performance
with tab1:
    DATA_SOURCE_KEY = 'kw_pfm'
    st.header("Keyword Performance Data Export")
    
    workspace_id, storefront_input, start_date, end_date, pfm_options = create_input_form(
        DATA_SOURCE_KEY, show_kw_pfm_options=True
    )
    
    # Điều kiện hiển thị nút cho tab này
    show_button_tab1 = (st.session_state.stage == 'initial' or 
                        st.session_state.params.get('data_source') != DATA_SOURCE_KEY)
    
    if show_button_tab1:
        if st.button("Preview Data", type="primary", use_container_width=True, key=f'get_data_{DATA_SOURCE_KEY}'):
            handle_get_data_button(
                workspace_id, storefront_input, start_date, end_date, DATA_SOURCE_KEY,
                **pfm_options
            )
            
    # Hiển thị kết quả cho tab này
    if st.session_state.params.get('data_source') == DATA_SOURCE_KEY and st.session_state.stage != 'initial':
        display_data_exporter()

# Product Tracking
with tab2:
    DATA_SOURCE_KEY = 'pt'
    st.header("Product Tracking Data Export")

    workspace_id, storefront_input, start_date, end_date, _ = create_input_form(DATA_SOURCE_KEY)
    
    # Điều kiện hiển thị nút cho tab này
    show_button_tab2 = (st.session_state.stage == 'initial' or 
                        st.session_state.params.get('data_source') != DATA_SOURCE_KEY)
                        
    if show_button_tab2:
        if st.button("Preview Data", type="primary", use_container_width=True, key=f'get_data_{DATA_SOURCE_KEY}'):
            handle_get_data_button(workspace_id, storefront_input, start_date, end_date, DATA_SOURCE_KEY)
            
    # Hiển thị kết quả cho tab này
    if st.session_state.params.get('data_source') == DATA_SOURCE_KEY and st.session_state.stage != 'initial':
        display_data_exporter()

# Competition Landscape
with tab3:
    st.header("Competition Landscape Data Export")
    st.write("Coming soon...")