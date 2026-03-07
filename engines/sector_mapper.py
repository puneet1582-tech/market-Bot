import pandas as pd
import logging
logging.basicConfig(level=logging.INFO)

def map_news_to_sectors(news_df=None):
    logging.info("SECTOR MAPPING EXECUTED")
    return pd.DataFrame()


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
