
import csv
import os
import requests
import yfinance as yf
from datetime import datetime

# ==========================================================
# DATA SOURCES
# ==========================================================

class DataSources:

    def get_price_yahoo(self, symbol):
        try:
            ticker = yf.Ticker(symbol + ".NS")
            hist = ticker.history(period="1y")
            if len(hist) > 0:
                return hist["Close"].iloc[-1]
        except:
            pass
        return None


# ==========================================================
# NSE SECTOR AUTHORITY
# ==========================================================

class SectorAuthority:

    def __init__(self):
        self.mapping = {}
        self.load()

    def load(self):

        try:
            with open("data/sector_index_base.csv") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    self.mapping[r["symbol"].upper()] = r["sector"].upper()
        except:
            pass

        try:
            with open("data/sector_master.csv") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    if r["symbol"].upper() not in self.mapping:
                        self.mapping[r["symbol"].upper()] = r["sector"].upper()
        except:
            pass

    def get(self, symbol):
        return self.mapping.get(symbol, "SMALL_CAP")


# ==========================================================
# GLOBAL EVENT ENGINE
# ==========================================================

class GlobalEventEngine:

    def __init__(self):
        self.event = "WAR"

        self.map = {
            "WAR": {
                "DEFENSE": 15,
                "ENERGY": 12,
                "METALS": 8,
                "IT": -5,
                "BANK": -3,
                "REALTY": -7,
                "AUTO": -6,
                "SMALL_CAP": -4
            }
        }

    def impact(self, sector):
        return self.map.get(self.event, {}).get(sector, -4)


# ==========================================================
# FUNDAMENTAL ENGINE
# ==========================================================

class FundamentalEngine:

    def business_strength(self, score):

        if score >= 1.0:
            return "STRONG"

        if score >= 0.7:
            return "MODERATE"

        return "WEAK"


# ==========================================================
# MASTER INTELLIGENCE SYSTEM
# ==========================================================

class UltimateIntelligence:

    def __init__(self):

        from core.master_brain import MasterBrain

        self.brain = MasterBrain()
        self.sector = SectorAuthority()
        self.global_engine = GlobalEventEngine()
        self.fundamental = FundamentalEngine()
        self.data = DataSources()

    def final_decision(self, strength, impact, mode):

        if strength == "STRONG" and impact >= 0 and mode == "INVEST":
            return "LONG TERM INVEST"

        if strength in ["STRONG","MODERATE"] and mode == "TRADE":
            return "SWING TRADE"

        if impact <= -6:
            return "GLOBAL RISK AVOID"

        return "HIGH RISK"

    def run(self):

        raw = self.brain.execute()

        mode = raw["MARKET_SUMMARY"]["mode"]

        result = {
            "generated_at": datetime.utcnow().isoformat(),
            "market_mode": mode,
            "global_event": self.global_engine.event,
            "stocks": []
        }

        for s in raw["TOP_20"]:

            symbol = s["symbol"]
            score = s["score"]

            sector = self.sector.get(symbol)
            impact = self.global_engine.impact(sector)
            strength = self.fundamental.business_strength(score)

            decision = self.final_decision(strength,impact,mode)

            price = self.data.get_price_yahoo(symbol)

            result["stocks"].append({

                "symbol":symbol,
                "sector":sector,
                "price":price,
                "strength":strength,
                "war_impact":impact,
                "decision":decision
            })

        return result


# ==========================================================
# EXECUTE
# ==========================================================

# disabled_entry_point

    system = UltimateIntelligence()

    output = system.run()

    print(output)



if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
