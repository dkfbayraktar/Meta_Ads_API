# Meta Ads API ile günlük ve saatlik verileri çeken yardımcı fonksiyonları içerir.

import requests
from config import GRAPH_API_BASE, GRAPH_API_VERSION


def fetch_ad_level_insights(token, date):
    """
    Belirtilen tarih için ad-level (reklam bazlı) performans verilerini çeker.
    """
    endpoint = f"{GRAPH_API_BASE}/{GRAPH_API_VERSION}/act_679253881166774/insights"
    params = {
        "level": "ad",
        "fields": "ad_id,ad_name,campaign_name,effective_status,spend,impressions,clicks,cpc,ctr",
        "time_range": {"since": date, "until": date},
        "access_token": token
    }

    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    return response.json().get("data", [])


# Eksik olan fetch_hourly_insights fonksiyonu buraya eklenecek

def fetch_hourly_insights(token, date):
    """
    Belirtilen tarih için campaign-level saatlik performans verilerini çeker.
    """
    endpoint = f"{GRAPH_API_BASE}/{GRAPH_API_VERSION}/act_679253881166774/insights"
    params = {
        "level": "campaign",
        "fields": "campaign_name,effective_status,spend,impressions,clicks,cpc,ctr",
        "time_range": {"since": date, "until": date},
        "time_increment": "hourly",
        "access_token": token
    }

    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    return response.json().get("data", [])
