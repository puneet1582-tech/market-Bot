"""
Ultimate Brain — 10-Year Fundamentals + Quarterly Comparison Engine
Institutional-grade fundamentals ingestion for long-term intelligence
"""

import yfinance as yf
from datetime import datetime


def fetch_10y_fundamentals(symbol):
    try:
        t = yf.Ticker(symbol)

        financials = t.financials
        balance = t.balance_sheet
        cashflow = t.cashflow

        data = {
            "symbol": symbol,
            "timestamp": str(datetime.utcnow()),
            "financials": financials.to_dict(),
            "balance_sheet": balance.to_dict(),
            "cashflow": cashflow.to_dict()
        }

        return data

    except Exception:
        return {
            "symbol": symbol,
            "timestamp": str(datetime.utcnow()),
            "financials": {},
            "balance_sheet": {},
            "cashflow": {}
        }


def quarterly_growth(financials_dict):
    try:
        periods = list(financials_dict.keys())
        if len(periods) < 2:
            return {}

        latest = financials_dict[periods[0]]
        prev = financials_dict[periods[1]]

        growth = {}
        for k in latest:
            if k in prev and prev[k] != 0:
                growth[k] = round(((latest[k] - prev[k]) / abs(prev[k])) * 100, 2)

        return growth

    except Exception:
        return {}
