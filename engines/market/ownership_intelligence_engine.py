import pandas as pd
import requests
import os
import time

INPUT_FILE = "data/processed/tradable_universe.csv"
OUTPUT_FILE = "data/processed/ownership_intelligence.csv"

def fetch_holding(symbol):
    # Yahoo finance summary endpoint
    url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{symbol}.NS?modules=majorHoldersBreakdown"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        result = data["quoteSummary"]["result"][0]["majorHoldersBreakdown"]

        insiders = result.get("insidersPercentHeld", {}).get("raw")
        institutions = result.get("institutionsPercentHeld", {}).get("raw")

        return insiders, institutions

    except:
        return None, None


def run():

    df = pd.read_csv(INPUT_FILE)

    records = []

    for sym in df["symbol"].unique():

        insiders, institutions = fetch_holding(sym)

        records.append({
            "symbol": sym,
            "insider_holding": insiders,
            "institutional_holding": institutions
        })

        time.sleep(0.5)

    out = pd.DataFrame(records)

    os.makedirs("data/processed", exist_ok=True)

    out.to_csv(OUTPUT_FILE, index=False)

    print("Ownership intelligence generated")
    print("Saved:", OUTPUT_FILE)


if __name__ == "__main__":
    run()
