import pandas as pd
import requests
import zipfile
import os
import time
from datetime import datetime
from io import BytesIO


OUTPUT_DIR = "data/bhavcopy"
os.makedirs(OUTPUT_DIR, exist_ok=True)


BASE_URLS = [
"https://archives.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{date}bhav.csv.zip",
"https://www1.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{date}bhav.csv.zip"
]


HEADERS = {
"User-Agent": "Mozilla/5.0",
"Accept": "*/*",
"Connection": "keep-alive",
"Accept-Language": "en-US,en;q=0.9"
}


def get_session():

    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        session.get("https://www.nseindia.com", timeout=10)
    except:
        pass

    return session


def build_dates():

    today = datetime.now()
    return {
        "year": today.strftime("%Y"),
        "month": today.strftime("%b").upper(),
        "date": today.strftime("%d%b%Y").upper()
    }


def download_from_url(session, url):

    r = session.get(url, timeout=20)

    if r.status_code != 200:
        return None

    try:
        z = zipfile.ZipFile(BytesIO(r.content))
        file = z.namelist()[0]

        df = pd.read_csv(z.open(file))
        return df

    except:
        return None


def download_bhavcopy():

    session = get_session()
    date = build_dates()

    for base in BASE_URLS:

        url = base.format(**date)

        try:

            df = download_from_url(session, url)

            if df is not None:
                return df

        except:
            continue

    raise Exception("Bhavcopy download failed from all sources")


def clean_equity(df):

    df = df[df["SERIES"] == "EQ"]

    df = df.rename(columns={
        "SYMBOL": "symbol",
        "CLOSE": "close",
        "TOTTRDQTY": "volume"
    })

    df = df[["symbol", "close", "volume"]]

    return df


def save(df):

    date = datetime.now().strftime("%Y%m%d")

    path = f"{OUTPUT_DIR}/bhav_{date}.csv"

    df.to_csv(path, index=False)

    print("Saved:", path)


def run():

    print("Downloading NSE bhavcopy...")

    for attempt in range(3):

        try:

            df = download_bhavcopy()

            df = clean_equity(df)

            save(df)

            print("Bhavcopy download success")

            return

        except Exception as e:

            print("Attempt failed:", attempt+1)

            time.sleep(3)

    raise Exception("Bhavcopy engine failed after retries")


if __name__ == "__main__":
    run()
