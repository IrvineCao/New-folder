import streamlit as st
import pandas as pd
from io import StringIO
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, ProgrammingError
from utils.database import get_connection
from data_logic import kwl_data, kw_pfm_data, product_tracking_data, pi_data
from utils.messaging import display_user_message


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
    Lấy dữ liệu từ CSDL, xử lý mệnh đề IN một cách thủ công để đảm bảo cú pháp đúng.
    """
    get_query_func = get_query_by_source(data_source)
    base_query_str = get_query_func(query_type)
    
    params_to_bind = kwargs.copy()

    # Xử lý mệnh đề IN cho storefront_ids bằng cách định dạng trực tiếp vào chuỗi
    if 'storefront_ids' in params_to_bind and isinstance(params_to_bind['storefront_ids'], (list, tuple)):
        storefront_ids = params_to_bind['storefront_ids']
        
        safe_ids = [int(sid) for sid in storefront_ids]
        
        if len(safe_ids) == 1:
            ids_string = f"({safe_ids[0]})"
        else:
            ids_string = str(tuple(safe_ids))

        base_query_str = base_query_str.replace(':storefront_ids', ids_string)
        
        del params_to_bind['storefront_ids']

    if limit is not None and query_type == 'data':
        final_query_str = f"{base_query_str} LIMIT {limit}"
    else:
        final_query_str = base_query_str
    
    query = text(final_query_str)
    
    with get_connection() as db:
        return pd.read_sql(query, db.connection(), params=params_to_bind)

def build_params_for_query(data_source: str, source_params: dict):
    """Xây dựng một từ điển tham số sạch cho câu lệnh SQL."""
    required_params = {
        "workspace_id": source_params.get("workspace_id"),
        "storefront_ids": source_params.get("storefront_ids"),
        "start_date": source_params.get("start_date"),
        "end_date": source_params.get("end_date"),
    }
    
    if data_source == 'kw_pfm':
        required_params["device_type"] = source_params.get("device_type")
        required_params["display_type"] = source_params.get("display_type")
        required_params["product_position"] = source_params.get("product_position")
        
    return required_params

def load_data(data_source: str, limit: int = None):
    """Tải dữ liệu dựa trên các tham số trong session state."""
    try:
        params_for_load = build_params_for_query(data_source, st.session_state.get('params', {}))
        
        df = get_data(
            query_type='data', 
            data_source=data_source, 
            limit=limit, 
            **params_for_load
        )
        return df
    except Exception as e:
        # Hiển thị thông báo chung cho người dùng
        st.error("An error occurred while loading data. Please check the Developer Log for details.")
        return None

def handle_export_process(workspace_id, storefront_input, start_date, end_date, data_source: str, **kwargs):
    """Xử lý toàn bộ quy trình: xác thực, đếm số dòng, và cập nhật trạng thái."""
    errors = validate_inputs(workspace_id, storefront_input, start_date, end_date)
    if errors:
        for error in errors:
            st.error(error)
        st.stop()
    
    st.session_state.params = {
        "workspace_id": int(workspace_id),
        "storefront_ids": process_storefront_input(storefront_input),
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
        "data_source": data_source,
        **kwargs
    }

    # --- CẬP NHẬT KHỐI TRY...EXCEPT ---
    try:
        with st.spinner("Checking data size..."):
            params_for_count = build_params_for_query(data_source, st.session_state.params)
            num_row_df = get_data('count', data_source, **params_for_count)
            num_row = num_row_df.iloc[0, 0] if not num_row_df.empty else 0
            st.session_state.params['num_row'] = num_row

        # --- THAY ĐỔI CÁCH XỬ LÝ LỖI VÀ CẢNH BÁO ---
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

    except OperationalError as e:
        st.error("❌ Database Connection Error. Please contact an administrator.")
        st.session_state.stage = 'initial'
    except ProgrammingError as e:
        st.error("❌ An error occurred with the data query. Please contact an administrator.")
        st.session_state.stage = 'initial'
    except Exception as e:
        st.error("❌ An unexpected error occurred. Please contact an administrator.")
        st.session_state.stage = 'initial'

# ... (các hàm còn lại không đổi) ...
def handle_get_data_button(workspace_id, storefront_input, start_date, end_date, data_source, **kwargs):
    """Hàm xử lý sự kiện khi nhấn nút 'Get Data'."""
    # Xóa thông báo cũ trước khi bắt đầu một hành động mới
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