import streamlit as st
import pandas as pd
from io import StringIO
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy import text
from utils.database import get_connection
from utils.helpers import trace_function_call
import importlib
from utils.input_config import DATA_SOURCE_CONFIGS


def get_query_by_source(data_source: str):
    """Dynamically import and return the get_query function based on the data source config."""
    config = DATA_SOURCE_CONFIGS.get(data_source)
    if not config or 'data_logic_module' not in config:
        raise ValueError(f"Unknown or misconfigured data source: {data_source}")

    module_name = config['data_logic_module']
    try:
        # Dynamically import the data logic module
        data_logic_module = importlib.import_module(f"data_logic.{module_name}")
        # Return the get_query function from the imported module
        return getattr(data_logic_module, 'get_query')
    except (ImportError, AttributeError) as e:
        raise ImportError(f"Could not import or find 'get_query' in module 'data_logic.{module_name}': {e}")


@st.cache_data(show_spinner=False, ttl=3600, persist=True)
def _execute_query(query: str, params_to_bind: dict) -> pd.DataFrame:
    print("--- DEBUG: EXECUTING QUERY ---")
    print(f"Query: {query}")
    print(f"Params: {params_to_bind}")
    print("-----------------------------")
    with get_connection() as db:
        return pd.read_sql(text(query), db.connection(), params=params_to_bind)


@trace_function_call
@st.cache_data(show_spinner=False, ttl=3600, persist=True)
def get_data(query_type: str, data_source: str, limit: int = None, **kwargs):
    """
    Fetches data from the DB.
    """
    get_query_func = get_query_by_source(data_source)
    base_query_str = get_query_func(query_type)
    
    params_to_bind = kwargs.copy()

    # SQLAlchemy's text() construct doesn't natively support expanding a list for an IN clause when used with pandas.read_sql.
    # To work around this, we safely format the list of integer IDs directly into the SQL string.
    # This is safe from SQL injection because we explicitly cast all IDs to integers first.
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



@trace_function_call
def load_data(data_source: str, limit: int = None):
    """Load data based on parameters in the session state."""
    try:
        params = st.session_state.get('params', {}).copy()
        if not params:
            return None

        # Parameters are already built, just remove non-SQL keys
        params.pop('data_source', None)
        params.pop('current_page', None)  # Remove page info but keep data_source in session
        params.pop('num_row', None)  # Remove row count info
        sql_params = params

        df = get_data("data", data_source, limit=limit, **sql_params)
        st.session_state.df = df
        return df
    except Exception as e:
        st.error(f"An error occurred while loading data: {str(e)}")
        return None


@trace_function_call
def get_row_count(data_source: str, **kwargs) -> int:
    """Get the total row count."""
    try:
        params = kwargs.copy()
        if not params:
            return None

        # Parameters are already built, just remove non-SQL keys
        params.pop('data_source', None)
        params.pop('current_page', None)  # Remove page info but keep data_source in session
        params.pop('num_row', None)  # Remove row count info
        sql_params = params

        # Get total row count
        num_row_df = get_data('count', data_source, **sql_params)
        num_row = num_row_df.iloc[0, 0] if not num_row_df.empty else 0
        return num_row
    except Exception as e:
        st.error(f"An error occurred while getting row count: {str(e)}")
        return None


@trace_function_call
def handle_export_process(data_source: str):
    """Handle the entire process: row counting, and status updates."""
    # `st.session_state.params` is now set by the caller (`create_action_buttons`)
    params = st.session_state.get('params', {}).copy()

    # Keep the data_source in params for tab state management
    # but remove other non-SQL keys for the database query
    current_page = params.pop('current_page', None)
    params.pop('data_source', None)
    sql_params = params

    try:
        with st.spinner("Checking data size..."):
            # Get total row count
            num_row = get_row_count(data_source, **sql_params)
            if num_row is None: # Handle case where get_row_count fails
                st.session_state.user_message = {
                    "type": "error",
                    "text": "Failed to check data size. Please try again."
                }
                st.session_state.stage = 'initial'
                return
            
            # Re-add the data_source to params so it's preserved for tab state
            st.session_state.params['num_row'] = num_row
            # Keep data_source in params for tab state management
            st.session_state.params['data_source'] = data_source
            if current_page:
                st.session_state.params['current_page'] = current_page

        # --- Handle user messages and warnings ---
        if num_row == 0:
            st.session_state.user_message = {
                "type": "warning",
                "text": "No data found for the selected criteria."
            }
            st.session_state.stage = 'initial'
            return
            
        elif int(num_row) > 50000:
            st.session_state.user_message = {
                "type": "error",
                "text": f"Data is too large to export ({num_row:,} rows). Please narrow your selection to under 50,000 rows."
            }
            st.session_state.stage = 'blocked'  # Set to blocked state instead of initial
            return
        else:
            # Data size is acceptable, proceed with loading preview
            st.session_state.stage = 'loading_preview'

    except OperationalError as e:
        st.session_state.user_message = {
            "type": "error",
            "text": "❌ Database Connection Error. Please try again later."
        }
        st.session_state.stage = 'initial'
    except ProgrammingError as e:
        st.session_state.user_message = {
            "type": "error", 
            "text": "❌ An error occurred with the data query. Please check your inputs."
        }
        st.session_state.stage = 'initial'
    except Exception as e:
        st.session_state.user_message = {
            "type": "error",
            "text": f"❌ An unexpected error occurred: {str(e)}"
        }
        st.session_state.stage = 'initial'


def convert_df_to_csv(df: pd.DataFrame):
    output = StringIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    return output.getvalue()