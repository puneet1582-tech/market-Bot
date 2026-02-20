"""
Ultimate Brain — Quarterly Fundamentals Auto-Ingestion Pipeline
Downloads quarterly financial statements for NSE symbols and stores them.
"""

import yfinance as yf
import pandas as pd
import os
from datetime import datetime

UNIVERSE_FILE = "nse_universe_master.csv"
OUTPUT_DIR = "data/fundamentals_quarterly"


def load_symbols():
    df = pd.read_csv(UNIVERSE_FILE)
    return df["SYMBOL_NS"].dropna().tolist()


def ensure_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def download_quarterly(symbol):
    try:
        ticker = yf.Ticker(symbol)
        q = ticker.quarterly_financials

        if q is None or q.empty:
            return False

        filepath = os.path.join(OUTPUT_DIR, f"{symbol}.csv")
        q.to_csv(filepath)
        return True
    except Exception:
        return False


def run_pipeline():
    ensure_dir()
    symbols = load_symbols()

    success = 0
    for s in symbols:
        if download_quarterly(s):
            success += 1

    return {
        "timestamp": str(datetime.utcnow()),
        "total_symbols": len(symbols),
        "downloaded": success
    }


# DISABLED ENTRY POINT
# # DISABLED ENTRY POINT
    print(run_pipeline())
