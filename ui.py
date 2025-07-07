import streamlit as st
from datetime import datetime, timedelta
from logic import handle_export_process, load_and_store_data, convert_df_to_csv

def create_input_form(source_key: str):
    """Creates a standardized input form and returns the values."""
    # Define the date range for the selection
    today = datetime.now().date()
    thirty_days_ago = today - timedelta(days=30)
    yesterday = today - timedelta(days=1)  # Always use yesterday for end_date

    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            workspace_id = st.text_input(
                "Workspace ID *", "",
                help="Enter the workspace ID (numeric)",
                key=f"ws_id_{source_key}"
            )
        with col2:
            storefront_input = st.text_input(
                "Storefront EID *", "",
                help="Enter one or more storefront IDs, comma-separated (max 5)",
                key=f"sf_id_{source_key}"
            )
        with col3:
            start_date = st.date_input(
                "Start Date *",
                value=thirty_days_ago,  # Default to 30 days ago
                min_value=thirty_days_ago,  # Min value: 30 days ago
                max_value=yesterday,  # Max value: yesterday
                key=f"start_date_{source_key}"
            )
        with col4:
            end_date = st.date_input(
                "End Date *",
                value=yesterday,  # Always set to yesterday
                min_value=thirty_days_ago,  # Min value: 30 days ago
                max_value=yesterday,  # Max value: yesterday only
                key=f"end_date_{source_key}"
            )
    
    st.write("---")
    return workspace_id, storefront_input, start_date, end_date



def display_main_ui():
    """Displays the main UI of the application."""
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio('Go to', ['Keyword Lab', 'Digital Shelf Analytics', 'Please Read Im Begging You'])

    # Keyword Lab Page
    if page == 'Keyword Lab':
        st.title("Keyword Level Data Export")
        workspace_id, storefront_input, start_date, end_date = create_input_form('kwl')

        if st.button("Get Data", type="primary", use_container_width=True, key='get_data_kwl'):
            handle_get_data_button(workspace_id, storefront_input, start_date, end_date, 'kwl')

    # Digital Shelf Analytics Page
    elif page == 'Digital Shelf Analytics':
        tab1, tab2 = st.tabs(["Keyword Performance", "Product Tracking"])

        # Keyword Performance Tab
        with tab1:
            st.title("Keyword Performance Data Export")
            workspace_id, storefront_input, start_date, end_date = create_input_form('kw_pfm')
            if st.button("Get Data", type="primary", use_container_width=True, key='get_data_kw_pfm'):
                handle_get_data_button(workspace_id, storefront_input, start_date, end_date, 'kw_pfm')

        # Product Tracking Tab
        with tab2:
            st.title("Product Tracking Data Export")
            workspace_id, storefront_input, start_date, end_date = create_input_form('pt')
            if st.button("Get Data", type="primary", use_container_width=True, key='get_data_pt'):
                handle_get_data_button(workspace_id, storefront_input, start_date, end_date, 'pt')

    # Note Page
    elif page == 'Please Read Im Begging You':
        with open("help.md", "r", encoding="utf-8") as f:
            about = f.read()
        st.markdown(about) 

    # Centralized State Handling for Data Display
    if st.session_state.stage == 'waiting_confirmation':
        num_row = st.session_state.params.get('num_row', 'many')
        st.warning(f"⚠️ Large dataset: {num_row:,} rows found. This may take a while to load.")
        
        with st.container():
            proceed = st.checkbox("I understand and want to proceed", key="proceed_box")
            if st.button("Confirm", key="confirm_button"):
                if proceed:
                    st.session_state.stage = 'loading'
                    st.rerun()
                else:
                    st.error("Please check the box to proceed.")

    elif st.session_state.stage == 'loading':
        load_and_store_data(st.session_state.params.get('data_source'))
        st.rerun() # Rerun to reflect the new 'loaded' state

    elif st.session_state.stage == 'loaded':
        # Check if the current page corresponds to the loaded data
        data_source = st.session_state.params.get('data_source')
        page_matches_data = (
            (page == 'Keyword Lab' and data_source == 'kwl') or
            (page == 'Digital Shelf Analytics' and data_source in ['kw_pfm', 'pt'])
        )

        if page_matches_data:
            df = st.session_state.df
            st.success(f"✅ Successfully loaded {len(df):,} rows")

            # Prepare data for download
            csv_data = convert_df_to_csv(df)
            file_name = f"{st.session_state.params.get('data_source', 'export')}_data_{datetime.now().strftime('%Y%m%d')}.csv"

            st.download_button(
               label="Export Full Data as CSV",
               data=csv_data,
               file_name=file_name,
               mime='text/csv',
               use_container_width=True,
               type="primary"
            )

            st.subheader("Data Preview (First 500 Rows)")
            st.data_editor(df.head(500), use_container_width=True, height=300)



def handle_get_data_button(workspace_id, storefront_input, start_date, end_date, data_source):
    """Handles the logic when 'Get Data' is clicked."""
    st.session_state.stage = 'initial'
    st.session_state.params = {}
    stage, params = handle_export_process(
        workspace_id,
        storefront_input,
        start_date,
        end_date,
        data_source=data_source
    )
    st.session_state.stage = stage
    st.session_state.params = params
    st.rerun()
