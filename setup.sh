#!/bin/bash

mkdir -p UltimateBrain/engines
mkdir -p UltimateBrain/data/bhavcopy
mkdir -p UltimateBrain/logs

cd UltimateBrain

pip install pandas requests python-dateutil

cat << 'REQ' > requirements.txt
pandas
requests
python-dateutil
REQ

cat << 'PY' > engines/bhavcopy_engine.py
import os
import requests
import zipfile
import pandas as pd
from datetime import datetime

DATA_FOLDER = "data/bhavcopy"

def download_bhavcopy():
    today = datetime.today()
    date = today.strftime("%d%m%Y")
    year = today.strftime("%Y")
    month = today.strftime("%b").upper()

    url = f"https://archives.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{date}bhav.csv.zip"

    os.makedirs(DATA_FOLDER, exist_ok=True)

    zip_path = os.path.join(DATA_FOLDER, "bhavcopy.zip")

    try:
        r = requests.get(url, timeout=30)

        if r.status_code != 200:
            print("Bhavcopy not available yet")
            return

        with open(zip_path, "wb") as f:
            f.write(r.content)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(DATA_FOLDER)

        print("Bhavcopy Downloaded")

    except Exception as e:
        print("Download Error:", e)


if __name__ == "__main__":
    download_bhavcopy()
PY

echo "SETUP COMPLETE"
