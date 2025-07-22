WITH filtered_storefront_data AS (
    SELECT
        storefront_a.created_datetime,
        storefront_a.keyword_id,
        storefront_a.storefront_id,
        storefront_a.display_type AS display_type,
        storefront_a.product_position AS product_position,
        storefront_a.device_type AS device_type,
        AVG(storefront_a.share_of_search) AS share_of_search,
        AVG(storefront_a.search_volume) AS search_volume
    FROM metric_share_of_search_storefront AS storefront_a
    WHERE storefront_a.timing = 'daily'
        AND (:device_type is null or storefront_a.device_type = :device_type)
        AND (:display_type is null or storefront_a.display_type = :display_type)
        AND (:product_position is null or storefront_a.product_position = :product_position)
        AND storefront_a.created_datetime BETWEEN :start_date AND :end_date
    GROUP BY
        storefront_a.created_datetime,
        storefront_a.keyword_id,
        storefront_a.storefront_id,
        storefront_a.display_type,
        storefront_a.product_position,
        storefront_a.device_type
),
main_query AS (
    SELECT
        gc.name AS global_company_name,
        sf.storefront_name,
        sf.storefront_sid,
        sf.udc__search_group_tag,
        sf.id AS storefront_id,
        sf.storefront_type,
        sf.shop_created_at,
        ws.id AS workspace_id,
        k.keyword,
        k.marketplace_name,
        k.country_name,
        fsa.device_type,
        fsa.display_type,
        fsa.product_position,
        fsa.search_volume,
        fsa.share_of_search,
        CAST(fsa.created_datetime AS DATETIME) AS created_datetime
    FROM passport_workspace AS ws
    INNER JOIN onsite_keyword_workspace AS kw_ws 
        ON kw_ws.workspace_id = ws.id
    INNER JOIN onsite_keyword_sharded AS k 
        ON k.id = kw_ws.keyword_id
    INNER JOIN filtered_storefront_data AS fsa 
        ON fsa.keyword_id = k.id
    INNER JOIN onsite_storefront AS sf 
        ON sf.id = fsa.storefront_id
    LEFT JOIN global_company AS gc 
        ON gc.id = sf.global_company_id
    WHERE ws.id = :workspace_id
)

SELECT
    global_company_name,
    AVG(search_volume) AS search_volume,
    AVG(share_of_search) AS share_of_search,
    storefront_name,
    created_datetime,
    marketplace_name,
    keyword,
    display_type,
    product_position,
    device_type
FROM main_query
GROUP BY
    global_company_name,
    storefront_name,
    created_datetime,
    marketplace_name,
    keyword,
    display_type,
    product_position,
    device_type
HAVING created_datetime IS NOT NULL
ORDER BY created_datetime,keyword