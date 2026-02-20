"""
ULTIMATE BRAIN
NSE UNIVERSE INGESTION ENGINE
Deterministic + Production Safe
"""

import csv
import requests
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UNIVERSE_PATH = PROJECT_ROOT / "data" / "universe"

NSE_UNIVERSE_URL = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"

class NSEUniverseEngine:

    def __init__(self):
        UNIVERSE_PATH.mkdir(parents=True, exist_ok=True)
        self.output_file = UNIVERSE_PATH / "nse_universe.csv"

    def fetch_universe(self):

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(NSE_UNIVERSE_URL, headers=headers, timeout=10)

        if response.status_code != 200:
            raise RuntimeError(f"NSE fetch failed: {response.status_code}")

        lines = response.text.splitlines()
        reader = csv.DictReader(lines)

        required_columns = ["SYMBOL"]

        if not all(col in reader.fieldnames for col in required_columns):
            raise RuntimeError("Unexpected NSE universe schema")

        symbols = []

        for row in reader:
            symbol = row["SYMBOL"].strip()
            if symbol and symbol.isalpha():
                symbols.append(symbol)

        if not symbols:
            raise RuntimeError("No symbols extracted from NSE file")

        with open(self.output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["symbol"])
            for s in sorted(set(symbols)):
                writer.writerow([s])

        return len(symbols)


if __name__ == "__main__":
    engine = NSEUniverseEngine()
    count = engine.fetch_universe()
    print(f"NSE Universe Updated | Total Symbols: {count}")
