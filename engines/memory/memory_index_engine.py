import pandas as pd
import os


FEATURE_STORE = "data/memory/market_feature_store.csv"

INDEX_OUTPUT = "data/memory/market_memory_index.csv"
CLUSTER_OUTPUT = "data/memory/pattern_clusters.csv"


def safe_read(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()


def normalize_signal(signal):

    if pd.isna(signal):
        return ""

    s = str(signal)

    parts = s.split("|")

    parts = sorted(parts)

    return "|".join(parts)


def build_index(df):

    df["signal_key"] = df["signals"].apply(normalize_signal)

    index = (
        df.groupby("signal_key")
        .size()
        .reset_index(name="occurrences")
    )

    return index


def build_clusters(df):

    cluster = (
        df.groupby(["sector","alpha_adjusted"])
        .size()
        .reset_index(name="count")
    )

    return cluster


def run():

    df = safe_read(FEATURE_STORE)

    if df.empty:
        print("Feature store empty")
        return

    index = build_index(df)

    clusters = build_clusters(df)

    index.to_csv(INDEX_OUTPUT,index=False)

    clusters.to_csv(CLUSTER_OUTPUT,index=False)

    print("Market memory index created")
    print("Unique patterns:",len(index))
    print("Sector clusters:",len(clusters))


if __name__ == "__main__":
    run()
