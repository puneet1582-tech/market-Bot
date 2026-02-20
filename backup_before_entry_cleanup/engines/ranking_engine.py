def rank_sectors(results):
    sector_scores = {}

    for row in results:
        sector = row["sector"]
        score = row["score"]

        if sector not in sector_scores:
            sector_scores[sector] = 0

        sector_scores[sector] += score

    ranked = sorted(sector_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked
