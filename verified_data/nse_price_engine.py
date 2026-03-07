import pandas as pd
import requests
from zipfile import ZipFile
from io import BytesIO
from datetime import datetime

url="https://archives.nseindia.com/content/historical/EQUITIES/2024/NOV/cm01NOV2024bhav.csv.zip"

r=requests.get(url)

z=ZipFile(BytesIO(r.content))

name=z.namelist()[0]

df=pd.read_csv(z.open(name))

df=df.rename(columns={
"SYMBOL":"symbol",
"CLOSE":"price"
})

df=df[["symbol","price"]]

df["date"]=datetime.today().strftime("%Y-%m-%d")

df.to_csv("data/price_history.csv",mode="a",index=False,header=False)

print("NSE price data added:",len(df))


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
