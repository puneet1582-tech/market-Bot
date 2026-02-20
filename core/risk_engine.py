"""
ULTIMATE BRAIN
RISK & CAPITAL MANAGEMENT ENGINE
System Risk State + Capital Allocation
"""

from core.master_brain_engine import MasterBrainEngine


class RiskEngine:

    def __init__(self):
        self.master_engine = MasterBrainEngine()

    def calculate_system_risk(self, report):

        stock_decisions = report["stock_decisions"]
        sector_summary = report["sector_summary"]

        total = len(stock_decisions)

        invest_count = sum(
            1 for s in stock_decisions.values()
            if s["mode"] == "INVEST"
        )

        defensive_count = sum(
            1 for s in stock_decisions.values()
            if s["mode"] == "DEFENSIVE"
        )

        avg_drawdown = sum(
            s["drawdown"] for s in stock_decisions.values()
        ) / total if total > 0 else 0

        strong_sectors = sum(
            1 for s in sector_summary.values()
            if s["classification"] == "STRONG_SECTOR"
        )

        # Risk State Logic
        if invest_count / total > 0.5 and avg_drawdown > -0.35 and strong_sectors > 2:
            state = "AGGRESSIVE"
            allocation = {
                "equity": 80,
                "cash": 20
            }

        elif defensive_count / total > 0.4 or avg_drawdown <= -0.5:
            state = "DEFENSIVE"
            allocation = {
                "equity": 40,
                "cash": 60
            }

        else:
            state = "NORMAL"
            allocation = {
                "equity": 60,
                "cash": 40
            }

        return {
            "system_state": state,
            "avg_drawdown": round(avg_drawdown, 4),
            "strong_sectors": strong_sectors,
            "capital_allocation": allocation
        }

    def run(self):

        master_report = self.master_engine.run()

        risk_output = self.calculate_system_risk(master_report)

        final_output = {
            "risk_summary": risk_output,
            "top_opportunities": master_report["top_opportunities"],
            "sector_summary": master_report["sector_summary"]
        }

        return final_output


if __name__ == "__main__":
    engine = RiskEngine()
    result = engine.run()
    print("RISK ENGINE COMPLETED")
    print(result)
