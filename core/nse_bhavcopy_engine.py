import requests
import pandas as pd
import os

def run():

    url="https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"

    headers={
        "User-Agent":"Mozilla/5.0",
        "Accept":"application/json",
        "Referer":"https://www.nseindia.com/"
    }

    session=requests.Session()

    session.get("https://www.nseindia.com",headers=headers)

    r=session.get(url,headers=headers)

    if r.status_code!=200:
        print("NSE API blocked:",r.status_code)
        return

    data=r.json()["data"]

    rows=[]

    for s in data:

        rows.append({
            "symbol":s["symbol"],
            "open":s.get("open"),
            "high":s.get("dayHigh"),
            "low":s.get("dayLow"),
            "close":s.get("lastPrice"),
            "volume":s.get("totalTradedVolume"),
            "date":s.get("lastUpdateTime")
        })

    df=pd.DataFrame(rows)

    os.makedirs("data/prices",exist_ok=True)

    df.to_csv("data/prices/latest_prices.csv",index=False)

    print("Market Data Downloaded from NSE API")

