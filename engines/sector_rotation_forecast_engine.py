"""
Ultimate Brain — Multi-Cycle Sector Rotation Forecast Engine
Forecasts next-cycle sector leadership based on rolling sector performance trends.
"""

import pandas as pd
import numpy as np
from datetime import datetime


def forecast_sector_rotation(sector_returns_df):
    """
    sector_returns_df columns:
    date, sector, return_pct
    """

    try:
        pivot = sector_returns_df.pivot(index="date", columns="sector", values="return_pct")

        rolling_perf = pivot.rolling(window=60).mean().iloc[-1]
        ranked = rolling_perf.sort_values(ascending=False)

        leaders = ranked.head(5).index.tolist()
        laggards = ranked.tail(5).index.tolist()

        return {
            "timestamp": str(datetime.utcnow()),
            "next_cycle_leaders": leaders,
            "lagging_sectors": laggards
        }

    except Exception:
        return {
            "timestamp": str(datetime.utcnow()),
            "next_cycle_leaders": [],
            "lagging_sectors": []
        }
