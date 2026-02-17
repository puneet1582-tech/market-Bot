# SECTOR INTELLIGENCE ENGINE
# Maps sectors to stocks and aggregates opportunity strength

SECTOR_MAP = {
    "ENERGY": ["RELIANCE.NS"],
    "IT": ["TCS.NS"],
    "BANKING": ["HDFCBANK.NS"]
}

def sector_strength(opportunity_list):
    sector_scores = {}

    for sector, stocks in SECTOR_MAP.items():
        scores = [
            op["score"]
            for op in opportunity_list
            if op["symbol"] in stocks
        ]

        if scores:
            sector_scores[sector] = sum(scores) / len(scores)
        else:
            sector_scores[sector] = 0

    return sector_scores
