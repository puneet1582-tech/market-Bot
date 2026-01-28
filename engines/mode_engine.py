from engines.sector_engine import SectorEngine

class ModeEngine:
    def __init__(self):
        self.sector_engine = SectorEngine()

    def decide_mode(self):
        ranked = self.sector_engine.rank_sectors()

        if not ranked:
            return "DEFENSIVE"

        top_sector, top_score, sector_why = ranked[0]


        if top_score >= 1:
            return "INVEST"
        elif top_score < 0:
            return "DEFENSIVE"
        else:
            return "TRADE"
