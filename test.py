import streamlit as st 
from db_connection import get_connection
from datetime import datetime, timedelta
from function import *
from kwl_data import *
from kw_pfm_data import *

if 'stage' not in st.session_state:
    st.session_state.stage = 'initial' # Các trạng thái: initial, waiting_confirmation, loading
if 'params' not in st.session_state:
    st.session_state.params = {}



# Sidebar navigation
with st.sidebar:
    st.title("Navigation")
    page = st.radio('Go to', ['KWL', 'DSA'])

if page == 'KWL':
    st.title("Keyword Data Export")
    
    workspace_id, storefront_input, start_date, end_date = kwl_page()
    
    # --- CẬP NHẬT TRẠNG THÁI KHI NHẤN NÚT ---
    if st.button("Get Data", type="primary", use_container_width=True, key='get_data_kwl'):
        # Pass 'kwl' as the data_source
        stage, params = handle_export_process(workspace_id, storefront_input, start_date, end_date, data_source='kwl')
        st.session_state.stage = stage
        st.session_state.params = params

    # --- XỬ LÝ LOGIC DỰA TRÊN TRẠNG THÁI HIỆN TẠI ---
    # Khối code này nằm ngoài `if st.button`, nên nó sẽ chạy mỗi lần rerun

    if st.session_state.stage == 'waiting_confirmation':
        num_row = st.session_state.params.get('num_row', 'many')
        st.warning(f"⚠️ Large dataset: {num_row:,} rows found. This may take a while to load.")
        
        # Dùng container để nhóm checkbox và nút lại
        with st.container():
            proceed = st.checkbox("I understand and want to proceed")
            confirm = st.button("Confirm")
            if proceed and confirm:
                # Nếu người dùng tick, chuyển sang trạng thái tải
                st.session_state.stage = 'loading'
                # Dùng rerun để ngay lập tức chạy lại script và vào nhánh 'loading'
                st.rerun()

    if st.session_state.stage == 'loading':
        # Pass the correct data_source to the display function
        load_data_and_display('kwl')

if page == 'DSA':
    tab_1, tab_2 = st.tabs(["Keyword PFM","Product Tracking"])
    
    with tab_1:
        st.title("Keyword PFM Data Export")
        workspace_id, storefront_input, start_date, end_date = kw_pfm_page()
        
        # --- CẬP NHẬT TRẠNG THÁI KHI NHẤN NÚT ---
        if st.button("Get Data", type="primary", use_container_width=True, key='get_data_dsa'):
            # Pass 'dsa' as the data_source
            stage, params = handle_export_process(workspace_id, storefront_input, start_date, end_date, data_source='dsa')
            st.session_state.stage = stage
            st.session_state.params = params

        # --- XỬ LÝ LOGIC DỰA TRÊN TRẠNG THÁI HIỆN TẠI ---
        # Khối code này nằm ngoài `if st.button`, nên nó sẽ chạy mỗi lần rerun

        if st.session_state.stage == 'waiting_confirmation':
            num_row = st.session_state.params.get('num_row', 'many')
            st.warning(f"⚠️ Large dataset: {num_row:,} rows found. This may take a while to load.")
            
            # Dùng container để nhóm checkbox và nút lại
            with st.container():
                proceed = st.checkbox("I understand and want to proceed")
                confirm = st.button("Confirm")
                if proceed and confirm:
                    # Nếu người dùng tick, chuyển sang trạng thái tải
                    st.session_state.stage = 'loading'
                    # Dùng rerun để ngay lập tức chạy lại script và vào nhánh 'loading'
                    st.rerun()

        if st.session_state.stage == 'loading':
            # Pass the correct data_source to the display function
            load_data_and_display('dsa')


    with tab_2:
        st.title("Product Tracking Data Export")
        # workspace_id, storefront_input, start_date, end_date = product_tracking_page()
    

# Add help text
with st.expander("Reminder"):
    with open("help.md", "r", encoding="utf-8") as f:
        about = f.read()
    st.markdown(about)