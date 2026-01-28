def rank_sectors(sector_map, news_impact, inet_impact):
    sector_score = {}

    for sector in sector_map.keys():
        score = 0
        score += news_impact.get(sector, 0)
        score += inet_impact.get(sector, 0)
        sector_score[sector] = score

    ranked = sorted(sector_score.items(), key=lambda x: x[1], 
reverse=True)
    return ranked

