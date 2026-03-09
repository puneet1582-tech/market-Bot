import os
import pandas as pd

BHAVCOPY_DIR = "data/bhavcopy"
OUTPUT_FILE = "data/processed/market_prices.csv"

def latest_csv():
    files = [f for f in os.listdir(BHAVCOPY_DIR) if f.endswith(".csv")]
    if not files:
        raise Exception("No CSV found in data/bhavcopy. Ensure ZIP extracted.")
    files.sort()
    return os.path.join(BHAVCOPY_DIR, files[-1])

def detect_error_file(path):
    with open(path, "r", errors="ignore") as f:
        first = f.readline().strip()
    if first.startswith('{"error"'):
        raise Exception(f"Bhavcopy file is NSE error response: {first}")

def pick(colnames, keys):
    for k in keys:
        for c in colnames:
            if k.lower() in c.lower():
                return c
    return None

def parse():
    path = latest_csv()
    print("Loading:", path)
    detect_error_file(path)

    df = pd.read_csv(path)
    cols = list(df.columns)

    sym = pick(cols, ["symbol"])
    opn = pick(cols, ["open"])
    hig = pick(cols, ["high"])
    low = pick(cols, ["low"])
    cls = pick(cols, ["close"])
    vol = pick(cols, ["qty","volume"])

    needed = [sym, opn, hig, low, cls, vol]
    if None in needed:
        raise Exception(f"Required columns missing. Columns present: {cols}")

    out = df[[sym, opn, hig, low, cls, vol]].copy()
    out.columns = ["symbol","open","high","low","close","volume"]
    out = out[out["symbol"].notna()]

    os.makedirs("data/processed", exist_ok=True)
    out.to_csv(OUTPUT_FILE, index=False)

    print("Parsed OK. Rows:", len(out))
    print("Saved:", OUTPUT_FILE)

if __name__ == "__main__":
    parse()
