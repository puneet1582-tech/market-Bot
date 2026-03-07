import pandas as pd
import os

DATA_FILE = "data/annual_10y/annual_fundamentals_10y.csv"
OUT_FILE = "data/business_evolution_10y.csv"


def build_business_evolution():

    if not os.path.exists(DATA_FILE):
        print("Annual fundamentals file missing.")
        return

    df = pd.read_csv(DATA_FILE)

    if "symbol" not in df.columns:
        print("Symbol column missing.")
        return

    results = []

    for symbol, group in df.groupby("symbol"):

        group = group.sort_values("year")

        rev_start = group["revenue"].iloc[0]
        rev_end = group["revenue"].iloc[-1]

        profit_start = group["net_profit"].iloc[0]
        profit_end = group["net_profit"].iloc[-1]

        debt_start = group["debt"].iloc[0]
        debt_end = group["debt"].iloc[-1]

        results.append({
            "symbol": symbol,
            "revenue_growth": rev_end - rev_start,
            "profit_growth": profit_end - profit_start,
            "debt_change": debt_end - debt_start,
            "years_analyzed": len(group)
        })

    out = pd.DataFrame(results)

    out.to_csv(OUT_FILE, index=False)

    print("BUSINESS EVOLUTION ENGINE COMPLETE")
    print("Companies analyzed:", len(out))
    print("Saved:", OUT_FILE)



if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
