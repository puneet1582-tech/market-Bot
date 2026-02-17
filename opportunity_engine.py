# REGIME ADAPTIVE OPPORTUNITY ENGINE

from datetime import datetime
from performance_evaluation_engine import evaluate_performance

def calculate_opportunity(symbol, price, market_mode="TRADE"):
    score = 0

    # ---- Base price strength ----
    if price >= 2500:
        score += 30
    elif price >= 1500:
        score += 20
    elif price >= 500:
        score += 10

    # ---- Momentum proxy ----
    if int(price) % 5 == 0:
        score += 20
    else:
        score += 10

    # ---- Stability ----
    score += 20

    # ---- Adaptive learning adjustment ----
    perf = evaluate_performance()
    if perf["invest_signals"] > perf["trade_signals"]:
        score += 5
    else:
        score -= 5

    # ---- Market regime adjustment ----
    if market_mode == "INVEST":
        score += 5
    elif market_mode == "DEFENSIVE":
        score -= 5

    # ---- Final mode decision ----
    if score >= 75:
        mode = "INVEST"
    elif score >= 55:
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
