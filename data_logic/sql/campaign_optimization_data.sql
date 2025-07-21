select 
    camp.general_tag as campaign_tag,
    camp.country_code,
    camp.marketplace_code,
    storefront.name as storefront_name,
    camp.tool_code,
    camp.name as campaign_name,
    camp.note as campaign_note,
    camp.status as campaign_status,
    camp.target as campaign_target,
    camp.objective as campaign_objective,
    camp.ads_status as campaign_ads_status,
    camp.budget_distributed_method as campaign_budget_distributed_method,
    camp.daily_budget as campaign_daily_budget,
    camp.assessment as campaign_assessment,
    concat(date(camp.timeline_from)," - ",date(camp.timeline_to)) as campaign_timeline,
    camp.first_search_slot,
    camp.max_bidding_price,
    sum(pfm.click) as campaign_clicks,
    sum(pfm.impression) as campaign_impressions,
    sum(pfm.click / pfm.impression) as campaign_cpc,
    sum(pfm.ads_gmv / pfm.cost) as campaign_roas,
    sum(pfm.cost / pfm.click) as cpc,
    sum(pfm.ads_gmv) as campaign_gmv,
    sum(pfm.cost) as campaign_cost
from kw_discovery_storefront_workspace workspace
join onsite_storefront ON onsite_storefront.id = workspace.storefront_id
join ads_ops_storefront storefront on onsite_storefront.ads_ops_storefront_id = storefront.id
join ads_ops_ads_campaigns camp on camp.storefront_id = storefront.id
left join ads_ops_ads_campaigns_performance pfm on pfm.ads_campaign_id = camp.id
    and date(pfm.created_datetime) between :start_date and :end_date
join global_company on storefront.global_company_id = global_company.id
where workspace.workspace_id = :workspace_id
and storefront.id in (:storefront_ids)
group by camp.id