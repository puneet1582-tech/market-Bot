import pandas as pd
import requests
import yfinance as yf
from io import StringIO
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

HEADERS={"User-Agent":"Mozilla/5.0"}

# ===============================
# NSE UNIVERSE
# ===============================

def fetch_nse_universe():

    url="https://archives.nseindia.com/content/equities/EQUITY_L.csv"

    r=requests.get(url,headers=HEADERS,timeout=30)

    df=pd.read_csv(StringIO(r.text))

    df=df.rename(columns={
        "SYMBOL":"symbol",
        "NAME OF COMPANY":"company",
        "ISIN NUMBER":"isin"
    })[["symbol","company","isin"]]

    df.to_csv(DATA_DIR/"stocks.csv",index=False)

    print("NSE stocks:",len(df))


# ===============================
# SECTOR CLASSIFICATION
# ===============================

def build_sector():

    df=pd.read_csv(DATA_DIR/"stocks.csv")

    keywords={
        "BANK":["BANK"],
        "IT":["TECH","INFOTECH","SOFTWARE"],
        "PHARMA":["PHARMA","DRUG"],
        "AUTO":["AUTO","MOTOR"],
        "METAL":["STEEL","METAL"],
        "INFRA":["INFRA","ENGINEERING"],
        "CHEMICAL":["CHEM","INDUSTRIES"]
    }

    sectors=[]

    for name in df["company"]:

        name=str(name).upper()

        sector="OTHER"

        for s,keys in keywords.items():

            if any(k in name for k in keys):

                sector=s
                break

        sectors.append(sector)

    df["sector"]=sectors

    df.to_csv(DATA_DIR/"stocks.csv",index=False)

    print("Sector mapping complete")


# ===============================
# FUNDAMENTALS (YAHOO)
# ===============================

def fetch_fundamentals():

    stocks=pd.read_csv(DATA_DIR/"stocks.csv")

    rows=[]

    for sym in stocks["symbol"][:200]:

        ticker=sym+".NS"

        try:

            t=yf.Ticker(ticker)

            info=t.info

            rows.append({

                "symbol":sym,

                "market_cap":info.get("marketCap"),

                "pe":info.get("trailingPE"),

                "roe":info.get("returnOnEquity"),

                "debt_equity":info.get("debtToEquity")

            })

        except:

            continue

    df=pd.DataFrame(rows)

    df.to_csv(DATA_DIR/"fundamentals.csv",index=False)

    print("Fundamental rows:",len(df))


# ===============================
# RUN
# ===============================

def run():

    print("ULTIMATE VERIFIED DATA ENGINE")

    fetch_nse_universe()

    build_sector()

    fetch_fundamentals()

    print("DATA ENGINE COMPLETE")


if __name__=="__main__":

    run()

