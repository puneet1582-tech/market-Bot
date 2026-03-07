import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

SYMBOL_FILE = "data/nse_symbols.csv"
SAVE_PATH = "data/fundamentals"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BASE_URL = "https://www.screener.in/company/{}/consolidated/"


def load_symbols():

    if not os.path.exists(SYMBOL_FILE):
        raise Exception("NSE symbol file missing")

    df = pd.read_csv(SYMBOL_FILE)

    return df["symbol"].dropna().tolist()


def fetch_fundamentals(symbol):

    url = BASE_URL.format(symbol)

    retries = 3

    for attempt in range(retries):

        try:

            r = requests.get(url, headers=HEADERS, timeout=20)

            if r.status_code != 200:
                return None

            soup = BeautifulSoup(r.text, "html.parser")

            tables = soup.find_all("table")

            if not tables:
                return None

            df = pd.read_html(str(tables[0]))[0]

            df["symbol"] = symbol

            return df

        except Exception as e:

            print("Retry:", symbol, attempt + 1)

            time.sleep(2)

    return None


def save_data(symbol, df):

    if df is None:
        return

    os.makedirs(SAVE_PATH, exist_ok=True)

    file = os.path.join(SAVE_PATH, f"{symbol}.csv")

    df.to_csv(file, index=False)

    print("Saved:", symbol)


def run():

    print("\nFUNDAMENTAL DATA PIPELINE START\n")

    symbols = load_symbols()

    total = len(symbols)

    print("Total symbols:", total)

    for i, s in enumerate(symbols):

        print(f"[{i+1}/{total}] Fetching {s}")

        df = fetch_fundamentals(s)

        save_data(s, df)

        time.sleep(1)

    print("\nFUNDAMENTAL DATA PIPELINE COMPLETE\n")


if __name__ == "__main__":
    pass

