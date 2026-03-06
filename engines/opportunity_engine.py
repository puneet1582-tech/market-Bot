import pandas as pd
from engines.news_weight_engine import news_weight

PRICE_FILE = "data/prices/historical_prices.csv"

def generate_top_opportunities():

    try:
        df = pd.read_csv(PRICE_FILE)
    except:
        return []

    if "symbol" not in df.columns or "price" not in df.columns:
        return []

    # ensure date column
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

    # last two rows per stock
    df = df.groupby("symbol").tail(2)

    # daily return
    df["return_1d"] = df.groupby("symbol")["price"].pct_change()

    df = df.dropna()

    # keep latest row per symbol
    df = df.groupby("symbol").tail(1)

    # news weighting
    weights = news_weight()
    df["news_boost"] = df["symbol"].map(weights).fillna(0)

    df["score"] = df["return_1d"] + (df["news_boost"] * 0.01)

    df = df.sort_values("score", ascending=False)

    result = []

    for _, r in df.head(20).iterrows():
        result.append({
            "symbol": r["symbol"],
            "score": round(float(r["score"] * 100), 2)
        })

    return result
