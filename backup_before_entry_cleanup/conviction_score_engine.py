# CONVICTION SCORE ENGINE
# Calculates institutional conviction score

def calculate_conviction_scores(opportunity_list, sector_scores, capital_flow, persistent_list):
    conviction_output = []

    for op in opportunity_list:
        symbol = op["symbol"]
        sector = op.get("sector", "UNKNOWN")

        score = op.get("score", 0)

        # ---- Sector strength contribution ----
        score += sector_scores.get(sector, 0) * 0.3

        # ---- Capital flow contribution ----
        score += capital_flow.get(sector, 0) * 0.2

        # ---- Persistence bonus ----
        if symbol in persistent_list:
            score += 10

        op["conviction_score"] = round(score, 2)
        conviction_output.append(op)

    return conviction_output
