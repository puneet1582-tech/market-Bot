def explain_mode(market_conditions, mode):
    reasons = []

    if market_conditions["volatility"] == "HIGH":
        reasons.append("Market volatility high hai")

    if market_conditions["liquidity"] == "LOW":
        reasons.append("Liquidity kam hai")

    if market_conditions["global_trend"] == "NEGATIVE":
        reasons.append("Global trend negative hai")

    explanation = " | ".join(reasons)
    return f"Mode: {mode} | Reason: {explanation}"


def explain_stock(stock, data, mode):
    reasons = []

    if data["risk"] == "LOW":
        reasons.append("Low risk business")
    if data["debt"] == 0:
        reasons.append("Debt free company")
    if data["profit"] > 30000:
        reasons.append("Consistent profit")

    reason_text = ", ".join(reasons)

    return f"Stock: {stock} | Mode: {mode} | Why: {reason_text}"


# TEST DATA (sirf test ke liye)
market_conditions = {
    "volatility": "HIGH",
    "liquidity": "LOW",
    "global_trend": "NEGATIVE"
}

mode = "DEFENSIVE MODE"

stock_data = {
    "risk": "LOW",
    "debt": 0,
    "profit": 42000
}

print(explain_mode(market_conditions, mode))
print(explain_stock("TCS", stock_data, mode))
