import os
import pandas as pd
import yfinance as yf


DATA_DIR = "data/prices"


def load_universe():

    path = "data/nse_symbols.csv"

    if not os.path.exists(path):
        print("Universe file missing")
        return []

    df = pd.read_csv(path)

    return df["symbol"].tolist()


def download_price(symbol):

    try:

        data = yf.download(symbol + ".NS", period="10y")

        if data.empty:
            return

        file = os.path.join(DATA_DIR, f"{symbol}.csv")

        data.to_csv(file)

        print("Saved:", symbol)

    except:

        pass


def run():

    print("\nMASTER DATA INGESTION STARTED\n")

    symbols = load_universe()

    if not symbols:
        print("No symbols found")
        return

    os.makedirs(DATA_DIR, exist_ok=True)

    for s in symbols:

        download_price(s)

    print("\nPRICE DATA COLLECTION COMPLETE\n")


if __name__ == "__main__":
    pass

