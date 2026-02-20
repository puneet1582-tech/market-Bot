"""
Ultimate Brain — Quarterly 3-Year Rolling Fundamental Comparison
Classifies stocks: Long-term / Swing / Intraday / Avoid
"""

import pandas as pd


def compute_growth(series):
    try:
        if len(series) < 2:
            return 0
        return ((series.iloc[0] - series.iloc[-1]) / abs(series.iloc[-1])) * 100
    except Exception:
        return 0


def classify_stock(financial_df):
    try:
        revenue_growth = compute_growth(financial_df["Revenue"])
        profit_growth = compute_growth(financial_df["NetProfit"])

        if revenue_growth > 20 and profit_growth > 20:
            return "LONG_TERM"
        elif revenue_growth > 10:
            return "SWING"
        elif revenue_growth > 0:
            return "INTRADAY"
        else:
            return "AVOID"
    except Exception:
        return "UNKNOWN"
