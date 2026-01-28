from engines.sector_engine import SectorEngine
from engines.index_engine import IndexEngine
from engines.volatility_engine import VolatilityEngine

class ModeEngineV2:
    def __init__(self):
        self.sector_engine = SectorEngine()
        self.index_engine = IndexEngine()
        self.vol_engine = VolatilityEngine()

    def decide_mode(self):
        ranked = self.sector_engine.rank_sectors()
        index_trend = self.index_engine.get_trend()
        volatility = self.vol_engine.get_volatility_state()

        reasons = []

        if not ranked:
            return "DEFENSIVE", "No sector strength data"

        top_sector, top_score, sector_why = ranked[0]

        reasons.append(f"Top sector: {top_sector} (score {top_score})")
        reasons.append(f"Sector reason: {sector_why}")
        reasons.append(f"Index trend: {index_trend}")
        reasons.append(f"Volatility: {volatility}")

        # Decision logic
        if index_trend == "DOWN" or volatility == "HIGH":
            return "DEFENSIVE", "; ".join(reasons)

        if index_trend == "UP" and top_score >= 1 and volatility == "LOW":
            return "INVEST", "; ".join(reasons)

        return "TRADE", "; ".join(reasons)
