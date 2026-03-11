import yfinance as yf
import pandas as pd
import os

SYMBOL_FILE="data/processed/tradable_universe.csv"
OUT_DIR="data/historical_prices"


def run():

    if not os.path.exists(SYMBOL_FILE):
        print("tradable_universe.csv missing")
        return

    symbols=pd.read_csv(SYMBOL_FILE)["symbol"].unique()

    for s in symbols:

        try:

            ticker=s+".NS"

            df=yf.download(
                ticker,
                period="10y",
                interval="1d",
                progress=False
            )

            if df.empty:
                continue

            df.reset_index(inplace=True)

            df["symbol"]=s

            path=f"{OUT_DIR}/{s}.csv"

            df.to_csv(path,index=False)

            print("Downloaded",s)

        except Exception as e:

            print("fail",s,e)


if __name__=="__main__":
    run()
