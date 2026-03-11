import pandas as pd
import os


FEATURE_STORE = "data/memory/market_feature_store.csv"

INDEX_OUTPUT = "data/memory/market_memory_index.csv"
CLUSTER_OUTPUT = "data/memory/pattern_clusters.csv"


REQUIRED_COLUMNS = [
    "symbol",
    "sector",
    "alpha_adjusted",
    "signals"
]


def safe_read(path):

    if not os.path.exists(path):
        print("Feature store missing")
        return pd.DataFrame()

    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print("Feature store read error:",e)
        return pd.DataFrame()


def validate_schema(df):

    missing = []

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            missing.append(col)

    if missing:
        print("Schema error. Missing columns:",missing)
        return False

    return True


def normalize_signal(signal):

    if pd.isna(signal):
        return ""

    s = str(signal)

    s = s.replace(" ","")
    s = s.upper()

    return s


def build_clusters(df):

    df["signals"] = df["signals"].apply(normalize_signal)

    clusters = (
        df.groupby(["sector","alpha_adjusted"])
        .size()
        .reset_index(name="count")
        .sort_values("count",ascending=False)
    )

    return clusters


def build_memory_index(df):

    memory = (
        df.groupby("signals")
        .size()
        .reset_index(name="frequency")
        .sort_values("frequency",ascending=False)
    )

    return memory


def run():

    df = safe_read(FEATURE_STORE)

    if df.empty:
        print("Feature store empty")
        return

    if not validate_schema(df):
        print("Memory engine aborted (schema invalid)")
        return

    clusters = build_clusters(df)

    memory_index = build_memory_index(df)

    clusters.to_csv(CLUSTER_OUTPUT,index=False)

    memory_index.to_csv(INDEX_OUTPUT,index=False)

    print("Memory index built")
    print("Patterns:",len(memory_index))
    print("Clusters:",len(clusters))


if __name__ == "__main__":
    run()
