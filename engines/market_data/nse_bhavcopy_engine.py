import pandas as pd
import requests
import zipfile
import os
from datetime import datetime
from io import BytesIO


UNIVERSE_FILE = "data/universe/nse_equity_universe.csv"
OUTPUT_FILE = "data/market/price_history.csv"


HEADERS = {
    "User-Agent":"Mozilla/5.0",
    "Accept":"*/*",
    "Connection":"keep-alive"
}


def build_url():

    today=datetime.now()

    date=today.strftime("%d%m%Y")

    url=f"https://archives.nseindia.com/content/historical/EQUITIES/{today.strftime('%Y')}/{today.strftime('%b').upper()}/cm{date}bhav.csv.zip"

    return url


def download_bhavcopy():

    url=build_url()

    r=requests.get(url,headers=HEADERS,timeout=30)

    if r.status_code!=200:
        raise Exception("Bhavcopy download failed")

    z=zipfile.ZipFile(BytesIO(r.content))

    name=z.namelist()[0]

    df=pd.read_csv(z.open(name))

    return df


def normalize(df):

    mapping={
        "SYMBOL":"symbol",
        "OPEN":"open",
        "HIGH":"high",
        "LOW":"low",
        "CLOSE":"close",
        "TOTTRDQTY":"volume",
        "TIMESTAMP":"date"
    }

    df=df.rename(columns=mapping)

    keep=list(mapping.values())

    df=df[keep]

    df["date"]=pd.to_datetime(df["date"],errors="coerce")

    return df


def filter_universe(df):

    universe=pd.read_csv(UNIVERSE_FILE)

    symbols=set(universe["SYMBOL"].astype(str))

    df=df[df["symbol"].astype(str).isin(symbols)]

    return df


def append_master(df):

    if os.path.exists(OUTPUT_FILE):

        master=pd.read_csv(OUTPUT_FILE)

        df=pd.concat([master,df],ignore_index=True)

        df=df.drop_duplicates(["symbol","date"])

    df.to_csv(OUTPUT_FILE,index=False)


def run():

    print("Downloading NSE bhavcopy...")

    df=download_bhavcopy()

    df=normalize(df)

    df=filter_universe(df)

    append_master(df)

    print("Price history updated:",len(df))


if __name__=="__main__":
    run()
