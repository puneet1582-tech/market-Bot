import pandas as pd

INPUT_FILE = "data/processed/market_prices.csv"
OUTPUT_FILE = "data/processed/tradable_universe.csv"

def filter_liquid_stocks():

    df = pd.read_csv(INPUT_FILE)

    df = df[df["volume"] > 50000]
    df = df[df["close"] > 20]

    df.to_csv(OUTPUT_FILE, index=False)

    print("Liquidity filter complete")
    print(f"Tradable stocks: {len(df)}")
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    filter_liquid_stocks()
