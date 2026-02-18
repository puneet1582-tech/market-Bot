"""
SECTOR MONEY FLOW ENGINE
Institutional-grade sector capital flow intelligence
Detects which sectors are receiving liquidity inflows / outflows
PHASE-2 REAL CORE BUILD
"""

import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

PRICE_FILE = "data/price_data.csv"
SECTOR_MAP_FILE = "data/sector_map.csv"
OUTPUT_FILE = "data/sector_money_flow.csv"


def load_data():
    prices = pd.read_csv(PRICE_FILE)
    sector_map = pd.read_csv(SECTOR_MAP_FILE)
    return prices, sector_map


def compute_sector_money_flow(prices, sector_map):

    # Merge sector info
    df = prices.merge(sector_map, on="symbol", how="left")

    # Liquidity proxy = Close * Volume
    df["money_flow"] = df["close"] * df["volume"]

    sector_flow = (
        df.groupby("sector")["money_flow"]
        .sum()
        .reset_index()
        .sort_values("money_flow", ascending=False)
    )

    sector_flow["timestamp"] = datetime.utcnow()

    return sector_flow


def run_sector_money_flow_engine():

    logging.info("SECTOR MONEY FLOW ENGINE STARTED")

    prices, sector_map = load_data()

    result = compute_sector_money_flow(prices, sector_map)

    result.to_csv(OUTPUT_FILE, index=False)

    logging.info("Sector money flow intelligence generated")


if __name__ == "__main__":
    run_sector_money_flow_engine()
