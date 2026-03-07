import pandas as pd
import os

DATA_FILE = "data/institutional_money_flow.csv"
OUT_FILE = "data/sector_strength_rank.csv"

def build_sector_strength():

    if not os.path.exists(DATA_FILE):
        print("Institutional money flow file missing.")
        return

    df = pd.read_csv(DATA_FILE)

    if "sector" not in df.columns:
        print("Sector column missing.")
        return

    df = df.sort_values("institutional_strength", ascending=False)

    df.to_csv(OUT_FILE, index=False)

    print("SECTOR MONEY FLOW ENGINE COMPLETE")
    print("Sectors ranked:", len(df))
    print("Saved:", OUT_FILE)


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
