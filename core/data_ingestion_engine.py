"""
ULTIMATE BRAIN
HYBRID DATA INGESTION ENGINE
AUTO + BOOTSTRAP SAFE MODE
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PRICE_DATA_PATH = PROJECT_ROOT / "data" / "prices"

SCHEMA = ["date", "symbol", "price"]


class DataIngestionEngine:

    def __init__(self):
        PRICE_DATA_PATH.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------
    # CHECK IF VALID PRICE FILE EXISTS
    # ---------------------------------------------------
    def valid_price_file_exists(self):
        files = list(PRICE_DATA_PATH.glob("*.csv"))
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if header == SCHEMA:
                    return True
        return False

    # ---------------------------------------------------
    # BOOTSTRAP DATA GENERATOR (DEV SAFE MODE)
    # ---------------------------------------------------
    def generate_bootstrap_data(self):
        file_path = PRICE_DATA_PATH / "bootstrap_prices.csv"

        symbols = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"]
        start_date = datetime.utcnow() - timedelta(days=30)

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(SCHEMA)

            for i in range(30):
                date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
                for symbol in symbols:
                    price = round(random.uniform(100, 3000), 2)
                    writer.writerow([date, symbol, price])

        return f"Bootstrap dataset created: {file_path.name}"

    # ---------------------------------------------------
    # MAIN INGESTION CONTROL
    # ---------------------------------------------------
    def ensure_data_ready(self):

        if self.valid_price_file_exists():
            return "Valid price data detected"

        return self.generate_bootstrap_data()
