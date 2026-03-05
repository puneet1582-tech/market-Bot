import requests
import pandas as pd
import os
import time
from datetime import datetime

OUT_FILE = "data/nse_price_history_clean.csv"

URL = "https://archives.nseindia.com/content/historical/EQUITIES/bhavcopy/pr/PR.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*",
    "Connection": "keep-alive"
}

def download_retry(url, retries=5):
    for i in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                return r.content
        except Exception:
            print("Retry:", i+1)
        time.sleep(2)
    return None


def build_price_dataset():

    print("DOWNLOADING NSE PRICE DATA...")

    content = download_retry(URL)

    if content is None:
        print("Price download failed.")
        return

    from io import StringIO
    df = pd.read_csv(StringIO(content.decode()))

    # schema detection
    cols = [c.upper() for c in df.columns]

    if "SYMBOL" not in cols:
        print("Invalid price schema.")
        return

    df.columns = cols

    price_df = pd.DataFrame()

    price_df["symbol"] = df["SYMBOL"]
    price_df["price"] = df["CLOSE"] if "CLOSE" in df.columns else df["LAST"]
    price_df["date"] = datetime.now().strftime("%Y-%m-%d")

    price_df = price_df.drop_duplicates()
    price_df = price_df.sort_values("symbol")

    os.makedirs("data", exist_ok=True)

    price_df.to_csv(OUT_FILE, index=False)

    print("NSE PRICE ENGINE COMPLETE")
    print("Rows:", len(price_df))
    print("Saved:", OUT_FILE)

