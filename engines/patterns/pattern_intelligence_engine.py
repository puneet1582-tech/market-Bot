import pandas as pd
import os


FEATURE_STORE = "data/memory/market_feature_store.csv"

PATTERN_LIBRARY = "data/memory/pattern_library.csv"
PATTERN_STATS = "data/memory/pattern_success_rate.csv"


def safe_read(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()


def extract_patterns(df):

    df["signal_pattern"] = df["signals"].astype(str)

    pattern_counts = (
        df.groupby("signal_pattern")
        .size()
        .reset_index(name="occurrences")
    )

    return pattern_counts


def compute_pattern_stats(df):

    df["signal_pattern"] = df["signals"].astype(str)

    stats = (
        df.groupby("signal_pattern")["alpha_adjusted"]
        .value_counts()
        .unstack(fill_value=0)
    )

    stats["total"] = stats.sum(axis=1)

    for col in stats.columns:
        if col != "total":
            stats[col+"_rate"] = stats[col] / stats["total"]

    stats = stats.reset_index()

    return stats


def run():

    store = safe_read(FEATURE_STORE)

    if store.empty:
        print("Feature store empty")
        return

    patterns = extract_patterns(store)

    stats = compute_pattern_stats(store)

    patterns.to_csv(PATTERN_LIBRARY,index=False)

    stats.to_csv(PATTERN_STATS,index=False)

    print("Pattern intelligence updated")
    print("Unique patterns:",len(patterns))


if __name__ == "__main__":
    run()
