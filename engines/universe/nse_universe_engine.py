import pandas as pd
import requests
import os
from io import StringIO

OUTPUT_FILE="data/universe/nse_equity_universe.csv"

URLS=[
    "https://archives.nseindia.com/content/equities/EQUITY_L.csv",
    "https://archives.nseindia.com/content/equities/EQUITY_L.csv?download=1"
]

HEADERS={
    "User-Agent":"Mozilla/5.0",
    "Accept":"text/csv"
}

def fetch_csv():

    for url in URLS:
        try:
            r=requests.get(url,headers=HEADERS,timeout=20)
            if r.status_code==200 and len(r.text)>1000:
                return pd.read_csv(StringIO(r.text))
        except:
            continue

    raise Exception("Universe download failed")


def clean(df):

    df=df.rename(columns={
        "SYMBOL":"symbol",
        "NAME OF COMPANY":"company_name",
        "SERIES":"series",
        "DATE OF LISTING":"listing_date",
        "ISIN NUMBER":"isin"
    })

    df=df[["symbol","company_name","series","listing_date","isin"]]

    df=df[df["series"].isin(["EQ","BE"])]

    df=df.dropna(subset=["symbol"])

    df["symbol"]=df["symbol"].astype(str).str.strip()

    df=df.drop_duplicates(subset=["symbol"])

    df=df.sort_values("symbol")

    df["sector"]="UNKNOWN"

    return df


def run():

    print("Downloading NSE equity universe...")

    raw=fetch_csv()

    clean_df=clean(raw)

    os.makedirs("data/universe",exist_ok=True)

    clean_df.to_csv(OUTPUT_FILE,index=False)

    print("Universe created:",len(clean_df))
    print("Saved:",OUTPUT_FILE)


if __name__=="__main__":
    run()
