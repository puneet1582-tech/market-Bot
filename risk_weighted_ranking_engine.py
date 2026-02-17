# RISK WEIGHTED RANKING ENGINE
# Ranks opportunities using risk-adjusted scoring

def risk_weighted_rank(opportunity_list):
    try:
        for op in opportunity_list:
            price = op.get("price", 0)

            # Basic risk proxy (higher price volatility assumed at lower price)
            if price < 500:
                risk = 1.2
            elif price < 1500:
                risk = 1.0
            else:
                risk = 0.9

            op["risk_adjusted_score"] = op.get("score", 0) * risk

        ranked = sorted(
            opportunity_list,
            key=lambda x: x.get("risk_adjusted_score", 0),
            reverse=True
        )

        return ranked

    except Exception as e:
        print("Risk ranking error:", e)
        return opportunity_list
