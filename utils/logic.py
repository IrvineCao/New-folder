import streamlit as st
import pandas as pd
from io import StringIO
from sqlalchemy import text
from utils.database import get_connection
from data_logic import kwl_data, kw_pfm_data, product_tracking_data, pi_data
from sqlalchemy.exc import OperationalError

def get_query_by_source(data_source: str):
    """
    Returns the appropriate get_query function based on the data source.
    """
    if data_source == 'kwl':
        return kwl_data.get_query
    elif data_source == 'kw_pfm':
        return kw_pfm_data.get_query
    elif data_source == 'pt':
        return product_tracking_data.get_query
    elif data_source == 'pi':
        return pi_data.get_query
    else:
        raise ValueError(f"Unknown data source: {data_source}")


def validate_inputs(workspace_id, storefront_input, start_date, end_date):
    """Validates the user inputs from the Streamlit UI."""
    errors = []
    workspace_id_list = [s.strip() for s in workspace_id.split(",") if s.strip()]
    if not workspace_id_list:
        errors.append("Workspace ID is required")
    elif len(workspace_id_list) > 1:
        errors.append("You can only enter one workspace ID.")
    elif not all(s.isdigit() for s in workspace_id_list):
        errors.append("Workspace ID must be numeric.")

    storefront_input_list = [s.strip() for s in storefront_input.split(",") if s.strip()]
    if not storefront_input_list:
        errors.append("Storefront EID is required")
    elif len(storefront_input_list) > 5:
        errors.append("You can only enter up to 5 storefront IDs.")
    elif not all(s.isdigit() for s in storefront_input_list):
        errors.append("Storefront EID must be numeric.")
    
    num_storefronts = len(storefront_input_list)
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
def get_data(query_type: str, data_source: str, limit: int = None, **kwargs):
    """
    Get data based on the specified query type using SQLAlchemy session.
    Can optionally limit the number of rows returned.
    """
    get_query_func = get_query_by_source(data_source)
    
    # Lấy câu lệnh SQL gốc
    base_query_str = get_query_func(query_type)
    
    # Tạo một truy vấn có thể thực thi từ chuỗi SQL
    query = text(base_query_str)
    
    # Nếu có tham số limit, bọc truy vấn gốc trong một truy vấn mới và thêm LIMIT
    if limit is not None and query_type == 'data':
        # Tạo một Common Table Expression (CTE) từ câu lệnh gốc
        cte = select(literal_column("*")).select_from(query).cte("original_query")
        # Tạo câu lệnh cuối cùng để chọn từ CTE và áp dụng LIMIT
        final_query = select(literal_column("*")).select_from(cte).limit(limit)
        query = final_query

    # Xử lý các tham số
    if 'storefront_ids' in kwargs and isinstance(kwargs['storefront_ids'], list):
        kwargs['storefront_ids'] = tuple(kwargs['storefront_ids'])

    # Thực thi truy vấn
    with get_connection() as db:
        return pd.read_sql(query, db.connection(), params=kwargs)


def handle_export_process(workspace_id, storefront_input, start_date, end_date, data_source: str, **kwargs):
    """Handle the export process with validation and data size checking."""
    errors = validate_inputs(workspace_id, storefront_input, start_date, end_date)
    if errors:
        for error in errors:
            st.error(error)
        st.stop()

    date_range_days = (end_date - start_date).days
    if 30 < date_range_days <= 60:
        st.warning(f"⚠️ The period is too long ({date_range_days} days). Processing may take longer than usual.")

    st.session_state.params = {
        "workspace_id": int(workspace_id),
        "storefront_ids": process_storefront_input(storefront_input),
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
        "data_source": data_source
    }
    st.session_state.params.update(kwargs)

    try:
        with st.spinner("Checking data size..."):
            count_params = st.session_state.params.copy()
            count_params['query_type'] = 'count'
            num_row_df = get_data(**count_params)
            num_row = num_row_df.iloc[0, 0] if not num_row_df.empty else 0
            st.session_state.params['num_row'] = num_row

        if num_row == 0 or num_row is None:
            st.warning("No data found for the selected criteria.")
            st.session_state.stage = 'initial'
        elif 10000 < num_row <= 50000:
            st.session_state.stage = 'waiting_confirmation'
        elif num_row > 50000:
            st.error(f"Data is too large to export ({num_row:,} rows). Please narrow your date range or storefronts.")
            st.session_state.stage = 'initial'
        else:
            st.session_state.stage = 'loading'
    except OperationalError:
        st.error("❌ Database connection failed. Please check the network or contact the administrator.")
        st.session_state.stage = 'initial'
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.session_state.stage = 'initial'

def load_data(data_source: str):
    """Load data based on params in session state and return a DataFrame."""
    try:
        data_params = st.session_state.params.copy()
        data_params['query_type'] = 'data'
        df = get_data(**data_params)
        return df
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        return None


def convert_df_to_csv(df: pd.DataFrame):
    """Convert a DataFrame to a CSV string for downloading."""
    output = StringIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    return output.getvalue()


def handle_get_data_button(workspace_id, storefront_input, start_date, end_date, data_source, **kwargs):
    """Xử lý logic khi nút 'Get Data' được nhấn."""
    # Xóa trạng thái cũ khi bắt đầu một yêu cầu mới
    if st.session_state.params.get('data_source') != data_source:
        st.session_state.stage = 'initial'
        st.session_state.params = {}
        st.session_state.df = None

    handle_export_process(
        workspace_id,
        storefront_input,
        start_date,
        end_date,
        data_source=data_source,
        **kwargs
    )