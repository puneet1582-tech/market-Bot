import requests
import pandas as pd
import zipfile
import os
from datetime import datetime,timedelta
from io import BytesIO

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


def try_download(date):

    url=build_url(date)

    try:

        r=requests.get(url,headers=HEADERS,timeout=20)

        if r.status_code!=200:
            return None

        z=zipfile.ZipFile(BytesIO(r.content))
        name=z.namelist()[0]

        df=pd.read_csv(z.open(name))

        return df

    except:
        return None


def run():

    today=datetime.now()

    for i in range(7):

        d=today-timedelta(days=i)

        df=try_download(d)

        if df is not None:

            os.makedirs("data/raw_bhavcopy",exist_ok=True)

            df.to_csv(OUTPUT,index=False)

            print("BHAVCOPY DOWNLOADED:",d.date())

            return


    if os.path.exists(OUTPUT):

        print("DOWNLOAD FAILED — USING OLD BHAVCOPY")

        return


    print("WARNING: No bhavcopy available, pipeline continues")


if __name__=="__main__":
    run()
