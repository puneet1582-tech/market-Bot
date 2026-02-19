"""
SECTOR MONEY FLOW ENGINE
Institutional Sector Rotation Intelligence
Authoritative Sector Map Based
"""

import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

PRICE_FILE = "data/nse_price_history.csv"
SECTOR_FILE = "data/sector_final_authority.csv"
OUTPUT_FILE = "data/sector_money_flow.csv"

def load_data():
    prices = pd.read_csv(PRICE_FILE)
    sectors = pd.read_csv(SECTOR_FILE)
    return prices, sectors

def compute_sector_money_flow(prices, sectors):

    # Merge authoritative sector mapping
    df = prices.merge(sectors[["symbol","sector"]], on="symbol", how="left")

    # Drop rows without sector
    df = df.dropna(subset=["sector"])

    # Compute price change per symbol
    grouped = df.groupby("symbol")["price"].agg(["first","last"]).reset_index()
    grouped["price_change_pct"] = ((grouped["last"] - grouped["first"]) / grouped["first"]) * 100

    # Merge back sector
    grouped = grouped.merge(sectors[["symbol","sector"]], on="symbol", how="left")

    # Sector aggregation
    sector_flow = grouped.groupby("sector")["price_change_pct"].mean().reset_index()

    sector_flow["computed_time"] = datetime.utcnow()

    return sector_flow

def run_sector_money_flow_engine():

    logging.info("SECTOR MONEY FLOW ENGINE STARTED")

    prices, sectors = load_data()

    result = compute_sector_money_flow(prices, sectors)

    result.to_csv(OUTPUT_FILE, index=False)

    logging.info("SECTOR MONEY FLOW COMPUTED SUCCESSFULLY")

if __name__ == "__main__":
    run_sector_money_flow_engine()
