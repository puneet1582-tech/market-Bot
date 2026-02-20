"""
Ultimate Brain — Early Warning Risk Radar Engine
Detects sudden volatility spikes, liquidity shocks, and regime shift signals.
"""

import numpy as np
from datetime import datetime


def detect_risk(volatility_series, liquidity_series):
    """
    volatility_series: list of recent volatility values
    liquidity_series: list of recent net liquidity values
    """

    try:
        vol_mean = np.mean(volatility_series)
        vol_latest = volatility_series[-1]

        liq_mean = np.mean(liquidity_series)
        liq_latest = liquidity_series[-1]

        risk_flags = []

        if vol_latest > vol_mean * 1.5:
            risk_flags.append("VOLATILITY_SPIKE")

        if liq_latest < liq_mean * 0.5:
            risk_flags.append("LIQUIDITY_SHOCK")

        regime_shift = len(risk_flags) > 0

        return {
            "timestamp": str(datetime.utcnow()),
            "risk_flags": risk_flags,
            "regime_shift_risk": regime_shift
        }

    except Exception:
        return {
            "timestamp": str(datetime.utcnow()),
            "risk_flags": [],
            "regime_shift_risk": False
        }
