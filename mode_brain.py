market_conditions = {
    "volatility": "HIGH",     # LOW / MEDIUM / HIGH
    "liquidity": "LOW",       # LOW / MEDIUM / HIGH
    "global_trend": "NEGATIVE"  # POSITIVE / NEUTRAL / NEGATIVE
}

def decide_mode(conditions):
    if conditions["volatility"] == "HIGH" and conditions["global_trend"] == "NEGATIVE":
        return "DEFENSIVE MODE"
    elif conditions["liquidity"] == "HIGH" and conditions["global_trend"] == "POSITIVE":
        return "INVEST MODE"
    else:
        return "TRADE MODE"

mode = decide_mode(market_conditions)

print("MARKET CONDITIONS:", market_conditions)
print("ACTIVE MODE:", mode)
