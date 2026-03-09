import pandas as pd
import os

INPUT_FILE = "data/processed/tradable_universe.csv"
MAP_FILE = "data/processed/stock_sector_map.csv"
OUTPUT_FILE = "data/processed/sector_intelligence.csv"

def ensure_map(symbols):

    if os.path.exists(MAP_FILE):
        return pd.read_csv(MAP_FILE)

    df = pd.DataFrame({
        "symbol": symbols,
        "sector": "UNKNOWN"
    })

    df.to_csv(MAP_FILE, index=False)

    return df


def run():

    df = pd.read_csv(INPUT_FILE)

    mapping = ensure_map(df["symbol"].unique())

    merged = df.merge(mapping, on="symbol", how="left")

    sector_view = (
        merged.groupby("sector")
        .agg(
            stocks=("symbol","count"),
            avg_price=("close","mean"),
            total_volume=("volume","sum")
        )
        .reset_index()
    )

    os.makedirs("data/processed", exist_ok=True)

    sector_view.to_csv(OUTPUT_FILE, index=False)

    print("Sector intelligence generated")
    print("Saved:", OUTPUT_FILE)


if __name__ == "__main__":
    run()
