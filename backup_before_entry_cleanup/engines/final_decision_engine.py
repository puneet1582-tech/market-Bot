import pandas as pd

FUND_PATH = "data/quarterly_fundamentals_clean.csv"
STOCKS_PATH = "data/stocks.csv"
NEWS_PATH = "data/news.csv"

class ConfidenceEngine:
    def __init__(self):
        self.fund = pd.read_csv(FUND_PATH)
        self.news = pd.read_csv(NEWS_PATH)

    def calculate(self, symbol):
        score = 0
        reasons = []

        df = self.fund[self.fund["symbol"] == symbol]

        if len(df) >= 6:
            score += 30
            reasons.append("Sufficient quarterly data available")
        else:
            reasons.append("Not enough quarterly data")

        if "profit" in df.columns and df["profit"].dropna().mean() > 0:
            score += 30
            reasons.append("Average profit positive")
        else:
            reasons.append("Profit weak or missing")

        if "sales" in df.columns and df["sales"].dropna().pct_change().mean() > 0:
            score += 20
            reasons.append("Sales trend positive")
        else:
            reasons.append("Sales trend not strong")

        pos_news = self.news[self.news["impact"] == "POSITIVE"]
        neg_news = self.news[self.news["impact"] == "NEGATIVE"]

        if len(pos_news) > len(neg_news):
            score += 20
            reasons.append("News sentiment positive")
        else:
            reasons.append("News sentiment mixed/negative")

        return {
            "confidence_percent": min(score, 100),
            "reasons": reasons
        }

class FinalDecisionEngine:
    def __init__(self):
        self.fund = pd.read_csv(FUND_PATH)
        self.stocks = pd.read_csv(STOCKS_PATH)
        self.conf = ConfidenceEngine()

    def decide(self, symbol):
        reasons = []

        stock_row = self.stocks[self.stocks["symbol"] == symbol]
        if stock_row.empty:
            return {"symbol": symbol, "decision": "NO DATA", "confidence": 0, "why": ["Stock not found"]}

        sector = stock_row.iloc[0]["sector"]

        df = self.fund[self.fund["symbol"] == symbol]

        if len(df) < 4:
            return {"symbol": symbol, "sector": sector, "decision": "NO DECISION", "confidence": 0,
                    "why": ["Not enough quarterly data"]}

        sales_trend = df["sales"].pct_change().mean()
        profit_trend = df["profit"].pct_change().mean()

        if sales_trend > 0:
            reasons.append("Sales trend rising")
        else:
            reasons.append("Sales trend weak")

        if profit_trend > 0:
            reasons.append("Profit trend rising")
        else:
            reasons.append("Profit trend weak")

        conf_data = self.conf.calculate(symbol)
        confidence = conf_data["confidence_percent"]
        reasons += conf_data["reasons"]

        if sales_trend > 0 and profit_trend > 0 and confidence >= 60:
            decision = "BUY"
        elif profit_trend < 0 and confidence < 40:
            decision = "SELL"
        else:
            decision = "AVOID"

        return {
            "symbol": symbol,
            "sector": sector,
            "decision": decision,
            "confidence": confidence,
            "why": reasons
        }

# DISABLED ENTRY POINT
# if __name__ == "__main__":
    fe = FinalDecisionEngine()
    print(fe.decide("RELIANCE"))
