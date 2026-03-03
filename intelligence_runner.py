from core.master_brain import MasterBrain
from global_event_engine import GlobalEventEngine
import csv

class IntelligenceNarrative:

    def __init__(self):
        self.brain = MasterBrain()
        self.event_engine = GlobalEventEngine()

    def run(self):
        raw_output = self.brain.execute()
        return self.build_readable_output(raw_output)

    def get_sector(self, symbol):

        try:
            with open("data/sector/sector_mapping.csv", newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["symbol"] == symbol:
                        return row["sector"]
        except:
            pass

        return "UNKNOWN"

    def build_readable_output(self, raw):

        report = {}
        report["MARKET_MODE"] = raw["MARKET_SUMMARY"]["mode"]
        report["GLOBAL_EVENT"] = "WAR"

        readable_stocks = []

        for stock in raw["TOP_20"]:

            symbol = stock["symbol"]
            sector = self.get_sector(symbol)
            impact = self.event_engine.get_sector_impact(sector)

            if impact > 0:
                impact_view = f"इस सेक्टर पर युद्ध का सकारात्मक असर (+{impact}%) संभव।"
            elif impact < 0:
                impact_view = f"इस सेक्टर पर युद्ध का नकारात्मक असर ({impact}%) संभव।"
            else:
                impact_view = "इस सेक्टर पर युद्ध का सीमित या तटस्थ असर।"

            readable_stocks.append({
                "symbol": symbol,
                "sector": sector,
                "global_impact": impact_view
            })

        report["TOP_STOCK_INTELLIGENCE"] = readable_stocks

        return report


if __name__ == "__main__":
    runner = IntelligenceNarrative()
    result = runner.run()
    print(result)
