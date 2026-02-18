"""
Ultimate Brain — Self-Learning Alpha Improvement Engine
Adjusts opportunity scoring weights based on historical performance feedback.
"""

from datetime import datetime


def adjust_weights(performance_df, current_weights):
    """
    performance_df columns:
    symbol, strategy_return_pct
    current_weights:
    dict of scoring weights
    """

    try:
        avg_return = performance_df["strategy_return_pct"].mean()

        updated_weights = dict(current_weights)

        if avg_return > 0:
            for k in updated_weights:
                updated_weights[k] = round(updated_weights[k] * 1.05, 4)
        else:
            for k in updated_weights:
                updated_weights[k] = round(updated_weights[k] * 0.95, 4)

        return {
            "timestamp": str(datetime.utcnow()),
            "average_return": float(avg_return),
            "updated_weights": updated_weights
        }

    except Exception:
        return {
            "timestamp": str(datetime.utcnow()),
            "average_return": 0,
            "updated_weights": current_weights
        }
