from engines.fundamental_engine import FundamentalEngine
from engines.promoter_engine import PromoterEngine
from engines.technical_engine import TechnicalEngine
from engines.price_engine import PriceEngine
from engines.news_engine import NewsEngine

class DecisionEngine:
    def __init__(self):
        self.fundamental = FundamentalEngine()
        self.smartmoney = PromoterEngine()
        self.technical = TechnicalEngine()
        self.price = PriceEngine()
        self.news = NewsEngine()

    def decide(self, symbol, sector):
        fund = self.fundamental.analyze(symbol)
        money = self.smartmoney.analyze(sector)
        tech = self.technical.analyze(symbol)
        price = self.price.analyze(symbol)
        news = self.news.analyze(sector)

        # Data trust rule
        if "decision" in fund:
            return {
                "symbol": symbol,
                "final_decision": "NO DECISION",
                "reason": fund["reason"]
            }

        sales = fund["sales_trend"]
        profit = fund["profit_trend"]
        fii = money.get("fii", "UNKNOWN")
        trend = tech.get("trend", "UNKNOWN")
        ath_drop = price.get("ath_drop_percent", 0)
        news_impact = news.get("news_impact", "NEUTRAL")

        reasons = []

        # Reason building
        if sales == "UP":
            reasons.append("Sales rising")
        if profit == "UP":
            reasons.append("Profit rising")
        if fii == "BUYING":
            reasons.append("FII buying")
        if fii == "SELLING":
            reasons.append("FII selling")
        if trend == "UP":
            reasons.append("Price trend up")
        if trend == "DOWN":
            reasons.append("Price trend down")
        if ath_drop > 30:
            reasons.append(f"Stock {ath_drop}% below ATH")
        if news_impact == "POSITIVE":
            reasons.append("Positive sector news")
        if news_impact == "NEGATIVE":
            reasons.append("Negative sector news")

        # FINAL LOGIC
        if sales == "UP" and profit == "UP" and fii == "BUYING" and trend == "UP" and news_impact != "NEGATIVE":
            decision = "BUY"
        elif sales == "UP" and profit == "UP" and (fii == "SELLING" or trend == "DOWN"):
            decision = "WARNING"
        else:
            decision = "AVOID"

        return {
            "symbol": symbol,
            "sector": sector,
            "fundamental": fund,
            "smart_money": money,
            "technical": tech,
            "price": price,
            "news": news,
            "final_decision": decision,
            "why": reasons
        }
