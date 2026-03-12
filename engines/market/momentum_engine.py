import pandas as pd

INPUT_FILE = "data/processed/market_prices.csv"
OUTPUT_FILE = "data/processed/momentum_stocks.csv"


def run():

    df = pd.read_csv(INPUT_FILE)

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values(["symbol", "date"])

    results = []

    for symbol, g in df.groupby("symbol"):

        g = g.tail(60)

        if len(g) < 20:
            continue

        last = g.iloc[-1]
        prev20 = g.tail(20)

        avg_volume = prev20["volume"].mean()

        price_change = (last["close"] - prev20.iloc[0]["close"]) / prev20.iloc[0]["close"]

        volume_spike = last["volume"] > avg_volume * 1.5

        if price_change > 0.05 and volume_spike:

            results.append({
                "symbol": symbol,
                "last_close": last["close"],
                "price_change_20d": round(price_change, 3),
                "volume_spike": True
            })

    out = pd.DataFrame(results)

    out.sort_values("price_change_20d", ascending=False, inplace=True)

    out.to_csv(OUTPUT_FILE, index=False)

    print("Momentum scan complete:", len(out), "stocks")


if __name__ == "__main__":
    run()
