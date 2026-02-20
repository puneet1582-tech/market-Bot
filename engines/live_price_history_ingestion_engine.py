"""
LIVE PRICE HISTORY INGESTION ENGINE
Downloads full historical + daily price data for entire NSE universe
Institutional-grade ingestion layer
"""

import pandas as pd
import yfinance as yf
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)

UNIVERSE_FILE = "data/nse_live_universe.csv"
OUTPUT_FILE = "data/nse_price_history.csv"

def load_symbols():
    df = pd.read_csv(UNIVERSE_FILE)
    return [s + ".NS" for s in df["symbol"].tolist()]

def download_symbol(symbol):
    try:
        df = yf.download(symbol, period="max", progress=False)
        df["symbol"] = symbol.replace(".NS","")
        return df
    except:
        return None

def run_price_ingestion():
    logging.info("Loading NSE universe")
    symbols = load_symbols()

    logging.info(f"Downloading price history for {len(symbols)} symbols")

    all_data = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(download_symbol, symbols)

        for r in results:
            if r is not None:
                all_data.append(r)

    if len(all_data) == 0:
        logging.error("No data downloaded")
        return

    final_df = pd.concat(all_data)
    final_df["ingestion_time"] = datetime.utcnow()

    final_df.to_csv(OUTPUT_FILE)

    logging.info("PRICE HISTORY INGESTION COMPLETED")

# DISABLED ENTRY POINT
# # DISABLED ENTRY POINT
    run_price_ingestion()
