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

def find_col(cols, options):
    for opt in options:
        for c in cols:
            if opt.lower() in c.lower():
                return c
    return None

def parse_bhavcopy():

    file_path = find_latest_bhavcopy()
    print(f"Loading Bhavcopy: {file_path}")

    df = pd.read_csv(file_path)

    cols = df.columns.tolist()

    symbol = find_col(cols, ["symbol"])
    open_p = find_col(cols, ["open"])
    high_p = find_col(cols, ["high"])
    low_p = find_col(cols, ["low"])
    close_p = find_col(cols, ["close"])
    volume = find_col(cols, ["qty", "volume"])
    date = find_col(cols, ["timestamp", "date"])

    required = [symbol, open_p, high_p, low_p, close_p, volume]

    if None in required:
        raise Exception(f"Required columns not found. Available columns: {cols}")

    df = df[[symbol, open_p, high_p, low_p, close_p, volume]]

    df.columns = [
        "symbol",
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    if date:
        df["date"] = pd.to_datetime(df[date], errors="coerce")
    else:
        df["date"] = pd.Timestamp.today()

    df = df[df["symbol"].notna()]

    os.makedirs("data/processed", exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("Bhavcopy parsed successfully")
    print(f"Saved to {OUTPUT_FILE}")
    print(f"Total stocks processed: {len(df)}")

if __name__ == "__main__":
    parse_bhavcopy()
