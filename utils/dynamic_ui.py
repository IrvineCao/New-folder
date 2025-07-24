"""
Dynamic UI Components System

This module generates UI components dynamically based on input configuration,
replacing the hardcoded form generation in ui_components.py.
"""

import streamlit as st
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, Optional, List
from utils.helpers import trace_function_call
from utils.input_config import get_input_config, get_data_source_config, INPUT_FIELDS
from utils.input_validator import validate_data_source_inputs, build_sql_params
from utils.logic import load_data, convert_df_to_csv

def create_dynamic_input_form(data_source: str) -> Tuple[Dict[str, Any], List[str]]:
    """
    Create a dynamic input form based on data source configuration.
    
    Args:
        data_source: Data source key (e.g., 'kwl', 'sf')
    
    Returns:
        Tuple of (input_values, validation_errors)
    """
    config = get_data_source_config(data_source)
    if not config:
        st.error(f"Unknown data source: {data_source}")
        return {}, [f"Unknown data source: {data_source}"]
    
    input_values = {}
    
    
    # Group inputs by type for better layout
    required_fields = []
    optional_fields = []
    
    for field_name in config["inputs"]:
        field_config = get_input_config(field_name)
        if field_config:
            if field_config.get("required", False):
                required_fields.append(field_name)
            else:
                optional_fields.append(field_name)
    
    # Render required fields first
    if required_fields:
        st.markdown("### Required Fields")
        with st.container():
            input_values.update(_render_input_fields(required_fields, data_source))
    
    # Render optional fields
    if optional_fields:
        st.markdown("### Optional Filters")
        with st.container():
            input_values.update(_render_input_fields(optional_fields, data_source))
    
    # Validate all inputs
    validation_errors = validate_data_source_inputs(data_source, input_values)
    
    st.write("---")
    return input_values, validation_errors

def _render_input_fields(field_names: list, data_source: str) -> Dict[str, Any]:
    """Render a list of input fields and return their values."""
    input_values = {}
    
    # Group fields for column layout
    text_fields = []
    other_fields = []
    
    for field_name in field_names:
        field_config = get_input_config(field_name)
        if field_config and field_config.get("type") == "text":
            text_fields.append(field_name)
        else:
            other_fields.append(field_name)
    
    # Render text fields in columns
    if text_fields:
        cols = st.columns(min(len(text_fields), 3))
        for i, field_name in enumerate(text_fields):
            with cols[i % len(cols)]:
                input_values[field_name] = _render_single_field(field_name, data_source)
    
    # Render other fields
    for field_name in other_fields:
        if field_name == "date_range":
            start_date, end_date = _render_date_range_field(field_name, data_source)
            input_values["start_date"] = start_date
            input_values["end_date"] = end_date
            input_values[field_name] = (start_date, end_date) if start_date and end_date else None
        else:
            input_values[field_name] = _render_single_field(field_name, data_source)
    
    return input_values

def _render_single_field(field_name: str, data_source: str) -> Any:
    """Render a single input field based on its configuration."""
    field_config = get_input_config(field_name)
    if not field_config:
        return None
    
    field_type = field_config.get("type")
    label = field_config["label"]
    required = field_config.get("required", False)
    help_text = field_config.get("help_text", "")
    
    # Add asterisk for required fields
    if required:
        label += " *"
    
    # Generate unique key for session state
    key = f"{field_name}_{data_source}"
    
    if field_type == "text":
        value = st.text_input(
            label,
            value=st.session_state.get(key, ""),
            key=key,
            help=help_text
        )
        
        # Show performance tip for storefront fields
        if field_name == "storefront_ids" and value and len(value.split(',')) > 1:
            st.info("💡 " + field_config.get("performance_tip", ""))
        
        return value
    
    elif field_type == "select":
        options = field_config.get("options", [])
        default_value = field_config.get("default", options[0] if options else "")
        
        # Find default index
        default_index = 0
        if default_value in options:
            default_index = options.index(default_value)
        
        return st.selectbox(
            label,
            options=options,
            index=default_index,
            key=key,
            help=help_text
        )
    
    return None

