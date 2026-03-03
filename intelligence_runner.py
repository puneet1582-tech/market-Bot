from core.master_brain import MasterBrain
from global_event_engine import GlobalEventEngine
import csv

class IntelligenceNarrative:

    def __init__(self):
        self.brain = MasterBrain()
        self.global_engine = GlobalEventEngine()
        self.sector_map = self.load_sector_map()

    def load_sector_map(self):
        mapping = {}
        try:
            with open("data/sector/sector_mapping.csv", newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    mapping[row["symbol"].strip().upper()] = row["sector"].strip().upper()
        except:
            pass
        return mapping

    def classify_sector(self, symbol):
        return self.sector_map.get(symbol, "SMALL_CAP")

    def build_war_impact_text(self, sector):
        impact = self.global_engine.get_sector_impact(sector)

        if impact > 0:
            return f"युद्ध की स्थिति में यह सेक्टर लगभग +{impact}% तक लाभ पा सकता है।"
        elif impact < 0:
            return f"युद्ध की स्थिति में यह सेक्टर लगभग {impact}% तक प्रभावित हो सकता है।"
        else:
            return "युद्ध का इस सेक्टर पर सीमित या तटस्थ प्रभाव।"

    def run(self):
        raw = self.brain.execute()

        report = {}
        report["MARKET_MODE"] = raw["MARKET_SUMMARY"]["mode"]
        report["GLOBAL_EVENT"] = self.global_engine.current_event

        enriched = []

        for stock in raw["TOP_20"]:

            symbol = stock["symbol"]
            sector = self.classify_sector(symbol)

            enriched.append({
                "symbol": symbol,
                "sector": sector,
                "war_impact_view": self.build_war_impact_text(sector)
            })

        report["TOP_STOCK_INTELLIGENCE"] = enriched

        return report


if __name__ == "__main__":
    runner = IntelligenceNarrative()
    result = runner.run()
    print(result)
