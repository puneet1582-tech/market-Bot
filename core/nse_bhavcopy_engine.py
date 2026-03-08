import requests
import zipfile
import pandas as pd
import os
from datetime import datetime

def run():

    today=datetime.now()

    date_str=today.strftime("%d%m%Y")

    year=today.strftime("%Y")
    month=today.strftime("%b").upper()

    url=f"https://archives.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{date_str}bhav.csv.zip"

    os.makedirs("data/bhavcopy",exist_ok=True)

    zip_path=f"data/bhavcopy/{date_str}.zip"

    r=requests.get(url,headers={"User-Agent":"Mozilla/5.0"})

    if r.status_code!=200:
        print("Bhavcopy download failed")
        return

    with open(zip_path,"wb") as f:
        f.write(r.content)

    with zipfile.ZipFile(zip_path,"r") as z:
        z.extractall("data/bhavcopy")

    csv_file=[f for f in os.listdir("data/bhavcopy") if f.endswith(".csv")][0]

    df=pd.read_csv(f"data/bhavcopy/{csv_file}")

    df=df[df["SERIES"]=="EQ"]

    df=df[[
        "SYMBOL",
        "OPEN",
        "HIGH",
        "LOW",
        "CLOSE",
        "TOTTRDQTY",
        "TIMESTAMP"
    ]]

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
