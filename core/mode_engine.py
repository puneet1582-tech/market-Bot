"""
ULTIMATE BRAIN
MODE CLASSIFICATION ENGINE
INVEST / TRADE / DEFENSIVE
"""

from core.price_structure_engine import PriceStructureEngine


class ModeEngine:

    def __init__(self):
        self.structure_engine = PriceStructureEngine()

    def classify(self, metrics):

        trend = metrics["trend"]
        cagr = metrics["cagr"]
        drawdown = metrics["max_drawdown"]

        if trend == "STRONG_UPTREND" and cagr and cagr > 0.15 and drawdown > -0.4:
            return "INVEST"

        if trend in ["STRONG_UPTREND", "WEAK_UPTREND"] and cagr and cagr > 0:
            return "TRADE"

        if trend == "DOWNTREND" or drawdown <= -0.5:
            return "DEFENSIVE"

        return "DEFENSIVE"

    def run(self):

        structure_output = self.structure_engine.run()

        mode_results = {}

        for symbol, metrics in structure_output.items():
            mode_results[symbol] = self.classify(metrics)

        return mode_results


if __name__ == "__main__":
    engine = ModeEngine()
    output = engine.run()
    print("Mode Engine Completed")
    print(list(output.items())[:10])
