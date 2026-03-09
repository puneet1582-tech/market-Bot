import pandas as pd
import os


PRICE_FILE = "data/processed/market_prices.csv"
SECTOR_MAP = "data/processed/stock_sector_map.csv"

SECTOR_OUTPUT = "data/processed/sector_money_flow.csv"
STOCK_OUTPUT = "data/processed/stock_money_flow.csv"
ROTATION_OUTPUT = "data/processed/capital_rotation.csv"


def safe_read(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()


def normalize_numeric(df, col):

    if col not in df.columns:
        return df

    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace(" ", "", regex=False)
    )

    df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def run():

    prices = safe_read(PRICE_FILE)
    sector_map = safe_read(SECTOR_MAP)

    if prices.empty:
        print("market_prices missing")
        return

    prices = normalize_numeric(prices,"close")
    prices = normalize_numeric(prices,"volume")

    prices = prices.dropna(subset=["close","volume"])

    prices["value_traded"] = prices["close"] * prices["volume"]

    prices.to_csv(STOCK_OUTPUT,index=False)


    if sector_map.empty:
        print("sector map missing")
        return

    df = prices.merge(sector_map,on="symbol",how="left")

    sector_flow = (
        df.groupby("sector")["value_traded"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    sector_flow.to_csv(SECTOR_OUTPUT,index=False)


    sector_flow["prev_flow"] = sector_flow["value_traded"].shift(1)

    sector_flow["rotation_signal"] = (
        sector_flow["value_traded"] > sector_flow["prev_flow"]
    )

    sector_flow.to_csv(ROTATION_OUTPUT,index=False)


    print("Capital flow analysis complete")
    print("Stocks analyzed:",len(prices))
    print("Sectors analyzed:",len(sector_flow))


if __name__ == "__main__":
    run()
