import streamlit as st
import pandas as pd
from io import StringIO
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, ProgrammingError
from utils.database import get_connection
from data_logic import kwl_data, kw_pfm_data, product_tracking_data, sf_data


def get_query_by_source(data_source: str):
    """Return the appropriate get_query function based on the data source."""
    query_map = {
        'kwl': kwl_data.get_query,
        'kw_pfm': kw_pfm_data.get_query,
        'pt': product_tracking_data.get_query,
        'sf': sf_data.get_query,
    }
    if data_source in query_map:
        return query_map[data_source]
    raise ValueError(f"Unknown data source: {data_source}")


@st.cache_data(show_spinner=False, ttl=3600, persist=True)
def get_data(query_type: str, data_source: str, limit: int = None, **kwargs):
    """
    Fetches data from the DB.
    """
    get_query_func = get_query_by_source(data_source)
    base_query_str = get_query_func(query_type)
    
    params_to_bind = kwargs.copy()

    # Handle the IN clause for storefront_ids by formatting directly into the string
    if 'storefront_ids' in params_to_bind and isinstance(params_to_bind['storefront_ids'], (list, tuple)) and ':storefront_ids' in base_query_str:
        storefront_ids = params_to_bind['storefront_ids']
        
        safe_ids = [int(sid) for sid in storefront_ids]
        
        if len(safe_ids) == 1:
            ids_string = f"({safe_ids[0]})"
        else:
            ids_string = str(tuple(safe_ids))

        base_query_str = base_query_str.replace(':storefront_ids', ids_string)
        
        del params_to_bind['storefront_ids']    
    elif 'storefront_ids' in params_to_bind:
        # Clean up storefront_ids if they are not needed in the query to avoid sending them to the DB driver
        del params_to_bind['storefront_ids']

    if limit is not None and query_type == 'data':
        final_query_str = f"{base_query_str} LIMIT {limit}"
    else:
        final_query_str = base_query_str
    
    query = text(final_query_str)
    
    with get_connection() as db:
        return pd.read_sql(query, db.connection(), params=params_to_bind)

def build_params_for_query(data_source: str, source_params: dict):
    """Build parameters for the SQL query."""
    params_map = {
        "workspace_id": source_params.get("workspace_id"),
        "storefront_ids": source_params.get("storefront_ids"),
        "start_date": source_params.get("start_date"),
        "end_date": source_params.get("end_date"),
    }

    # Filter out None values to only include necessary parameters
    required_params = {k: v for k, v in params_map.items() if v is not None}

    if data_source == 'kw_pfm':
        device_type = source_params.get("device_type")
        if device_type != 'None':
            required_params["device_type"] = device_type

        display_type = source_params.get("display_type")
        if display_type != 'None':
            required_params["display_type"] = display_type

        product_position = source_params.get("product_position")
        if product_position != 'None':
            required_params["product_position"] = product_position
        
    return required_params

def load_data(data_source: str, limit: int = None):
    """Load data based on parameters in the session state."""
    
    try:
        params_for_load = build_params_for_query(data_source, st.session_state.get('params', {}))

        df = get_data(
            query_type='data', 
            data_source=data_source, 
            limit=limit, 
            **params_for_load
        )
        return df
    except Exception:
        st.error("An error occurred while loading data.")
        return None


