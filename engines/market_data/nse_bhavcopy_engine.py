import pandas as pd
import requests
import zipfile
import os
import time
import logging
from datetime import datetime, timedelta
from io import BytesIO


OUTPUT_DIR="data/bhavcopy"
OUTPUT_FILE="data/bhavcopy/cm_today_bhav.csv"

os.makedirs(OUTPUT_DIR,exist_ok=True)

logging.basicConfig(
    filename="logs/bhavcopy_engine.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


ARCHIVE_SOURCES=[
"https://archives.nseindia.com/content/historical/EQUITIES",
"https://nsearchives.nseindia.com/content/historical/EQUITIES"
]


HEADERS={
"User-Agent":"Mozilla/5.0",
"Accept":"*/*",
"Connection":"keep-alive"
}


def build_url(base,date):

    year=date.strftime("%Y")
    month=date.strftime("%b").upper()
    day=date.strftime("%d%b%Y").upper()

    return f"{base}/{year}/{month}/cm{day}bhav.csv.zip"


def download_zip(url):

    try:

        r=requests.get(url,headers=HEADERS,timeout=20)

        if r.status_code==200:

            return BytesIO(r.content)

    except Exception:

        return None

    return None


def parse_zip(zip_bytes):

    z=zipfile.ZipFile(zip_bytes)

    name=z.namelist()[0]

    df=pd.read_csv(z.open(name))

    return df


def try_sources(date):

    for base in ARCHIVE_SOURCES:

        url=build_url(base,date)

        logging.info(f"Trying {url}")

        data=download_zip(url)

        if data:

            try:

                df=parse_zip(data)

                logging.info("Bhavcopy downloaded")

                return df

            except Exception:

                continue

    return None


def find_latest():

    today=datetime.utcnow()

    for i in range(10):

        date=today-timedelta(days=i)

        df=try_sources(date)

        if df is not None:

            return df

        time.sleep(1)

    return None


def run():

    logging.info("Bhavcopy engine start")

    df=find_latest()

    if df is None:

        raise Exception("Bhavcopy download failed")

    df.to_csv(OUTPUT_FILE,index=False)

    logging.info("Bhavcopy saved")

    print("Bhavcopy rows:",len(df))


if __name__=="__main__":
    run()
