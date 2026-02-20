"""
ULTIMATE BRAIN
DAILY INCREMENTAL NSE UPDATER
Duplicate Safe | Production Mode
"""

import requests
import zipfile
import io
import pandas as pd
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PRICE_FILE = PROJECT_ROOT / "data" / "prices" / "historical_prices.csv"
UNIVERSE_FILE = PROJECT_ROOT / "data" / "universe" / "nse_universe.csv"

BASE_URL = "https://archives.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{date}bhav.csv.zip"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9"
}


class NSEIncrementalUpdater:

    def __init__(self):
        if not PRICE_FILE.exists():
            raise RuntimeError("Historical price file missing")
        self.universe = set(pd.read_csv(UNIVERSE_FILE)["symbol"].unique())
        self.price_df = pd.read_csv(PRICE_FILE)

    def last_date(self):
        return pd.to_datetime(self.price_df["date"]).max()

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

        last_available = self.last_date()
        today = datetime.utcnow()

        if last_available.date() >= today.date():
            return "Already Up To Date"

        next_date = last_available + pd.Timedelta(days=1)

        df = self.download_bhavcopy(next_date)

        if df is None:
            return "No new bhavcopy available"

        df = df[df["SYMBOL"].isin(self.universe)]

        new_rows = []

        for _, row in df.iterrows():
            new_rows.append({
                "date": next_date.strftime("%Y-%m-%d"),
                "symbol": row["SYMBOL"],
                "price": row["CLOSE"]
            })

        if not new_rows:
            return "No matching symbols"

        new_df = pd.DataFrame(new_rows)

        combined = pd.concat([self.price_df, new_df], ignore_index=True)
        combined.drop_duplicates(subset=["date", "symbol"], inplace=True)

        combined.to_csv(PRICE_FILE, index=False)

        return f"Added rows: {len(new_rows)}"


if __name__ == "__main__":
    updater = NSEIncrementalUpdater()
    result = updater.run()
    print(result)
