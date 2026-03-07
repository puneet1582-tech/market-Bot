import pandas as pd
import os

FUNDAMENTAL_FILE = "data/fundamentals/fundamentals.csv"
OUTPUT_FILE = "data/fundamentals/fundamental_trend.csv"

def run_quarter_comparison():

    if not os.path.exists(FUNDAMENTAL_FILE):
        print("Fundamental dataset not found")
        return

    df = pd.read_csv(FUNDAMENTAL_FILE)

    df["revenue_trend"] = "unknown"
    df["profit_trend"] = "unknown"

    df.to_csv(OUTPUT_FILE, index=False)

    print("Quarter comparison base created")

if __name__ == "__main__":
    run_quarter_comparison()
