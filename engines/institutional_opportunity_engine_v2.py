"""
PHASE-2 REAL CORE
INSTITUTIONAL OPPORTUNITY ENGINE V2 (PILOT)

Combines:
- 10Y fundamental strength
- Momentum
- Sector money flow
- Composite institutional score
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

FUND_FILE = "data/fundamentals_10y_pilot.csv"
PRICE_FILE = "data/nse_price_history.csv"
SECTOR_AUTH_FILE = "data/sector_final_authority.csv"
SECTOR_FLOW_FILE = "data/sector_money_flow.csv"

OUTPUT_FILE = "data/top20_institutional_v2.csv"


# -------------------------------------------------
# UTILITIES
# -------------------------------------------------

def safe_cagr(start, end, years):
    if start <= 0 or years <= 0:
        return 0
    return ((end / start) ** (1 / years) - 1) * 100


# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

def load_data():
    fundamentals = pd.read_csv(FUND_FILE)
    prices = pd.read_csv(PRICE_FILE)
    sector_auth = pd.read_csv(SECTOR_AUTH_FILE)
    sector_flow = pd.read_csv(SECTOR_FLOW_FILE)

    return fundamentals, prices, sector_auth, sector_flow


# -------------------------------------------------
# FUNDAMENTAL SCORING
# -------------------------------------------------

def build_fundamental_scores(fund_df):

    grouped = fund_df.groupby("symbol")

    records = []

    for symbol, df in grouped:

        df = df.sort_values("year")

        if len(df) < 5:
            continue

        revenue_start = df.iloc[0]["revenue"]
        revenue_end = df.iloc[-1]["revenue"]

        profit_start = df.iloc[0]["net_profit"]
        profit_end = df.iloc[-1]["net_profit"]

        years = len(df) - 1

        rev_cagr = safe_cagr(revenue_start, revenue_end, years)
        profit_cagr = safe_cagr(profit_start, profit_end, years)

        avg_roe = df["roe"].mean()
        avg_debt = df["debt"].mean()

        fundamental_score = (
            rev_cagr * 0.35 +
            profit_cagr * 0.35 +
            avg_roe * 0.20 -
            (avg_debt / 1e9) * 0.10
        )

        records.append({
            "symbol": symbol,
            "rev_cagr": rev_cagr,
            "profit_cagr": profit_cagr,
            "avg_roe": avg_roe,
            "fundamental_score": fundamental_score
        })

    return pd.DataFrame(records)


# -------------------------------------------------
# MOMENTUM SCORE
# -------------------------------------------------

def build_momentum_score(price_df):

    grouped = price_df.groupby("symbol")

    records = []

    for symbol, df in grouped:

        prices = df["close"].dropna().values

        if len(prices) < 2:
            continue

        momentum = ((prices[-1] - prices[0]) / prices[0]) * 100

        records.append({
            "symbol": symbol,
            "momentum_score": momentum
        })

    return pd.DataFrame(records)


# -------------------------------------------------
# FINAL COMPOSITE
# -------------------------------------------------

def build_final_scores(fund_df, momentum_df, sector_auth, sector_flow):

    df = fund_df.merge(momentum_df, on="symbol", how="left")
    df = df.merge(sector_auth, on="symbol", how="left")
    df = df.merge(sector_flow[["sector", "price_change_pct"]], on="sector", how="left")

    df["momentum_score"] = df["momentum_score"].fillna(0)
    df["price_change_pct"] = df["price_change_pct"].fillna(0)

    df["composite_score"] = (
        df["fundamental_score"] * 0.5 +
        df["momentum_score"] * 0.3 +
        df["price_change_pct"] * 0.2
    )

    df["computed_time"] = datetime.utcnow()

    return df.sort_values("composite_score", ascending=False)


# -------------------------------------------------
# RUN ENGINE
# -------------------------------------------------

def run_institutional_v2():

    logging.info("INSTITUTIONAL OPPORTUNITY ENGINE V2 STARTED")

    fundamentals, prices, sector_auth, sector_flow = load_data()

    fund_scores = build_fundamental_scores(fundamentals)
    momentum_scores = build_momentum_score(prices)

    final_df = build_final_scores(
        fund_scores,
        momentum_scores,
        sector_auth,
        sector_flow
    )

    top20 = final_df.head(20)

    top20.to_csv(OUTPUT_FILE, index=False)

    logging.info("TOP-20 V2 BUILT SUCCESSFULLY")


if __name__ == "__main__":
    run_institutional_v2()
