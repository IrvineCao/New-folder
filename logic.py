import streamlit as st
import pandas as pd
from io import StringIO
from kwl_data import get_query as get_kwl_query
from kw_pfm_data import get_query as get_kw_pfm_query
from product_tracking_data import get_query as get_pt_query
from pi_data import get_query as get_pi_query
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
    elif data_source == 'pi':
        return get_pi_query
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
    
    date_range_days = (end_date - start_date).days
    if date_range_days > 60: # Ví dụ: Giới hạn cứng là 90 ngày
        errors.append(f"The period is too long ({date_range_days} days). Please select up to 60 days to ensure performance.")

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

    # Đảm bảo storefront_ids là một tuple để tương thích với câu lệnh 'IN' của SQL
    if 'storefront_ids' in kwargs and isinstance(kwargs['storefront_ids'], list):
        kwargs['storefront_ids'] = tuple(kwargs['storefront_ids'])

    with get_connection() as db:
        # Truyền thẳng kwargs vào params, SQLAlchemy sẽ tự động khớp các biến
        return pd.read_sql(text(query), db.connection(), params=kwargs)



def handle_export_process(workspace_id, storefront_input, start_date, end_date, data_source: str, **kwargs):
    """Handle the export process with validation and data size checking."""
    errors = validate_inputs(workspace_id, storefront_input, start_date, end_date)
    if errors:
        for error in errors:
            st.error(error)
        st.stop()

    # Cảnh báo nếu khoảng thời gian quá dài
    date_range_days = (end_date - start_date).days
    if 30 < date_range_days <= 60:
        st.warning(f"⚠️ The period is too long ({date_range_days} days). Processing may take longer than usual.")

    # 1. Lưu tất cả tham số vào session_state
    st.session_state.params = {
        "workspace_id": int(workspace_id),
        "storefront_ids": process_storefront_input(storefront_input),
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
        "data_source": data_source
    }
    st.session_state.params.update(kwargs) # Thêm các tham số phụ như device_type

    try:
        with st.spinner("Checking data size..."):
            # 2. Tạo bản sao từ session_state để gọi hàm count
            count_params = st.session_state.params.copy()
            count_params['query_type'] = 'count'

            # 3. Gọi get_data với các tham số đã được "mở" ra
            num_row_df = get_data(**count_params)
            num_row = num_row_df.iloc[0, 0] if not num_row_df.empty else 0
            st.session_state.params['num_row'] = num_row

        # Logic phân loại số dòng giữ nguyên
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
            # Tạo bản sao từ session_state để gọi hàm lấy data
            data_params = st.session_state.params.copy()
            data_params['query_type'] = 'data'

            df = get_data(**data_params)
            st.session_state.df = df
            st.session_state.stage = 'loaded'
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        st.session_state.stage = 'initial'



def convert_df_to_csv(df: pd.DataFrame):
    """Convert a DataFrame to a CSV string for downloading."""
    output = StringIO()
    
    # test định dạng file csv
    # Sửa từ 'utf-8' thành 'utf-8-sig'
    df.to_csv(output, index=False, encoding='utf-8-sig')
    
    return output.getvalue()