def fundamental_score(row):
    score = 0

    if row["promoter_holding"] >= 50 and row["pledge"] == 0:
        score += 30
    if row["cash_flow_years"] >= 2:
        score += 25
    if row["debt_trend"] in ["stable", "reducing", "zero"]:
        score += 20
    if row["revenue_growth"] >= 10:
        score += 15

    return score

