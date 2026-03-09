import pandas as pd
import os


FUNDAMENTALS_FILE = "data/processed/company_fundamentals_10y.csv"
OUTPUT_FILE = "data/processed/business_evolution.csv"


def safe_read(path):

    if os.path.exists(path):
        return pd.read_csv(path)

    return pd.DataFrame()


def revenue_trend(df):

    values = df["revenue"].dropna().values

    if len(values) < 3:
        return "UNKNOWN"

    if values[-1] > values[0] * 2:
        return "STRONG_GROWTH"

    if values[-1] > values[0]:
        return "MODERATE_GROWTH"

    if values[-1] < values[0]:
        return "DECLINE"

    return "STABLE"


def profit_trend(df):

    values = df["profit"].dropna().values

    if len(values) < 3:
        return "UNKNOWN"

    if values[-1] > values[0] * 2:
        return "STRONG_PROFIT_GROWTH"

    if values[-1] > values[0]:
        return "PROFIT_GROWTH"

    if values[-1] < values[0]:
        return "PROFIT_DECLINE"

    return "STABLE"


def roce_quality(df):

    if "roce" not in df.columns:
        return "UNKNOWN"

    avg = df["roce"].mean()

    if avg > 20:
        return "EXCELLENT"

    if avg > 15:
        return "GOOD"

    if avg > 10:
        return "AVERAGE"

    return "WEAK"


def classify_business(row):

    rev = row["revenue_trend"]
    prof = row["profit_trend"]
    roce = row["roce_quality"]


    if rev == "STRONG_GROWTH" and prof == "STRONG_PROFIT_GROWTH" and roce == "EXCELLENT":
        return "COMPOUNDER"

    if rev == "MODERATE_GROWTH" and prof in ["PROFIT_GROWTH","STRONG_PROFIT_GROWTH"]:
        return "QUALITY_BUSINESS"

    if rev == "DECLINE":
        return "DECLINING_BUSINESS"

    return "AVERAGE_BUSINESS"


def run():

    df = safe_read(FUNDAMENTALS_FILE)

    if df.empty:
        print("Fundamentals data missing")
        return


    result = []

    for symbol, group in df.groupby("symbol"):

        group = group.sort_values("year")

        rev = revenue_trend(group)
        prof = profit_trend(group)
        roce = roce_quality(group)

        result.append({
            "symbol": symbol,
            "revenue_trend": rev,
            "profit_trend": prof,
            "roce_quality": roce
        })


    out = pd.DataFrame(result)

    out["business_type"] = out.apply(
        classify_business,
        axis=1
    )

    out.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Business evolution analysis complete")
    print("Companies analysed:",len(out))


if __name__ == "__main__":
    run()
