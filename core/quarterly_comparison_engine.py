import os
import pandas as pd

def run():

    print("Quarterly Comparison Engine Running")

    os.makedirs("data/analysis", exist_ok=True)

    fundamentals="data/fundamentals/fundamental_10y.csv"

    if not os.path.exists(fundamentals):
        print("No fundamental data yet")
        return

    df=pd.read_csv(fundamentals)

    if df.empty:
        print("Fundamental dataset empty")
        return

    summary=df.groupby("symbol").tail(4)

    summary.to_csv("data/analysis/quarterly_summary.csv",index=False)

    print("Quarterly comparison completed")

