import streamlit as st
from datetime import datetime, timedelta
from logic import handle_export_process, load_data, convert_df_to_csv

def create_input_form(source_key: str, show_kw_pfm_options: bool = False):
    """
    Tạo form nhập liệu chuẩn, có thể tùy chọn hiển thị thêm các bộ lọc.
    
    Args:
        source_key (str): Key duy nhất cho các widget của form.
        show_kw_pfm_options (bool): Nếu True, hiển thị thêm các bộ lọc cho Keyword Performance.
    
    Returns:
        Tuple: Chứa các giá trị đầu vào từ người dùng.
    """
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    # Định nghĩa các tùy chọn cho dropdown
    date_options = {
        "Last 30 days": {"start": today - timedelta(days=30), "end": yesterday},
        "This month": {"start": today.replace(day=1), "end": yesterday},
        "Last month": {
            "start": (today.replace(day=1) - timedelta(days=1)).replace(day=1),
            "end": today.replace(day=1) - timedelta(days=1)
        },
        "Custom time range": None
    }

    start_date = None
    end_date = None
    pfm_options = {} # Từ điển để chứa các tùy chọn phụ

    with st.container():
        # --- Hàng 1 cho các input chính ---
        main_cols = st.columns(3)
        with main_cols[0]:
            workspace_id = st.text_input("Workspace ID *", "", key=f"ws_id_{source_key}")
        with main_cols[1]:
            storefront_input = st.text_input("Storefront EID *", "", key=f"sf_id_{source_key}")
            if len(storefront_input.split(',')) > 1:
                st.info("💡 Pro-tip: For faster performance with multiple storefronts, select a smaller date range (e.g.,30-60 days).")
        with main_cols[2]:
            selected_option = st.selectbox(
                "Select time range *",
                options=list(date_options.keys()),
                index=0,
                key=f"date_preset_{source_key}"
            )

        # --- Hàng 2 cho Custom time range (chỉ hiển thị khi cần) ---
        if selected_option == "Custom time range":
            custom_date_cols = st.columns(2)
            with custom_date_cols[0]:
                start_date = st.date_input("Start Date", value=yesterday, max_value=yesterday, key=f"start_date_{source_key}")
            with custom_date_cols[1]:
                end_date = st.date_input("End Date", value=yesterday, max_value=yesterday, key=f"end_date_{source_key}")
        else:
            dates = date_options[selected_option]
            start_date = dates["start"]
            end_date = dates["end"]
        
        # --- Cột cho các input phụ (chỉ hiển thị khi cần) ---
        if show_kw_pfm_options:
            st.write("Additional options:")
            extra_cols = st.columns(3)
            with extra_cols[0]:
                pfm_options['device_type'] = st.selectbox("Device Type", ('Mobile', 'Desktop'), key=f'device_type_{source_key}')
            with extra_cols[1]:
                pfm_options['display_type'] = st.selectbox("Display Type", ('Paid', 'Organic','Top'), key=f'display_type_{source_key}')
            with extra_cols[2]:
                pfm_options['product_position'] = st.selectbox("Product Position", ('-1','4','10'), key=f'product_pos_{source_key}')

    st.write("---")
    return workspace_id, storefront_input, start_date, end_date, pfm_options



