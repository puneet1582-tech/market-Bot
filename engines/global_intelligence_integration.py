"""
Ultimate Brain — Global Intelligence Integration Layer
Phase-2 Integration Module
"""

from engines.global_news_engine import fetch_global_news
from engines.sector_mapper import map_news_to_sectors


def global_intelligence_snapshot():
    news = fetch_global_news()
    sector_impact = map_news_to_sectors(news)

    return {
        "news": news,
        "sector_impact": sector_impact
    }
