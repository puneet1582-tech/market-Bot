import pandas as pd

PRICE_FILE="data/prices/historical_prices.csv"

def generate_top_opportunities():

    try:
        df=pd.read_csv(PRICE_FILE)
    except:
        return []

    if "price" not in df.columns:
        return []

    df["return_1d"]=df["price"].pct_change()

    df=df.dropna()

    df=df.sort_values("return_1d",ascending=False)

    result=[]

    for _,r in df.head(20).iterrows():

        result.append({
            "symbol":r["symbol"],
            "score":round(float(r["return_1d"]),4)
        })

    return result
