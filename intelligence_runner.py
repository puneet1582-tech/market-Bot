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

    def war_impact_percent(self, sector):
        return self.global_engine.get_sector_impact(sector)

    def multibagger_logic(self, sector, impact):
        if impact > 8:
            return "संरचनात्मक कम्पाउंडर संभावित"
        elif impact >= 0:
            return "उभरता हुआ मजबूत स्टॉक"
        else:
            return "लंबी अवधि के लिए उपयुक्त नहीं"

    def swing_logic(self, market_mode, impact):
        if market_mode == "TRADE" and impact >= 0:
            return "स्विंग ट्रेड के लिए उपयुक्त"
        elif market_mode == "TRADE":
            return "स्विंग में सावधानी"
        else:
            return "स्विंग के लिए उपयुक्त नहीं"

    def final_label(self, multi, swing):
        if "कम्पाउंडर" in multi:
            return "LONG TERM WEALTH CREATION"
        elif "स्विंग ट्रेड के लिए उपयुक्त" in swing:
            return "SHORT TERM OPPORTUNITY"
        else:
            return "HIGH RISK / AVOID"

    def run(self):
        raw = self.brain.execute()
        market_mode = raw["MARKET_SUMMARY"]["mode"]

        report = {}
        report["MARKET_MODE"] = market_mode
        report["GLOBAL_EVENT"] = self.global_engine.current_event

        enriched = []

        for stock in raw["TOP_20"]:

            symbol = stock["symbol"]
            sector = self.classify_sector(symbol)
            impact = self.war_impact_percent(sector)

            multi = self.multibagger_logic(sector, impact)
            swing = self.swing_logic(market_mode, impact)
            final = self.final_label(multi, swing)

            enriched.append({
                "symbol": symbol,
                "sector": sector,
                "war_impact_percent": impact,
                "multibagger_view": multi,
                "swing_view": swing,
                "final_label": final
            })

        report["TOP_STOCK_INTELLIGENCE"] = enriched

        return report


# disabled_entry_point
    runner = IntelligenceNarrative()
    result = runner.run()
    print(result)
