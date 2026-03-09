import pandas as pd
import os


PRICE_FILE = "data/processed/market_prices.csv"
SECTOR_MAP = "data/processed/stock_sector_map.csv"

STOCK_OUTPUT = "data/processed/stock_money_flow.csv"
SECTOR_OUTPUT = "data/processed/sector_money_flow.csv"


def safe_read(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()


def run():

    prices = safe_read(PRICE_FILE)
    sector_map = safe_read(SECTOR_MAP)

    if prices.empty:
        print("Price data missing")
        return

    df = prices.copy()

    if "close" not in df.columns or "volume" not in df.columns:
        print("Required columns missing")
        return

    df["close"] = pd.to_numeric(df["close"],errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"],errors="coerce")

    df["money_flow"] = df["close"] * df["volume"]

    stock_flow = df.groupby("symbol",as_index=False)["money_flow"].sum()

    stock_flow.to_csv(STOCK_OUTPUT,index=False)

    if not sector_map.empty:

        df = df.merge(sector_map,on="symbol",how="left")

        sector_flow = df.groupby("sector",as_index=False)["money_flow"].sum()

        sector_flow.to_csv(SECTOR_OUTPUT,index=False)

    print("Capital flow analysis complete")


if __name__ == "__main__":
    run()
