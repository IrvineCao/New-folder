from function import handle_export_process
from datetime import datetime, timedelta
import streamlit as st

query_params = {
    "count": """

    """,
    "data": """
    
    """
}

def get_query(query_name, storefront_placeholders, tag_placeholders):
    """
    Get a query by name and format it with storefront and tag placeholders
    
    Args:
        query_name (str): Name of the query to retrieve ('count' or 'data')
        storefront_placeholders (str): Placeholder string for storefront IDs (e.g., '%s, %s')
        tag_placeholders (str): Placeholder string for tags (e.g., '%s, %s')
        
    Returns:
        str: Formatted SQL query
    """
    return query_params[query_name].format(
        storefront_placeholders=storefront_placeholders,
        tag_placeholders=tag_placeholders
    )

def product_tracking_page():
    st.title("Product Tracking Data Export")

    with st.container():
        col6, col7, col8, col9, col10 = st.columns(5)
        with col6:
            workspace_id_pt = st.text_input("Workspace ID *", "", 
                                            help="Enter the workspace ID (numeric)", key="workspace_id_pt")
        with col7:
            storefront_input_pt = st.text_input("Storefront EID *", "", 
                                            help="Enter one or more storefront IDs, comma-separated", key="storefront_input_pt")
        with col8:
            tags_input_pt = st.text_input("Tags *", "", 
                                            help="Enter one or more tags, comma-separated", key="tags_input_pt")
        with col9:
            start_date_pt = st.date_input("Start Date *", value=datetime.now() - timedelta(days=30), max_value=datetime.now().date() - timedelta(days=1), key="start_date_pt")
        with col10:
            end_date_pt = st.date_input("End Date *", value=datetime.now().date() - timedelta(days=1), max_value=datetime.now().date() - timedelta(days=1), key="end_date_pt")

    st.write("---")

    if st.button("Get Data", type="primary", use_container_width=True, key="get_data_pt"):
        stage, params = handle_export_process('pi', workspace_id_pt, storefront_input_pt, start_date_pt, end_date_pt, tags_input_pt)
        st.session_state.stage = stage
        st.session_state.params = params