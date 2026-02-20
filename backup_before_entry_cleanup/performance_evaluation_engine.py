# PERFORMANCE EVALUATION ENGINE
# Evaluates logged opportunity decisions

import json

PERFORMANCE_FILE = "performance_log.json"

def evaluate_performance():
    try:
        with open(PERFORMANCE_FILE, "r") as f:
            data = json.load(f)

        total = len(data)

        invest = sum(1 for x in data if x["decision_mode"] == "INVEST")
        trade = sum(1 for x in data if x["decision_mode"] == "TRADE")
        defensive = sum(1 for x in data if x["decision_mode"] == "DEFENSIVE")

        return {
            "total_signals": total,
            "invest_signals": invest,
            "trade_signals": trade,
            "defensive_signals": defensive
        }

    except:
        return {
            "total_signals": 0,
            "invest_signals": 0,
            "trade_signals": 0,
            "defensive_signals": 0
        }
