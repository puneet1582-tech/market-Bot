import os
import requests
import pandas as pd
import yfinance as yf
from io import StringIO

UNIVERSE_FILE = "data/nse_symbols.csv"
PRICE_DIR = "data/prices"

NSE_EQUITY_URL = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"


def build_nse_universe():

    print("\nDownloading NSE equity list...")

    r = requests.get(NSE_EQUITY_URL, timeout=30)

    if r.status_code != 200:
        raise Exception("NSE universe download failed")

    csv_data = StringIO(r.text)

    df = pd.read_csv(csv_data)

    df = df.rename(columns={"SYMBOL": "symbol"})

    df = df[["symbol"]]

    os.makedirs("data", exist_ok=True)

    df.to_csv(UNIVERSE_FILE, index=False)

    print("NSE universe saved:", len(df), "stocks")


def load_symbols():

    if not os.path.exists(UNIVERSE_FILE):
        raise Exception("NSE universe file missing")

    df = pd.read_csv(UNIVERSE_FILE)

    return df["symbol"].dropna().tolist()


def fetch_price(symbol):

    ticker = symbol + ".NS"

    try:

        df = yf.download(
            ticker,
            period="10y",
            interval="1d",
            progress=False
        )

        if df.empty:
            return None

        df.reset_index(inplace=True)

        df["symbol"] = symbol

        return df

    except Exception as e:

        print("Error:", symbol, e)

        return None


def save_price(symbol, df):

    if df is None:
        return

    os.makedirs(PRICE_DIR, exist_ok=True)

    path = os.path.join(PRICE_DIR, f"{symbol}.csv")

    df.to_csv(path, index=False)

    print("Saved:", symbol)


def run_pipeline():

    print("\n===== NSE COMPLETE DATA PIPELINE START =====\n")

    build_nse_universe()

    symbols = load_symbols()

    print("Total NSE stocks:", len(symbols))

    for i, sym in enumerate(symbols):

        print(f"[{i+1}/{len(symbols)}] Fetching {sym}")

        df = fetch_price(sym)

        save_price(sym, df)

    print("\n===== PIPELINE COMPLETE =====\n")


if __name__ == "__main__":

    run_pipeline()
