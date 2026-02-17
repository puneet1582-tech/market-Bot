"""
Ultimate Brain — Global Intelligence Engine
Institutional Grade Module
Handles global news ingestion and sector impact mapping
"""

import logging
from engines.global_news_engine import fetch_global_news
from engines.sector_mapper import map_news_to_sectors

logger = logging.getLogger("GlobalIntelligence")


class GlobalIntelligenceEngine:

    def __init__(self):
        self.last_snapshot = None

    def generate_snapshot(self):
        try:
            news = fetch_global_news()
            sector_impact = map_news_to_sectors(news)

            snapshot = {
                "news": news,
                "sector_impact": sector_impact
            }

            self.last_snapshot = snapshot
            return snapshot

        except Exception as e:
            logger.exception("Global Intelligence Failure")
            return self.last_snapshot or {
                "news": [],
                "sector_impact": {}
            }
