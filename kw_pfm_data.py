from datetime import datetime, timedelta
import streamlit as st

query_params = {
    "count": """
        WITH
            dim_data AS (
                SELECT
                    sf.storefront_type,
                    kw.keyword,
                    ws_tag.name,
                    kw.id AS dim_keyword_id,
                    kw.country_name AS keyword_country,
                    kw_ws.id AS keyword_ws_id,
                    sf.storefront_name,
                    sf.id AS storefront_id,
                    sf.storefront_sid,
                    sf.ads_ops_storefront_id AS aos_id,
                    sf_ws.workspace_id
                FROM
                    onsite_storefront sf
                    JOIN onsite_storefront_workspace sf_ws ON sf_ws.storefront_id = sf.id
                    JOIN passport_workspace ws ON sf_ws.workspace_id = ws.id
                    JOIN onsite_keyword_workspace kw_ws ON kw_ws.workspace_id = ws.id
                    JOIN onsite_keyword_sharded kw ON kw_ws.keyword_id = kw.id
                    JOIN onsite_keyword_workspace_tag kw_ws_tag ON kw_ws_tag.keyword_workspace_id = kw_ws.id
                    LEFT JOIN onsite_workspace_tag ws_tag ON ws_tag.id = kw_ws_tag.workspace_tag_id
                WHERE
                    sf.ads_ops_storefront_id IN ({storefront_placeholders})
                    AND ws.id = %s
            ),
            sos_metrics AS (
                SELECT
                    s.timing,
                    s.keyword_id AS sos_keyword_id,
                    s.storefront_id,
                    Month(created_datetime) as sos_date
                FROM global_company gc
                    JOIN onsite_storefront sf ON sf.global_company_id = gc.id
                    JOIN metric_share_of_search_storefront s ON s.storefront_id = sf.id
                    JOIN (SELECT DISTINCT dim_keyword_id,storefront_id FROM dim_data) dim 
                        ON s.keyword_id = dim.dim_keyword_id
                        AND s.storefront_id = dim.storefront_id
                WHERE true
                    AND s.device_type = 'Mobile'
                    AND s.display_type = 'Paid'
                    AND s.product_position = '10'
                    AND s.timing = 'daily'
                    AND DATE(created_datetime) BETWEEN %s AND %s
                GROUP BY
                    s.keyword_id,
                    s.storefront_id,
                    Month(created_datetime)
            ),
            ads_metrics AS (
                SELECT
                    p.timing,
                    p.ads_ops_storefront_id,
                    p.keyword_id AS ads_keyword_id,
                    p.tool_id,
                    Month(created_datetime) as ads_date
                FROM
                    ads_ops_storefront aos
                    JOIN onsite_storefront_keyword_ads_performance p ON p.ads_ops_storefront_id = aos.id
                    JOIN (
                        SELECT DISTINCT
                            dim_keyword_id,
                            aos_id
                        FROM
                            dim_data
                    ) dim ON p.keyword_id = dim.dim_keyword_id
                    AND p.ads_ops_storefront_id = dim.aos_id
                WHERE
                    p.timing = 'daily'
                    AND DATE(created_datetime) BETWEEN %s AND %s
                GROUP BY
                    p.ads_ops_storefront_id,
                    p.keyword_id,
                    p.tool_id,
                    Month(created_datetime)
            ),
            main_data AS (
                SELECT
                    d.*,
                    s.sos_date
                FROM
                    dim_data d
                    JOIN sos_metrics s ON s.sos_keyword_id = d.dim_keyword_id
                    AND s.storefront_id = d.storefront_id
                    LEFT JOIN ads_metrics a ON a.ads_keyword_id = d.dim_keyword_id
                    AND a.ads_ops_storefront_id = d.aos_id
            )
            -- Final result
        SELECT COUNT(1)
        FROM (SELECT 1
        FROM main_data
        GROUP BY workspace_id,storefront_id,keyword_ws_id,sos_date) as count_query
    """,
    "data": """
        WITH
            dim_data AS (
                SELECT
                    sf.storefront_type,
                    kw.keyword,
                    ws_tag.name,
                    kw.id AS dim_keyword_id,
                    kw.country_name AS keyword_country,
                    kw_ws.id AS keyword_ws_id,
                    sf.storefront_name,
                    sf.id AS storefront_id,
                    sf.storefront_sid,
                    aos.id AS aos_id,
                    sf_ws.workspace_id
                FROM
                    onsite_storefront sf
                    JOIN onsite_storefront_workspace sf_ws ON sf_ws.storefront_id = sf.id
                    JOIN ads_ops_storefront aos ON sf_ws.ads_ops_storefront_id = aos.id
                    JOIN passport_workspace ws ON sf_ws.workspace_id = ws.id
                    JOIN onsite_keyword_workspace kw_ws ON kw_ws.workspace_id = ws.id
                    JOIN onsite_keyword_sharded kw ON kw_ws.keyword_id = kw.id
                    JOIN onsite_keyword_workspace_tag kw_ws_tag ON kw_ws_tag.keyword_workspace_id = kw_ws.id
                    LEFT JOIN onsite_workspace_tag ws_tag ON ws_tag.id = kw_ws_tag.workspace_tag_id
                WHERE
                    sf.ads_ops_storefront_id IN ({storefront_placeholders})
                    AND ws.id = %s
            ),
            sos_metrics AS (
                SELECT
                    s.timing,
                    s.keyword_id AS sos_keyword_id,
                    s.storefront_id,
                    Month(created_datetime) as sos_date,
                    MAX(s.display_type) AS display_type,
                    AVG(s.share_of_search) AS share_of_search,
                    MAX(s.product_position) AS product_position,
                    AVG(s.suggested_bidding_price) AS suggested_cpc,
                    MAX(s.device_type) AS device_type,
                    AVG(s.search_volume) AS search_volume
                FROM global_company gc
                    JOIN onsite_storefront sf ON sf.global_company_id = gc.id
                    JOIN metric_share_of_search_storefront s ON s.storefront_id = sf.id
                    JOIN (SELECT DISTINCT dim_keyword_id,storefront_id FROM dim_data) dim 
                        ON s.keyword_id = dim.dim_keyword_id
                        AND s.storefront_id = dim.storefront_id
                WHERE true
                    AND s.device_type = 'Mobile'
                    AND s.display_type = 'Paid'
                    AND s.product_position = '10'
                    AND s.timing = 'daily'
                    AND DATE(created_datetime) BETWEEN %s AND %s
                GROUP BY
                    s.keyword_id,
                    s.storefront_id,
                    Month(created_datetime)
            ),
            ads_metrics AS (
                SELECT
                    p.timing,
                    p.ads_ops_storefront_id,
                    p.keyword_id AS ads_keyword_id,
                    p.tool_id,
                    Month(created_datetime) as ads_date,
                    SUM(p.ads_order) AS ads_order,
                    SUM(p.cost) AS cost,
                    SUM(p.direct_order) AS direct_order,
                    SUM(p.ads_gmv) AS ads_gmv,
                    SUM(p.direct_atc) AS direct_atc,
                    SUM(p.direct_gmv) AS direct_gmv,
                    SUM(p.direct_item_sold) AS direct_item_sold,
                    SUM(p.click) AS click,
                    SUM(p.atc) AS atc,
                    SUM(p.ads_item_sold) AS ads_item_sold,
                    SUM(p.impression) AS impression,
                    AVG(p.active_skus) AS active_skus,
                    SUM(p.direct_conversion) AS direct_conversion,
                    SUM(p.conversion) AS conversion,
                    AVG(p.active_shops) AS active_shops
                FROM
                    ads_ops_storefront aos
                    JOIN onsite_storefront_keyword_ads_performance p ON p.ads_ops_storefront_id = aos.id
                    JOIN (
                        SELECT DISTINCT
                            dim_keyword_id,
                            aos_id
                        FROM
                            dim_data
                    ) dim ON p.keyword_id = dim.dim_keyword_id
                    AND p.ads_ops_storefront_id = dim.aos_id
                WHERE
                    p.timing = 'daily'
                    AND DATE(created_datetime) BETWEEN %s AND %s
                GROUP BY
                    p.ads_ops_storefront_id,
                    p.keyword_id,
                    p.tool_id,
                    Month(created_datetime)
            ),
            main_data AS (
                SELECT
                    d.*,
                    s.search_volume,
                    s.share_of_search,
                    s.suggested_cpc,
                    s.sos_date,
                    a.ads_order,
                    a.cost,
                    a.direct_order,
                    a.ads_gmv,
                    a.direct_atc,
                    a.direct_gmv,
                    a.direct_item_sold,
                    a.click,
                    a.atc,
                    a.ads_item_sold,
                    a.impression,
                    a.active_skus,
                    a.direct_conversion,
                    a.conversion,
                    a.active_shops,
                    (a.cost / NULLIF(a.click, 0)) AS cpc
                FROM
                    dim_data d
                    JOIN sos_metrics s ON s.sos_keyword_id = d.dim_keyword_id
                    AND s.storefront_id = d.storefront_id
                    LEFT JOIN ads_metrics a ON a.ads_keyword_id = d.dim_keyword_id
                    AND a.ads_ops_storefront_id = d.aos_id
            )
            -- Final result
        SELECT
            keyword,
            storefront_name,
            sos_date as month,
            AVG(search_volume) AS search_volume,
            MAX(atc) AS atc,
            MAX(cost) AS cost,
            MAX(click) AS click,
            MAX(ads_order) AS ads_order,
            MAX(conversion) AS conversion,
            MAX(direct_atc) AS direct_atc,
            MAX(direct_gmv) AS direct_gmv,
            MAX(impression) AS impression,
            MAX(active_skus) AS active_skus,
            MAX(active_shops) AS active_shops,
            MAX(direct_order) AS direct_order,
            MAX(ads_item_sold) AS ads_item_sold,
            MAX(direct_item_sold) AS direct_item_sold,
            MAX(direct_conversion) AS direct_conversion,
            AVG(share_of_search) AS escore,
            MAX(ads_gmv) AS ads_gmv,
            AVG(suggested_cpc) AS benchmark_CPC,
            MAX(cpc) AS cpc
        FROM
            main_data
        GROUP BY
            workspace_id,
            storefront_id,
            keyword_ws_id,
            sos_date;
    """
}

