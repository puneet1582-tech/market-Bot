def news_score(row):
    score = 0

    if row["news_type"] in ["Policy_Positive", "Result_Positive"]:
        score += 20
    if row["news_type"] == "Regulatory_Negative":
        score -= 30

    if row["impact"] == "High":
        score += 10
    elif row["impact"] == "Low":
        score -= 5

    return score

