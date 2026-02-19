"""
PHASE-2 REAL CORE
SECTOR MONEY FLOW ENGINE (DATA-VALIDATED VERSION)

Uses:
- data/nse_price_history.csv
- data/nse_live_universe.csv
- data/sector_map.csv

Computes:
- Stock price momentum
- Sector aggregated momentum
"""

import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

PRICE_FILE = "data/nse_price_history.csv"
UNIVERSE_FILE = "data/nse_live_universe.csv"
SECTOR_MAP_FILE = "data/sector_map.csv"
OUTPUT_FILE = "data/sector_money_flow.csv"


def load_data():
    prices = pd.read_csv(PRICE_FILE)
    universe = pd.read_csv(UNIVERSE_FILE)
    sector_keywords = pd.read_csv(SECTOR_MAP_FILE)
    return prices, universe, sector_keywords


def compute_price_momentum(prices):
    momentum_data = []

    grouped = prices.groupby("symbol")

    for symbol, df in grouped:
        df = df.reset_index(drop=True)
        first_price = df.loc[0, "price"]
        last_price = df.loc[len(df) - 1, "price"]

        if first_price == 0:
            continue

        pct_change = ((last_price - first_price) / first_price) * 100

        momentum_data.append({
            "symbol": symbol,
            "price_change_pct": round(pct_change, 2)
        })

    return pd.DataFrame(momentum_data)


def map_sector(symbol_df, universe, sector_keywords):

    merged = symbol_df.merge(universe[["symbol", "company_name"]], on="symbol", how="left")

    def detect_sector(name):
        if pd.isna(name):
            return "Unknown"

        name_upper = name.upper()

        for _, row in sector_keywords.iterrows():
            if row["keyword"] in name_upper:
                return row["sector"]

        return "Others"

    merged["sector"] = merged["company_name"].apply(detect_sector)

    return merged


def aggregate_sector_strength(mapped_df):

    sector_strength = mapped_df.groupby("sector")["price_change_pct"].mean().reset_index()

    sector_strength = sector_strength.sort_values(by="price_change_pct", ascending=False)

    return sector_strength


def run_sector_money_flow_engine():

    logging.info("SECTOR MONEY FLOW ENGINE STARTED")

    prices, universe, sector_keywords = load_data()

    momentum = compute_price_momentum(prices)

    mapped = map_sector(momentum, universe, sector_keywords)

    sector_strength = aggregate_sector_strength(mapped)

    sector_strength["computed_time"] = datetime.now()

    sector_strength.to_csv(OUTPUT_FILE, index=False)

    logging.info("SECTOR MONEY FLOW ENGINE COMPLETED")
    logging.info(f"Output saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    run_sector_money_flow_engine()
