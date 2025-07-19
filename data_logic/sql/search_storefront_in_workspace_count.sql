SELECT COUNT(1)
FROM onsite_storefront sf
JOIN kw_discovery_storefront_workspace sfw ON sf.id = sfw.storefront_id
WHERE sfw.workspace_id = :workspace_id
AND sf.ads_ops_storefront_id IS NOT NULL 