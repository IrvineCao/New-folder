import streamlit as st
from datetime import datetime, timedelta # <-- Sửa lỗi ở dòng này
from utils.logic import load_data, convert_df_to_csv
from utils.activity_logger import log_activity
import time

def create_input_form(source_key: str, show_kw_pfm_options: bool = False):
    """
    Tạo form nhập liệu chuẩn, lưu lại lựa chọn của người dùng.
    """
    ws_key = f"ws_id_{source_key}"
    sf_key = f"sf_id_{source_key}"
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1) # <-- Lỗi xảy ra ở đây
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
            workspace_id = st.text_input("Workspace ID *", st.session_state.get(ws_key, ""), key=ws_key)
        with main_cols[1]:
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
    """
    Hiển thị toàn bộ luồng xử lý dữ liệu từ preview đến download,
    bao gồm cả việc ghi lại các hành động.
    """
    
    # Giai đoạn 1: Tải preview (500 dòng)
    if st.session_state.stage == 'loading_preview':
        start_time = time.time()
        with st.spinner("Loading preview (500 rows)..."):
            df_preview = load_data(st.session_state.params.get('data_source'), limit=500)
            if df_preview is not None and not df_preview.empty:
                st.session_state.df_preview = df_preview
                st.session_state.stage = 'loaded'
            else:
                # Ghi lại hành động không tìm thấy dữ liệu
                log_activity(action="PREVIEW_DATA_NOT_FOUND", details=st.session_state.params)
                st.warning("No data found for the selected criteria.")
                st.session_state.stage = 'initial'
        st.session_state.query_duration = time.time() - start_time
        st.rerun()
    
    # Giai đoạn 2: Hiển thị preview và các tùy chọn
    elif st.session_state.stage == 'loaded':
        df_preview = st.session_state.get('df_preview')
        if df_preview is None:
            st.session_state.stage = 'initial'
            st.rerun()

        st.success("✅ Preview loaded successfully!")
        
        # --- PHẦN TÓM TẮT ---
        total_rows_estimated = st.session_state.params.get('num_row', 0)
        num_storefronts = len(st.session_state.params.get('storefront_ids', []))
        start_date_obj = datetime.strptime(st.session_state.params['start_date'], '%Y-%m-%d')
        end_date_obj = datetime.strptime(st.session_state.params['end_date'], '%Y-%m-%d')
        total_days = (end_date_obj - start_date_obj).days + 1
        query_duration = st.session_state.get('query_duration', 0)

        with st.expander("📊 **Export Summary**", expanded=True):
            cols = st.columns(4)
            cols[0].metric("Total Rows (Estimated)", f"{total_rows_estimated:,}")
            cols[1].metric("Date Range", f"{total_days} days")
            cols[2].metric("Storefronts", num_storefronts)
            cols[3].metric("Preview Query Time", f"{query_duration:.2f} s")
            
        cols_action = st.columns(2)
        with cols_action[0]:
            if st.button("🚀 Export Full Data", use_container_width=True, type="primary"):
                # Ghi lại hành động nhấn nút export
                log_activity(
                    action="EXPORT_FULL_DATA_CLICK",
                    details={"data_source": st.session_state.params.get('data_source')}
                )
                st.session_state.stage = 'exporting_full'
                st.rerun()
        with cols_action[1]:
            if st.button("🔄 Start New Export", use_container_width=True):
                # Ghi lại hành động reset
                log_activity(action="START_NEW_EXPORT")
                st.session_state.stage = 'initial'
                st.session_state.df_preview = None
                st.session_state.params = {}
                st.rerun()

        st.subheader("Preview data (first 500 rows)")
        st.data_editor(df_preview, use_container_width=True, height=300)

    # Giai đoạn 3: Tải toàn bộ dữ liệu
    elif st.session_state.stage == 'exporting_full':
        with st.spinner("Exporting full data, this may take a while..."):
            full_df = load_data(st.session_state.params.get('data_source')) # Không có limit
            if full_df is not None:
                # Ghi lại hành động export thành công
                log_activity(
                    action="EXPORT_FULL_DATA_SUCCESS",
                    details={
                        "data_source": st.session_state.params.get('data_source'),
                        "rows_exported": len(full_df)
                    }
                )
                csv_data = convert_df_to_csv(full_df)
                file_name = f"{st.session_state.params.get('data_source')}_data_{datetime.now().strftime('%Y%m%d')}.csv"
                st.session_state.download_info = {"data": csv_data, "file_name": file_name}
                st.session_state.stage = 'download_ready'
                st.rerun()

    # Giai đoạn 4: Sẵn sàng tải xuống
    elif st.session_state.stage == 'download_ready':
        st.success("✅ Your full data export is ready to download!")
        info = st.session_state.download_info
        st.download_button(
           label="📥 Download CSV Now",
           data=info['data'],
           file_name=info['file_name'],
           mime='text/csv',
           use_container_width=True,
           type="primary",
           # Ghi lại hành động khi nhấn nút download
           on_click=log_activity,
           kwargs={"action": "DOWNLOAD_CSV_CLICK", "details": {"file_name": info['file_name']}}
        )
        if st.button("🔄 Start New Export", use_container_width=True):
            log_activity(action="START_NEW_EXPORT")
            st.session_state.stage = 'initial'
            st.rerun()
