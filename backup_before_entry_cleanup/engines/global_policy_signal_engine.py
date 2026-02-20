"""
Ultimate Brain — Global Policy & Central Bank Signal Intelligence Engine
Transforms central-bank policy signals into market-impact indicators.
"""

from datetime import datetime


POLICY_IMPACT_MAP = {
    "RATE_HIKE": "NEGATIVE_EQUITY",
    "RATE_CUT": "POSITIVE_EQUITY",
    "QE": "LIQUIDITY_POSITIVE",
    "QT": "LIQUIDITY_NEGATIVE",
    "NEUTRAL": "NEUTRAL"
}


def interpret_policy(policy_event):
    """
    policy_event examples:
    RATE_HIKE, RATE_CUT, QE, QT
    """
    impact = POLICY_IMPACT_MAP.get(policy_event, "NEUTRAL")

    return {
        "timestamp": str(datetime.utcnow()),
        "policy_event": policy_event,
        "market_impact_signal": impact
    }
