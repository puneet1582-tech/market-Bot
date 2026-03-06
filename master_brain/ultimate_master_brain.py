import pandas as pd
import json

def sector_check(symbol):

    stocks=pd.read_csv("data/stocks.csv")

    row=stocks[stocks["symbol"]==symbol]

    if len(row)==0:
        return "UNKNOWN"

    return row.iloc[0]["sector"]


def business_check(symbol):

    try:

        price=pd.read_csv("data/price_history.csv")

    except:

        return "DATA_MISSING"

    df=price[price["symbol"]==symbol]

    if len(df)<200:
        return "WEAK"

    growth=df["price"].pct_change().mean()

    if growth>0.002:
        return "STRONG"

    if growth>0:

        return "AVERAGE"

    return "WEAK"


def decision(business):

    if business=="STRONG":

        return "LONG TERM INVEST"

    if business=="AVERAGE":

        return "TRADE"

    return "AVOID"


def run():

    stocks=pd.read_csv("data/stocks.csv")

    symbols=stocks["symbol"].tolist()

    results=[]

    for s in symbols[:20]:

        sector=sector_check(s)

        business=business_check(s)

        final=decision(business)

        results.append({

            "stock":s,
            "sector":sector,
            "business":business,
            "decision":final

        })

    print(json.dumps(results,indent=2))


if __name__=="__main__":

    run()

