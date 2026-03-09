import os
import pandas as pd

BHAVCOPY_DIR = "data/bhavcopy"
OUTPUT_FILE = "data/processed/market_prices.csv"

def find_latest_bhavcopy():
    files = [f for f in os.listdir(BHAVCOPY_DIR) if f.endswith(".csv")]
    if not files:
        raise Exception("No bhavcopy CSV found")

    files.sort()
    return os.path.join(BHAVCOPY_DIR, files[-1])

def parse_bhavcopy():

    file_path = find_latest_bhavcopy()
    print(f"Loading Bhavcopy: {file_path}")

    df = pd.read_csv(file_path)

    required_cols = [
        "SYMBOL",
        "OPEN",
        "HIGH",
        "LOW",
        "CLOSE",
        "TOTTRDQTY",
        "TIMESTAMP"
    ]

    df = df[required_cols]

    df.columns = [
        "symbol",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "date"
    ]

    df = df[df["symbol"].notna()]

    df["date"] = pd.to_datetime(df["date"], dayfirst=True)

    os.makedirs("data/processed", exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("Bhavcopy parsed successfully")
    print(f"Saved to {OUTPUT_FILE}")
    print(f"Total stocks processed: {len(df)}")

if __name__ == "__main__":
    parse_bhavcopy()
