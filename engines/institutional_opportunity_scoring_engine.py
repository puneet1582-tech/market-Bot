"""
INSTITUTIONAL OPPORTUNITY SCORING ENGINE
Top-20 Daily Opportunity Detection Core
Production-grade composite scoring layer
"""

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

UNIVERSE_FILE = "data/nse_live_universe.csv"
PRICE_FILE = "data/price_history.csv"
FUNDAMENTALS_FILE = "data/fundamentals_master.csv"
OUTPUT_FILE = "data/top20_opportunities.csv"


def load_data():
    universe = pd.read_csv(UNIVERSE_FILE)
    prices = pd.read_csv(PRICE_FILE)
    fundamentals = pd.read_csv(FUNDAMENTALS_FILE)
    return universe, prices, fundamentals


def compute_scores(universe, prices, fundamentals):

    df = universe.merge(fundamentals, on="symbol", how="left")

    # Example composite institutional score (expandable)
    df["score"] = (
        df["roe"].fillna(0) * 0.25 +
        df["roce"].fillna(0) * 0.25 +
        df["net_profit"].fillna(0) * 0.25 +
        (1 / (df["debt"].replace(0, 1))) * 0.25
    )

    df = df.sort_values("score", ascending=False)
    return df.head(20)


def run_institutional_scoring():

    logging.info("Loading master datasets")
    universe, prices, fundamentals = load_data()

    logging.info("Computing institutional composite scores")
    top20 = compute_scores(universe, prices, fundamentals)

    top20.to_csv(OUTPUT_FILE, index=False)

    logging.info("TOP-20 OPPORTUNITY LIST GENERATED")


# DISABLED ENTRY POINT
# # DISABLED ENTRY POINT
    run_institutional_scoring()
