import pandas as pd
import os
from datetime import datetime


SIGNAL_FILE = "data/processed/signal_matrix.csv"
ALPHA_FILE = "data/processed/alpha_opportunities.csv"

FEATURE_STORE = "data/memory/market_feature_store.csv"


def safe_read(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()


def run():

    signals = safe_read(SIGNAL_FILE)
    alpha = safe_read(ALPHA_FILE)

    if signals.empty:
        print("Signal data missing")
        return

    today = datetime.utcnow().strftime("%Y-%m-%d")

    signals["date"] = today

    if not alpha.empty:
        alpha["alpha_flag"] = True
        df = signals.merge(alpha[["symbol","alpha_flag"]], on="symbol", how="left")
    else:
        df = signals.copy()
        df["alpha_flag"] = False


    if os.path.exists(FEATURE_STORE):

        hist = pd.read_csv(FEATURE_STORE)

        df = pd.concat([hist,df],ignore_index=True)

        df = df.drop_duplicates(subset=["date","symbol"],keep="last")

    df.to_csv(FEATURE_STORE,index=False)

    print("Feature store updated")
    print("Rows:",len(df))


if __name__ == "__main__":
    run()
