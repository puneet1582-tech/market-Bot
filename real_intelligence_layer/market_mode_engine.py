class MarketModeEngine:

    def determine_mode(self, liquidity, volatility):
        if liquidity == "High" and volatility == "Low":
            return "INVEST"
        elif volatility == "High":
            return "TRADE"
        else:
            return "DEFENSIVE"
