import pandas as pd
import requests
import zipfile
import os
import time
from datetime import datetime, timedelta
from io import BytesIO

OUTPUT_DIR="data/bhavcopy"
OUTPUT_FILE="data/bhavcopy/cm_today_bhav.csv"

os.makedirs(OUTPUT_DIR,exist_ok=True)

ARCHIVE_URL="https://archives.nseindia.com/content/historical/EQUITIES"
NEW_ARCHIVE="https://nsearchives.nseindia.com/content/historical/EQUITIES"

HEADERS={
"User-Agent":"Mozilla/5.0",
"Accept":"*/*",
"Connection":"keep-alive"
}

def build_url(date):

    year=date.strftime("%Y")
    month=date.strftime("%b").upper()
    day=date.strftime("%d%b%Y").upper()

    return [
        f"{ARCHIVE_URL}/{year}/{month}/cm{day}bhav.csv.zip",
        f"{NEW_ARCHIVE}/{year}/{month}/cm{day}bhav.csv.zip"
    ]


def download(url):

    try:

        r=requests.get(url,headers=HEADERS,timeout=15)

        if r.status_code!=200:
            return None

        return r.content

    except:
        return None


def extract_zip(content):

    with zipfile.ZipFile(BytesIO(content)) as z:

        name=z.namelist()[0]

        df=pd.read_csv(z.open(name))

        return df


def find_latest_bhavcopy():

    today=datetime.utcnow()

    for i in range(10):

        d=today-timedelta(days=i)

        urls=build_url(d)

        for url in urls:

            print("Trying:",url)

            content=download(url)

            if content:

                df=extract_zip(content)

                return df

        time.sleep(1)

    raise Exception("Bhavcopy download failed")


def clean(df):

    df=df[df["SERIES"]=="EQ"]

    df=df.rename(columns={
        "SYMBOL":"symbol",
        "CLOSE":"close",
        "TOTTRDQTY":"volume"
    })

    df=df[["symbol","close","volume"]]

    return df


def run():

    print("Downloading NSE bhavcopy...")

    df=find_latest_bhavcopy()

    df=clean(df)

    df.to_csv(OUTPUT_FILE,index=False)

    print("Saved:",OUTPUT_FILE)


if __name__=="__main__":
    run()
