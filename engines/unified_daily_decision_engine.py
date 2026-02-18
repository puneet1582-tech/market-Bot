"""
Ultimate Brain — Unified Daily Institutional Decision Engine
Combines market mode, opportunity intelligence, and fundamentals
to produce final daily institutional decisions.
"""

from datetime import datetime


def generate_daily_decision(market_mode, opportunities, classifications):
    decisions = []

    for op in opportunities:
        sym = op.get("symbol")
        cls = classifications.get(sym, "UNKNOWN")

        action = "HOLD"

        if market_mode == "INVEST" and cls == "LONG_TERM":
            action = "ACCUMULATE"
        elif market_mode == "TRADE" and cls in ["SWING", "INTRADAY"]:
            action = "TRADE"
        elif market_mode == "DEFENSIVE":
            action = "REDUCE"

        decisions.append({
            "symbol": sym,
            "classification": cls,
            "action": action,
            "timestamp": str(datetime.utcnow())
        })

    return decisions
