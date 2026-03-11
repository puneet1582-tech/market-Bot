import pandas as pd
import os


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
        print("Signal matrix missing")
        return

    df = signals.copy()

    if not alpha.empty:

        alpha_map = alpha[["symbol","alpha_adjusted"]]

        df = df.merge(
            alpha_map,
            on="symbol",
            how="left"
        )

    else:

        df["alpha_adjusted"] = "NEUTRAL"


    os.makedirs("data/memory",exist_ok=True)

    if os.path.exists(FEATURE_STORE):

        old = pd.read_csv(FEATURE_STORE)

        df = pd.concat([old,df],ignore_index=True)

        df = df.drop_duplicates(
            subset=["symbol","signals","alpha_adjusted"],
            keep="last"
        )

    df.to_csv(FEATURE_STORE,index=False)

    print("Feature store updated")
    print("Rows:",len(df))


if __name__ == "__main__":
    run()
