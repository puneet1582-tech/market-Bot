"""
SECTOR MONEY FLOW ENGINE
Keyword-based sector mapping + price aggregation
Production-grade architecture
"""

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

PRICE_FILE = "data/price_data.csv"
UNIVERSE_FILE = "data/nse_live_universe.csv"
SECTOR_KEYWORD_FILE = "data/sector_map.csv"
OUTPUT_FILE = "data/sector_money_flow.csv"


def load_data():
    prices = pd.read_csv(PRICE_FILE)
    universe = pd.read_csv(UNIVERSE_FILE)
    sector_keywords = pd.read_csv(SECTOR_KEYWORD_FILE)
    return prices, universe, sector_keywords


def assign_sector(company_name, sector_keywords):
    company_name = str(company_name).upper()
    for _, row in sector_keywords.iterrows():
        if row["keyword"] in company_name:
            return row["sector"]
    return "Others"


def compute_sector_money_flow(prices, universe, sector_keywords):

    # Map sector using keyword logic
    universe["sector"] = universe["company_name"].apply(
        lambda x: assign_sector(x, sector_keywords)
    )

    # Merge prices with sector info
    df = prices.merge(
        universe[["symbol", "sector"]],
        on="symbol",
        how="left"
    )

    # Calculate daily money flow
    if "close" in df.columns and "volume" in df.columns:
        df["money_flow"] = df["close"] * df["volume"]
    else:
        raise Exception("Price file missing required columns: close, volume")

    sector_flow = (
        df.groupby("sector")["money_flow"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    return sector_flow


def run_sector_money_flow_engine():
    logging.info("SECTOR MONEY FLOW ENGINE STARTED")

    prices, universe, sector_keywords = load_data()
    result = compute_sector_money_flow(prices, universe, sector_keywords)

    result.to_csv(OUTPUT_FILE, index=False)

    logging.info("SECTOR MONEY FLOW ENGINE COMPLETED")
    logging.info(f"Top Sector: {result.iloc[0]['sector']}")


if __name__ == "__main__":
    run_sector_money_flow_engine()
