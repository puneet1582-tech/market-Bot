import requests
import zipfile
import pandas as pd
import logging
import time
import os
from datetime import datetime,timedelta
from io import BytesIO


logging.basicConfig(
    filename="logs/data_core.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


OUTPUT="data/raw_bhavcopy/latest_bhavcopy.csv"


HEADERS={
    "User-Agent":"Mozilla/5.0",
    "Accept":"*/*",
    "Connection":"keep-alive"
}


def download(url):

    try:
        r=requests.get(url,headers=HEADERS,timeout=20)

        if r.status_code!=200:
            return None

        return r.content

    except Exception as e:

        logging.error(str(e))
        return None



def extract_zip(content):

    try:

        z=zipfile.ZipFile(BytesIO(content))

        for f in z.namelist():

            if f.endswith(".csv"):

                return pd.read_csv(z.open(f))

    except:

        return None



def normalize(df):

    cols=[c.upper() for c in df.columns]

    df.columns=cols

    if "SYMBOL" not in cols:
        return None

    df=df[df["SERIES"]=="EQ"]

    return df



def build_urls(d):

    dd=d.strftime("%d")
    mm=d.strftime("%m")
    yyyy=d.strftime("%Y")
    mmm=d.strftime("%b").upper()

    urls=[

        f"https://archives.nseindia.com/content/historical/EQUITIES/{yyyy}/{mmm}/cm{dd}{mmm}{yyyy}bhav.csv.zip",

        f"https://nsearchives.nseindia.com/content/historical/EQUITIES/{yyyy}/{mmm}/cm{dd}{mmm}{yyyy}bhav.csv.zip"

    ]

    return urls



def search():

    today=datetime.today()

    for i in range(0,10):

        d=today-timedelta(days=i)

        urls=build_urls(d)

        for u in urls:

            logging.info(f"TRY {u}")

            data=download(u)

            if not data:
                continue

            df=extract_zip(data)

            if df is None:
                continue

            df=normalize(df)

            if df is None:
                continue

            df.to_csv(OUTPUT,index=False)

            logging.info("SUCCESS")

            return True

        time.sleep(1)

    return False



def run():

    ok=search()

    if not ok:
        raise Exception("DATA INGESTION FAILED")

    print("Bhavcopy downloaded")


if __name__=="__main__":
    run()
