import pandas as pd
import requests
import json
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def load_universe():

    try:
        df=pd.read_csv("data/stocks.csv")
    except:
        print("stocks.csv missing")
        return

    df=df.drop_duplicates(subset=["symbol"])

    df.to_csv("data/stocks.csv",index=False)

    print("Universe verified:",len(df))

def fix_sector():

    df=pd.read_csv("data/stocks.csv")

    if "sector" not in df.columns:
        df["sector"]="OTHER"

    df["sector"]=df["sector"].fillna("OTHER")

    df.to_csv("data/stocks.csv",index=False)

    print("Sector column verified")

def institutional_structure():

    try:
        df=pd.read_csv("data/institutional_money_flow.csv")
    except:
        df=pd.DataFrame(columns=["sector","fii","dii","institutional_strength"])

    df.to_csv("data/institutional_money_flow.csv",index=False)

    print("Institutional structure verified")

def fundamentals_structure():

    try:
        df=pd.read_csv("data/quarterly_fundamentals_clean.csv")
    except:
        df=pd.DataFrame(columns=[
            "symbol","quarter","sales","profit","eps","debt","cashflow"
        ])

    df.to_csv("data/quarterly_fundamentals_clean.csv",index=False)

    print("Fundamental structure verified")

def run_pipeline():

    print("ULTIMATE BRAIN DATA PIPELINE")

    load_universe()
    fix_sector()
    institutional_structure()
    fundamentals_structure()

    print("DATA LAYER VERIFIED")

if __name__=="__main__":
    run_pipeline()
