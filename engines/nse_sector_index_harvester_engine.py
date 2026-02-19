"""
NSE SECTOR INDEX HARVESTER ENGINE
Institutional Layer-1 Sector Classification
"""

import os
import requests
import pandas as pd
import logging
from datetime import datetime
from io import StringIO

logging.basicConfig(level=logging.INFO)

OUTPUT_FILE = "data/sector_index_base.csv"

SECTOR_INDEX_URLS = {
    "BANK": "https://archives.nseindia.com/content/indices/ind_niftybanklist.csv",
    "IT": "https://archives.nseindia.com/content/indices/ind_niftyitlist.csv",
    "PHARMA": "https://archives.nseindia.com/content/indices/ind_niftypharmalist.csv",
    "AUTO": "https://archives.nseindia.com/content/indices/ind_niftyautolist.csv",
    "FMCG": "https://archives.nseindia.com/content/indices/ind_niftyfmcglist.csv",
    "METAL": "https://archives.nseindia.com/content/indices/ind_niftymetallist.csv",
    "REALTY": "https://archives.nseindia.com/content/indices/ind_niftyrealtylist.csv",
    "MEDIA": "https://archives.nseindia.com/content/indices/ind_niftymedialist.csv",
    "ENERGY": "https://archives.nseindia.com/content/indices/ind_niftyenergylist.csv"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}


def ensure_data_directory():
    if not os.path.exists("data"):
        os.makedirs("data")


def fetch_sector_index(sector, url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        df = pd.read_csv(StringIO(response.text))
        df.columns = df.columns.str.strip()

        symbol_column = None
        for col in df.columns:
            if col.upper() == "SYMBOL":
                symbol_column = col
                break

        if symbol_column is None:
            logging.warning(f"SYMBOL column not found for {sector}")
            return pd.DataFrame()

        symbols = df[symbol_column].dropna().unique().tolist()

        result = pd.DataFrame({
            "symbol": symbols,
            "sector": sector,
            "source_layer": "NSE_INDEX",
            "computed_time": datetime.utcnow()
        })

        return result

    except Exception as e:
        logging.warning(f"Failed fetching {sector}: {e}")
        return pd.DataFrame()


def run_sector_index_harvester():
    logging.info("NSE SECTOR INDEX HARVESTER STARTED")

    ensure_data_directory()

    all_data = []

    for sector, url in SECTOR_INDEX_URLS.items():
        logging.info(f"Fetching {sector}")
        df = fetch_sector_index(sector, url)
        if not df.empty:
            all_data.append(df)

    if not all_data:
        logging.error("No sector data fetched")
        return

    final_df = pd.concat(all_data, ignore_index=True)
    final_df.drop_duplicates(subset=["symbol"], inplace=True)

    final_df.to_csv(OUTPUT_FILE, index=False)

    logging.info(f"Sector base built. Total classified symbols: {len(final_df)}")


if __name__ == "__main__":
    run_sector_index_harvester()
