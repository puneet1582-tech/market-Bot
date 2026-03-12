import os
import pandas as pd
from datetime import datetime

BHAV="data/raw_bhavcopy/latest_bhavcopy.csv"
PRICES="data/processed/market_prices.csv"

def run():

    print("\n===== MARKET DATA CONTROLLER =====")

    source=None

    if os.path.exists(BHAV):
        source="BHAVCOPY"

    elif os.path.exists(PRICES):
        source="PRICE_DATABASE"

    else:
        source="NO_DATA"

    if source=="BHAVCOPY":

        df=pd.read_csv(BHAV)

        print("DATA SOURCE : NSE BHAVCOPY")
        print("ROWS :",len(df))

    elif source=="PRICE_DATABASE":

        df=pd.read_csv(PRICES)

        last=df["date"].max()

        print("DATA SOURCE : HISTORICAL DATABASE")
        print("LAST MARKET DATE :",last)
        print("ROWS :",len(df))

    else:

        print("ERROR : NO MARKET DATA AVAILABLE")

    print("===== DATA CONTROL COMPLETE =====")

if __name__=="__main__":
    run()
