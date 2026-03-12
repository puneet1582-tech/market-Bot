import pandas as pd

INPUT="data/processed/market_prices.csv"
OUTPUT="data/processed/market_prices.csv"

def run():

    print("\n===== NORMALIZING MARKET PRICE DATABASE =====")

    df=pd.read_csv(INPUT,low_memory=False)

    df["date"]=pd.to_datetime(df["date"],errors="coerce")

    numeric_cols=["open","high","low","close","volume"]

    for c in numeric_cols:
        df[c]=pd.to_numeric(df[c],errors="coerce")

    df=df.dropna(subset=["date","symbol"])

    df=df.sort_values(["symbol","date"])

    df.to_csv(OUTPUT,index=False)

    print("NORMALIZATION COMPLETE")
    print("ROWS:",len(df))
    print("SYMBOLS:",df["symbol"].nunique())
    print("LAST DATE:",df["date"].max())

if __name__=="__main__":
    run()
