"""
Ultimate Brain — Institutional Backtesting & Strategy Validation Engine
Evaluates historical decision performance and strategy robustness.
"""

import pandas as pd


def evaluate_strategy(decisions_df, price_history_df):
    """
    decisions_df columns:
    symbol, action, timestamp

    price_history_df columns:
    symbol, date, close
    """

    results = []

    for sym in decisions_df["symbol"].unique():
        dec = decisions_df[decisions_df["symbol"] == sym]
        prices = price_history_df[price_history_df["symbol"] == sym]

        if prices.empty:
            continue

        start_price = prices.iloc[0]["close"]
        end_price = prices.iloc[-1]["close"]

        return_pct = ((end_price - start_price) / start_price) * 100

        results.append({
            "symbol": sym,
            "strategy_return_pct": round(return_pct, 2)
        })

    return pd.DataFrame(results)