def _render_date_range_field(field_name: str, data_source: str) -> Tuple[Optional[Any], Optional[Any]]:
    """Render date range field with presets."""
    field_config = get_input_config(field_name)
    if not field_config:
        return None, None
    
    label = field_config["label"]
    required = field_config.get("required", False)
    presets = field_config.get("presets", {})
    
    if required:
        label += " *"
    
    # Date preset selection
    preset_key = f"date_preset_{data_source}"
    selected_preset = st.selectbox(
        label,
        options=list(presets.keys()),
        index=0,
        key=preset_key
    )
    
    start_date, end_date = None, None
    
    if selected_preset == "Custom time range":
        # Custom date inputs
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                value=datetime.now().date() - timedelta(days=1),
                max_value=datetime.now().date() - timedelta(days=1),
                key=f"start_date_{data_source}"
            )
        with col2:
            end_date = st.date_input(
                "End Date",
                value=datetime.now().date() - timedelta(days=1),
                max_value=datetime.now().date() - timedelta(days=1),
                key=f"end_date_{data_source}"
            )
    else:
        # Use preset dates
        preset_dates = presets[selected_preset]
        if preset_dates:
            start_date = preset_dates["start"]
            end_date = preset_dates["end"]
    
    return start_date, end_date

def display_validation_errors(errors: list):
    """Display validation errors in a user-friendly format."""
    if errors:
        st.error("Please fix the following issues:")
        for error in errors:
            st.error(f"• {error}")
        return True
    return False

@trace_function_call
def create_action_buttons(data_source: str, input_values: Dict[str, Any], validation_errors: List[str]):
    """Create action buttons for data export."""
    # Disable button if there are validation errors
    button_disabled = len(validation_errors) > 0
    
    if st.button(
        "🚀 Get Data",
        key=f"get_data_button_{data_source}",
        type="primary",
        disabled=button_disabled,
        use_container_width=True,
        help="Click to start data export process" if not button_disabled else "Please fix validation errors first"
    ):
        # Reset the trace for the new action
        if 'call_trace' in st.session_state:
            st.session_state.call_trace = []

        if not validation_errors:
            # Build SQL parameters
            sql_params = build_sql_params(data_source, input_values)
            
            # Store current page and data source info for tab state management
            current_page = st.session_state.get('current_page')
            
            # Store in session state for processing
            st.session_state.params = {
                "data_source": data_source,
                "current_page": current_page,  # Save page info for tab state
                **sql_params
            }
            
            # Import and call the refactored logic
            from utils.logic import handle_export_process
            
            handle_export_process(data_source=data_source)
            st.rerun()


# --- Helper functions for display_data_exporter ---
def _handle_loading_preview():
    """Stage 1: Load a preview of the data (first 500 rows)."""
    start_time = time.time()
    with st.spinner("Loading preview (500 rows)..."):
        df_preview = load_data(st.session_state.params.get('data_source'), limit=500)
        if df_preview is not None and not df_preview.empty:
            st.session_state.df_preview = df_preview
            st.session_state.stage = 'loaded'
        else:
            st.warning("No data found for the selected criteria.")
            st.session_state.stage = 'initial'
    st.session_state.query_duration = time.time() - start_time
    st.rerun()

def _display_results():
    """Stage 2: Display the data preview and summary metrics."""
    df_preview = st.session_state.get('df_preview')
    if df_preview is None:
        st.session_state.stage = 'initial'
        st.rerun()

    st.success("✅ Preview loaded successfully!")
    
    with st.expander("**Summary (from Preview)**", expanded=True):
        params = st.session_state.get('params', {})
        total_rows_estimated = params.get('num_row', 0)
        num_storefronts = len(params.get('storefront_ids') or [])
        start_date_str = params.get('start_date')
        end_date_str = params.get('end_date')
        
        if start_date_str and end_date_str:
            start_date_obj = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date_str, '%Y-%m-%d')
            total_days = (end_date_obj - start_date_obj).days + 1
            date_range_display = f"{total_days} days"
        else:
            date_range_display = "N/A"
        query_duration = st.session_state.get('query_duration', 0)

        cols = st.columns(5)
        cols[0].metric("Total Rows (Estimated)", f"{total_rows_estimated:,}")
        cols[1].metric("Total Columns", len(df_preview.columns))
        cols[2].metric("Date Range", date_range_display)
        cols[3].metric("Storefronts", num_storefronts)
        cols[4].metric("Preview Query Time", f"{query_duration:.2f} s")
        
    st.markdown("---")
    cols_action = st.columns(2)
    with cols_action[0]:
        # Check if export is allowed (under 50k rows)
        total_rows = st.session_state.get('params', {}).get('num_row', 0)
        export_disabled = bool(total_rows > 50000)
        
        if st.button(
            "🚀 Export Full Data", 
            use_container_width=True, 
            type="primary",
            disabled=export_disabled,
            help="Export the full dataset" if not export_disabled else f"Export disabled: Too many rows ({total_rows:,}). Maximum allowed: 50,000 rows."
        ):
            if 'call_trace' in st.session_state:
                st.session_state.call_trace = []
            st.session_state.stage = 'exporting_full'
            st.rerun()
            
    with cols_action[1]:
        if st.button("🔄 Start New Export", use_container_width=True):
            st.session_state.stage = 'initial'
            st.session_state.df_preview = None
            st.session_state.params = {}
            st.rerun()

    st.subheader("Preview data (first 500 rows)")
    st.data_editor(df_preview, use_container_width=True, height=300)

