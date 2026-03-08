import requests
import zipfile
import pandas as pd
import os
from datetime import datetime,timedelta

def download_for_date(d):

    date_str=d.strftime("%d%m%Y")
    year=d.strftime("%Y")
    month=d.strftime("%b").upper()

    url=f"https://archives.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{date_str}bhav.csv.zip"

    headers={
        "User-Agent":"Mozilla/5.0",
        "Accept":"*/*",
        "Connection":"keep-alive"
    }

    r=requests.get(url,headers=headers,timeout=20)

    if r.status_code!=200:
        return None

    os.makedirs("data/bhavcopy",exist_ok=True)

    zip_path=f"data/bhavcopy/{date_str}.zip"

    with open(zip_path,"wb") as f:
        f.write(r.content)

    with zipfile.ZipFile(zip_path,"r") as z:
        z.extractall("data/bhavcopy")

    return True


def run():

    today=datetime.now()

    for i in range(7):

        d=today-timedelta(days=i)

        ok=download_for_date(d)

        if ok:

            csv_file=None

            for f in os.listdir("data/bhavcopy"):
                if f.endswith(".csv"):
                    csv_file=f
                    break

            if not csv_file:
                print("CSV not found")
                return

            df=pd.read_csv(f"data/bhavcopy/{csv_file}")

            df=df[df["SERIES"]=="EQ"]

            df=df[
                [
                    "SYMBOL",
                    "OPEN",
                    "HIGH",
                    "LOW",
                    "CLOSE",
                    "TOTTRDQTY",
                    "TIMESTAMP"
                ]
            ]

            df.columns=[
                "symbol",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "date"
            ]

            os.makedirs("data/prices",exist_ok=True)

            df.to_csv("data/prices/latest_prices.csv",index=False)

            print("Bhavcopy Engine Completed")

            return

    print("Bhavcopy not found for last 7 days")

