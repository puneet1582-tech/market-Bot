"""
PHASE-2 REAL CORE
PRODUCTION PRICE INGESTION ENGINE
60-Day Rolling Institutional Layer
Memory Safe + Batch Controlled
"""

import pandas as pd
import yfinance as yf
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO)

UNIVERSE_FILE = "data/nse_live_universe.csv"
OUTPUT_FILE = "data/nse_price_history.csv"

BATCH_SIZE = 40
MAX_WORKERS = 5


def load_universe():
    df = pd.read_csv(UNIVERSE_FILE)
    symbols = df["symbol"].tolist()
    return [s + ".NS" for s in symbols]


def download_symbol(symbol):
    try:
        df = yf.download(
            symbol,
            period="60d",
            interval="1d",
            progress=False,
            threads=False
        )

        if df.empty:
            return None

        df.reset_index(inplace=True)
        df["symbol"] = symbol.replace(".NS", "")
        df = df[["Date", "symbol", "Close"]]
        df.rename(columns={"Close": "price"}, inplace=True)

        return df

    except Exception as e:
        logging.warning(f"Failed {symbol}: {e}")
        return None


def run_price_ingestion_production():
    logging.info("PRICE INGESTION PRODUCTION STARTED")

    symbols = load_universe()
    total = len(symbols)
    logging.info(f"Total symbols to process: {total}")

    all_data = []

    for i in range(0, total, BATCH_SIZE):
        batch = symbols[i:i + BATCH_SIZE]
        logging.info(f"Processing batch {i} to {i+len(batch)}")

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(download_symbol, s) for s in batch]

            for future in as_completed(futures):
                result = future.result()
                if result is not None:
                    all_data.append(result)

    if not all_data:
        logging.error("No price data downloaded")
        return

    final_df = pd.concat(all_data, ignore_index=True)

    final_df["ingestion_time"] = datetime.utcnow()

    final_df.to_csv(OUTPUT_FILE, index=False)

    logging.info(f"PRICE INGESTION COMPLETED: {len(final_df)} rows written")


# DISABLED ENTRY POINT
# # DISABLED ENTRY POINT
    run_price_ingestion_production()
