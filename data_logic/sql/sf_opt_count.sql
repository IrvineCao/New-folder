    select count(1) 
    from(select 1
    from kw_discovery_storefront_workspace workspace
    join onsite_storefront ON onsite_storefront.id = workspace.storefront_id
    join ads_ops_storefront on onsite_storefront.ads_ops_storefront_id = ads_ops_storefront.id
    join dashboard_ads on dashboard_ads.storefront_id = ads_ops_storefront.id
        and date(dashboard_ads.created_datetime) between :start_date and :end_date
    join global_company on ads_ops_storefront.global_company_id = global_company.id
    where workspace.workspace_id = :workspace_id
    and ads_ops_storefront.id in :storefront_ids
    group by onsite_storefront.id)