import pandas as pd
import os

INPUT_FILE = "data/processed/top_opportunities.csv"
OUTPUT_FILE = "data/processed/sector_strength.csv"
MAP_FILE = "data/processed/stock_sector_map.csv"

def ensure_sector_map(df):
    if os.path.exists(MAP_FILE):
        return pd.read_csv(MAP_FILE)

    # default mapping file create (user later update kar sakta hai)
    m = pd.DataFrame({
        "symbol": df["symbol"].unique(),
        "sector": "UNKNOWN"
    })
    m.to_csv(MAP_FILE, index=False)
    return m

def run():

    df = pd.read_csv(INPUT_FILE)

    sector_map = ensure_sector_map(df)

    df = df.merge(sector_map, on="symbol", how="left")

    sector_stats = (
        df.groupby("sector")
        .agg(
            stocks=("symbol","count"),
            avg_momentum=("momentum","mean"),
            total_volume=("volume","sum")
        )
        .reset_index()
        .sort_values(by="avg_momentum", ascending=False)
    )

    sector_stats.to_csv(OUTPUT_FILE, index=False)

    print("Sector intelligence generated")
    print(sector_stats)

if __name__ == "__main__":
    run()
