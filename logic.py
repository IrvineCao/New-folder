import streamlit as st
import pandas as pd
from io import StringIO
from kwl_data import get_query as get_kwl_query
from kw_pfm_data import get_query as get_kw_pfm_query
from product_tracking_data import get_query as get_pt_query
from sqlalchemy import text
from database import get_connection

# Helper function to select the correct get_query function
def get_query_by_source(data_source: str):
    """
    Returns the appropriate get_query function based on the data source.
    """
    if data_source == 'kwl':
        return get_kwl_query
    elif data_source == 'kw_pfm':
        return get_kw_pfm_query
    elif data_source == 'pt':
        return get_pt_query
    else:
        raise ValueError(f"Unknown data source: {data_source}")


def validate_inputs(workspace_id, storefront_input, start_date, end_date):
    """Validates the user inputs from the Streamlit UI."""
    errors = []
    workspace_id = [s.strip().isdigit() for s in workspace_id.split(",") if s.strip()]
    if not workspace_id:
        errors.append("Workspace ID is required")
    elif len(workspace_id) > 1:
        errors.append("You can only enter one workspace ID.")
    elif not all(workspace_id):
        errors.append("Workspace ID must be numeric.")

    storefront_input = [s.strip().isdigit() for s in storefront_input.split(",") if s.strip()]
    if not storefront_input:
        errors.append("Storefront EID is required")
    elif len(storefront_input) > 5:
        errors.append("You can only enter up to 5 storefront IDs.")
    elif not all(storefront_input):
        errors.append("Storefront EID must be numeric.")

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
def get_data(query_type: str, data_source: str, **kwargs):
    """
    Get data based on the specified query type using SQLAlchemy session.
    """
    get_query_func = get_query_by_source(data_source)
    query = get_query_func(query_type)

    # Prepare parameters for the SQL query from kwargs
    params = {
        'workspace_id': kwargs.get('workspace_id'),
        'storefront_ids': tuple(kwargs.get('storefront_id', [])),
        'start_date': kwargs.get('start_date'),
        'end_date': kwargs.get('end_date')
    }

    # Add extra parameters for kw_pfm data source
    if data_source == 'kw_pfm':
        params['device_type'] = kwargs.get('device_type')
        params['display_type'] = kwargs.get('display_type')
        params['product_position'] = kwargs.get('product_position')

    with get_connection() as db:
        # Use text() to enable named parameters and safely pass them to the database.
        return pd.read_sql(text(query), db.connection(), params=params)


def handle_export_process(workspace_id, storefront_input, start_date, end_date, data_source: str, **kwargs):
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
    st.session_state.params.update(kwargs)
    
    # Prepare parameters for get_data, including extra ones for kw_pfm
    get_data_params = {
        'workspace_id': st.session_state.params['workspace_id'],
        'storefront_id': tuple(st.session_state.params['storefront_ids']),
        'start_date': st.session_state.params['start_date_str'],
        'end_date': st.session_state.params['end_date_str'],
        'query_type': "count",
        'data_source': data_source
    }
    if data_source == 'kw_pfm':
        get_data_params['device_type'] = st.session_state.params.get('device_type')
        get_data_params['display_type'] = st.session_state.params.get('display_type')
        get_data_params['product_position'] = st.session_state.params.get('product_position')

    try:
        with st.spinner("Checking data size..."):
            num_row_df = get_data(**get_data_params)
            num_row = num_row_df.iloc[0, 0]
            st.session_state.params['num_row'] = num_row

        if num_row == 0:
            st.warning("No data found for the selected criteria.")
            st.session_state.stage = 'initial'
        elif 10000 < num_row <= 50000:
            st.session_state.stage = 'waiting_confirmation'
        elif num_row > 50000:
            st.error(f"Data is too large to export ({num_row:,} rows). Please narrow your date range or storefronts.")
            st.session_state.stage = 'initial'
        else:
            st.session_state.stage = 'loading'

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.session_state.stage = 'initial'

    return st.session_state.stage, st.session_state.params


def load_and_store_data(data_source: str):
    """Load data and store it in the session state."""
    try:
        with st.spinner("Loading data..."):
            params = st.session_state.params

            # Prepare parameters for get_data, including extra ones for kw_pfm
            get_data_params = {
                'workspace_id': params['workspace_id'],
                'storefront_id': tuple(params['storefront_ids']),
                'start_date': params['start_date_str'],
                'end_date': params['end_date_str'],
                'query_type': "data",
                'data_source': data_source
            }
            if data_source == 'kw_pfm':
                get_data_params['device_type'] = params.get('device_type')
                get_data_params['display_type'] = params.get('display_type')
                get_data_params['product_position'] = params.get('product_position')

            df = get_data(**get_data_params)
            st.session_state.df = df
            st.session_state.stage = 'loaded'
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        st.session_state.stage = 'initial'


def convert_df_to_csv(df: pd.DataFrame):
    """Convert a DataFrame to a CSV string for downloading."""
    output = StringIO()
    df.to_csv(output, index=False, encoding='utf-8')
    return output.getvalue()
