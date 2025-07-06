import streamlit as st
from datetime import datetime, timedelta
from logic import handle_export_process, load_data_and_display

def create_input_form(source_key: str):
    """Creates a standardized input form and returns the values."""
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
                help="Enter one or more storefront IDs, comma-separated",
                key=f"sf_id_{source_key}"
            )
        with col3:
            start_date = st.date_input(
                "Start Date *",
                value=datetime.now() - timedelta(days=30),
                max_value=datetime.now().date() - timedelta(days=1),
                key=f"start_date_{source_key}"
            )
        with col4:
            end_date = st.date_input(
                "End Date *",
                value=datetime.now().date() - timedelta(days=1),
                max_value=datetime.now().date() - timedelta(days=1),
                key=f"end_date_{source_key}"
            )
    st.write("---")
    return workspace_id, storefront_input, start_date, end_date

def display_main_ui():
    """Displays the main UI of the application."""
    st.sidebar.title("Navigation")
    page = st.sidebar.radio('Go to', ['KWL', 'DSA'])

    if page == 'KWL':
        st.title("Keyword Level Data Export")
        with st.expander("Help"):
            st.write("Please fill in all required fields and click 'Get Data' to begin.")

        workspace_id, storefront_input, start_date, end_date = create_input_form('kwl')

        if st.button("Get Data", type="primary", use_container_width=True, key='get_data_kwl'):
            handle_get_data_button(workspace_id, storefront_input, start_date, end_date, 'kwl')

    elif page == 'DSA':
        tab1, tab2 = st.tabs(["Keyword Performance", "Product Tracking"])

        with tab1:
            st.title("Keyword Performance Data Export")
            workspace_id, storefront_input, start_date, end_date = create_input_form('dsa')
            if st.button("Get Data", type="primary", use_container_width=True, key='get_data_dsa'):
                handle_get_data_button(workspace_id, storefront_input, start_date, end_date, 'dsa')

        with tab2:
            st.title("Product Tracking Data Export")
            workspace_id, storefront_input, start_date, end_date = create_input_form('pt')
            if st.button("Get Data", type="primary", use_container_width=True, key='get_data_pt'):
                handle_get_data_button(workspace_id, storefront_input, start_date, end_date, 'pt')

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
        load_data_and_display(st.session_state.params.get('data_source'))

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
