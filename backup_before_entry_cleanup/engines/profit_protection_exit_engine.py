"""
Ultimate Brain — Profit Protection & Dynamic Exit Engine
Determines trailing stop levels and exit signals dynamically.
"""

from datetime import datetime


def calculate_exit(entry_price, current_price):
    try:
        gain_pct = ((current_price - entry_price) / entry_price) * 100

        if gain_pct >= 25:
            trailing_stop = current_price * 0.90
            exit_signal = "PROFIT_LOCK"
        elif gain_pct >= 10:
            trailing_stop = current_price * 0.92
            exit_signal = "TRAIL_PROTECT"
        elif gain_pct < -10:
            trailing_stop = entry_price * 0.90
            exit_signal = "STOP_LOSS"
        else:
            trailing_stop = entry_price * 0.95
            exit_signal = "HOLD"

        return {
            "timestamp": str(datetime.utcnow()),
            "entry_price": entry_price,
            "current_price": current_price,
            "gain_pct": round(gain_pct, 2),
            "trailing_stop": round(trailing_stop, 2),
            "exit_signal": exit_signal
        }

    except Exception:
        return {
            "timestamp": str(datetime.utcnow()),
            "exit_signal": "UNKNOWN"
        }
