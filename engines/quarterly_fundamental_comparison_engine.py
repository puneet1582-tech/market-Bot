"""
Ultimate Brain — Quarterly Fundamental Comparison Engine
Computes 3-year rolling quarterly growth trends for revenue and profit.
"""

import pandas as pd
import os
from datetime import datetime

INPUT_DIR = "data/fundamentals_quarterly"
OUTPUT_FILE = "data/fundamental_growth_scores.csv"


def compute_growth(df):
    try:
        df = df.T
        df = df.sort_index()

        if len(df) < 12:
            return None

        recent = df.iloc[-1]
        past = df.iloc[-12]

        revenue_growth = (
            (recent.get("Total Revenue", 0) - past.get("Total Revenue", 0))
            / max(abs(past.get("Total Revenue", 1)), 1)
        ) * 100

        profit_growth = (
            (recent.get("Net Income", 0) - past.get("Net Income", 0))
            / max(abs(past.get("Net Income", 1)), 1)
        ) * 100

        return revenue_growth, profit_growth
    except Exception:
        return None


def run_engine():
    rows = []

    for f in os.listdir(INPUT_DIR):
        if not f.endswith(".csv"):
            continue

        symbol = f.replace(".csv", "")
        df = pd.read_csv(os.path.join(INPUT_DIR, f), index_col=0)

        g = compute_growth(df)
        if g:
            rows.append({
                "symbol": symbol,
                "revenue_growth_3y": round(g[0], 2),
                "profit_growth_3y": round(g[1], 2),
                "timestamp": str(datetime.utcnow())
            })

    if rows:
        pd.DataFrame(rows).to_csv(OUTPUT_FILE, index=False)

    return len(rows)


if __name__ == "__main__":
    print("Processed:", run_engine())
