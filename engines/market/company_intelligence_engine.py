import pandas as pd
import requests
import os

INPUT_FILE = "data/processed/tradable_universe.csv"
OUTPUT_FILE = "data/processed/company_intelligence.csv"

def fetch_company(symbol):

    url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{symbol}.NS?modules=defaultKeyStatistics,financialData"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        stats = data["quoteSummary"]["result"][0]

        marketcap = stats["defaultKeyStatistics"]["marketCap"]["raw"]
        roe = stats["financialData"]["returnOnEquity"]["raw"]
        debt = stats["financialData"]["totalDebt"]["raw"]

        return marketcap, roe, debt

    except:
        return None, None, None


def run():

    df = pd.read_csv(INPUT_FILE)

    records = []

    for sym in df["symbol"].unique():

        mc, roe, debt = fetch_company(sym)

        records.append({
            "symbol": sym,
            "marketcap": mc,
            "roe": roe,
            "debt": debt
        })

    out = pd.DataFrame(records)

    os.makedirs("data/processed", exist_ok=True)

    out.to_csv(OUTPUT_FILE, index=False)

    print("Company intelligence generated")
    print("Saved:", OUTPUT_FILE)


if __name__ == "__main__":
    run()
