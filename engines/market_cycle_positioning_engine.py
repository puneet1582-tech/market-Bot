"""
Ultimate Brain — Market Cycle Positioning Engine
Determines current market cycle phase using liquidity, volatility,
and trend signals.
"""

from datetime import datetime


def detect_market_cycle(liquidity_signal, volatility_level, trend_strength):
    """
    liquidity_signal: POSITIVE_LIQUIDITY / NEGATIVE_LIQUIDITY / NEUTRAL
    volatility_level: numeric volatility index
    trend_strength: POSITIVE / NEGATIVE / SIDEWAYS
    """

    cycle = "DEFENSIVE"

    try:
        if liquidity_signal == "POSITIVE_LIQUIDITY" and trend_strength == "POSITIVE":
            cycle = "EXPANSION"
        elif liquidity_signal == "POSITIVE_LIQUIDITY" and trend_strength == "SIDEWAYS":
            cycle = "ACCUMULATION"
        elif liquidity_signal == "NEGATIVE_LIQUIDITY" and trend_strength == "NEGATIVE":
            cycle = "DEFENSIVE"
        else:
            cycle = "DISTRIBUTION"

        return {
            "timestamp": str(datetime.utcnow()),
            "market_cycle": cycle,
            "inputs": {
                "liquidity": liquidity_signal,
                "volatility": volatility_level,
                "trend": trend_strength
            }
        }

    except Exception:
        return {
            "timestamp": str(datetime.utcnow()),
            "market_cycle": "UNKNOWN"
        }
