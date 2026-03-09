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


def run():

    prices = safe_read(PRICE_FILE)
    sector_map = safe_read(SECTOR_MAP)

    if prices.empty or sector_map.empty:
        print("Missing price or sector data")
        return


    df = prices.merge(sector_map,on="symbol",how="left")


    df["value_traded"] = df["close"] * df["volume"]


    sector_flow = (
        df.groupby("sector")
        .agg(
            total_volume=("volume","sum"),
            total_value=("value_traded","sum"),
            avg_price=("close","mean"),
            stock_count=("symbol","nunique")
        )
        .reset_index()
    )


    sector_flow["flow_strength"] = sector_flow["total_value"].rank(ascending=False)


    stock_flow = (
        df.groupby(["symbol","sector"])
        .agg(
            volume=("volume","sum"),
            value=("value_traded","sum"),
            avg_price=("close","mean")
        )
        .reset_index()
    )


    stock_flow["money_rank"] = stock_flow["value"].rank(ascending=False)


    top_sectors = sector_flow.sort_values("flow_strength").head(5)

    rotation = df[df["sector"].isin(top_sectors["sector"])]

    rotation = (
        rotation.groupby(["symbol","sector"])
        .agg(
            value=("value_traded","sum"),
            volume=("volume","sum")
        )
        .reset_index()
    )

    rotation = rotation.sort_values("value",ascending=False)


    sector_flow.to_csv(SECTOR_OUTPUT,index=False)
    stock_flow.to_csv(STOCK_OUTPUT,index=False)
    rotation.to_csv(ROTATION_OUTPUT,index=False)


    print("Capital flow analysis complete")
    print("Sector flows:",len(sector_flow))
    print("Stock flows:",len(stock_flow))


if __name__ == "__main__":
    run()
