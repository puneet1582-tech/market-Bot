import pandas as pd

STOCKS_PATH = "data/stocks.csv"
TECH_PATH = "data/technical.csv"
FUND_PATH = "data/fundamentals.csv"

class StockEngine:
    def __init__(self):
        self.stocks = pd.read_csv(STOCKS_PATH)
        self.tech = pd.read_csv(TECH_PATH)
        self.fund = pd.read_csv(FUND_PATH)

    def pick_leader(self, sector):
        # filter stocks by sector
        sector_stocks = self.stocks[self.stocks["sector"] == sector]

        results = []

        for _, row in sector_stocks.iterrows():
            symbol = row["symbol"]

            tech_row = self.tech[self.tech["stock"] == symbol]
            fund_row = self.fund[self.fund["symbol"] == symbol]

            if tech_row.empty or fund_row.empty:
                continue

            tech_row = tech_row.iloc[0]
            fund_row = fund_row.iloc[0]

            score = 0
            reasons = []

            # Technical logic
            if tech_row["trend"] == "UP":
                score += 2
                reasons.append("Trend UP")
            elif tech_row["trend"] == "SIDEWAYS":
                score += 1
                reasons.append("Trend SIDEWAYS")
            else:
                score -= 2
                reasons.append("Trend DOWN")

            rsi = float(tech_row["rsi"])
            if rsi > 60:
                score += 1
                reasons.append("RSI strong")
            elif rsi < 40:
                score -= 1
                reasons.append("RSI weak")

            # Fundamental logic
            debt = fund_row["debt_trend"]
            if debt in ["reducing", "zero", "stable"]:
                score += 1
                reasons.append("Debt healthy")
            else:
                score -= 1
                reasons.append("Debt increasing")

            growth = float(fund_row["revenue_growth"])
            if growth > 10:
                score += 1
                reasons.append("Good revenue growth")

            pledge = float(fund_row["pledge"])
            if pledge > 10:
                score -= 1
                reasons.append("High pledge")

            results.append({
                "symbol": symbol,
                "score": score,
                "why": "; ".join(reasons)
            })

        if not results:
            return None

        results = sorted(results, key=lambda x: x["score"], reverse=True)
        return results[0]
