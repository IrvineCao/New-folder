import streamlit as st
import pandas as pd
from db_connection import get_connection
from kwl_data import get_query as get_kwl_query
from kw_pfm_data import get_query as get_dsa_query
from product_tracking_data import get_query as get_pt_query

# Helper function to select the correct get_query function
def get_query_by_source(data_source: str):
    """
    Returns the appropriate get_query function based on the data source.
    """
    if data_source == 'kwl':
        return get_kwl_query
    elif data_source == 'dsa':
        return get_dsa_query
    elif data_source == 'pt':
        return get_pt_query
    else:
        raise ValueError(f"Unknown data source: {data_source}")

def validate_inputs(workspace_id, storefront_input, start_date, end_date):
    """Validates the user inputs from the Streamlit UI."""
    errors = []
    if not workspace_id:
        errors.append("Workspace ID is required.")
    elif not workspace_id.isdigit():
        errors.append("Workspace ID must be numeric.")
    if not storefront_input:
        errors.append("Storefront EID is required.")
    if start_date > end_date:
        errors.append("Start date cannot be after end date.")
    return errors

def process_storefront_input(storefront_input):
    """Processes the comma-separated storefront IDs into a list of integers."""
    try:
        return [int(eid.strip()) for eid in storefront_input.split(',')]
    except ValueError:
        return None

@st.cache_data(show_spinner=False, ttl=3600, persist=True)
def get_data(_conn, workspace_id, storefront_id, start_date, end_date, query_type: str, data_source: str):
    """
    Get data based on the specified query type.
    """
    if not isinstance(storefront_id, (list, tuple)):
        storefront_id = (storefront_id,)
    
    storefront_placeholders = ', '.join(['%s'] * len(storefront_id))
    
    get_query_func = get_query_by_source(data_source)
    query = get_query_func(query_type, storefront_placeholders)
    
    if data_source == 'kwl':
        params = (start_date, end_date) + tuple(storefront_id) + (workspace_id,) + tuple(storefront_id) + (workspace_id,)
    elif data_source == 'dsa':
        params = tuple(storefront_id) + (workspace_id,) + (start_date, end_date) + (start_date, end_date)
    elif data_source == 'pt':
        params = (start_date, end_date) + tuple(storefront_id) + (workspace_id,)
    else:
        st.error("Invalid data source specified.")
        return pd.DataFrame()

    with _conn.cursor() as cur:
        cur.execute(query, params)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        return pd.DataFrame(rows, columns=columns)

def handle_export_process(workspace_id, storefront_input, start_date, end_date, data_source: str):
    """Handle the export process with validation and data size checking."""
    errors = validate_inputs(workspace_id, storefront_input, start_date, end_date)
    if errors:
        for error in errors:
            st.error(error)
        st.stop()
    
    storefront_ids = process_storefront_input(storefront_input)
    if not storefront_ids:
        st.error("Invalid Storefront EID format")
        st.stop()
    
    st.session_state.params = {
        "workspace_id": int(workspace_id),
        "storefront_ids": storefront_ids,
        "start_date_str": start_date.strftime('%Y-%m-%d'),
        "end_date_str": end_date.strftime('%Y-%m-%d'),
        "data_source": data_source
    }
    
    try:
        with st.spinner("Checking data size..."), get_connection() as conn:
            num_row_df = get_data(
                conn, 
                st.session_state.params["workspace_id"], 
                st.session_state.params["storefront_ids"], 
                st.session_state.params["start_date_str"], 
                st.session_state.params["end_date_str"],
                "count",
                st.session_state.params["data_source"]
            )
            num_row = num_row_df.iloc[0, 0] if not num_row_df.empty else 0
            st.session_state.params['num_row'] = num_row

        if num_row == 0:
            st.warning("No data found for the selected criteria")
            st.session_state.stage = 'initial'
        elif 10000 < num_row < 50000:
            st.session_state.stage = 'waiting_confirmation'
        elif num_row >= 50000:
            st.error(f"Large dataset: {num_row:,} rows found. Please reduce the number of storefronts selected.")
            st.stop()
        else:
            st.session_state.stage = 'loading'

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.session_state.stage = 'initial'
    
    return st.session_state.stage, st.session_state.params

def load_data_and_display(data_source: str):
    """Load and display keyword data based on the current session state parameters."""
    try:
        with st.spinner("Loading data..."):
            params = st.session_state.params
            with get_connection() as conn:
                df = get_data(conn, params["workspace_id"], params["storefront_ids"], 
                           params["start_date_str"], params["end_date_str"], "data", params["data_source"])
            
            if df.empty:
                st.warning("No data returned from the query")
            else:
                st.success(f"✅ Successfully loaded {len(df)} rows")
                st.subheader("Data Preview")
                st.dataframe(df, use_container_width=True)
                
                st.session_state.stage = 'initial'

    except Exception as e:
        st.error(f"An error occurred during data load: {str(e)}")
        st.session_state.stage = 'initial'
