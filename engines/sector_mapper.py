"""
SECTOR MAPPER ENGINE
Maps incoming news / signals to sectors
Production Compatibility Wrapper
"""

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

SECTOR_MAP_FILE = "data/sector_map.csv"


def load_sector_map():
    try:
        return pd.read_csv(SECTOR_MAP_FILE)
    except Exception as e:
        logging.error(f"Sector map load failed: {e}")
        return pd.DataFrame()


def map_news_to_sectors(news_df=None):
    """
    Compatibility function required by global intelligence integration
    """

    sector_map = load_sector_map()

    if news_df is None or sector_map.empty:
        logging.warning("News or sector map missing. Returning empty mapping.")
        return pd.DataFrame()

    # Example merge logic
    try:
        mapped = news_df.merge(sector_map, how="left", on="symbol")
        return mapped
    except Exception as e:
        logging.error(f"Sector mapping failed: {e}")
        return pd.DataFrame()
