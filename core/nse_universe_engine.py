import requests
import pandas as pd
import time
import os

URL = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
OUT_FILE = "data/nse_universe_full.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive"
}

def download_with_retry(url, retries=5):

    for i in range(retries):

        try:
            r = requests.get(url, headers=HEADERS, timeout=15)

            if r.status_code == 200:
                return r.content

        except Exception as e:
            print("Download attempt failed:", i+1)

        time.sleep(2)

    return None


def build_nse_universe():

    print("DOWNLOADING NSE STOCK UNIVERSE...")

    content = download_with_retry(URL)

    if content is None:
        print("Failed to download NSE universe.")
        return

    from io import StringIO

    df = pd.read_csv(StringIO(content.decode()))

    if "SYMBOL" not in df.columns:
        print("Invalid NSE schema.")
        return

    df = df.rename(columns={"SYMBOL": "symbol"})

    df = df[["symbol"]]

    df = df.drop_duplicates()

    df = df.sort_values("symbol")

    os.makedirs("data", exist_ok=True)

    df.to_csv(OUT_FILE, index=False)

    print("NSE UNIVERSE ENGINE COMPLETE")
    print("Total stocks:", len(df))
    print("Saved:", OUT_FILE)



if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
