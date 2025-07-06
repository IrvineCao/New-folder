from datetime import datetime, timedelta
import streamlit as st


query_params = {
    "count": """
        WITH main_query AS (
                SELECT
                    keyword.id AS keyword_id,
                    storefront.ads_ops_storefront_id AS ads_ops_storefront_id,
                    storefront_workspace.workspace_id AS workspace_id,
                    storefront_keyword_a.est_daily_search_volume AS daily_search_volume,
                    storefront_workspace.storefront_id AS workspace_storefront_id
                FROM onsite_storefront AS storefront
                    INNER JOIN kw_discovery_storefront_workspace AS storefront_workspace 
                        ON storefront_workspace.storefront_id = storefront.id
                    INNER JOIN onsite_keyword_sharded AS keyword ON (true)
                    INNER JOIN kw_discovery_storefront_keyword AS storefront_keyword 
                        ON storefront_keyword.keyword_id = keyword.id
                        AND storefront_keyword.storefront_id = storefront.id
                    LEFT JOIN (
                        SELECT
                            storefront_keyword_a.timing AS timing,
                            storefront_keyword_a.keyword_id,
                            storefront_keyword_a.storefront_id,
                            SUM(storefront_keyword_a.est_daily_search_volume) AS est_daily_search_volume
                        FROM onsite_keyword_sharded AS keyword
                        INNER JOIN kw_discovery_storefront_keyword_perf AS storefront_keyword_a 
                            ON storefront_keyword_a.keyword_id = keyword.id
                        WHERE true                    
                            AND storefront_keyword_a.timing = 'daily'
                            AND created_datetime BETWEEN %s AND %s
                        GROUP BY
                            storefront_keyword_a.keyword_id,
                            storefront_keyword_a.storefront_id
                    ) storefront_keyword_a 
                        ON (storefront_keyword_a.keyword_id = keyword.id)
                        AND storefront_keyword_a.storefront_id = storefront.id
                        AND storefront_keyword_a.timing = 'daily'
                WHERE true
                    AND storefront_keyword.keyword_type != 'irrelevant'
                    and storefront.ads_ops_storefront_id IN ({storefront_placeholders})
                    and workspace_id = %s
                GROUP BY storefront_keyword.id,storefront_workspace.workspace_id,storefront_workspace.storefront_id
                HAVING
                    (
                        MAX(storefront_keyword.keyword_type) != 'irrelevant'
                        and SUM(storefront_keyword_a.est_daily_search_volume) > '0'
                        and MAX(storefront.ads_ops_storefront_id) IN ({storefront_placeholders})
                        and MAX(workspace_id) = %s
                    )
            )
        select count(1)
        from(SELECT 1
        FROM main_query
        GROUP BY keyword_id,workspace_id,workspace_storefront_id)
    """,
    "data": """
        WITH main_query AS (
                SELECT
                    storefront.id AS storefront_id,
                    storefront_workspace.storefront_division AS storefront_division,
                    storefront.country_code AS country_code,
                    storefront.storefront_sid AS storefront_sid,
                    storefront.storefront_name AS storefront_name,
                    storefront.marketplace_code AS marketplace_code,
                    storefront_keyword.keyword_type AS keyword_type,
                    keyword.keyword AS keyword,
                    storefront_keyword.category_name AS category_name,
                    keyword.id AS keyword_id,
                    storefront_keyword.active_skus AS active_skus,
                    storefront_keyword.operational_status AS operational_status,
                    storefront.ads_ops_storefront_id AS ads_ops_storefront_id,
                    storefront_keyword.brand_name AS brand_name,
                    storefront_keyword.tag_1 AS tag_1,
                    storefront_keyword.tag_2 AS tag_2,
                    storefront_keyword.function AS function,
                    storefront_workspace.workspace_id AS workspace_id,
                    storefront_keyword.note_1 AS note_1,
                    storefront_keyword.note_2 AS note_2,
                    storefront_keyword.peak_day_roas AS peak_day_roas,
                    storefront_keyword.peak_day_ads_gmv AS peak_day_ads_gmv,
                    storefront_keyword.peak_day_bau_ads_gmv AS peak_day_bau_ads_gmv,
                    storefront_keyword_a.est_daily_search_volume AS daily_search_volume,
                    storefront_keyword_a.suggested_bidding_price AS suggested_bidding_price,
                    storefront_keyword.current_avg_bidding_price AS current_avg_bidding_price,
                    storefront_keyword_a.ads_gmv AS ads_gmv,
                    (storefront_keyword_a.ads_gmv / storefront_keyword_a.cost) AS roas,
                    storefront_keyword_a.cost AS cost,
                    storefront_keyword_a.ads_item_sold AS ads_item_sold,
                    (storefront_keyword_a.cost / storefront_keyword_a.click) AS cpc,
                    (storefront_keyword_a.click / storefront_keyword_a.impression) AS ctr,
                    storefront_keyword_a.click AS click,
                    (storefront_keyword_a.ads_item_sold / storefront_keyword_a.click) AS cr,
                    storefront_keyword_a.impression AS impression,
                    storefront_workspace.storefront_id AS workspace_storefront_id
                FROM onsite_storefront AS storefront
                    INNER JOIN kw_discovery_storefront_workspace AS storefront_workspace 
                        ON storefront_workspace.storefront_id = storefront.id
                    INNER JOIN onsite_keyword_sharded AS keyword ON (true)
                    INNER JOIN kw_discovery_storefront_keyword AS storefront_keyword 
                        ON storefront_keyword.keyword_id = keyword.id
                        AND storefront_keyword.storefront_id = storefront.id
                    LEFT JOIN (
                        SELECT
                            storefront_keyword_a.timing AS timing,
                            storefront_keyword_a.keyword_id,
                            storefront_keyword_a.storefront_id,
                            SUM(storefront_keyword_a.ads_gmv) AS ads_gmv,
                            SUM(storefront_keyword_a.cost) AS cost,
                            SUM(storefront_keyword_a.ads_item_sold) AS ads_item_sold,
                            SUM(storefront_keyword_a.impression) AS impression,
                            AVG(storefront_keyword_a.suggested_bidding_price) AS suggested_bidding_price,
                            SUM(storefront_keyword_a.est_daily_search_volume) AS est_daily_search_volume,
                            SUM(storefront_keyword_a.click) AS click
                        FROM onsite_keyword_sharded AS keyword
                        INNER JOIN kw_discovery_storefront_keyword_perf AS storefront_keyword_a 
                            ON storefront_keyword_a.keyword_id = keyword.id
                        WHERE true                    
                            AND storefront_keyword_a.timing = 'daily'
                            AND created_datetime BETWEEN %s AND %s
                        GROUP BY
                            storefront_keyword_a.keyword_id,
                            storefront_keyword_a.storefront_id
                    ) storefront_keyword_a 
                        ON (storefront_keyword_a.keyword_id = keyword.id)
                        AND storefront_keyword_a.storefront_id = storefront.id
                        AND storefront_keyword_a.timing = 'daily'
                WHERE true
                    AND storefront_keyword.keyword_type != 'irrelevant'
                    and storefront.ads_ops_storefront_id IN ({storefront_placeholders})
                    and workspace_id = %s
                GROUP BY storefront_keyword.id,storefront_workspace.workspace_id,storefront_workspace.storefront_id
                HAVING
                    (
                        MAX(storefront_keyword.keyword_type) != 'irrelevant'
                        and SUM(storefront_keyword_a.est_daily_search_volume) > '0'
                        and MAX(storefront.ads_ops_storefront_id) IN ({storefront_placeholders})
                        and MAX(workspace_id) = %s
                    )
            )
        SELECT
            marketplace_code,
            country_code,
            storefront_id,
            storefront_name,
            keyword,keyword_id,
            keyword_type,
            brand_name,
            category_name,
            tag_1,tag_2,
            operational_status,
            
            function,
            storefront_division,
            active_skus,
            note_1,note_2,

            peak_day_ads_gmv,
            peak_day_bau_ads_gmv,
            SUM(daily_search_volume) AS total_daily_search_volume,
            AVG(suggested_bidding_price) AS avg_suggested_bidding_price,
            current_avg_bidding_price,
            SUM(ads_gmv) AS total_ads_gmv,
            AVG(roas) AS avg_roas,
            SUM(cost) AS total_cost,
            SUM(ads_item_sold) AS total_ads_item_sold,
            AVG(cpc) AS avg_cpc,
            AVG(ctr) AS avg_ctr,
            SUM(click) AS total_clicks,
            AVG(cr) AS avg_cr,
            SUM(impression) AS total_impressions
        FROM main_query
        GROUP BY keyword_id,workspace_id,workspace_storefront_id
        limit 10
    """
}

def get_query(query_name, storefront_placeholders):
    """
    Get a query by name and format it with storefront placeholders
    
    Args:
        query_name (str): Name of the query to retrieve ('count' or 'data')
        storefront_placeholders (str): Placeholder string for storefront IDs (e.g., '%s, %s')
        
    Returns:
        str: Formatted SQL query
    """
    return query_params[query_name].format(storefront_placeholders=storefront_placeholders)


