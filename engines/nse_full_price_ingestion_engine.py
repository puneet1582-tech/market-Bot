import os
import pandas as pd
import yfinance as yf


DATA_PATH = "data/prices"


def load_nse_universe():

    file = "data/nse_symbols.csv"

    if not os.path.exists(file):
        print("NSE universe file missing")
        return []

    df = pd.read_csv(file)

    if "symbol" not in df.columns:
        print("symbol column missing")
        return []

    return df["symbol"].tolist()


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

    path = os.path.join(DATA_PATH, symbol + ".csv")

    df.to_csv(path, index=False)

    print("Saved:", symbol)


def run_ingestion():

    print("\nNSE FULL PRICE INGESTION STARTED\n")

    symbols = load_nse_universe()

    if not symbols:
        print("Universe empty")
        return

    print("Total symbols:", len(symbols))

    for symbol in symbols:

        df = fetch_price(symbol)

        save_price(symbol, df)

    print("\nFULL NSE PRICE INGESTION COMPLETE\n")


if __name__ == "__main__":
    pass

    os.makedirs(DATA_PATH, exist_ok=True)

    run_ingestion()
