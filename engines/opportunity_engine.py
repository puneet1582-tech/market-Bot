import pandas as pd

PRICE_FILE="data/prices/latest_prices.csv"

def generate_top_opportunities():

    try:
        df=pd.read_csv(PRICE_FILE)
    except:
        return []

    df["score"]=df["return_1d"]+df["volume_change"]

    df=df.sort_values("score",ascending=False)

    result=[]

    for _,r in df.head(20).iterrows():

        result.append({
            "symbol":r["symbol"],
            "score":round(float(r["score"]),3)
        })

    return result
