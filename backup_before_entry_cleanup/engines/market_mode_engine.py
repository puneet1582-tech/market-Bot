import statistics


class MarketModeEngine:
    """
    Multi-Factor Market Mode Intelligence Engine
    Determines INVEST / TRADE / DEFENSIVE mode
    using liquidity, volatility, sentiment, and trend structure
    """

    def __init__(self):
        pass

    # -------------------------
    # FACTOR SCORING FUNCTIONS
    # -------------------------

    def liquidity_score(self, fii_flow, dii_flow):
        total = fii_flow + dii_flow
        if total > 0:
            return 80
        elif total == 0:
            return 50
        else:
            return 30

    def volatility_score(self, volatility_index):
        if volatility_index < 15:
            return 80
        elif volatility_index < 25:
            return 60
        else:
            return 30

    def sentiment_score(self, sentiment):
        # sentiment expected 0-100
        return sentiment

    def trend_score(self, index_returns):
        if len(index_returns) < 3:
            return 50
        avg_return = statistics.mean(index_returns[-3:])
        if avg_return > 0:
            return 75
        else:
            return 35

    # -------------------------
    # MODE DETECTION
    # -------------------------

    def detect_mode(self, market_data):
        """
        market_data example:
        {
            "fii_flow": 1200,
            "dii_flow": 500,
            "volatility_index": 14,
            "sentiment": 65,
            "index_returns": [0.5, 0.3, -0.1]
        }
        """

        liquidity = self.liquidity_score(
            market_data.get("fii_flow", 0),
            market_data.get("dii_flow", 0)
        )

        volatility = self.volatility_score(
            market_data.get("volatility_index", 20)
        )

        sentiment = self.sentiment_score(
            market_data.get("sentiment", 50)
        )

        trend = self.trend_score(
            market_data.get("index_returns", [])
        )

        final_score = (liquidity + volatility + sentiment + trend) / 4

        if final_score >= 70:
            mode = "INVEST"
        elif final_score >= 50:
            mode = "TRADE"
        else:
            mode = "DEFENSIVE"

        return {
            "mode": mode,
            "score": round(final_score, 2),
            "liquidity_score": liquidity,
            "volatility_score": volatility,
            "sentiment_score": sentiment,
            "trend_score": trend
        }
