import streamlit as st
from datetime import datetime, timedelta
from utils.logic import load_data, convert_df_to_csv
import time

def create_input_form(source_key: str, show_kw_pfm_options: bool = False):
    """
    Tạo form nhập liệu chuẩn, có thể tùy chọn hiển thị thêm các bộ lọc.
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


def display_data_exporter():
    """
    Hiển thị các nút và thông báo liên quan đến việc xuất dữ liệu.
    """
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
        start_time = time.time()
        with st.spinner("Loading data, please wait..."):
            df = load_data(st.session_state.params.get('data_source'))
            if df is not None:
                st.session_state.df = df
                st.session_state.stage = 'loaded'
            else:
                st.session_state.stage = 'initial'
        
        end_time = time.time()
        st.session_state.query_duration = end_time - start_time
        st.rerun()

    elif st.session_state.stage == 'loaded':
        df = st.session_state.get('df')
        if df is not None and not df.empty:
            
            # --- PHẦN TÓM TẮT MỚI ---
            st.success("✅ Data loaded successfully!")

            # Tính toán các chỉ số
            total_rows = len(df)
            num_storefronts = len(st.session_state.params.get('storefront_ids', []))
            
            start_date_str = st.session_state.params.get('start_date')
            end_date_str = st.session_state.params.get('end_date')
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            total_days = (end_date - start_date).days + 1

            query_duration = st.session_state.get('query_duration', 0)

            # Hiển thị tóm tắt
            with st.expander("📊 **Export Summary**", expanded=True):
                cols = st.columns(4)
                cols[0].metric("Total Rows", f"{total_rows:,}")
                cols[1].metric("Date Range", f"{total_days} days")
                cols[2].metric("Storefronts", num_storefronts)
                cols[3].metric("Query Time", f"{query_duration:.2f} s")
            # --- KẾT THÚC PHẦN TÓM TẮT ---

            csv_data = convert_df_to_csv(df)
            file_name = f"{st.session_state.params.get('data_source')}_data_{datetime.now().strftime('%Y%m%d')}.csv"

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