import pandas as pd
from config.paths import FUNDAMENTALS_FILE


def load_data():
    return pd.read_csv(FUNDAMENTALS_FILE)


def decide_market_mode():
    return "INVEST"


def stock_score(row):

    score = 0
    reason = []

    if row["revenue_growth"] >= 10:
        score += 1
        reason.append("Revenue growth strong")

    if row["promoter_holding"] >= 50:
        score += 1
        reason.append("Promoter holding high")

    if row["pledge"] == 0:
        score += 1
        reason.append("No pledge")

    if row["cash_flow_years"] >= 3:
        score += 1
        reason.append("Stable cash flow")

    if row["debt_trend"] in ["stable", "reducing", "zero"]:
        score += 1
        reason.append("Debt under control")

    return score, ", ".join(reason)


def generate_report():

    df = load_data()

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
