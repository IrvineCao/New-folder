import streamlit as st
from datetime import datetime, timedelta
from utils.logic import load_data, convert_df_to_csv
import time

def create_input_form(source_key: str, show_kw_pfm_options: bool = False):
    """
    Tạo form nhập liệu chuẩn, có thể tùy chọn hiển thị thêm các bộ lọc.
    """
    # --- Lưu và tải lại lựa chọn của người dùng ---
    ws_key = f"ws_id_{source_key}"
    sf_key = f"sf_id_{source_key}"

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    date_options = {
        "Last 30 days": {"start": today - timedelta(days=30), "end": yesterday},
        "This month": {"start": today.replace(day=1), "end": yesterday},
        "Last month": {
            "start": (today.replace(day=1) - timedelta(days=1)).replace(day=1),
            "end": today.replace(day=1) - timedelta(days=1)
        },
        "Custom time range": None
    }
    start_date, end_date, pfm_options = None, None, {}

    with st.container():
        main_cols = st.columns(3)
        with main_cols[0]:
            # Sử dụng st.session_state để lưu giá trị
            workspace_id = st.text_input("Workspace ID *", st.session_state.get(ws_key, ""), key=ws_key)
        with main_cols[1]:
            # Sử dụng st.session_state để lưu giá trị
            storefront_input = st.text_input("Storefront EID *", st.session_state.get(sf_key, ""), key=sf_key)
            if len(storefront_input.split(',')) > 1:
                st.info("💡 Pro-tip: For faster performance, select a smaller date range.")
        with main_cols[2]:
            selected_option = st.selectbox(
                "Select time range *", options=list(date_options.keys()), index=0, key=f"date_preset_{source_key}"
            )

        if selected_option == "Custom time range":
            custom_date_cols = st.columns(2)
            with custom_date_cols[0]:
                start_date = st.date_input("Start Date", value=yesterday, max_value=yesterday, key=f"start_date_{source_key}")
            with custom_date_cols[1]:
                end_date = st.date_input("End Date", value=yesterday, max_value=yesterday, key=f"end_date_{source_key}")
        else:
            dates = date_options[selected_option]
            start_date, end_date = dates["start"], dates["end"]
        
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
    if st.session_state.stage == 'loading_preview':
        start_time = time.time()
        with st.spinner("Loading preview (500 rows)..."):
            # Chỉ tải 500 dòng để xem trước
            df_preview = load_data(st.session_state.params.get('data_source'), limit=500)
            if df_preview is not None:
                st.session_state.df_preview = df_preview
                st.session_state.stage = 'loaded'
            else:
                st.session_state.stage = 'initial'
        end_time = time.time()
        st.session_state.query_duration = end_time - start_time
        st.rerun()

    elif st.session_state.stage == 'loaded':
        df_preview = st.session_state.get('df_preview')
        if df_preview is not None and not df_preview.empty:
            st.success("✅ Preview loaded successfully!")
            
            # --- PHẦN TÓM TẮT ---
            total_rows_estimated = st.session_state.params.get('num_row', 0)
            num_storefronts = len(st.session_state.params.get('storefront_ids', []))
            start_date, end_date = datetime.strptime(st.session_state.params['start_date'], '%Y-%m-%d'), datetime.strptime(st.session_state.params['end_date'], '%Y-%m-%d')
            total_days = (end_date - start_date).days + 1
            query_duration = st.session_state.get('query_duration', 0)

            with st.expander("📊 **Export Summary**", expanded=True):
                cols = st.columns(4)
                cols[0].metric("Total Rows (Estimated)", f"{total_rows_estimated:,}")
                cols[1].metric("Date Range", f"{total_days} days")
                cols[2].metric("Storefronts", num_storefronts)
                cols[3].metric("Preview Query Time", f"{query_duration:.2f} s")
            
            # --- NÚT EXPORT FULL DATA ---
            if st.button("🚀 Export Full Data", use_container_width=True, type="primary"):
                st.session_state.stage = 'exporting_full'
                st.rerun()

            st.subheader("Preview data (first 500 rows)")
            st.data_editor(df_preview, use_container_width=True, height=300)

            # --- NÚT RESET ---
            if st.button("🔄 Start New Export", use_container_width=True):
                # Xóa các session state liên quan
                for key in list(st.session_state.keys()):
                    if key.startswith('ws_id_') or key.startswith('sf_id_'):
                        del st.session_state[key]
                st.session_state.stage = 'initial'
                st.session_state.df_preview = None
                st.session_state.params = {}
                st.rerun()
        else:
            st.warning("No data to display.")
            st.session_state.stage = 'initial'
    
    elif st.session_state.stage == 'exporting_full':
        with st.spinner("Exporting full data, please wait..."):
            full_df = load_data(st.session_state.params.get('data_source')) # Tải toàn bộ dữ liệu
            if full_df is not None:
                csv_data = convert_df_to_csv(full_df)
                file_name = f"{st.session_state.params.get('data_source')}_data_{datetime.now().strftime('%Y%m%d')}.csv"
                # Hiển thị nút download khi đã sẵn sàng
                st.session_state.download_info = {"data": csv_data, "file_name": file_name}
                st.session_state.stage = 'download_ready'
                st.rerun()

    elif st.session_state.stage == 'download_ready':
        st.success("✅ Your full data export is ready to download!")
        info = st.session_state.download_info
        st.download_button(
           label="📥 Download Now",
           data=info['data'],
           file_name=info['file_name'],
           mime='text/csv',
           use_container_width=True,
           type="primary"
        )
        if st.button("🔄 Start New Export", use_container_width=True):
            st.session_state.stage = 'initial'
            st.session_state.df_preview = None
            st.session_state.params = {}
            st.rerun()