def handle_export_process(workspace_id, storefront_input, start_date, end_date, data_source: str, **kwargs):
    """Handle the entire process: validation, row counting, and status updates."""
    required_inputs = kwargs.get('required_inputs', [])
    errors = validate_inputs(workspace_id, storefront_input, start_date, end_date, required_inputs)
    if errors:
        for error in errors:
            st.error(error)
        st.stop()
    
    def process_storefront_input(storefront_input):
        try:
            return [int(eid.strip()) for eid in storefront_input.split(',')]
        except (ValueError, AttributeError):
            return None
    
    st.session_state.params = {
        "workspace_id": int(workspace_id) if workspace_id else None,
        "storefront_ids": process_storefront_input(storefront_input),
        "start_date": start_date.strftime('%Y-%m-%d') if start_date else None,
        "end_date": end_date.strftime('%Y-%m-%d') if end_date else None,
        "data_source": data_source,
        **kwargs
    }

    try:
        with st.spinner("Checking data size..."):
            params_for_count = build_params_for_query(data_source, st.session_state.params)
            num_row_df = get_data('count', data_source, **params_for_count)
            num_row = num_row_df.iloc[0, 0] if not num_row_df.empty else 0
            st.session_state.params['num_row'] = num_row

        # --- Handle user messages and warnings ---
        if num_row == 0:
            st.session_state.user_message = {
                "type": "warning",
                "text": "No data found for the selected criteria."
            }
            st.session_state.stage = 'initial'
        elif num_row > 50000:
            st.session_state.user_message = {
                "type": "error",
                "text": f"Data is too large to export ({num_row:,} rows). Please narrow your selection."
            }
            st.session_state.stage = 'initial'
        else:
            st.session_state.stage = 'loading_preview'

    except OperationalError:
        st.error("❌ Database Connection Error.")
        st.session_state.stage = 'initial'
    except ProgrammingError:
        st.error("❌ An error occurred with the data query.")
        st.session_state.stage = 'initial'
    except Exception:
        st.error("❌ An unexpected error occurred.")
        st.session_state.stage = 'initial'


def handle_get_data_button(workspace_id, storefront_input, start_date, end_date, data_source, **kwargs):
    """Handler for the 'Get Data' button click event."""
    # Clear old messages before starting a new action
    st.session_state.user_message = None

    if st.session_state.params.get('data_source') != data_source:
        st.session_state.stage = 'initial'
        st.session_state.params = {}
        st.session_state.df_preview = None

    handle_export_process(
        workspace_id,
        storefront_input,
        start_date,
        end_date,
        data_source=data_source,
        **kwargs
    )
    st.rerun()


def validate_inputs(workspace_id, storefront_input, start_date, end_date, required_inputs):
    errors = []
    if 'workspace_id' in required_inputs and not workspace_id:
        errors.append("Workspace ID is required")
    elif workspace_id:
        workspace_id_list = [s.strip() for s in workspace_id.split(",") if s.strip()]
        if not workspace_id_list:
            errors.append("Workspace ID is required")
        elif len(workspace_id_list) > 1:
            errors.append("You can only enter one workspace ID.")
        elif not all(s.isdigit() for s in workspace_id_list):
            errors.append("Workspace ID must be numeric.")

    # Only validate storefront_input if it is provided
    if storefront_input:
        storefront_input_list = [s.strip() for s in storefront_input.split(",") if s.strip()]
        if 'storefront_ids' in required_inputs and not storefront_input_list:
            errors.append("Storefront EID is required")
        elif len(storefront_input_list) > 5:
            errors.append("You can only enter up to 5 storefront IDs.")
        elif not all(s.isdigit() for s in storefront_input_list):
            errors.append("Storefront EID must be numeric.")
        
        num_storefronts = len(storefront_input_list)
        if 'date_range' in required_inputs and start_date and end_date:
            date_range_days = (end_date - start_date).days
            max_days_allowed = 60

            if num_storefronts > 1 and num_storefronts <= 2:
                max_days_allowed = 60
            elif num_storefronts > 2:
                max_days_allowed = 30

            if date_range_days > max_days_allowed:
                errors.append(
                    f"With {num_storefronts} storefront(s), the maximum allowed period is {max_days_allowed} days. "
                    f"Please select a shorter date range."
                )

    if 'date_range' in required_inputs and (not start_date or not end_date):
        errors.append("Date range is required")
    elif start_date and end_date and start_date > end_date:
        errors.append("Start date cannot be after end date.")
        
    return errors


def convert_df_to_csv(df: pd.DataFrame):
    output = StringIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    return output.getvalue()