"""
ULTIMATE BRAIN
NSE OFFICIAL BHAVCOPY ENGINE
Deterministic Historical Builder
"""

import requests
import zipfile
import io
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw_bhavcopy"
PRICE_PATH = PROJECT_ROOT / "data" / "prices"
UNIVERSE_FILE = PROJECT_ROOT / "data" / "universe" / "nse_universe.csv"

BASE_URL = "https://archives.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{date}bhav.csv.zip"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9"
}

START_DATE = datetime.utcnow() - timedelta(days=365*2)   # 2 years initial test
END_DATE = datetime.utcnow()


class NSEBhavcopyEngine:

    def __init__(self):
        RAW_PATH.mkdir(parents=True, exist_ok=True)
        PRICE_PATH.mkdir(parents=True, exist_ok=True)
        self.output_file = PRICE_PATH / "historical_prices.csv"

    def load_universe(self):
        df = pd.read_csv(UNIVERSE_FILE)
        return set(df["symbol"].dropna().unique())

    def download_bhavcopy(self, date):
        date_str = date.strftime("%d%b%Y").upper()
        year = date.strftime("%Y")
        month = date.strftime("%b").upper()

        url = BASE_URL.format(year=year, month=month, date=date_str)

        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code != 200:
                return None

            z = zipfile.ZipFile(io.BytesIO(r.content))
            file_name = z.namelist()[0]
            df = pd.read_csv(z.open(file_name))
            return df
        except:
            return None

    def run(self):

        universe = self.load_universe()
        all_rows = []

        current_date = START_DATE

        for _ in tqdm(range((END_DATE - START_DATE).days)):
            df = self.download_bhavcopy(current_date)

            if df is not None and "SYMBOL" in df.columns:
                df = df[df["SYMBOL"].isin(universe)]

                for _, row in df.iterrows():
                    all_rows.append({
                        "date": current_date.strftime("%Y-%m-%d"),
                        "symbol": row["SYMBOL"],
                        "price": row["CLOSE"]
                    })

            current_date += timedelta(days=1)

        if not all_rows:
            raise RuntimeError("No bhavcopy data fetched")

        out_df = pd.DataFrame(all_rows)
        out_df.to_csv(self.output_file, index=False)

        return len(all_rows)


if __name__ == "__main__":
    engine = NSEBhavcopyEngine()
    count = engine.run()
    print(f"Bhavcopy Historical Stored | Rows: {count}")
