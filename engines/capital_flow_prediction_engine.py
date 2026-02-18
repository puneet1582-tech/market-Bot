"""
Ultimate Brain — Capital Flow Prediction Engine
Forecasts liquidity direction using historical FII/DII flow trends.
"""

import pandas as pd
import numpy as np
from datetime import datetime


def forecast_liquidity(flow_df):
    """
    flow_df columns:
    date, fii_flow, dii_flow
    """

    try:
        flow_df["net_flow"] = flow_df["fii_flow"] + flow_df["dii_flow"]

        rolling = flow_df["net_flow"].rolling(window=5).mean().iloc[-1]

        direction = "NEUTRAL"
        if rolling > 0:
            direction = "POSITIVE_LIQUIDITY"
        elif rolling < 0:
            direction = "NEGATIVE_LIQUIDITY"

        return {
            "timestamp": str(datetime.utcnow()),
            "liquidity_signal": direction,
            "rolling_net_flow": float(rolling)
        }

    except Exception:
        return {
            "timestamp": str(datetime.utcnow()),
            "liquidity_signal": "UNKNOWN",
            "rolling_net_flow": 0
        }
