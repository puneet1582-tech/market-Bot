import os
import pandas as pd
from datetime import datetime

DATA_DIR = "data/fundamentals"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "quarterly_comparison_report.csv")


def load_fundamental_files():

    frames = []

    if not os.path.exists(DATA_DIR):
        print("Fundamentals folder not found")
        return None

    for f in os.listdir(DATA_DIR):

        if f.endswith(".csv"):

            path = os.path.join(DATA_DIR, f)

            try:

                df = pd.read_csv(path)

                df["source_file"] = f

                frames.append(df)

            except Exception as e:

                print("Error reading:", f)

    if not frames:
        return None

    data = pd.concat(frames, ignore_index=True)

    return data


def clean_data(df):

    df.columns = [c.strip().lower() for c in df.columns]

    required = ["symbol", "quarter", "revenue", "net_profit", "debt"]

    for col in required:
        if col not in df.columns:
            df[col] = None

    return df


def quarterly_comparison(df):

    results = []

    companies = df["symbol"].unique()

    for company in companies:

        cdf = df[df["symbol"] == company]

        cdf = cdf.sort_values("quarter")

        prev_row = None

        for _, row in cdf.iterrows():

            if prev_row is None:
                prev_row = row
                continue

            revenue_growth = None
            profit_growth = None
            debt_change = None

            try:
                revenue_growth = (row["revenue"] - prev_row["revenue"]) / prev_row["revenue"] * 100
            except:
                pass

            try:
                profit_growth = (row["net_profit"] - prev_row["net_profit"]) / prev_row["net_profit"] * 100
            except:
                pass

            try:
                debt_change = row["debt"] - prev_row["debt"]
            except:
                pass

            results.append({

                "symbol": company,
                "quarter": row["quarter"],
                "revenue_growth_%": revenue_growth,
                "profit_growth_%": profit_growth,
                "debt_change": debt_change

            })

            prev_row = row

    return pd.DataFrame(results)


def save_report(df):

    df["generated_at"] = datetime.now()

    df.to_csv(OUTPUT_FILE, index=False)

    print("Quarterly comparison report created:", OUTPUT_FILE)


def run():

    data = load_fundamental_files()

    if data is None:
        print("No fundamental data found")
        return

    data = clean_data(data)

    result = quarterly_comparison(data)

    save_report(result)


if __name__ == "__main__":