def _handle_exporting_full():
    """Stage 3: Load the full dataset and prepare it for download."""
    # Double-check row limit before proceeding
    total_rows = st.session_state.get('params', {}).get('num_row', 0)
    if int(total_rows) > 50000:
        st.error(f"❌ Export blocked: Dataset too large ({total_rows:,} rows). Maximum allowed: 50,000 rows.")
        st.session_state.stage = 'blocked'
        st.rerun()
        return
    
    with st.spinner("Exporting full data, this may take a while..."):
        full_df = load_data(st.session_state.params.get('data_source'))
        if full_df is not None:
            csv_data = convert_df_to_csv(full_df)
            file_name = f"{st.session_state.params.get('data_source')}_data_{datetime.now().strftime('%Y%m%d')}.csv"
            st.session_state.download_info = {"data": csv_data, "file_name": file_name}
            st.session_state.stage = 'download_ready'
            st.rerun()

def _display_download_ready():
    """Stage 4: Display the download button for the exported CSV."""
    st.success("✅ Your full data export is ready to download!")
    info = st.session_state.download_info
    st.download_button(
       label="📥 Download CSV Now",
       data=info['data'],
       file_name=info['file_name'],
       mime='text/csv',
       use_container_width=True,
       type="primary",
    )
    if st.button("🔄 Start New Export", use_container_width=True):
        st.session_state.stage = 'initial'
        st.rerun()

def _display_blocked_state():
    """Stage: Display blocked state when data is too large."""
    params = st.session_state.get('params', {})
    total_rows = int(params.get('num_row', 0))
    
    st.error(f"🚫 Export blocked: Dataset contains {total_rows:,} rows")
    st.warning("**Maximum allowed: 50,000 rows**")
    
    st.markdown("### 💡 Suggestions to reduce data size:")
    st.markdown("""
    - **Reduce date range**: Select a shorter time period
    - **Reduce storefronts**: Select fewer storefront EIDs  
    - **Add more filters**: Use optional filters to narrow down results
    """)
    
    if st.button("🔄 Modify Selection", use_container_width=True, type="primary"):
        st.session_state.stage = 'initial'
        st.session_state.df_preview = None
        st.session_state.params = {}
        st.rerun()


# --- Main Display Function --- 
def display_data_exporter():
    """Display the entire data processing flow from preview to download."""    
    stage_map = {
        'loading_preview': _handle_loading_preview,
        'loaded': _display_results,
        'exporting_full': _handle_exporting_full,
        'download_ready': _display_download_ready,
        'blocked': _display_blocked_state,  # New blocked state
    }
    
    current_stage = st.session_state.get('stage', 'initial')
    if current_stage in stage_map:
        stage_map[current_stage]()

def get_form_summary(data_source: str, input_values: Dict[str, Any]) -> str:
    """Generate a summary of the current form configuration."""
    config = get_data_source_config(data_source)
    if not config:
        return "Unknown configuration"
    
    summary_parts = [f"**{config['name']}**"]
    
    for field_name in config["inputs"]:
        field_config = get_input_config(field_name)
        if not field_config:
            continue
        
        value = input_values.get(field_name)
        if value:
            if field_name == "date_range":
                start_date = input_values.get("start_date")
                end_date = input_values.get("end_date")
                if start_date and end_date:
                    days = (end_date - start_date).days + 1
                    summary_parts.append(f"• Date Range: {days} days ({start_date} to {end_date})")
            elif field_name == "storefront_ids":
                count = len(str(value).split(",")) if value else 0
                summary_parts.append(f"• Storefronts: {count} selected")
            else:
                summary_parts.append(f"• {field_config['label']}: {value}")
    
    return "\n".join(summary_parts)