import pandas as pd
import os

FLOW_FILE = "data/institutional_money_flow.csv"
SECTOR_FILE = "data/sector_index_base.csv"
OUT_FILE = "data/sector_strength_rank.csv"

def build_sector_strength():

    if not os.path.exists(FLOW_FILE):
        print("Institutional flow file missing.")
        return

    if not os.path.exists(SECTOR_FILE):
        print("Sector index file missing.")
        return

    flow = pd.read_csv(FLOW_FILE)
    sector_index = pd.read_csv(SECTOR_FILE)

    if "sector" not in flow.columns:
        print("Sector column missing in institutional flow.")
        return

    result = flow.copy()

    result["sector_strength"] = result["net_flow"]

    result = result.sort_values("sector_strength", ascending=False)

    result["sector_rank"] = range(1, len(result) + 1)

    result.to_csv(OUT_FILE, index=False)

    print("SECTOR MONEY FLOW ENGINE COMPLETE")
    print("Sectors ranked:", len(result))
    print("Saved:", OUT_FILE)


if __name__ == "__main__":
    build_sector_strength()