def display_main_ui():
    """Hiển thị giao diện chính của ứng dụng."""
    st.sidebar.title("Navigation")
    page = st.sidebar.radio('Go to', ['Keyword Lab', 'Digital Shelf Analytics','Performance Index', 'Please Read Im Begging You'])

    is_loading = st.session_state.stage in ['loading', 'waiting_confirmation']

    if page == 'Keyword Lab':
        st.title("Keyword Level Data Export")
        
        workspace_id, storefront_input, start_date, end_date, _ = create_input_form('kwl')
        if st.button("Get Data", type="primary", use_container_width=True, key='get_data_kwl', disabled=is_loading):
            handle_get_data_button(workspace_id, storefront_input, start_date, end_date, 'kwl')


    elif page == 'Digital Shelf Analytics':
        tab1, tab2, tab3 = st.tabs(["Keyword Performance", "Product Tracking","Competition Landscape"])

        with tab1:
            st.title("Keyword Performance Data Export")
            workspace_id, storefront_input, start_date, end_date, pfm_options = create_input_form(
                'kw_pfm', show_kw_pfm_options=True
            )
            
            if st.button("Get Data", type="primary", use_container_width=True, key='get_data_kw_pfm', disabled=is_loading):
                handle_get_data_button(
                    workspace_id, storefront_input, start_date, end_date, 'kw_pfm',
                    **pfm_options # "Mở" từ điển thành các tham số
                )

        with tab2:
            st.title("Product Tracking Data Export")
            workspace_id, storefront_input, start_date, end_date, _ = create_input_form('pt')
            if st.button("Get Data", type="primary", use_container_width=True, key='get_data_pt', disabled=is_loading):
                handle_get_data_button(workspace_id, storefront_input, start_date, end_date, 'pt')

        with tab3:
            st.title("Competition Landscape Data Export")
            st.write("Coming soon...")
            # workspace_id, storefront_input, start_date, end_date, _ = create_input_form('pi')
            # if st.button("Get Data", type="primary", use_container_width=True, key='get_data_pi', disabled=is_loading):
            #     handle_get_data_button(workspace_id, storefront_input, start_date, end_date, 'pi')


# Development Zone
    # Performance Index
    elif page == 'Performance Index':
        st.title("Performance Index Data Export")
        st.write("Coming soon...")

        # st.title("Performance Index Data Export")
        # workspace_id, storefront_input, start_date, end_date, _ = create_input_form('pi')
        # if st.button("Get Data", type="primary", use_container_width=True, key='get_data_pi', disabled=is_loading):
        #     handle_get_data_button(workspace_id, storefront_input, start_date, end_date, 'pi')
# Development Zone


    elif page == 'Please Read Im Begging You':
        try:
            with open("help.md", "r", encoding="utf-8") as f:
                about = f.read()
            st.markdown(about)
        except FileNotFoundError:
            st.error("File help.md không tìm thấy.")

    if st.session_state.stage == 'waiting_confirmation':
        num_row = st.session_state.params.get('num_row', 'N/A')
        st.warning(f"⚠️ Large data: {num_row:,} rows found. This process may take a while.")
        
        col_confirm, col_cancel = st.columns(2)
        if col_confirm.button("Confirm and Proceed", key="confirm_button", use_container_width=True):
            st.session_state.stage = 'loading'
            st.rerun()
        if col_cancel.button("Cancel", key="cancel_button", use_container_width=True):
            st.session_state.stage = 'initial'
            st.rerun()

    elif st.session_state.stage == 'loading':
        with st.spinner("Loading data, please wait..."):
            df = load_data(st.session_state.params.get('data_source'))
            if df is not None:
                st.session_state.df = df
                st.session_state.stage = 'loaded'
            else:
                st.session_state.stage = 'initial'
        st.rerun()

    elif st.session_state.stage == 'loaded':
        data_source = st.session_state.params.get('data_source')
        page_matches_data = (
            (page == 'Keyword Lab' and data_source == 'kwl') or
            (page == 'Digital Shelf Analytics' and data_source in ['kw_pfm', 'pt'])
        )

        if page_matches_data:
            df = st.session_state.get('df', None)
            if df is not None and not df.empty:
                st.success(f"✅ Data loaded successfully {len(df):,} rows")
                csv_data = convert_df_to_csv(df)
                file_name = f"{data_source}_data_{datetime.now().strftime('%Y%m%d')}.csv"

                st.download_button(
                   label="Export Full Data as CSV",
                   data=csv_data,
                   file_name=file_name,
                   mime='text/csv',
                   use_container_width=True,
                   type="primary"
                )

                st.subheader("Preview data (first 500 rows)")
                st.data_editor(df.head(500), use_container_width=True, height=300)
            else:
                st.warning("No data to display.")
                st.session_state.stage = 'initial'


def handle_get_data_button(workspace_id, storefront_input, start_date, end_date, data_source, **kwargs):
    """Xử lý logic khi nút 'Get Data' được nhấn."""
    st.session_state.stage = 'initial'
    st.session_state.params = {}
    
    stage, params = handle_export_process(
        workspace_id,
        storefront_input,
        start_date,
        end_date,
        data_source=data_source,
        **kwargs
    )
    st.session_state.stage = stage
    st.session_state.params = params
    st.rerun()