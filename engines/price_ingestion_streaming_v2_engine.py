"""
PRICE INGESTION STREAMING V2 ENGINE
Production-Grade | Memory Safe | Resume Capable | Streaming Writer

- Downloads 60 day daily price data
- Writes symbol-by-symbol (no giant concat)
- Resume safe (skips already processed symbols)
- Low memory footprint
"""

import os
import logging
import pandas as pd
import yfinance as yf
from datetime import datetime
from time import sleep

logging.basicConfig(level=logging.INFO)

UNIVERSE_FILE = "data/nse_live_universe.csv"
OUTPUT_FILE = "data/nse_price_history.csv"
FAILED_FILE = "data/price_failed_symbols.csv"

BATCH_SLEEP = 0.2  # rate limit safety


def load_universe():
    df = pd.read_csv(UNIVERSE_FILE)
    return df["symbol"].dropna().unique().tolist()


def load_processed_symbols():
    if not os.path.exists(OUTPUT_FILE):
        return set()

    try:
        df = pd.read_csv(OUTPUT_FILE, usecols=["symbol"])
        return set(df["symbol"].unique())
    except Exception:
        return set()


def append_to_csv(df):
    write_header = not os.path.exists(OUTPUT_FILE)
    df.to_csv(OUTPUT_FILE, mode="a", header=write_header, index=False)


def log_failed(symbol):
    with open(FAILED_FILE, "a") as f:
        f.write(symbol + "\n")


def download_symbol(symbol):
    try:
        ticker = symbol + ".NS"
        data = yf.download(ticker, period="60d", interval="1d", progress=False)

        if data.empty:
            return None

        data.reset_index(inplace=True)

        data["symbol"] = symbol
        data["ingestion_time"] = datetime.utcnow()

        data = data[["Date", "Open", "High", "Low", "Close", "Volume", "symbol", "ingestion_time"]]

        return data

    except Exception as e:
        logging.warning(f"Failed {symbol}: {e}")
        return None


def run_price_ingestion_streaming_v2():

    logging.info("PRICE INGESTION STREAMING V2 STARTED")

    universe = load_universe()
    processed = load_processed_symbols()

    remaining = [s for s in universe if s not in processed]

    logging.info(f"Total universe: {len(universe)}")
    logging.info(f"Already processed: {len(processed)}")
    logging.info(f"Remaining to process: {len(remaining)}")

    for idx, symbol in enumerate(remaining, start=1):

        logging.info(f"[{idx}/{len(remaining)}] Processing {symbol}")

        df = download_symbol(symbol)

        if df is None:
            log_failed(symbol)
            continue

        append_to_csv(df)

        sleep(BATCH_SLEEP)

    logging.info("PRICE INGESTION STREAMING V2 COMPLETED")


if __name__ == "__main__":
    run_price_ingestion_streaming_v2()
