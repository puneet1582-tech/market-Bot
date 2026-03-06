import pandas as pd
from engines.news_weight_engine import news_weight
from engines.sector_strength_engine import sector_strength

PRICE_FILE = "data/prices/historical_prices.csv"

SECTOR_MAP = {
    "IT": ["TCS","INFY","HCLTECH","WIPRO"],
    "BANK": ["HDFCBANK","ICICIBANK","SBIN","KOTAKBANK"],
    "AUTO": ["MARUTI","TATAMOTORS","M&M"],
    "METAL": ["TATASTEEL","JSWSTEEL","HINDALCO"],
    "DEFENCE": ["HAL","BEL","BDL"]
}

def stock_sector(symbol):
    for s,stocks in SECTOR_MAP.items():
        if symbol in stocks:
            return s
    return None


def generate_top_opportunities():

    try:
        df = pd.read_csv(PRICE_FILE)
    except:
        return []

    if "symbol" not in df.columns or "price" not in df.columns:
        return []

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

    df = df.groupby("symbol").tail(2)

    df["ret"] = df.groupby("symbol")["price"].pct_change()

    df = df.dropna()

    df = df.groupby("symbol").tail(1)

    # news weights
    nw = news_weight()

    # sector strength
    ss = sector_strength()

    df["sector"] = df["symbol"].apply(stock_sector)

    df["news_boost"] = df["symbol"].map(nw).fillna(0)
    df["sector_boost"] = df["sector"].map(ss).fillna(0)

    df["score"] = df["ret"] + (df["news_boost"]*0.01) + (df["sector_boost"]*0.5)

    df = df.sort_values("score", ascending=False)

    result=[]

    for _,r in df.head(20).iterrows():

        result.append({
            "symbol":r["symbol"],
            "score":round(float(r["score"]*100),2)
        })

    return result
