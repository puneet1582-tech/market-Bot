"""
ULTIMATE BRAIN
HISTORICAL PRICE INGESTION ENGINE
Yahoo Finance Based
10-Year Daily Data
Long Format: date,symbol,price
"""

import csv
import requests
import time
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UNIVERSE_FILE = PROJECT_ROOT / "data" / "universe" / "nse_universe.csv"
PRICE_PATH = PROJECT_ROOT / "data" / "prices"

START_DATE = "2014-01-01"
END_DATE = datetime.utcnow().strftime("%Y-%m-%d")

def date_to_unix(date_str):
    return int(datetime.strptime(date_str, "%Y-%m-%d").timestamp())

class HistoricalPriceEngine:

    def __init__(self):
        PRICE_PATH.mkdir(parents=True, exist_ok=True)
        self.output_file = PRICE_PATH / "historical_prices.csv"

    def load_universe(self):
        if not UNIVERSE_FILE.exists():
            raise RuntimeError("Universe file missing")

        symbols = []
        with open(UNIVERSE_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                symbols.append(row["symbol"].strip())

        if not symbols:
            raise RuntimeError("Universe empty")

        return symbols[:50]  # limit first 50 for stability (expand later)

    def fetch_symbol_data(self, symbol):
        period1 = date_to_unix(START_DATE)
        period2 = date_to_unix(END_DATE)

        url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}.NS?period1={period1}&period2={period2}&interval=1d&events=history"

        response = requests.get(url, timeout=15)

        if response.status_code != 200:
            return []

        lines = response.text.splitlines()
        reader = csv.DictReader(lines)

        rows = []

        for row in reader:
            if row["Close"] and row["Date"]:
                rows.append({
                    "date": row["Date"],
                    "symbol": symbol,
                    "price": row["Close"]
                })

        return rows

    def run(self):

        symbols = self.load_universe()

        all_rows = []

        for symbol in symbols:
            try:
                data = self.fetch_symbol_data(symbol)
                all_rows.extend(data)
                time.sleep(0.5)
            except:
                continue

        if not all_rows:
            raise RuntimeError("No historical data fetched")

        with open(self.output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["date", "symbol", "price"])
            writer.writeheader()
            writer.writerows(all_rows)

        return len(all_rows)


if __name__ == "__main__":
    engine = HistoricalPriceEngine()
    count = engine.run()
    print(f"Historical Data Stored | Rows: {count}")
