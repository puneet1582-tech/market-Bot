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
        df=df.groupby("symbol").tail(2)

    # calculate return
    df["return_1d"]=df.groupby("symbol")["price"].pct_change()

    df=df.dropna()

    # keep latest row per stock
    df=df.groupby("symbol").tail(1)

    # rank
    df=df.sort_values("return_1d",ascending=False)

    result=[]

    for _,r in df.head(20).iterrows():

        result.append({
            "symbol":r["symbol"],
            "score":round(float(r["return_1d"]*100),2)
        })

    return result
