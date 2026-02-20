"""
ULTIMATE BRAIN
TOP OPPORTUNITY SELECTOR ENGINE
INVEST Mode Ranking + Risk Filter
"""

from core.mode_engine import ModeEngine
from core.price_structure_engine import PriceStructureEngine


class OpportunityEngine:

    def __init__(self):
        self.mode_engine = ModeEngine()
        self.structure_engine = PriceStructureEngine()

    def run(self):

        mode_output = self.mode_engine.run()
        structure_output = self.structure_engine.run()

        invest_candidates = []

        for symbol, mode in mode_output.items():

            if mode != "INVEST":
                continue

            metrics = structure_output.get(symbol)

            if not metrics:
                continue

            cagr = metrics.get("cagr")
            drawdown = metrics.get("max_drawdown")

            if cagr is None:
                continue

            # Risk filter
            if drawdown <= -0.5:
                continue

            invest_candidates.append({
                "symbol": symbol,
                "cagr": cagr,
                "drawdown": drawdown
            })

        # Rank by CAGR descending
        ranked = sorted(
            invest_candidates,
            key=lambda x: x["cagr"],
            reverse=True
        )

        top_20 = ranked[:20]

        return {
            "total_invest_candidates": len(invest_candidates),
            "top_20": top_20
        }


if __name__ == "__main__":
    engine = OpportunityEngine()
    result = engine.run()
    print("Top Opportunity Engine Completed")
    print(result)
