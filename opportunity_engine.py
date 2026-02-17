# MULTI-FACTOR OPPORTUNITY ENGINE

from datetime import datetime
from performance_evaluation_engine import evaluate_performance

def calculate_opportunity(symbol, price, market_mode="TRADE", sector_score=0, capital_flow=0):
    score = 0

    # ---- Price strength ----
    if price >= 2500:
        score += 25
    elif price >= 1500:
        score += 15
    elif price >= 500:
        score += 8

    # ---- Sector strength factor ----
    score += sector_score * 0.2

    # ---- Capital flow factor ----
    if capital_flow > 0:
        score += 10
    elif capital_flow < 0:
        score -= 5

    # ---- Learning adjustment ----
    perf = evaluate_performance()
    if perf["invest_signals"] > perf["trade_signals"]:
        score += 5

    # ---- Market regime adjustment ----
    if market_mode == "INVEST":
        score += 5
    elif market_mode == "DEFENSIVE":
        score -= 5

    # ---- Final classification ----
    if score >= 60:
        mode = "INVEST"
    elif score >= 40:
        mode = "TRADE"
    else:
        mode = "DEFENSIVE"

    return {
        "symbol": symbol,
        "price": price,
        "score": score,
        "mode": mode,
        "timestamp": str(datetime.now())
    }
