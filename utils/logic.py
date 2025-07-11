import streamlit as st
import pandas as pd
from io import StringIO
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, ProgrammingError
from utils.database import get_connection
from data_logic import kwl_data, kw_pfm_data, product_tracking_data, pi_data

def get_query_by_source(data_source: str):
    """Trả về hàm get_query phù hợp dựa trên nguồn dữ liệu."""
    query_map = {
        'kwl': kwl_data.get_query,
        'kw_pfm': kw_pfm_data.get_query,
        'pt': product_tracking_data.get_query,
        'pi': pi_data.get_query,
    }
    if data_source in query_map:
        return query_map[data_source]
    raise ValueError(f"Unknown data source: {data_source}")

@st.cache_data(show_spinner=False, ttl=3600, persist=True)
def get_data(query_type: str, data_source: str, limit: int = None, **kwargs):
    """
    Lấy dữ liệu từ CSDL, có thể tùy chọn giới hạn số dòng.
    Hàm này được cache để tăng tốc độ.
    """
    get_query_func = get_query_by_source(data_source)
    base_query_str = get_query_func(query_type)

    if limit is not None and query_type == 'data':
        final_query_str = f"{base_query_str} LIMIT {limit}"
    else:
        final_query_str = base_query_str
    
    query = text(final_query_str)

    if 'storefront_ids' in kwargs and isinstance(kwargs['storefront_ids'], list):
        kwargs['storefront_ids'] = tuple(kwargs['storefront_ids'])

    with get_connection() as db:
        return pd.read_sql(query, db.connection(), params=kwargs)

def load_data(data_source: str, limit: int = None):
    """Tải dữ liệu dựa trên các tham số trong session_state."""
    try:
        # Lấy các tham số từ session_state một cách an toàn
        params = st.session_state.get('params', {}).copy()
        
        # Loại bỏ các khóa không phải là tham số của query
        params.pop('data_source', None)
        params.pop('num_row', None)
        
        df = get_data(
            query_type='data', 
            data_source=data_source, 
            limit=limit, 
            **params
        )
        return df
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        return None

def handle_export_process(workspace_id, storefront_input, start_date, end_date, data_source: str, **kwargs):
    """
    Xử lý toàn bộ quy trình: xác thực, đếm số dòng, và cập nhật trạng thái.
    """
    errors = validate_inputs(workspace_id, storefront_input, start_date, end_date)
    if errors:
        for error in errors:
            st.error(error)
        st.stop()
    
    # Tập trung tất cả tham số vào một nơi duy nhất
    st.session_state.params = {
        "workspace_id": int(workspace_id),
        "storefront_ids": process_storefront_input(storefront_input),
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
        "data_source": data_source,
        **kwargs
    }

    try:
        with st.spinner("Checking data size..."):
            # Lấy các tham số cho query count từ st.session_state.params
            params_for_count = st.session_state.params.copy()
            params_for_count.pop('data_source', None)
            
            num_row_df = get_data('count', data_source, **params_for_count)
            num_row = num_row_df.iloc[0, 0] if not num_row_df.empty else 0
            st.session_state.params['num_row'] = num_row

        if num_row == 0:
            st.warning("No data found for the selected criteria.")
            st.session_state.stage = 'initial'
        elif num_row > 50000:
            st.error(f"Data is too large to export ({num_row:,} rows). Please narrow your selection.")
            st.session_state.stage = 'initial'
        else:
            # Nếu thành công, chuyển sang giai đoạn tải preview
            st.session_state.stage = 'loading_preview'

    except OperationalError:
        st.error("❌ Database Connection Error. Please contact the administrator.")
        st.session_state.stage = 'initial'
    except ProgrammingError as e:
        st.error(f"❌ SQL Error. The query could not be executed. Details: {e}")
        st.session_state.stage = 'initial'
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.session_state.stage = 'initial'

def handle_get_data_button(workspace_id, storefront_input, start_date, end_date, data_source, **kwargs):
    """Hàm xử lý sự kiện khi nhấn nút 'Get Data'."""
    # Reset lại trạng thái nếu đang thực hiện cho một nguồn dữ liệu mới
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
    # Chạy lại script để giao diện được cập nhật theo 'stage' mới
    st.rerun()

def validate_inputs(workspace_id, storefront_input, start_date, end_date):
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
    try:
        return [int(eid.strip()) for eid in storefront_input.split(',')]
    except ValueError:
        return None

def convert_df_to_csv(df: pd.DataFrame):
    output = StringIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    return output.getvalue()