"""
SECTOR MONEY FLOW ENGINE (SAFE MODE)
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

    # Ensure required columns exist
    prices = prices[["symbol", "price"]].copy()

    # Convert price safely
    prices["price"] = pd.to_numeric(prices["price"], errors="coerce")

    # Drop invalid price rows
    prices = prices.dropna(subset=["price"])

    return prices, sectors

def compute_sector_money_flow(prices, sectors):

    df = prices.merge(sectors[["symbol","sector"]], on="symbol", how="left")
    df = df.dropna(subset=["sector"])

    grouped = df.groupby("symbol")["price"].agg(["first","last"]).reset_index()
    grouped["price_change_pct"] = (
        (grouped["last"] - grouped["first"]) / grouped["first"]
    ) * 100

    grouped = grouped.merge(sectors[["symbol","sector"]], on="symbol", how="left")

    sector_flow = grouped.groupby("sector")["price_change_pct"].mean().reset_index()
    sector_flow["computed_time"] = datetime.utcnow()

    return sector_flow

def run_sector_money_flow_engine():

    logging.info("SECTOR MONEY FLOW ENGINE STARTED")

    prices, sectors = load_data()
    result = compute_sector_money_flow(prices, sectors)

    result.to_csv(OUTPUT_FILE, index=False)

    logging.info("SECTOR MONEY FLOW COMPUTED SUCCESSFULLY")
