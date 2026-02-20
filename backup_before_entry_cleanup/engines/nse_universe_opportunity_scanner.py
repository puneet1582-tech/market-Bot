"""
Ultimate Brain — NSE Universe Opportunity Scanner
Scans entire NSE universe and generates daily Top-20 opportunity list
"""

import pandas as pd
from datetime import datetime


def load_universe():
    try:
        df = pd.read_csv("nse_universe.csv")
        return df["symbol"].tolist()
    except Exception:
        return []


def rank_opportunities(price_data):
    ranked = sorted(price_data, key=lambda x: x.get("score", 0), reverse=True)
    return ranked[:20]


def generate_opportunity_list(price_feed):
    universe = load_universe()
    opportunities = []

    for s in universe:
        d = price_feed.get(s, {})
        score = d.get("price", 0)  # placeholder scoring logic
        opportunities.append({
            "symbol": s,
            "score": score,
            "timestamp": str(datetime.utcnow())
        })

    return rank_opportunities(opportunities)
