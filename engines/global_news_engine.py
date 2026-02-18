import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
NEWS_FILE = "data/news.csv"

def fetch_global_news():
    try:
        return pd.read_csv(NEWS_FILE)
    except:
        return pd.DataFrame()

def run_global_news_engine():
    logging.info("GLOBAL NEWS ENGINE EXECUTED")
    fetch_global_news()
