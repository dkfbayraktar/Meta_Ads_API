# Meta Ads API ile günlük ve saatlik verileri çeken yardımcı fonksiyonları içerir.

import requests
from config import GRAPH_API_BASE, GRAPH_API_VERSION, AD_ACCOUNTS


def fetch_ad_level_insights(token, date):
    """
    Tüm tanımlı reklam hesapları için ad bazında performans verilerini çeker ve her reklamın sayfa kimliğini ve adını ekler.
    """
    all_data = []

    for account_key, account_info in AD_ACCOUNTS.items():
        ad_account_id = account_info["id"]
        ad_account_name = account_info["name"]

        insights_endpoint = f"{GRAPH_API_BASE}/{GRAPH_API_VERSION}/act_{ad_account_id}/insights"
        insights_params = {
            "level": "ad",
            "fields": "ad_id,ad_name,campaign_name,effective_status,spend,impressions,clicks,cpc,ctr,actions",
            "breakdowns": "age,gender,country,region,platform_position,publisher_platform",
            "time_range": {"since": date, "until": date},
            "access_token": token
        }

        insights_response = requests.get(insights_endpoint, params=insights_params)
        if insights_response.status_code != 200:
            continue

        data = insights_response.json().get("data", [])

        for record in data:
            ad_id = record.get("ad_id")
            if not ad_id:
                continue

            # Ad creative üzerinden page_id alma
            creative_endpoint = f"{GRAPH_API_BASE}/{GRAPH_API_VERSION}/{ad_id}?fields=adcreatives{object_story_spec}"
            creative_params = {"access_token": token}
            creative_response = requests.get(creative_endpoint, params=creative_params)
            if creative_response.status_code != 200:
                continue

            try:
                creatives = creative_response.json().get("adcreatives", {}).get("data", [])
                if creatives:
                    object_story_spec = creatives[0].get("object_story_spec", {})
                    page_id = object_story_spec.get("page_id")
                    record["page_id"] = page_id

                    # Page adını getir
                    if page_id:
                        page_endpoint = f"{GRAPH_API_BASE}/{GRAPH_API_VERSION}/{page_id}?fields=name"
                        page_response = requests.get(page_endpoint, params=creative_params)
                        if page_response.status_code == 200:
                            record["page_name"] = page_response.json().get("name")
            except Exception:
                continue

            # CPM (Cost per Mille) hesapla
            try:
                spend = float(record.get("spend", 0))
                impressions = int(record.get("impressions", 0))
                if impressions > 0:
                    record["cpm"] = round((spend / impressions) * 1000, 4)
                else:
                    record["cpm"] = None
            except (ValueError, TypeError):
                record["cpm"] = None

            # Actions: Purchase, AddToCart, InitiateCheckout
            record["purchases"] = 0
            record["add_to_cart"] = 0
            record["initiate_checkout"] = 0
            for action in record.get("actions", []):
                try:
                    value = int(float(action.get("value", 0)))
                except (ValueError, TypeError):
                    value = 0

                if action.get("action_type") == "offsite_conversion.purchase":
                    record["purchases"] = value
                elif action.get("action_type") == "add_to_cart":
                    record["add_to_cart"] = value
                elif action.get("action_type") == "initiate_checkout":
                    record["initiate_checkout"] = value

            # Conversion Rate hesapla: purchases / clicks
            try:
                clicks = int(record.get("clicks", 0))
                purchases = int(record.get("purchases", 0))
                if clicks > 0:
                    record["conversion_rate"] = round((purchases / clicks) * 100, 2)
                else:
                    record["conversion_rate"] = None
            except (ValueError, TypeError):
                record["conversion_rate"] = None

            # Funnel Conversion Rate: (purchases / (add_to_cart + initiate_checkout + purchases)) * 100
            try:
                funnel_total = sum([
                    int(record.get("add_to_cart", 0)),
                    int(record.get("initiate_checkout", 0)),
                    int(record.get("purchases", 0))
                ])
                if funnel_total > 0:
                    record["funnel_conversion_rate"] = round((record["purchases"] / funnel_total) * 100, 2)
                else:
                    record["funnel_conversion_rate"] = None
            except (ValueError, TypeError):
                record["funnel_conversion_rate"] = None

            # Cost Per Purchase (spend / purchases)
            try:
                purchases = int(record.get("purchases", 0))
                if purchases > 0:
                    record["cost_per_purchase"] = round(spend / purchases, 2)
                else:
                    record["cost_per_purchase"] = None
            except (ValueError, TypeError):
                record["cost_per_purchase"] = None

            record["ad_account_id"] = ad_account_id
            record["ad_account_name"] = ad_account_name
            all_data.append(record)

    return all_data
