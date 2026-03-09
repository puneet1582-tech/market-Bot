import pandas as pd

INPUT_FILE = "data/processed/market_prices.csv"
OUTPUT_FILE = "data/processed/tradable_universe.csv"

def filter_liquid_stocks():

    df = pd.read_csv(INPUT_FILE)

    # convert numeric columns safely
    df["volume"] = (
        df["volume"]
        .astype(str)
        .str.replace(",", "")
    )

    df["close"] = (
        df["close"]
        .astype(str)
        .str.replace(",", "")
    )

    df["volume"] = pd.to_numeric(df["volume"], errors="coerce")
    df["close"] = pd.to_numeric(df["close"], errors="coerce")

    df = df.dropna(subset=["volume", "close"])

    df = df[df["volume"] > 50000]
    df = df[df["close"] > 20]

    df.to_csv(OUTPUT_FILE, index=False)

    print("Liquidity filter complete")
    print("Tradable stocks:", len(df))


if __name__ == "__main__":
    filter_liquid_stocks()
