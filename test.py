import streamlit as st 
from db_connection import get_connection
from datetime import datetime, timedelta
from function import handle_export_process, load_data_and_display
from kwl_data import kwl_page
from kw_pfm_data import kw_pfm_page

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
    # Add help text
    with st.expander("Reminder"):
        with open("help.md", "r", encoding="utf-8") as f:
            about = f.read()
        st.markdown(about)

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

        def product_tracking_page():
            """Creates the UI for the Product Tracking page and returns the user inputs."""
            with st.container():
                col6, col7, col8, col9 = st.columns(4)
                with col6:
                    workspace_id_pt = st.text_input("Workspace ID *", "", 
                                                     help="Enter the workspace ID (numeric)", key="workspace_id_pt")
                with col7:
                    storefront_input_pt = st.text_input("Storefront EID *", "", 
                                                     help="Enter one or more storefront IDs, comma-separated", key="storefront_input_pt")
                with col8:
                    start_date_pt = st.date_input("Start Date *", value=datetime.now() - timedelta(days=30), max_value=datetime.now().date() - timedelta(days=1), key="start_date_pt")
                with col9:
                    end_date_pt = st.date_input("End Date *", value=datetime.now().date() - timedelta(days=1), max_value=datetime.now().date() - timedelta(days=1), key="end_date_pt")
            return workspace_id_pt, storefront_input_pt, start_date_pt, end_date_pt

        workspace_id_pt, storefront_input_pt, start_date_pt, end_date_pt = product_tracking_page()

        st.write("---")
        
        # --- CẬP NHẬT TRẠNG THÁI KHI NHẤN NÚT ---
        if st.button("Get Data", type="primary", use_container_width=True, key='get_data_pt'):
            # Pass 'pt' as the data_source
            stage, params = handle_export_process(workspace_id_pt, storefront_input_pt, start_date_pt, end_date_pt, data_source='pt')
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
            load_data_and_display('pt')
    

