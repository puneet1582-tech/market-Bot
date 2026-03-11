import pandas as pd
import requests
import os
from io import StringIO


OUTPUT_FILE = "data/universe/nse_equity_universe.csv"


URLS = [
    "https://archives.nseindia.com/content/equities/EQUITY_L.csv",
    "https://archives.nseindia.com/content/equities/EQUITY_L.csv?download=1"
]


HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/csv"
}


def fetch_csv():

    for url in URLS:

        try:

            r = requests.get(url, headers=HEADERS, timeout=20)

            if r.status_code == 200 and len(r.text) > 100:

                return pd.read_csv(StringIO(r.text))

        except Exception:
            continue

    raise Exception("Unable to download NSE universe")


def normalize_columns(df):

    mapping = {}

    for c in df.columns:

        cl = c.lower()

        if "symbol" in cl:
            mapping[c] = "symbol"

        elif "company" in cl or "name" in cl:
            mapping[c] = "company_name"

        elif "series" in cl:
            mapping[c] = "series"

        elif "isin" in cl:
            mapping[c] = "isin"

    df = df.rename(columns=mapping)

    return df


def clean(df):

    df = normalize_columns(df)

    required = ["symbol","company_name"]

    for col in required:

        if col not in df.columns:
            raise Exception("Critical column missing: " + col)

    if "series" not in df.columns:
        df["series"] = "EQ"

    if "isin" not in df.columns:
        df["isin"] = ""

    df = df[["symbol","company_name","series","isin"]]

    df["symbol"] = df["symbol"].astype(str).str.strip()

    df = df[df["symbol"] != ""]

    df = df[df["series"].astype(str).str.upper() == "EQ"]

    df = df.drop_duplicates(subset=["symbol"])

    df = df.sort_values("symbol")

    return df


def run():

    print("Downloading NSE equity universe...")

    raw = fetch_csv()

    clean_df = clean(raw)

    os.makedirs("data/universe", exist_ok=True)

    clean_df.to_csv(OUTPUT_FILE, index=False)

    print("Saved:", OUTPUT_FILE)

    print("Total NSE symbols:", len(clean_df))


if __name__ == "__main__":
    run()
