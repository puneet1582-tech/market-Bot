import requests
import pandas as pd
import zipfile
import logging
import os
import time
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


def generate_dates():

    today=datetime.utcnow().date()

    dates=[]

    for i in range(7):
        d=today-timedelta(days=i)
        dates.append(d)

    return dates


def build_url(date):

    dd=date.strftime("%d")
    mmm=date.strftime("%b").upper()
    yyyy=date.strftime("%Y")

    url=f"https://archives.nseindia.com/content/historical/EQUITIES/{yyyy}/{mmm}/cm{dd}{mmm}{yyyy}bhav.csv.zip"

    return url


def try_download(url):

    try:

        r=requests.get(url,headers=HEADERS,timeout=15)

        if r.status_code!=200:
            return None

        z=zipfile.ZipFile(BytesIO(r.content))

        name=z.namelist()[0]

        df=pd.read_csv(z.open(name))

        return df

    except Exception as e:

        logging.warning(f"Download failed {url}")
        return None


def normalize(df):

    cols=df.columns.str.lower()

    df.columns=cols

    keep=[
    "symbol",
    "open",
    "high",
    "low",
    "close",
    "tottrdqty"
    ]

    df=df[keep]

    df=df.rename(columns={
    "tottrdqty":"volume"
    })

    return df


def run():

    dates=generate_dates()

    for d in dates:

        url=build_url(d)

        logging.info(f"Trying {url}")

        df=try_download(url)

        if df is not None:

            df=normalize(df)

            os.makedirs("data/raw_bhavcopy",exist_ok=True)

            df.to_csv(OUTPUT,index=False)

            print("BHAVCOPY DOWNLOADED")

            logging.info("SUCCESS")

            return

        time.sleep(2)

    raise Exception("DATA INGESTION FAILED")


if __name__=="__main__":
    run()
