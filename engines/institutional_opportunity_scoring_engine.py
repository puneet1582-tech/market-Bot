"""
Ultimate Brain — Institutional Opportunity Scoring Engine
Combines price momentum, liquidity, and fundamental growth scores
to produce institutional opportunity ranking.
"""

import pandas as pd
import os
from datetime import datetime

PRICE_DIR = "data/price_history"
FUNDAMENTAL_FILE = "data/fundamental_growth_scores.csv"
OUTPUT_FILE = "data/institutional_opportunity_scores.csv"


def compute_price_score(df):
    try:
        if len(df) < 60:
            return 0

        recent = df["Close"].iloc[-1]
        past = df["Close"].iloc[-60]

        return ((recent - past) / max(abs(past), 1)) * 100
    except Exception:
        return 0


def run_scoring():
    fundamentals = pd.read_csv(FUNDAMENTAL_FILE)
    scores = []

    for f in os.listdir(PRICE_DIR):
        if not f.endswith(".csv"):
            continue

        symbol = f.replace(".csv", "")
        price_df = pd.read_csv(os.path.join(PRICE_DIR, f))

        price_score = compute_price_score(price_df)

        fund = fundamentals[fundamentals["symbol"] == symbol]
        if fund.empty:
            continue

        rev = fund.iloc[0]["revenue_growth_3y"]
        prof = fund.iloc[0]["profit_growth_3y"]

        total_score = (price_score * 0.4) + (rev * 0.3) + (prof * 0.3)

        scores.append({
            "symbol": symbol,
            "price_momentum_score": round(price_score, 2),
            "revenue_growth_3y": rev,
            "profit_growth_3y": prof,
            "institutional_score": round(total_score, 2),
            "timestamp": str(datetime.utcnow())
        })

    if scores:
        pd.DataFrame(scores).sort_values(
            by="institutional_score", ascending=False
        ).to_csv(OUTPUT_FILE, index=False)

    return len(scores)


if __name__ == "__main__":
    print("Scored:", run_scoring())
