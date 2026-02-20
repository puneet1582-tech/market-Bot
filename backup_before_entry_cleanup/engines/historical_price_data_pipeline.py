"""
Ultimate Brain — Historical Price Data Pipeline
Downloads 10+ year historical price data for NSE universe symbols.
"""

import yfinance as yf
import pandas as pd
import os
from datetime import datetime

UNIVERSE_FILE = "nse_universe_master.csv"
OUTPUT_DIR = "data/price_history"


def load_symbols():
    df = pd.read_csv(UNIVERSE_FILE)
    return df["SYMBOL_NS"].dropna().tolist()


def ensure_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def download_symbol(symbol):
    try:
        data = yf.download(symbol, period="10y", interval="1d", progress=False)
        if data.empty:
            return False

        filepath = os.path.join(OUTPUT_DIR, f"{symbol}.csv")
        data.to_csv(filepath)
        return True
    except Exception:
        return False


def run_pipeline():
    ensure_dir()
    symbols = load_symbols()

    success = 0
    for s in symbols:
        if download_symbol(s):
            success += 1

    return {
        "timestamp": str(datetime.utcnow()),
        "total_symbols": len(symbols),
        "downloaded": success
    }


# DISABLED ENTRY POINT
# if __name__ == "__main__":
    print(run_pipeline())
