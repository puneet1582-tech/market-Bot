import pandas as pd
import os


SIGNAL_FILE = "data/processed/signal_matrix.csv"
ALPHA_FILE = "data/processed/alpha_opportunities.csv"
SECTOR_MAP = "data/processed/stock_sector_map.csv"

OUTPUT_FILE = "data/memory/market_feature_store.csv"


REQUIRED_COLUMNS = [
    "symbol",
    "sector",
    "signals",
    "alpha_adjusted"
]


def safe_read(path):

    if not os.path.exists(path):
        return pd.DataFrame()

    try:
        return pd.read_csv(path)

    except Exception as e:
        print("Read error:",path)
        return pd.DataFrame()



def validate_schema(df):

    missing = []

    for col in REQUIRED_COLUMNS:

        if col not in df.columns:
            missing.append(col)

    if len(missing) > 0:

        print("Schema error. Missing columns:",missing)

        return False

    return True



def build_feature_store():

    signals = safe_read(SIGNAL_FILE)
    alpha = safe_read(ALPHA_FILE)
    sector_map = safe_read(SECTOR_MAP)

    if signals.empty:
        print("Signal matrix missing")
        return

    df = signals.copy()

    if not alpha.empty:
        df = df.merge(
            alpha[["symbol","alpha_adjusted"]],
            on="symbol",
            how="left"
        )

    if not sector_map.empty:

        if "sector" not in df.columns:

            df = df.merge(
                sector_map,
                on="symbol",
                how="left"
            )

    if not validate_schema(df):
        print("Feature store aborted")
        return


    df["signal_count"] = df["signals"].astype(str).apply(
        lambda x: len(x.split("|")) if x != "nan" else 0
    )


    df["alpha_adjusted"] = df["alpha_adjusted"].fillna("NONE")


    df = df.sort_values(
        by=["alpha_adjusted","signal_count"],
        ascending=[True,False]
    )


    os.makedirs("data/memory",exist_ok=True)

    df.to_csv(OUTPUT_FILE,index=False)

    print("Feature store built")
    print("Rows:",len(df))



def run():

    build_feature_store()



if __name__ == "__main__":
    run()
