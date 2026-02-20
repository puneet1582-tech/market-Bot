import pandas as pd

# Load fundamentals
df = pd.read_csv("data/fundamentals.csv")

def decide_market_mode():
    # Abhi simple rakhenge
    return "INVEST"

def stock_score(row):
    score = 0
    reason = []

    # Revenue growth
    if row["revenue_growth"] >= 10:
        score += 1
        reason.append("Revenue growth strong")

    # Promoter holding
    if row["promoter_holding"] >= 50:
        score += 1
        reason.append("Promoter holding high")

    # Pledge
    if row["pledge"] == 0:
        score += 1
        reason.append("No pledge")

    # Cash flow years
    if row["cash_flow_years"] >= 3:
        score += 1
        reason.append("Stable cash flow")

    # Debt trend
    if row["debt_trend"] in ["stable", "reducing", "zero"]:
        score += 1
        reason.append("Debt under control")

    return score, ", ".join(reason)

def generate_report():
    report = {}
    mode = decide_market_mode()
    report["MODE"] = mode
    report["STOCKS"] = []

    for _, row in df.iterrows():
        score, reason = stock_score(row)

        if score >= 4:
            decision = "BUY"
        elif score == 3:
            decision = "WAIT"
        else:
            decision = "AVOID"

        report["STOCKS"].append({
            "symbol": row["symbol"],
            "decision": decision,
            "score": score,
            "reason": reason
        })

    return report

# DISABLED ENTRY POINT
# if __name__ == "__main__":
    rep = generate_report()
    print("MARKET MODE:", rep["MODE"])
    print("STOCK ANALYSIS:\n")
    for s in rep["STOCKS"]:
        print(
            s["symbol"],
            "=>",
            s["decision"],
            "| SCORE:", s["score"],
            "|", s["reason"]
        )

