"""
ULTIMATE BRAIN
COMBINED FUNDAMENTAL + PRICE INTELLIGENCE ENGINE
Final Label: LONG_TERM / SWING / INTRADAY / AVOID
"""

from core.price_structure_engine import PriceStructureEngine
from core.mode_engine import ModeEngine


class IntelligenceEngine:

    def __init__(self):
        self.structure_engine = PriceStructureEngine()
        self.mode_engine = ModeEngine()

    def classify(self, metrics, mode):

        trend = metrics["trend"]
        cagr = metrics["cagr"]
        drawdown = metrics["max_drawdown"]

        # LONG TERM
        if mode == "INVEST" and trend == "STRONG_UPTREND" and cagr and cagr > 0.18:
            return "LONG_TERM"

        # SWING
        if mode in ["INVEST", "TRADE"] and trend in ["STRONG_UPTREND", "WEAK_UPTREND"]:
            return "SWING"

        # INTRADAY
        if mode == "TRADE" and drawdown > -0.2:
            return "INTRADAY"

        return "AVOID"

    def run(self):

        structure_output = self.structure_engine.run()
        mode_output = self.mode_engine.run()

        final_output = {}

        for symbol, metrics in structure_output.items():

            mode = mode_output.get(symbol)

            if not mode:
                continue

            final_label = self.classify(metrics, mode)

            final_output[symbol] = {
                "mode": mode,
                "trend": metrics["trend"],
                "cagr": metrics["cagr"],
                "drawdown": metrics["max_drawdown"],
                "final_label": final_label
            }

        return final_output


if __name__ == "__main__":
    engine = IntelligenceEngine()
    result = engine.run()
    print("Combined Intelligence Engine Completed")
    print(list(result.items())[:10])
