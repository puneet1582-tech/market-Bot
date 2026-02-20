# MARKET REGIME INTELLIGENCE ENGINE
# Estimates probability of market regimes

def estimate_market_regime(market_data):
    try:
        volatility = market_data.get("volatility_index", 20)
        sentiment = market_data.get("sentiment", 50)
        fii_flow = market_data.get("fii_flow", 0)

        bull_prob = 0
        bear_prob = 0
        sideways_prob = 0

        # ---- Simple institutional regime logic ----
        if sentiment > 60 and fii_flow > 0:
            bull_prob += 60
        if sentiment < 40 and fii_flow < 0:
            bear_prob += 60

        if volatility > 20:
            sideways_prob += 50

        remaining = 100 - (bull_prob + bear_prob + sideways_prob)
        if remaining > 0:
            sideways_prob += remaining

        return {
            "bull_probability": bull_prob,
            "bear_probability": bear_prob,
            "sideways_probability": sideways_prob
        }

    except Exception as e:
        print("Regime estimation error:", e)
        return {
            "bull_probability": 33,
            "bear_probability": 33,
            "sideways_probability": 34
        }