def get_query(query_name, storefront_placeholders):
    """
    Get a query by name and format it with storefront and tag placeholders
    
    Args:
        query_name (str): Name of the query to retrieve ('count' or 'data')
        storefront_placeholders (str): Placeholder string for storefront IDs (e.g., '%s, %s')
        
    Returns:
        str: Formatted SQL query
    """
    return query_params[query_name].format(
        storefront_placeholders=storefront_placeholders
    )

def kw_pfm_page():
    # Input section
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            workspace_id = st.text_input("Workspace ID *", "", 
                                        help="Enter the workspace ID (numeric)")
        with col2:
            storefront_input = st.text_input("Storefront EID *", "", 
                                        help="Enter one or more storefront IDs, comma-separated")
        with col3:
            start_date = st.date_input("Start Date *", 
                                    value=datetime.now() - timedelta(days=30),  # Keep 30 days ago as default start
                                    max_value=datetime.now().date() - timedelta(days=1))  # Can't select future dates
        with col4:
            end_date = st.date_input("End Date *", 
                                    value=datetime.now().date() - timedelta(days=1),  # Set to yesterday
                                    max_value=datetime.now().date() - timedelta(days=1))  # Can't select today or future
    # Add some spacing
    st.write("---")
    return workspace_id, storefront_input, start_date, end_date


