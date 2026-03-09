import pandas as pd
import os


RAW_DIR = "data/fundamentals/raw"
OUTPUT_FILE = "data/fundamentals/processed/fundamentals_master.csv"


def load_raw_files():

    files = []

    if not os.path.exists(RAW_DIR):
        return []

    for f in os.listdir(RAW_DIR):

        if f.endswith(".csv"):

            path = os.path.join(RAW_DIR,f)

            try:

                df = pd.read_csv(path)

                files.append(df)

            except:

                pass

    return files


def normalize(df):

    columns = {c.lower():c for c in df.columns}

    rename = {}

    if "revenue" in columns:
        rename[columns["revenue"]] = "revenue"

    if "sales" in columns:
        rename[columns["sales"]] = "revenue"

    if "net profit" in columns:
        rename[columns["net profit"]] = "net_profit"

    if "profit" in columns:
        rename[columns["profit"]] = "net_profit"

    if "roce" in columns:
        rename[columns["roce"]] = "roce"

    if "debt" in columns:
        rename[columns["debt"]] = "debt"

    df = df.rename(columns=rename)

    return df


def run():

    data = load_raw_files()

    if len(data) == 0:

        print("No raw fundamentals found")

        return


    frames = []

    for df in data:

        df = normalize(df)

        frames.append(df)


    master = pd.concat(frames,ignore_index=True)

    master.to_csv(
        OUTPUT_FILE,
        index=False
    )


    print("Fundamental master dataset created")
    print("Rows:",len(master))


if __name__ == "__main__":
    run()
