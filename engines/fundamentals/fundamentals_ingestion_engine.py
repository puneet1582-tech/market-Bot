import pandas as pd
import os
import glob

RAW_PATH = "data/fundamentals/raw"
OUT_PATH = "data/fundamentals/processed/fundamentals_master.csv"


def load_files():

    files = glob.glob(f"{RAW_PATH}/*.csv")

    if not files:
        print("No fundamentals files found")
        return None

    frames = []

    for f in files:

        try:

            df = pd.read_csv(f)

            if "symbol" not in df.columns:
                continue

            frames.append(df)

        except Exception as e:

            print("File error:",f)


    if not frames:
        return None

    return pd.concat(frames,ignore_index=True)



def normalize(df):

    cols = [c.lower() for c in df.columns]

    df.columns = cols

    numeric_cols = [
        "revenue",
        "profit",
        "net_profit",
        "roe",
        "roce",
        "debt"
    ]

    for c in numeric_cols:

        if c in df.columns:

            df[c] = pd.to_numeric(df[c],errors="coerce")

    return df



def run():

    df = load_files()

    if df is None:

        print("No fundamentals files found")

        return

    df = normalize(df)

    df.to_csv(
        OUT_PATH,
        index=False
    )

    print("Fundamentals ingestion complete")
    print("Rows:",len(df))


if __name__ == "__main__":
    run()
