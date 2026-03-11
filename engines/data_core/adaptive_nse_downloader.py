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
"Accept":"*/*",
"Connection":"keep-alive"
}

def try_download(date):

    d=date.strftime("%d%b%Y").upper()
    m=date.strftime("%b").upper()
    y=date.strftime("%Y")

    url=f"{BASE}/{y}/{m}/cm{d}bhav.csv.zip"

    try:

        r=requests.get(url,headers=HEADERS,timeout=15)

        if r.status_code!=200:
            return None

        z=zipfile.ZipFile(BytesIO(r.content))
        name=z.namelist()[0]

        df=pd.read_csv(z.open(name))

        os.makedirs("data/raw_bhavcopy",exist_ok=True)

        df.to_csv(OUTPUT,index=False)

        print("Bhavcopy downloaded:",d)

        return True

    except:
        return None


def run():

    today=datetime.utcnow()

    for i in range(7):

        d=today-timedelta(days=i)

        result=try_download(d)

        if result:
            print("DATA INGESTION SUCCESS")
            return

    if os.path.exists(OUTPUT):
        print("Using previous bhavcopy")
        return

    raise Exception("DATA INGESTION FAILED")


if __name__=="__main__":
    run()
