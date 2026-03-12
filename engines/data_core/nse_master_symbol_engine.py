import pandas as pd
import requests
import os
from io import StringIO

URL="https://archives.nseindia.com/content/equities/EQUITY_L.csv"

OUT="data/processed/tradable_universe.csv"

HEADERS={
"User-Agent":"Mozilla/5.0",
"Accept":"text/html,application/xhtml+xml",
}

def run():

    print("\n===== BUILDING NSE MASTER UNIVERSE =====")

    r=requests.get(URL,headers=HEADERS,timeout=30)

    if r.status_code!=200:
        print("NSE request failed")
        return

    df=pd.read_csv(StringIO(r.text))

    df=df.rename(columns={
        "SYMBOL":"symbol",
        "NAME OF COMPANY":"company",
        " SERIES":"series"
    })

    df=df[["symbol","company","series"]]

    df=df[df["series"]=="EQ"]

    df=df.drop_duplicates("symbol")

    os.makedirs("data/processed",exist_ok=True)

    df.to_csv(OUT,index=False)

    print("TOTAL NSE STOCKS:",len(df))
    print("UNIVERSE FILE CREATED")

if __name__=="__main__":
    run()
