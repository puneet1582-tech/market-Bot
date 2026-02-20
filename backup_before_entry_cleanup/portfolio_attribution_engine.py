# PORTFOLIO PERFORMANCE ATTRIBUTION ENGINE
# Calculates allocation contribution summary

import json

PORTFOLIO_HISTORY_FILE = "portfolio_lifecycle.json"

def calculate_portfolio_attribution():
    try:
        with open(PORTFOLIO_HISTORY_FILE, "r") as f:
            history = json.load(f)

        contribution = {}

        for entry in history:
            for item in entry.get("portfolio", []):
                symbol = item["symbol"]
                contribution[symbol] = contribution.get(symbol, 0) + item.get("allocation_percent", 0)

        return contribution

    except:
        return {}
