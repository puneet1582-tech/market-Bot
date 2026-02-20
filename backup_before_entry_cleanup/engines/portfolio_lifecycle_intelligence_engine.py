"""
Ultimate Brain — Portfolio Lifecycle Intelligence Engine
Tracks lifecycle stage of each portfolio position.
"""

from datetime import datetime


def evaluate_lifecycle(entry_price, current_price):
    """
    Determines lifecycle stage based on price movement from entry.
    """

    try:
        change_pct = ((current_price - entry_price) / entry_price) * 100

        if change_pct > 25:
            stage = "REDUCE"
        elif change_pct > 10:
            stage = "HOLD"
        elif change_pct > 0:
            stage = "BUILD_UP"
        elif change_pct > -10:
            stage = "ENTRY"
        else:
            stage = "EXIT"

        return {
            "timestamp": str(datetime.utcnow()),
            "entry_price": entry_price,
            "current_price": current_price,
            "change_pct": round(change_pct, 2),
            "lifecycle_stage": stage
        }

    except Exception:
        return {
            "timestamp": str(datetime.utcnow()),
            "lifecycle_stage": "UNKNOWN"
        }
