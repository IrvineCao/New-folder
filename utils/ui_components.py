import streamlit as st
from datetime import datetime, timedelta
from utils.logic import load_data, convert_df_to_csv
import time

# --- Create input form + save user selections ---
def create_input_form(source_key: str, show_kw_pfm_options: bool = False, required_inputs: list = None):
    """
    Create a standard input form and save the user's selections.
    """
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

    workspace_id, storefront_input, start_date, end_date = None, None, None, None

    if required_inputs is None:
        required_inputs = ['workspace_id', 'storefront_id', 'date_range']

    with st.container():
        main_cols = st.columns(3)
        if 'workspace_id' in required_inputs:
            with main_cols[0]:
                workspace_id = st.text_input("Workspace ID *", st.session_state.get(ws_key, ""), key=ws_key)
        if 'storefront_id' in required_inputs:
            with main_cols[1]:
                storefront_input = st.text_input("Storefront EID *", st.session_state.get(sf_key, ""), key=sf_key)
                if storefront_input and len(storefront_input.split(',')) > 1:
                    st.info("💡 Pro-tip: For faster performance, select a smaller date range.")
        if 'date_range' in required_inputs:
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
                pfm_options['device_type'] = st.selectbox("Device Type", ('Mobile', 'Desktop','None'), key=f'device_type_{source_key}')
            with extra_cols[1]:
                pfm_options['display_type'] = st.selectbox("Display Type", ('Paid', 'Organic','Top','None'), key=f'display_type_{source_key}')
            with extra_cols[2]:
                pfm_options['product_position'] = st.selectbox("Product Position", ('-1','4','10','None'), key=f'product_pos_{source_key}')

    st.write("---")
    return workspace_id, storefront_input, start_date, end_date, pfm_options


# --- Display the entire data processing flow from preview to download ---
def display_data_exporter():
    """
    Display the entire data processing flow from preview to download.
    """
    
    # Stage 1: Load preview
    if st.session_state.stage == 'loading_preview':
        start_time = time.time()
        with st.spinner("Loading preview (500 rows)..."):
            df_preview = load_data(st.session_state.params.get('data_source'), limit=500)
            if df_preview is not None and not df_preview.empty:
                st.session_state.df_preview = df_preview
                st.session_state.stage = 'loaded'
            else:
                st.warning("No data found for the selected criteria.")
                st.session_state.stage = 'initial'
        st.session_state.query_duration = time.time() - start_time
        st.rerun()
    
    # Stage 2: Display results
    elif st.session_state.stage == 'loaded':
        df_preview = st.session_state.get('df_preview')
        if df_preview is None:
            st.session_state.stage = 'initial'
            st.rerun()

        st.success("✅ Preview loaded successfully!")
        
        with st.expander("**Summary (from Preview)**", expanded=True):
            params = st.session_state.get('params', {})
            total_rows_estimated = params.get('num_row', 0)
            num_storefronts = len(params.get('storefront_ids') or [])
            start_date_str = params.get('start_date')
            end_date_str = params.get('end_date')
            
            if start_date_str and end_date_str:
                start_date_obj = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date_obj = datetime.strptime(end_date_str, '%Y-%m-%d')
                total_days = (end_date_obj - start_date_obj).days + 1
                date_range_display = f"{total_days} days"
            else:
                date_range_display = "N/A"
            query_duration = st.session_state.get('query_duration', 0)

            cols = st.columns(5)
            cols[0].metric("Total Rows (Estimated)", f"{total_rows_estimated:,}")
            cols[1].metric("Total Columns", len(df_preview.columns))
            cols[2].metric("Date Range", date_range_display)
            cols[3].metric("Storefronts", num_storefronts)
            cols[4].metric("Preview Query Time", f"{query_duration:.2f} s")
            
        st.markdown("---")
        # --- Action buttons ---
        cols_action = st.columns(2)
        with cols_action[0]:
            if st.button("🚀 Export Full Data", use_container_width=True, type="primary"):
                st.session_state.stage = 'exporting_full'
                st.rerun()
        with cols_action[1]:
            if st.button("🔄 Start New Export", use_container_width=True):
                st.session_state.stage = 'initial'
                st.session_state.df_preview = None
                st.session_state.params = {}
                st.rerun()

        st.subheader("Preview data (first 500 rows)")
        st.data_editor(df_preview, use_container_width=True, height=300)

    # Stage 3: Export full data
    elif st.session_state.stage == 'exporting_full':
        with st.spinner("Exporting full data, this may take a while..."):
            full_df = load_data(st.session_state.params.get('data_source'))
            if full_df is not None:
                csv_data = convert_df_to_csv(full_df)
                file_name = f"{st.session_state.params.get('data_source')}_data_{datetime.now().strftime('%Y%m%d')}.csv"
                st.session_state.download_info = {"data": csv_data, "file_name": file_name}
                st.session_state.stage = 'download_ready'
                st.rerun()

    # Stage 4: Download
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
        )
        if st.button("🔄 Start New Export", use_container_width=True):
            st.session_state.stage = 'initial'
            st.rerun()
