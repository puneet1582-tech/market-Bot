import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

SYMBOL_FILE = "data/nse_symbols.csv"
SAVE_PATH = "data/ownership"

BASE_URL = "https://www.screener.in/company/{}/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def load_symbols():

    df = pd.read_csv(SYMBOL_FILE)

    return df["symbol"].dropna().tolist()


def fetch_ownership(symbol):

    url = BASE_URL.format(symbol)

    try:

        r = requests.get(url, headers=HEADERS, timeout=20)

        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.text, "html.parser")

        tables = soup.find_all("table")

        for table in tables:

            if "Shareholding Pattern" in table.text:
                pass

                df = pd.read_html(str(table))[0]

                df["symbol"] = symbol

                return df

        return None

    except Exception as e:

        print("Error:", symbol)

        return None


def save_data(symbol, df):

    if df is None:
        return

    os.makedirs(SAVE_PATH, exist_ok=True)

    file = os.path.join(SAVE_PATH, f"{symbol}.csv")

    df.to_csv(file, index=False)

    print("Saved:", symbol)


def run():

    print("\nINSTITUTIONAL OWNERSHIP PIPELINE START\n")

    symbols = load_symbols()

    total = len(symbols)

    for i, s in enumerate(symbols):

        print(f"[{i+1}/{total}] Fetching {s}")

        df = fetch_ownership(s)

        save_data(s, df)

        time.sleep(2)

    print("\nOWNERSHIP PIPELINE COMPLETE\n")


if __name__ == "__main__":
    pass

