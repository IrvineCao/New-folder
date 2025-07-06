import streamlit as st
from db_connection import get_connection
from kwl_data import get_query
import pandas as pd

conn = get_connection()


#--------------------------------------------------#
#------------ function dung chung -----------------#
#--------------------------------------------------#
def validate_inputs(workspace_id, storefront_id, start_date, end_date, tag_input):
    """Validate all input parameters for the export process.
    
    Args:
        workspace_id (str): The workspace ID to validate
        storefront_id (str): The storefront ID(s) to validate (can be comma-separated)
        start_date (datetime.date): The start date of the date range
        end_date (datetime.date): The end date of the date range
        
    Returns:
        list: A list of error messages. Empty list means validation passed.
    """
    errors = []
    
    if not workspace_id.isdigit():
        errors.append("Workspace ID must be a number")
    if not storefront_id.replace(',', '').replace(' ', '').isdigit():
        errors.append("Storefront EID must be a number or comma-separated numbers")
    if end_date < start_date:
        errors.append("End date cannot be before start date")
    if not tag_input.replace(',', '').replace(' ', ''):
        errors.append("Tags must be a text or comma-separated text")
    
    return errors

def process_storefront_input(storefront_input):
    """Convert a comma-separated string of storefront IDs into a tuple of integers.
    
    Args:
        storefront_input (str): A string containing comma-separated storefront IDs
        
    Returns:
        tuple: A tuple of integers representing the storefront IDs, or None if conversion fails
    """
    try:
        return tuple(int(id.strip()) for id in storefront_input.split(','))
    except (ValueError, AttributeError):
        return None

def load_data_and_display():
    """Load and display keyword data based on the current session state parameters.
    
    This function retrieves data using the parameters stored in the session state,
    displays a preview of the data, and updates the UI accordingly.
    
    The function handles the following states:
    - Shows a loading spinner while fetching data
    - Displays a warning if no data is found
    - Shows a success message with the number of rows loaded
    - Displays a preview of the data in a scrollable table
    - Resets the stage to 'initial' after successful loading
    
    Raises:
        Exception: If there's an error during data loading, the error is caught and
                 displayed to the user, and the stage is reset to 'initial'.
    """
    try:
        with st.spinner("Loading data..."):
            params = st.session_state.params
            # Create a new connection for this query
            with get_connection() as conn:
                df = get_data(conn, params["workspace_id"], params["storefront_ids"], 
                           params["start_date_str"], params["end_date_str"],"data")
            
            if df.empty:
                st.warning("No data returned from the query")
            else:
                st.success(f"✅ Successfully loaded {len(df)} rows")
                st.subheader("Data Preview")
                st.dataframe(df, use_container_width=True)
                
                # Reset to initial state after loading is complete
                st.session_state.stage = 'initial'

    except Exception as e:
        st.error(f"An error occurred during data load: {str(e)}")
        st.session_state.stage = 'initial' # Reset nếu có lỗi



#--------------------------------------------------#
#------------- handle export process --------------#
#--------------------------------------------------#
def handle_export_process_kwl(workspace_id, storefront_input, start_date, end_date):
    """Handle the export process with validation and data size checking.
    
    This function orchestrates the export process by:
    1. Validating input parameters
    2. Processing storefront IDs
    3. Saving parameters to session state
    4. Checking data size and determining the next stage
    
    Args:
        workspace_id (str): The workspace ID for the export
        storefront_input (str): Comma-separated string of storefront IDs
        start_date (datetime.date): Start date for the export
        end_date (datetime.date): End date for the export
        
    Returns:
        tuple: A tuple containing:
            - str: The current stage ('initial', 'waiting_confirmation', 'loading', or 'error')
            - dict: The parameters used for the export
            
    Note:
        This function updates the session state with the current parameters
        and the number of rows in the dataset.
    """
    errors = validate_inputs(workspace_id, storefront_input, start_date, end_date)
        
    if errors:
        for error in errors:
            st.error(error)
        st.stop()
            
    storefront_ids = process_storefront_input(storefront_input)
    if not storefront_ids:
        st.error("Invalid Storefront EID format")
        st.stop()
    
    # Save parameters to session state for reuse in subsequent runs
    st.session_state.params = {
        "workspace_id": int(workspace_id),
        "storefront_ids": storefront_ids,
        "start_date_str": start_date.strftime('%Y-%m-%d'),
        "end_date_str": end_date.strftime('%Y-%m-%d')
    }
    
    try:
        with st.spinner("Checking data size..."), get_connection() as conn:
            # Get the number of rows in the result set
            num_row_df = get_data(
                conn, 
                st.session_state.params["workspace_id"], 
                st.session_state.params["storefront_ids"], 
                st.session_state.params["start_date_str"], 
                st.session_state.params["end_date_str"],
                "count"
            )
            num_row = num_row_df.iloc[0, 0] if not num_row_df.empty else 0
            st.session_state.params['num_row'] = num_row

        # Determine the next stage based on the number of rows
        if num_row == 0:
            st.warning("No data found for the selected criteria")
            st.session_state.stage = 'initial'  # Reset state
        elif 10000 < num_row < 50000:
            # Large dataset -> switch to waiting for confirmation
            st.session_state.stage = 'waiting_confirmation'
        elif num_row >= 50000:
            # Very large dataset -> show error and stop
            st.error(f"Large dataset: {num_row:,} rows found. Please reduce the number of storefronts selected.")
            st.stop()
        else:
            # Small dataset -> proceed directly to loading
            st.session_state.stage = 'loading'

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.session_state.stage = 'initial'  # Reset state on error
    
    return st.session_state.stage, st.session_state.params


