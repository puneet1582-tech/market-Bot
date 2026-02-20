from engines.decision_engine import DecisionEngine

class PortfolioEngine:
    def __init__(self, capital):
        self.capital = capital
        self.brain = DecisionEngine()

    def build_portfolio(self, stock_list):
        buy_stocks = []

        for symbol, sector in stock_list:
            result = self.brain.decide(symbol, sector)
            if result["final_decision"] == "BUY":
                buy_stocks.append(symbol)

        if not buy_stocks:
            return {
                "capital": self.capital,
                "message": "NO BUY SIGNALS",
                "allocation": {}
            }

        per_stock = round(self.capital / len(buy_stocks), 2)

        allocation = {}
        for stock in buy_stocks:
            allocation[stock] = per_stock

        return {
            "capital": self.capital,
            "buy_stocks": buy_stocks,
            "allocation": allocation
        }
