import os
import pandas as pd

def run():

    print("Price History Engine Running")

    latest="data/prices/latest_prices.csv"

    if not os.path.exists(latest):
        print("No market data")
        return

    df=pd.read_csv(latest)

    os.makedirs("data/prices/history",exist_ok=True)

    df.to_csv("data/prices/history/history_latest.csv",index=False)

    print("Price history updated")

