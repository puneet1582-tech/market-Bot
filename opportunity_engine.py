# OPPORTUNITY DETECTION ENGINE
# Core Intelligence Layer (INVEST / TRADE / DEFENSIVE)

from datetime import datetime

def calculate_opportunity(symbol, price):
    """
    Simple scoring framework (initial live integration layer)
    Later will connect with fundamentals, sector, liquidity, news
    """

    if price > 2000:
        mode = "INVEST"
        score = 80
    elif price > 1000:
        mode = "TRADE"
        score = 65
    else:
        mode = "DEFENSIVE"
        score = 45

    return {
        "symbol": symbol,
        "price": price,
        "score": score,
        "mode": mode,
        "timestamp": str(datetime.now())
    }
