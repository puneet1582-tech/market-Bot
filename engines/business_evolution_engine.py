import pandas as pd
import os

FUNDAMENTAL_FILE = "data/fundamentals/fundamentals.csv"
TREND_FILE = "data/fundamentals/fundamental_trend.csv"
OWNERSHIP_FILE = "data/fundamentals/ownership_data.csv"

OUTPUT_FILE = "data/fundamentals/business_strength.csv"

def run_business_evolution():

    if not os.path.exists(FUNDAMENTAL_FILE):
        print("Fundamental data missing")
        return

    if not os.path.exists(TREND_FILE):
        print("Trend data missing")
        return

    if not os.path.exists(OWNERSHIP_FILE):
        print("Ownership data missing")
        return

    fundamentals = pd.read_csv(FUNDAMENTAL_FILE)
    trends = pd.read_csv(TREND_FILE)
    ownership = pd.read_csv(OWNERSHIP_FILE)

    df = fundamentals.merge(trends, on="symbol", how="left")
    df = df.merge(ownership, on="symbol", how="left")

    df["business_signal"] = "neutral"

    df.to_csv(OUTPUT_FILE, index=False)

    print("Business evolution dataset created")

if __name__ == "__main__":
    run_business_evolution()
