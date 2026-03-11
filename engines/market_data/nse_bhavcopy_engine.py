import pandas as pd
import requests
import zipfile
import os
import time
from datetime import datetime
from io import BytesIO


OUTPUT_DIR = "data/bhavcopy"
OUTPUT_FILE = "data/bhavcopy/cm_today_bhav.csv"

os.makedirs(OUTPUT_DIR,exist_ok=True)


URL_PATTERNS = [

"https://archives.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{date}bhav.csv.zip",

"https://www1.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{date}bhav.csv.zip",

"https://nsearchives.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{date}bhav.csv.zip"

]


HEADERS = {

"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
"Accept":"*/*",
"Connection":"keep-alive",
"Accept-Language":"en-US,en;q=0.9"

}


def get_session():

    s=requests.Session()

    s.headers.update(HEADERS)

    try:

        s.get("https://www.nseindia.com",timeout=10)

    except:
        pass

    return s


def generate_dates():

    today=datetime.today()

    for i in range(5):

        d=today - pd.Timedelta(days=i)

        yield d.strftime("%d%b%Y").upper(),d.strftime("%Y"),d.strftime("%b").upper()


def download(session,url):

    try:

        r=session.get(url,timeout=15)

        if r.status_code==200:

            return r.content

    except:
        pass

    return None


def extract(content):

    z=zipfile.ZipFile(BytesIO(content))

    name=z.namelist()[0]

    z.extract(name,OUTPUT_DIR)

    return os.path.join(OUTPUT_DIR,name)


def normalize(csv_path):

    df=pd.read_csv(csv_path)

    df=df[df["SERIES"]=="EQ"]

    df=df.rename(columns={

    "SYMBOL":"symbol",

    "CLOSE":"close",

    "TOTTRDQTY":"volume"

    })

    df=df[["symbol","close","volume"]]

    df.to_csv(OUTPUT_FILE,index=False)


def run():

    session=get_session()

    print("Downloading NSE bhavcopy...")

    for date,year,month in generate_dates():

        for pattern in URL_PATTERNS:

            url=pattern.format(date=date,year=year,month=month)

            content=download(session,url)

            if content:

                csv_path=extract(content)

                normalize(csv_path)

                print("Bhavcopy saved:",OUTPUT_FILE)

                return

        time.sleep(2)

    raise Exception("Bhavcopy download failed across all sources")


if __name__=="__main__":
    run()
