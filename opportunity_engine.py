# INSTITUTIONAL OPPORTUNITY ENGINE
# Quant-style scoring foundation

from datetime import datetime

def calculate_opportunity(symbol, price):
    score = 0

    # ---- Price Strength ----
    if price >= 2500:
        score += 30
    elif price >= 1500:
        score += 20
    elif price >= 500:
        score += 10

    # ---- Liquidity Proxy (temporary logic) ----
    if price % 5 == 0:
        score += 20
    else:
        score += 10

    # ---- Trend Proxy ----
    if price > 1000:
        score += 20
    else:
        score += 10

    # ---- Base Stability ----
    score += 20

    # ---- Mode Decision ----
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
