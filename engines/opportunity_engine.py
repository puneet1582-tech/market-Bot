from engines.news_weight_engine import news_weight
import pandas as pd

PRICE_FILE="data/prices/historical_prices.csv"

def generate_top_opportunities():

    try:
        df=pd.read_csv(PRICE_FILE)
    except:
        return []

    # ensure required columns
    if "symbol" not in df.columns or "price" not in df.columns:
        return []

    # convert date
    if "date" in df.columns:
        df["date"]=pd.to_datetime(df["date"])

        # latest record per stock
        df=df.sort_values("date")
    weights=news_weight()

    df["news_boost"]=df["symbol"].map(weights).fillna(0)

    df["return_1d"]=df["return_1d"]+(df["news_boost"]*0.01)

        df=df.groupby("symbol").tail(2)

    # calculate return
    df["return_1d"]=df.groupby("symbol")["price"].pct_change()

    df=df.dropna()

    # keep latest row per stock
    df=df.groupby("symbol").tail(1)

    # rank
    df=df.sort_values("return_1d",ascending=False)
    weights=news_weight()

    df["news_boost"]=df["symbol"].map(weights).fillna(0)

    df["return_1d"]=df["return_1d"]+(df["news_boost"]*0.01)


    result=[]

    for _,r in df.head(20).iterrows():

        result.append({
            "symbol":r["symbol"],
            "score":round(float(r["return_1d"]*100),2)
        })

    return result
