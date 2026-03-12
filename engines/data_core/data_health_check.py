import pandas as pd
import os

PRICE_FILE="data/processed/market_prices.csv"
BHAV_FILE="data/raw_bhavcopy/latest_bhavcopy.csv"

def run():

    print("\n===== DATA HEALTH CHECK =====")

    if os.path.exists(BHAV_FILE):
        print("BHAVCOPY : OK")
    else:
        print("BHAVCOPY : MISSING")

    if os.path.exists(PRICE_FILE):

        df=pd.read_csv(PRICE_FILE)

        last_date=df["date"].max()

        print("MARKET PRICE FILE : OK")

        print("LAST MARKET DATE :",last_date)

        print("TOTAL RECORDS :",len(df))

        print("TOTAL SYMBOLS :",df["symbol"].nunique())

    else:

        print("MARKET PRICE FILE : MISSING")

if __name__=="__main__":
    run()
