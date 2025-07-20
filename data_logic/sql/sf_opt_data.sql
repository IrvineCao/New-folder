    select 
        global_company.name as company_name,
        dashboard_ads.storefront_id,
        ads_ops_storefront.name as storefront_name,
        ads_ops_storefront.country_code,
        ads_ops_storefront.marketplace_code,
        sum(gmv) as gmv,
        sum(cost) as cost,
        sum(gmv/cost) as roas,
        sum(cost/click) as cpc,
        sum(click) as click,
        sum(impression) as impression,
        sum(ads_order) as ads_order,
        sum(direct_gmv) as direct_gmv,
        sum(direct_ads_order) as direct_ads_order,
        sum(direct_item_sold) as direct_item_sold,
        sum(item_sold) as item_sold
    from kw_discovery_storefront_workspace workspace
    join onsite_storefront ON onsite_storefront.id = workspace.storefront_id
    join ads_ops_storefront on onsite_storefront.ads_ops_storefront_id = ads_ops_storefront.id
    join dashboard_ads on dashboard_ads.storefront_id = ads_ops_storefront.id
        and date(dashboard_ads.created_datetime) between :start_date and :end_date
    join global_company on ads_ops_storefront.global_company_id = global_company.id
    where workspace.workspace_id = :workspace_id
    and ads_ops_storefront.id in :storefront_ids
    group by onsite_storefront.id