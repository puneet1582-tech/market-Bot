import pandas as pd

PRICE_FILE = "data/processed/market_prices.csv"
MAP_FILE = "data/processed/stock_sector_map.csv"
OUTPUT_FILE = "data/processed/sector_money_flow.csv"

def run():

    prices = pd.read_csv(PRICE_FILE)
    sector_map = pd.read_csv(MAP_FILE)

    prices["date"] = pd.to_datetime(prices["date"])

    prices = prices.sort_values(["symbol","date"])

    results = []

    for symbol, g in prices.groupby("symbol"):

        g = g.tail(30)

        if len(g) < 20:
            continue

        start = g.iloc[0]["close"]
        end = g.iloc[-1]["close"]

        ret = (end - start) / start

        results.append({
            "symbol": symbol,
            "return_20d": ret
        })

    df = pd.DataFrame(results)

    df = df.merge(sector_map, on="symbol", how="left")

    sector_flow = (
        df.groupby("sector")
        .agg(
            avg_return_20d=("return_20d","mean"),
            stocks_in_sector=("symbol","count")
        )
        .reset_index()
    )

    sector_flow = sector_flow.sort_values(
        "avg_return_20d",
        ascending=False
    )

    sector_flow.to_csv(OUTPUT_FILE, index=False)

    print("Sector money flow calculated")


if __name__ == "__main__":
    run()
