import requests
import pandas as pd
import os
import time
from datetime import datetime

OUT_FILE = "data/nse_price_history_clean.csv"

BHAVCOPY_URL = "https://archives.nseindia.com/products/content/sec_bhavdata_full.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*",
    "Connection": "keep-alive",
    "Referer": "https://www.nseindia.com"
}


def build_price_dataset():

    print("DOWNLOADING NSE PRICE DATA...")

    session = requests.Session()

    try:
        session.get("https://www.nseindia.com", headers=HEADERS, timeout=10)
    except:
        pass

    for attempt in range(5):

        try:

            r = session.get(BHAVCOPY_URL, headers=HEADERS, timeout=20)

            if r.status_code == 200:

                from io import StringIO

                df = pd.read_csv(StringIO(r.text))

                cols = [c.strip().upper() for c in df.columns]

                df.columns = cols

                if "SYMBOL" not in df.columns:
                    print("Invalid schema")
                    return

                price_df = pd.DataFrame()

                price_df["symbol"] = df["SYMBOL"]
                price_df["price"] = df["CLOSE_PRICE"]
                price_df["date"] = datetime.now().strftime("%Y-%m-%d")

                price_df = price_df.drop_duplicates()

                os.makedirs("data", exist_ok=True)

                price_df.to_csv(OUT_FILE, index=False)

                print("NSE PRICE ENGINE COMPLETE")
                print("Rows:", len(price_df))
                print("Saved:", OUT_FILE)

                return

        except Exception:
            pass

        time.sleep(2)

    print("Price download failed.")

