"""
Ultimate Brain — Portfolio Stress Testing Engine
Simulates portfolio performance under different macro scenarios.
"""

import pandas as pd


SCENARIO_FACTORS = {
    "MARKET_CRASH": -0.30,
    "RATE_HIKE": -0.10,
    "BULL_RUN": 0.25,
    "SIDEWAYS": 0.02
}


def simulate_portfolio(portfolio_weights, scenario):
    factor = SCENARIO_FACTORS.get(scenario, 0)

    results = []

    for sym, weight in portfolio_weights.items():
        impact = weight * factor
        results.append({
            "symbol": sym,
            "weight": weight,
            "scenario": scenario,
            "impact_pct": round(impact * 100, 2)
        })

    return pd.DataFrame(results)
