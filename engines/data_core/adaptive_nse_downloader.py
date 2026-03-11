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


BASE_URLS=[
"https://archives.nseindia.com/content/historical/EQUITIES",
"https://nsearchives.nseindia.com/content/historical/EQUITIES"
]


HEADERS={
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
"Accept":"*/*",
"Connection":"keep-alive",
"Accept-Language":"en-US,en;q=0.9"
}


def bootstrap_session():

    s=requests.Session()

    try:
        s.get(
            "https://www.nseindia.com",
            headers=HEADERS,
            timeout=10
        )
    except:
        pass

    return s


def generate_url(date,base):

    yyyy=date.strftime("%Y")
    mmm=date.strftime("%b").upper()
    dd=date.strftime("%d")

    file=f"cm{dd}{mmm}{yyyy}bhav.csv.zip"

    return f"{base}/{yyyy}/{mmm}/{file}"


def try_download(session,url):

    try:

        r=session.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        if r.status_code!=200:
            return None

        return r.content

    except:
        return None


def extract_csv(binary):

    z=zipfile.ZipFile(BytesIO(binary))

    name=z.namelist()[0]

    df=pd.read_csv(z.open(name))

    return df


def run():

    session=bootstrap_session()

    today=datetime.today()

    for i in range(7):

        date=today-timedelta(days=i)

        for base in BASE_URLS:

            url=generate_url(date,base)

            logging.info(f"TRY {url}")

            data=try_download(session,url)

            if data:

                try:

                    df=extract_csv(data)

                    os.makedirs(
                        os.path.dirname(OUTPUT),
                        exist_ok=True
                    )

                    df.to_csv(OUTPUT,index=False)

                    print("BHAVCOPY DOWNLOADED")
                    print("Rows:",len(df))

                    logging.info("SUCCESS")

                    return

                except Exception as e:

                    logging.error("ZIP ERROR")

        time.sleep(1)

    raise Exception("DATA INGESTION FAILED")


if __name__=="__main__":
    run()
