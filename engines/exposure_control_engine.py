"""
Ultimate Brain — Institutional Exposure Control Engine
Adjusts total portfolio exposure based on market cycle positioning.
"""

from datetime import datetime


EXPOSURE_MAP = {
    "EXPANSION": 1.00,
    "ACCUMULATION": 0.80,
    "DISTRIBUTION": 0.60,
    "DEFENSIVE": 0.40
}


def determine_exposure(market_cycle):
    exposure = EXPOSURE_MAP.get(market_cycle, 0.50)

    return {
        "timestamp": str(datetime.utcnow()),
        "market_cycle": market_cycle,
        "recommended_exposure_ratio": exposure
    }