def handle_export_process_kw_pfm(workspace_id, storefront_input, start_date, end_date):
    """Handle the export process with validation and data size checking.
    
    This function orchestrates the export process by:
    1. Validating input parameters
    2. Processing storefront IDs
    3. Saving parameters to session state
    4. Checking data size and determining the next stage
    
    Args:
        workspace_id (str): The workspace ID for the export
        storefront_input (str): Comma-separated string of storefront IDs
        start_date (datetime.date): Start date for the export
        end_date (datetime.date): End date for the export
        
    Returns:
        tuple: A tuple containing:
            - str: The current stage ('initial', 'waiting_confirmation', 'loading', or 'error')
            - dict: The parameters used for the export
            
    Note:
        This function updates the session state with the current parameters
        and the number of rows in the dataset.
    """
    errors = validate_inputs(workspace_id, storefront_input, start_date, end_date)
        
    if errors:
        for error in errors:
            st.error(error)
        st.stop()
            
    storefront_ids = process_storefront_input(storefront_input)
    if not storefront_ids:
        st.error("Invalid Storefront EID format")
        st.stop()
    
    # Save parameters to session state for reuse in subsequent runs
    st.session_state.params = {
        "workspace_id": int(workspace_id),
        "storefront_ids": storefront_ids,
        "start_date_str": start_date.strftime('%Y-%m-%d'),
        "end_date_str": end_date.strftime('%Y-%m-%d')
    }
    
    try:
        with st.spinner("Checking data size..."), get_connection() as conn:
            # Get the number of rows in the result set
            num_row_df = get_data(
                conn, 
                st.session_state.params["workspace_id"], 
                st.session_state.params["storefront_ids"], 
                st.session_state.params["start_date_str"], 
                st.session_state.params["end_date_str"],
                "count"
            )
            num_row = num_row_df.iloc[0, 0] if not num_row_df.empty else 0
            st.session_state.params['num_row'] = num_row

        # Determine the next stage based on the number of rows
        if num_row == 0:
            st.warning("No data found for the selected criteria")
            st.session_state.stage = 'initial'  # Reset state
        elif 10000 < num_row < 50000:
            # Large dataset -> switch to waiting for confirmation
            st.session_state.stage = 'waiting_confirmation'
        elif num_row >= 50000:
            # Very large dataset -> show error and stop
            st.error(f"Large dataset: {num_row:,} rows found. Please reduce the number of storefronts selected.")
            st.stop()
        else:
            # Small dataset -> proceed directly to loading
            st.session_state.stage = 'loading'

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.session_state.stage = 'initial'  # Reset state on error
    
    return st.session_state.stage, st.session_state.params



#--------------------------------------------------#
#------------------- get data ---------------------#
#--------------------------------------------------#
@st.cache_data(show_spinner=False, ttl=3600, persist=True)
def get_data(_conn, workspace_id, storefront_id, start_date, end_date, query_type: str):
    """
    Get data based on the specified query type.
    
    Args:
        _conn: Database connection
        workspace_id: Workspace ID to filter by
        storefront_id: Single storefront ID or tuple of IDs
        start_date: Start date for the query
        end_date: End date for the query
        query_type: Type of query to execute ('count' or 'data')
        
    Returns:
        DataFrame: A DataFrame containing the query results.
    """
    if not isinstance(storefront_id, (list, tuple)):
        storefront_id = (storefront_id,)
    
    storefront_placeholders = ', '.join(['%s'] * len(storefront_id))
    query = get_query(query_type, storefront_placeholders)
    
    # Parameters for the new queries
    params = (start_date, end_date) + tuple(storefront_id) + (workspace_id,) + tuple(storefront_id) + (workspace_id,)
    
    with _conn.cursor() as cur:
        cur.execute(query, params)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        return pd.DataFrame(rows, columns=columns)