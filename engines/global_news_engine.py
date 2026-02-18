"""
GLOBAL NEWS ENGINE
Compatibility Execution Wrapper
"""

import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)

NEWS_FILE = "data/news.csv"


def run_global_news_engine():
    """
    Master Brain compatible global news execution
    """

    logging.info("GLOBAL NEWS ENGINE STARTED")

    try:
        news_df = pd.read_csv(NEWS_FILE)
        logging.info(f"Loaded {len(news_df)} global news records")
    except Exception as e:
        logging.warning(f"News data load failed: {e}")

    logging.info("GLOBAL NEWS ENGINE COMPLETED")
