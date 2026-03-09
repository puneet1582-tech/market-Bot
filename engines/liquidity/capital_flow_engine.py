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


def compute_flow(df):

    df["close"] = pd.to_numeric(df["close"],errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"],errors="coerce")

    df["money_flow"] = df["close"] * df["volume"]

    return df


def run():

    prices = safe_read(PRICE_FILE)
    sector_map = safe_read(SECTOR_MAP)

    if prices.empty:
        print("Price data missing")
        return

    df = prices.copy()

    df = compute_flow(df)

    stock_flow = (
        df.groupby("symbol")["money_flow"]
        .sum()
        .reset_index()
    )

    stock_flow = stock_flow.sort_values(
        by="money_flow",
        ascending=False
    )

    stock_flow.to_csv(
        STOCK_OUTPUT,
        index=False
    )

    if not sector_map.empty:

        merged = stock_flow.merge(
            sector_map,
            on="symbol",
            how="left"
        )

        sector_flow = (
            merged.groupby("sector")["money_flow"]
            .sum()
            .reset_index()
        )

        sector_flow = sector_flow.sort_values(
            by="money_flow",
            ascending=False
        )

        sector_flow.to_csv(
            SECTOR_OUTPUT,
            index=False
        )

    print("Capital flow analysis complete")
    print("Stocks analysed:",len(stock_flow))


if __name__ == "__main__":
    run()
