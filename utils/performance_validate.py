# data_logic/performance_validation_data.py

from utils.config import PROJECT_ROOT
import streamlit as st

def _get_query_from_file(file_path: str) -> str:
    """Helper function to read SQL file safely."""
    path = PROJECT_ROOT / "data_logic" / "sql" / file_path
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError as e:
        st.error(f"Query file not found: {path.resolve()}")
        raise e

# Multi-level performance query
PERFORMANCE_QUERY = """
WITH campaign_performance AS (
    SELECT
        camp.storefront_id,
        'campaign' as level,
        MONTH(perf.created_datetime) as month,
        SUM(perf.impression) as impressions,
        SUM(perf.click) as clicks,
        SUM(perf.ads_gmv) as gmv,
        SUM(perf.cost) as expense,
        CASE 
            WHEN SUM(perf.cost) > 0 THEN SUM(perf.ads_gmv) / SUM(perf.cost)
            ELSE 0 
        END as roas
    FROM ads_ops_ads_campaigns camp
    INNER JOIN ads_ops_ads_campaigns_performance perf 
        ON camp.id = perf.ads_campaign_id
    WHERE camp.storefront_id IN :storefront_ids
        AND MONTH(perf.created_datetime) IN :months
    GROUP BY camp.storefront_id, MONTH(perf.created_datetime)
), 

object_performance AS (
    SELECT
        obj.storefront_id,
        'object' as level,
        MONTH(perf.created_datetime) as month,
        SUM(perf.impression) as impressions,
        SUM(perf.click) as clicks,
        SUM(perf.ads_gmv) as gmv,
        SUM(perf.cost) as expense,
        CASE 
            WHEN SUM(perf.cost) > 0 THEN SUM(perf.ads_gmv) / SUM(perf.cost)
            ELSE 0 
        END as roas
    FROM ads_ops_ads_objects obj
    INNER JOIN ads_ops_ads_objects_performance perf 
        ON obj.id = perf.ads_object_id
    WHERE obj.storefront_id IN :storefront_ids
        AND MONTH(perf.created_datetime) IN :months
    GROUP BY obj.storefront_id, MONTH(perf.created_datetime)
),

placement_performance AS (
    SELECT
        pl.storefront_id,
        'placement' as level,
        MONTH(perf.created_datetime) as month,
        SUM(perf.impression) as impressions,
        SUM(perf.click) as clicks,
        SUM(perf.ads_gmv) as gmv,
        SUM(perf.cost) as expense,
        CASE 
            WHEN SUM(perf.cost) > 0 THEN SUM(perf.ads_gmv) / SUM(perf.cost)
            ELSE 0 
        END as roas
    FROM ads_ops_ads_placements pl
    INNER JOIN ads_ops_ads_placements_performance perf 
        ON pl.id = perf.ads_placement_id
    WHERE pl.storefront_id IN :storefront_ids
        AND MONTH(perf.created_datetime) IN :months
        AND perf.timing = 'daily'
    GROUP BY pl.storefront_id, MONTH(perf.created_datetime)
),

unified_performance AS (
    SELECT * FROM campaign_performance
    UNION ALL
    SELECT * FROM object_performance
    UNION ALL
    SELECT * FROM placement_performance
)

SELECT 
    storefront_id,
    CASE 
        WHEN :aggregate_levels = true THEN 'aggregated'
        ELSE level 
    END as level,
    month,
    CASE 
        WHEN :aggregate_levels = true THEN SUM(impressions)
        ELSE impressions 
    END as impressions,
    CASE 
        WHEN :aggregate_levels = true THEN SUM(clicks)
        ELSE clicks 
    END as clicks,
    CASE 
        WHEN :aggregate_levels = true THEN SUM(gmv)
        ELSE gmv 
    END as gmv,
    CASE 
        WHEN :aggregate_levels = true THEN SUM(expense)
        ELSE expense 
    END as expense,
    CASE 
        WHEN :aggregate_levels = true AND SUM(expense) > 0 THEN SUM(gmv) / SUM(expense)
        WHEN :aggregate_levels = false THEN roas
        ELSE 0 
    END as roas
FROM unified_performance
GROUP BY 
    storefront_id,
    month,
    CASE 
        WHEN :aggregate_levels = true THEN 'aggregated'
        ELSE level 
    END
ORDER BY storefront_id, month, level
"""

# Count query for validation
COUNT_QUERY = """
WITH campaign_count AS (
    SELECT COUNT(DISTINCT CONCAT(camp.storefront_id, '-', MONTH(perf.created_datetime))) as cnt
    FROM ads_ops_ads_campaigns camp
    INNER JOIN ads_ops_ads_campaigns_performance perf ON camp.id = perf.ads_campaign_id
    WHERE camp.storefront_id IN :storefront_ids AND MONTH(perf.created_datetime) IN :months
),
object_count AS (
    SELECT COUNT(DISTINCT CONCAT(obj.storefront_id, '-', MONTH(perf.created_datetime))) as cnt
    FROM ads_ops_ads_objects obj
    INNER JOIN ads_ops_ads_objects_performance perf ON obj.id = perf.ads_object_id
    WHERE obj.storefront_id IN :storefront_ids AND MONTH(perf.created_datetime) IN :months
),
placement_count AS (
    SELECT COUNT(DISTINCT CONCAT(pl.storefront_id, '-', MONTH(perf.created_datetime))) as cnt
    FROM ads_ops_ads_placements pl
    INNER JOIN ads_ops_ads_placements_performance perf ON pl.id = perf.ads_placement_id
    WHERE pl.storefront_id IN :storefront_ids AND MONTH(perf.created_datetime) IN :months
        AND perf.timing = 'daily'
)
SELECT 
    CASE 
        WHEN :aggregate_levels = true THEN (
            SELECT COUNT(DISTINCT CONCAT(storefront_id, '-', month))
            FROM (
                SELECT storefront_id, month FROM (SELECT 1) dummy
                CROSS JOIN (SELECT UNNEST(:storefront_ids) as storefront_id) sf
                CROSS JOIN (SELECT UNNEST(:months) as month) mn
            ) combinations
        )
        ELSE (
            COALESCE((SELECT cnt FROM campaign_count), 0) +
            COALESCE((SELECT cnt FROM object_count), 0) +
            COALESCE((SELECT cnt FROM placement_count), 0)
        )
    END as total_count
"""

query_params = {
    "data": PERFORMANCE_QUERY,
    "count": COUNT_QUERY
}

def get_query(query_name: str) -> str:
    """Gets a query by name from the pre-loaded dictionary."""
    return query_params.get(query_name, "")

# Helper function to build dynamic parameters
def build_validation_params(storefront_ids, months, level_filter=None, aggregate_levels=False):
    """
    Build parameters for performance validation query.
    
    Args:
        storefront_ids: List of storefront IDs
        months: List of month numbers (1-12)
        level_filter: 'campaign', 'object', 'placement', or None for all
        aggregate_levels: True to sum all levels, False to keep separate
    
    Returns:
        Dictionary of query parameters
    """
    return {
        "storefront_ids": storefront_ids,
        "months": months,
        "level_filter": level_filter,
        "aggregate_levels": aggregate_levels
    }