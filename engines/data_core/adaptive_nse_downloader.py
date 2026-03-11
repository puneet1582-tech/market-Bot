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
"user-agent":"Mozilla/5.0",
"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"accept-language":"en-US,en;q=0.9"
}


def try_download(url):

    try:

        r=requests.get(url,headers=HEADERS,timeout=20)

        if r.status_code!=200:
            return None

        if url.endswith(".zip"):

            z=zipfile.ZipFile(BytesIO(r.content))

            for name in z.namelist():

                if name.endswith(".csv"):

                    return pd.read_csv(z.open(name))

        else:

            return pd.read_csv(BytesIO(r.content))

    except Exception as e:

        logging.warning(f"FAILED SOURCE {url}")

        return None


def build_urls(date):

    dd=date.strftime("%d")
    mmm=date.strftime("%b").upper()
    yyyy=date.strftime("%Y")

    urls=[

    f"https://archives.nseindia.com/content/historical/EQUITIES/{yyyy}/{mmm}/cm{dd}{mmm}{yyyy}bhav.csv.zip",

    f"https://nsearchives.nseindia.com/content/historical/EQUITIES/{yyyy}/{mmm}/cm{dd}{mmm}{yyyy}bhav.csv.zip",

    f"https://www1.nseindia.com/content/historical/EQUITIES/{yyyy}/{mmm}/cm{dd}{mmm}{yyyy}bhav.csv.zip"

    ]

    return urls


def fetch():

    today=datetime.utcnow()

    for i in range(10):

        date=today-timedelta(days=i)

        urls=build_urls(date)

        for url in urls:

            logging.info(f"TRY {url}")

            df=try_download(url)

            if df is not None and len(df)>10:

                logging.info(f"SUCCESS {url}")

                return df

        time.sleep(1)

    return None


def clean(df):

    df=df.rename(columns=str.lower)

    keep=[

    "symbol",
    "open",
    "high",
    "low",
    "close",
    "tottrdqty",
    "timestamp"

    ]

    cols=[c for c in keep if c in df.columns]

    df=df[cols]

    df=df.rename(columns={"tottrdqty":"volume"})

    df=df[df["symbol"].str.len()>1]

    return df


def run():

    df=fetch()

    if df is None:

        raise Exception("DATA INGESTION FAILED")

    df=clean(df)

    os.makedirs(os.path.dirname(OUTPUT),exist_ok=True)

    df.to_csv(OUTPUT,index=False)

    print("BHAVCOPY INGESTED")
    print("ROWS:",len(df))


if __name__=="__main__":

    run()
