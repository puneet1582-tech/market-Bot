import requests
import pandas as pd
import zipfile
import os
import logging
from datetime import datetime,timedelta
from io import BytesIO

logging.basicConfig(
    filename="logs/data_core.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

OUTPUT="data/raw_bhavcopy/latest_bhavcopy.csv"

BASE="https://archives.nseindia.com/content/historical/EQUITIES"

HEADERS={
"User-Agent":"Mozilla/5.0",
"Accept":"text/html,application/xhtml+xml",
"Accept-Language":"en-US,en;q=0.9",
}

def build_url(date):

    d=date.strftime("%d%b%Y").upper()
    y=date.strftime("%Y")
    m=date.strftime("%b").upper()

    return f"{BASE}/{y}/{m}/cm{d}bhav.csv.zip"


def download_day(date):

    url=build_url(date)

    try:

        r=requests.get(url,headers=HEADERS,timeout=20)

        if r.status_code!=200:
            return None

        z=zipfile.ZipFile(BytesIO(r.content))
        name=z.namelist()[0]

        df=pd.read_csv(z.open(name))

        return df

    except Exception as e:

        logging.error(f"download failed {date} {e}")
        return None


def run():

    today=datetime.now()

    for i in range(5):

        d=today-timedelta(days=i)

        df=download_day(d)

        if df is not None:

            df.to_csv(OUTPUT,index=False)

            print("BHAVCOPY DOWNLOADED",d.date())

            return

    if os.path.exists(OUTPUT):

        print("Using previous bhavcopy fallback")

        return

    raise Exception("DATA INGESTION FAILED")


if __name__=="__main__":
    run()
