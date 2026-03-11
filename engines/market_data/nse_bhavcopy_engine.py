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


BASE_URL="https://archives.nseindia.com/content/historical/EQUITIES"


HEADERS={
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Language":"en-US,en;q=0.5",
"Connection":"keep-alive"
}


def build_url(date):

    year=date.strftime("%Y")
    month=date.strftime("%b").upper()
    d=date.strftime("%d%b%Y").upper()

    return f"{BASE_URL}/{year}/{month}/cm{d}bhav.csv.zip"


def download(session,url):

    r=session.get(url,headers=HEADERS,timeout=20)

    if r.status_code!=200:
        return None

    return r.content


def extract_zip(content):

    z=zipfile.ZipFile(BytesIO(content))
    name=z.namelist()[0]

    df=pd.read_csv(z.open(name))

    return df


def normalize_columns(df):

    cols=[c.strip().upper() for c in df.columns]

    df.columns=cols

    rename_map={
    "SYMBOL":"symbol",
    "CLOSE":"close",
    "TOTTRDQTY":"volume"
    }

    df=df.rename(columns=rename_map)

    return df


def try_dates(session):

    today=datetime.now()

    for i in range(7):

        d=today-timedelta(days=i)

        url=build_url(d)

        print("Trying:",url)

        content=download(session,url)

        if content:

            print("Downloaded:",d.date())

            return content

        time.sleep(1)

    return None


def run():

    print("Downloading NSE bhavcopy...")

    session=requests.Session()

    session.get("https://www.nseindia.com",headers=HEADERS)

    content=try_dates(session)

    if not content:
        raise Exception("Bhavcopy download failed")

    df=extract_zip(content)

    df=normalize_columns(df)

    df.to_csv(OUTPUT_FILE,index=False)

    print("Saved:",OUTPUT_FILE)


if __name__=="__main__":
    run()
