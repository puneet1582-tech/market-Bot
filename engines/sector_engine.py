import pandas as pd

FII_PATH = "data/fii_dii.csv"
NEWS_PATH = "data/news.csv"

# 🔁 Sector name mapping
SECTOR_MAP = {
    "Energy": "IT",        # map Energy money flow to IT stocks for now
    "Micro": "Smallcap",
    "Finance": "Finance",
    "IT": "IT"
}

class SectorEngine:
    def __init__(self):
        self.fii = pd.read_csv(FII_PATH)
        self.news = pd.read_csv(NEWS_PATH)

    def normalize_sector(self, sector):
        return SECTOR_MAP.get(sector, sector)

    def rank_sectors(self):
        scores = {}
        reasons = {}

        # FII/DII score (direction + strength)
        for _, row in self.fii.iterrows():
            raw_sector = row["sector"]
            sector = self.normalize_sector(raw_sector)

            fii = float(row["fii"])
            dii = float(row["dii"])

            score = 0
            flow = fii + dii

            # direction
            if fii > 0:
                score += 1
            else:
                score -= 1

            if dii > 0:
                score += 0.5
            else:
                score -= 0.5

            # strength (big money)
            if flow > 500:
                score += 1
            elif flow < -500:
                score -= 1

            scores[sector] = scores.get(sector, 0) + score
            reasons.setdefault(sector, []).append(f"Money flow: {flow}")

        # News score
        for _, row in self.news.iterrows():
            raw_sector = row["sector"]
            sector = self.normalize_sector(raw_sector)

            impact = row["impact"]

            if sector not in scores:
                scores[sector] = 0
                reasons[sector] = []

            if impact == "POSITIVE":
                scores[sector] += 1
                reasons[sector].append("Positive news")
            elif impact == "NEGATIVE":
                scores[sector] -= 1
                reasons[sector].append("Negative news")

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return [(sector, score, "; ".join(reasons.get(sector, []))) for sector, score in ranked]
