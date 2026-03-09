import pandas as pd
import os

OPPORTUNITY_FILE = "data/processed/top_opportunities.csv"
SECTOR_FILE = "data/processed/sector_strength.csv"
MAP_FILE = "data/processed/stock_sector_map.csv"
OUTPUT_FILE = "data/processed/final_decisions.csv"

def run():

    df = pd.read_csv(OPPORTUNITY_FILE)

    if os.path.exists(MAP_FILE):
        mapping = pd.read_csv(MAP_FILE)
        df = df.merge(mapping, on="symbol", how="left")
    else:
        df["sector"] = "UNKNOWN"

    if os.path.exists(SECTOR_FILE):
        sector = pd.read_csv(SECTOR_FILE)
        df = df.merge(sector[["sector","avg_momentum"]], on="sector", how="left")
    else:
        df["avg_momentum"] = df["momentum"]

    decisions = []

    for _, r in df.iterrows():

        momentum = r["momentum"]
        sector_mom = r["avg_momentum"]

        if momentum > 3 and sector_mom > 2:
            mode = "INVEST"
        elif momentum > 1:
            mode = "TRADE"
        else:
            mode = "DEFENSIVE"

        decisions.append(mode)

    df["decision"] = decisions

    df = df.sort_values(by="momentum", ascending=False)

    df.to_csv(OUTPUT_FILE, index=False)

    print("Decision engine completed")
    print("Saved:", OUTPUT_FILE)

if __name__ == "__main__":
    run()
