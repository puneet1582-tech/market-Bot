"""
INSTITUTIONAL TOP-20 OPPORTUNITY ENGINE
Momentum + Sector Rotation Based
Phase-2 Operational Core
"""

import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

PRICE_FILE = "data/nse_price_history.csv"
SECTOR_FLOW_FILE = "data/sector_money_flow.csv"
SECTOR_AUTH_FILE = "data/sector_final_authority.csv"
OUTPUT_FILE = "data/top20_institutional_opportunities.csv"


def load_data():
    prices = pd.read_csv(PRICE_FILE)
    sector_flow = pd.read_csv(SECTOR_FLOW_FILE)
    sector_auth = pd.read_csv(SECTOR_AUTH_FILE)
    return prices, sector_flow, sector_auth


def compute_momentum(prices):
    grouped = prices.groupby("symbol")["price"].agg(["first","last"]).reset_index()
    grouped["momentum_score"] = ((grouped["last"] - grouped["first"]) / grouped["first"]) * 100
    return grouped[["symbol","momentum_score"]]


def build_top20():

    prices, sector_flow, sector_auth = load_data()

    momentum = compute_momentum(prices)

    # Merge sector
    df = momentum.merge(sector_auth[["symbol","sector"]], on="symbol", how="left")

    # Merge sector strength
    df = df.merge(sector_flow[["sector","price_change_pct"]], on="sector", how="left")

    df.rename(columns={"price_change_pct":"sector_strength"}, inplace=True)

    df.fillna(0, inplace=True)

    # Composite Score
    df["composite_score"] = (
        0.6 * df["momentum_score"] +
        0.4 * df["sector_strength"]
    )

    df["computed_time"] = datetime.utcnow()

    df.sort_values(by="composite_score", ascending=False, inplace=True)

    top20 = df.head(20)

    return top20


def run_institutional_top20_engine():
    logging.info("INSTITUTIONAL TOP-20 ENGINE STARTED")

    top20 = build_top20()

    top20.to_csv(OUTPUT_FILE, index=False)

    logging.info("TOP-20 OPPORTUNITIES GENERATED")


if __name__ == "__main__":
    run_institutional_top20_engine()
