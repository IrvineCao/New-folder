select count(1)
from (select 1
from kw_discovery_storefront_workspace workspace
join onsite_storefront ON onsite_storefront.id = workspace.storefront_id
join ads_ops_storefront storefront on onsite_storefront.ads_ops_storefront_id = storefront.id
join ads_ops_ads_campaigns camp on camp.storefront_id = storefront.id
left join ads_ops_ads_campaigns_performance pfm on pfm.ads_campaign_id = camp.id
    and date(pfm.created_datetime) between :start_date and :end_date
join global_company on storefront.global_company_id = global_company.id
where workspace.workspace_id = :workspace_id
and storefront.id in (:storefront_ids)
group by camp.id)