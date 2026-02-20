"""
ULTIMATE BRAIN
SECTOR INTELLIGENCE ENGINE
Sector Strength Classification
"""

import pandas as pd
from pathlib import Path
from collections import defaultdict
from core.intelligence_engine import IntelligenceEngine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SECTOR_FILE = PROJECT_ROOT / "data" / "sector" / "sector_mapping.csv"


class SectorEngine:

    def __init__(self):
        if not SECTOR_FILE.exists():
            raise RuntimeError("Sector mapping file missing")

        self.mapping = pd.read_csv(SECTOR_FILE)
        self.intelligence_engine = IntelligenceEngine()

    def run(self):

        intelligence_output = self.intelligence_engine.run()

        sector_data = defaultdict(list)

        for symbol, metrics in intelligence_output.items():

            row = self.mapping[self.mapping["symbol"] == symbol]

            if row.empty:
                continue

            sector = row.iloc[0]["sector"]
            cagr = metrics.get("cagr")
            trend = metrics.get("trend")

            if cagr is not None:
                sector_data[sector].append({
                    "cagr": cagr,
                    "trend": trend
                })

        sector_summary = {}

        for sector, stocks in sector_data.items():

            avg_cagr = sum(s["cagr"] for s in stocks) / len(stocks)

            strong_trend_count = sum(
                1 for s in stocks if s["trend"] == "STRONG_UPTREND"
            )

            strength_ratio = strong_trend_count / len(stocks)

            if avg_cagr > 0.15 and strength_ratio > 0.5:
                classification = "STRONG_SECTOR"
            elif avg_cagr > 0:
                classification = "NEUTRAL_SECTOR"
            else:
                classification = "WEAK_SECTOR"

            sector_summary[sector] = {
                "avg_cagr": round(avg_cagr, 4),
                "strength_ratio": round(strength_ratio, 4),
                "classification": classification
            }

        return sector_summary


if __name__ == "__main__":
    engine = SectorEngine()
    result = engine.run()
    print("Sector Intelligence Engine Completed")
    print(result)
