import pandas as pd
import os

DATA_FILE = "data/fii_dii.csv"
OUT_FILE = "data/institutional_money_flow.csv"

def build_institutional_trend():

    if not os.path.exists(DATA_FILE):
        print("FII/DII file missing.")
        return

    df = pd.read_csv(DATA_FILE)

    if "sector" not in df.columns:
        print("Sector column missing.")
        return

    df["institutional_strength"] = df["fii"] + df["dii"]

    df = df.sort_values("institutional_strength", ascending=False)

    df.to_csv(OUT_FILE, index=False)

    print("FII/DII TREND ENGINE COMPLETE")
    print("Sectors analyzed:", len(df))
    print("Saved:", OUT_FILE)


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
