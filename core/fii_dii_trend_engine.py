import pandas as pd
import os

DATA_FILE = "data/fii_dii.csv"
OUT_FILE = "data/institutional_money_flow.csv"

def build_institutional_trend():

    if not os.path.exists(DATA_FILE):
        print("FII/DII data file missing.")
        return

    df = pd.read_csv(DATA_FILE)

    if not {"sector","fii","dii"}.issubset(df.columns):
        print("Invalid schema in fii_dii.csv")
        return

    df["net_flow"] = df["fii"] + df["dii"]

    def classify(x):
        if x > 0:
            return "ACCUMULATION"
        elif x < 0:
            return "DISTRIBUTION"
        else:
            return "NEUTRAL"

    df["smart_money_signal"] = df["net_flow"].apply(classify)

    df.to_csv(OUT_FILE, index=False)

    print("FII/DII TREND ENGINE COMPLETE")
    print("Sectors analyzed:", len(df))
    print("Saved:", OUT_FILE)


# disabled_entry_point
    build_institutional_trend()
