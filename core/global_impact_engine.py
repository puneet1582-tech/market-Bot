"""
ULTIMATE BRAIN
GLOBAL NEWS → SECTOR → STOCK IMPACT ENGINE
Structured Deterministic Model
"""

import pandas as pd
from pathlib import Path
from core.sector_engine import SectorEngine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVENT_FILE = PROJECT_ROOT / "data" / "global" / "global_events.csv"
SECTOR_FILE = PROJECT_ROOT / "data" / "sector" / "sector_mapping.csv"


class GlobalImpactEngine:

    def __init__(self):
        self.events = pd.read_csv(EVENT_FILE)
        self.sector_mapping = pd.read_csv(SECTOR_FILE)
        self.sector_engine = SectorEngine()

    def run(self):

        sector_summary = self.sector_engine.run()

        impact_results = {}

        for _, event_row in self.events.iterrows():

            sector = event_row["sector"]
            impact = event_row["impact"]

            affected_stocks = self.sector_mapping[
                self.sector_mapping["sector"] == sector
            ]["symbol"].tolist()

            for stock in affected_stocks:

                if stock not in impact_results:
                    impact_results[stock] = []

                impact_results[stock].append(impact)

        final_impact = {}

        for stock, impacts in impact_results.items():

            if "NEGATIVE" in impacts:
                classification = "NEGATIVE_IMPACT"
            elif "POSITIVE" in impacts:
                classification = "POSITIVE_IMPACT"
            else:
                classification = "NEUTRAL_IMPACT"

            final_impact[stock] = classification

        return final_impact


if __name__ == "__main__":
    engine = GlobalImpactEngine()
    result = engine.run()
    print("Global Impact Engine Completed")
    print(result)
