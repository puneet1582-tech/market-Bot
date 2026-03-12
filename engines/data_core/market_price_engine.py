import pandas as pd
import os

INPUT_FILE = "data/bhavcopy/cm_today_bhav.csv"
OUTPUT_FILE = "data/processed/market_prices.csv"

def run():

    if not os.path.exists(INPUT_FILE):
        print("Bhavcopy file missing")
        return

    df = pd.read_csv(INPUT_FILE)

    df = df.rename(columns={
        "SYMBOL":"symbol",
        "CLOSE":"close",
        "TOTTRDQTY":"volume"
    })

    df = df[["symbol","close","volume"]]

    df["close"] = pd.to_numeric(df["close"],errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"],errors="coerce")

    df = df.dropna()

    os.makedirs("data/processed",exist_ok=True)

    df.to_csv(OUTPUT_FILE,index=False)

    print("MARKET PRICE DATA CREATED")
    print("TOTAL STOCKS:",len(df))

if __name__ == "__main__":
    run()
