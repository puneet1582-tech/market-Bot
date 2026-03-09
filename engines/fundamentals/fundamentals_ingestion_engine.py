import pandas as pd
import os
import glob


INPUT_DIR = "data/raw/fundamentals"
OUTPUT_FILE = "data/processed/company_fundamentals_10y.csv"


REQUIRED_COLUMNS = [
    "symbol",
    "year",
    "revenue",
    "profit",
    "operating_margin",
    "roe",
    "roce",
    "debt",
    "free_cash_flow"
]


def load_files():

    files = glob.glob(os.path.join(INPUT_DIR,"*.csv"))

    frames = []

    for f in files:

        try:

            df = pd.read_csv(f)

            frames.append(df)

        except:

            pass

    if frames:

        return pd.concat(frames,ignore_index=True)

    return pd.DataFrame()


def normalize_schema(df):

    for col in REQUIRED_COLUMNS:

        if col not in df.columns:

            df[col] = None

    df = df[REQUIRED_COLUMNS]

    return df


def clean_numeric(df):

    numeric_cols = [
        "revenue",
        "profit",
        "operating_margin",
        "roe",
        "roce",
        "debt",
        "free_cash_flow"
    ]

    for c in numeric_cols:

        df[c] = (
            df[c]
            .astype(str)
            .str.replace(",","")
        )

        df[c] = pd.to_numeric(df[c],errors="coerce")

    return df


def run():

    df = load_files()

    if df.empty:

        print("No fundamentals files found")

        return


    df = normalize_schema(df)

    df = clean_numeric(df)

    df = df.sort_values(
        ["symbol","year"]
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Fundamentals ingestion complete")
    print("Rows:",len(df))


if __name__ == "__main__":
    run()
