import pandas as pd
import os

INPUT_FILE = "data/fundamentals/processed/fundamentals_master.csv"
OUTPUT_FILE = "data/fundamentals/processed/business_evolution.csv"


def safe_read(path):

    if os.path.exists(path):
        return pd.read_csv(path)

    return pd.DataFrame()


def classify_business(df):

    revenue_growth = df["revenue"].pct_change().mean()
    profit_growth = df["net_profit"].pct_change().mean()
    roce_avg = df["roce"].mean()
    debt_trend = df["debt"].pct_change().mean()

    if revenue_growth > 0.15 and profit_growth > 0.15 and roce_avg > 18:
        return "WORLD_CLASS_BUSINESS"

    if revenue_growth > 0.10 and profit_growth > 0.10:
        return "QUALITY_BUSINESS"

    if revenue_growth > 0:
        return "AVERAGE_BUSINESS"

    return "WEAK_BUSINESS"


def run():

    df = safe_read(INPUT_FILE)

    if df.empty:
        print("No fundamentals master data")
        return

    results = []

    for symbol, group in df.groupby("symbol"):

        group = group.sort_values("year")

        classification = classify_business(group)

        results.append({
            "symbol": symbol,
            "business_quality": classification
        })

    out = pd.DataFrame(results)

    out.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Business evolution analysis complete")
    print("Companies analysed:",len(out))


if __name__ == "__main__":
    run()
