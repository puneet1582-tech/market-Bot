import csv
from datetime import datetime
from core.master_brain import MasterBrain

# ==========================================================
# GLOBAL EVENT MODEL (REALISTIC & STABLE)
# ==========================================================

class GlobalEventEngine:

    def __init__(self):
        self.current_event = "WAR"

        self.impact = {
            "WAR": {
                "DEFENSE": 15,
                "ENERGY": 12,
                "OIL": 12,
                "METALS": 8,
                "IT": -5,
                "BANK": -3,
                "BANKING": -3,
                "AUTO": -6,
                "REALTY": -7,
                "SMALL_CAP": -4
            }
        }

    def get_impact(self, sector):
        return self.impact.get(self.current_event, {}).get(sector.upper(), -4)


# ==========================================================
# INSTITUTIONAL INTELLIGENCE ENGINE
# ==========================================================

class InstitutionalIntelligence:

    def __init__(self):
        self.brain = MasterBrain()
        self.global_engine = GlobalEventEngine()
        self.sector_map = self.load_sector_data()

    # ------------------------------------------------------
    # LOAD REAL NSE SECTOR AUTHORITY
    # ------------------------------------------------------

    def load_sector_data(self):
        mapping = {}

        # Primary: NSE Index Base
        try:
            with open("data/sector_index_base.csv", newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    symbol = row["symbol"].strip().upper()
                    sector = row["sector"].strip().upper()
                    if sector and sector != "UNKNOWN":
                        mapping[symbol] = sector
        except:
            pass

        # Secondary: sector_master
        try:
            with open("data/sector_master.csv", newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    symbol = row["symbol"].strip().upper()
                    sector = row["sector"].strip().upper()
                    if symbol not in mapping and sector != "UNKNOWN":
                        mapping[symbol] = sector
        except:
            pass

        return mapping

    # ------------------------------------------------------
    # BUSINESS STRENGTH (STABLE RULE BASED)
    # ------------------------------------------------------

    def classify_strength(self, score):
        if score >= 1.0:
            return "STRONG"
        elif score >= 0.7:
            return "MODERATE"
        else:
            return "WEAK"

    # ------------------------------------------------------
    # FINAL DECISION LOGIC (NO RANDOM CHANGE)
    # ------------------------------------------------------

    def final_decision(self, strength, war_impact, market_mode):

        if strength == "STRONG" and war_impact >= 0 and market_mode == "INVEST":
            return "LONG TERM INVEST"

        if strength in ["STRONG", "MODERATE"] and market_mode == "TRADE":
            return "SWING / SHORT TERM"

        if war_impact <= -6:
            return "AVOID (GLOBAL RISK HIGH)"

        return "HIGH RISK / MONITOR"

    # ------------------------------------------------------
    # RUN FULL SYSTEM
    # ------------------------------------------------------

    def run(self):

        raw = self.brain.execute()

        market_mode = raw["MARKET_SUMMARY"]["mode"]
        top_stocks = raw["TOP_20"]

        result = {
            "generated_at": datetime.utcnow().isoformat(),
            "market_mode": market_mode,
            "global_event": self.global_engine.current_event,
            "stocks": []
        }

        for stock in top_stocks:

            symbol = stock["symbol"]
            score = stock["score"]

            sector = self.sector_map.get(symbol, "SMALL_CAP")
            war_impact = self.global_engine.get_impact(sector)
            strength = self.classify_strength(score)
            decision = self.final_decision(strength, war_impact, market_mode)

            result["stocks"].append({
                "symbol": symbol,
                "sector": sector,
                "business_strength": strength,
                "war_impact_percent": war_impact,
                "final_decision": decision
            })

        return result


# ==========================================================
# EXECUTE
# ==========================================================

# disabled_entry_point
    system = InstitutionalIntelligence()
    output = system.run()
    print(output)



if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
