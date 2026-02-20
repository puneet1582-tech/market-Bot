"""
Ultimate Brain — Institutional Timing Optimization Engine
Determines whether capital deployment should be Immediate, Staggered, or Delayed
based on exposure ratio, volatility level, and market cycle.
"""

from datetime import datetime


def optimize_timing(exposure_ratio, volatility_level, market_cycle):
    """
    exposure_ratio: float (0 to 1)
    volatility_level: numeric volatility indicator
    market_cycle: EXPANSION / ACCUMULATION / DISTRIBUTION / DEFENSIVE
    """

    decision = "WAIT"

    try:
        if market_cycle == "EXPANSION" and volatility_level < 20:
            decision = "DEPLOY"
        elif market_cycle in ["ACCUMULATION", "DISTRIBUTION"]:
            decision = "STAGGER"
        else:
            decision = "WAIT"

        return {
            "timestamp": str(datetime.utcnow()),
            "market_cycle": market_cycle,
            "exposure_ratio": exposure_ratio,
            "volatility_level": volatility_level,
            "timing_decision": decision
        }

    except Exception:
        return {
            "timestamp": str(datetime.utcnow()),
            "timing_decision": "WAIT"
        }
