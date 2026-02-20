"""
LIVE NSE UNIVERSE INGESTION ENGINE
Production-Grade NSE Listed Equity Universe Auto Fetcher
"""

import os
import requests
import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

NSE_UNIVERSE_URL = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
OUTPUT_FILE = "data/nse_live_universe.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}

def ensure_data_directory():
    if not os.path.exists("data"):
        os.makedirs("data")

def download_nse_universe():
    logging.info("Downloading NSE Equity Universe...")
    response = requests.get(NSE_UNIVERSE_URL, headers=HEADERS, timeout=30)
    response.raise_for_status()

    with open(OUTPUT_FILE, "wb") as f:
        f.write(response.content)

    logging.info("Download completed")

def clean_universe():
    df = pd.read_csv(OUTPUT_FILE)
    df.columns = [c.strip().lower() for c in df.columns]

    df = df[df["series"] == "EQ"]
    df.rename(columns={"name of company": "company_name"}, inplace=True)
    df["ingestion_time"] = datetime.utcnow()

    df.to_csv(OUTPUT_FILE, index=False)
    logging.info(f"Universe ready. Total stocks: {len(df)}")

def run_live_nse_universe_ingestion():
    ensure_data_directory()
    download_nse_universe()
    clean_universe()

# DISABLED ENTRY POINT
# if __name__ == "__main__":
    run_live_nse_universe_ingestion()
