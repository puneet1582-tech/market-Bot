from engines.mode_engine_v2 import ModeEngineV2
from engines.sector_engine import SectorEngine
from engines.stock_engine import StockEngine
from engines.final_decision_engine import FinalDecisionEngine
from engines.fii_dii_engine import get_money_flow

class TradingBrainEngine:
    def __init__(self):
        self.mode_engine = ModeEngineV2()
        self.sector_engine = SectorEngine()
        self.stock_engine = StockEngine()
        self.final_engine = FinalDecisionEngine()

    def decide_trade(self):
        # 1. Market Mode
        market_mode, market_why = self.mode_engine.decide_mode()

        if market_mode == "DEFENSIVE":
            return {"decision": "NO TRADE", "why": f"Market defensive: {market_why}"}

        # 2. Sector
        ranked_sectors = self.sector_engine.rank_sectors()
        if not ranked_sectors:
            return {"decision": "NO TRADE", "why": "No strong sector"}

        top_sector, sector_score, sector_why = ranked_sectors[0]

        # 3. Stock
        stock = self.stock_engine.pick_leader(top_sector)
        if not stock:
            return {"decision": "NO TRADE", "why": "No strong stock in sector"}

        symbol = stock["symbol"]

        # 4. Fundamental confidence
        final = self.final_engine.decide(symbol)

        if final["decision"] != "BUY":
            return {
                "decision": "NO TRADE",
                "why": f"Stock not confirmed by fundamentals: {final['why']}"
            }

        # 5. Money flow (extra filter)
        money_flow = get_money_flow()

        if money_flow["mood"] == "RISK OFF":
            return {"decision": "NO TRADE", "why": "Overall money flow is risk-off"}

        return {
            "decision": "TRADE",
            "market_mode": market_mode,
            "sector": top_sector,
            "stock": symbol,
            "why": {
                "market": market_why,
                "sector": sector_why,
                "stock": stock["why"],
                "fundamental": final["why"],
                "money_flow": money_flow["reason"]
            }
        }
