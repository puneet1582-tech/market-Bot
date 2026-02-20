from engines.decision_engine import DecisionEngine
from engines.narrative_engine import NarrativeEngine
from engines.mode_engine import ModeEngine

class FinalReportEngine:
    def __init__(self):
        self.decision = DecisionEngine()
        self.narrative = NarrativeEngine()
        self.mode = ModeEngine()

    def generate_report(self, symbol, sector):
        decision_result = self.decision.decide(symbol, sector)
        narrative_result = self.narrative.generate_report()
        current_mode = self.mode.decide_mode()

        report = {}

        report["TITLE"] = "TOMORROW MARKET OUTLOOK (MASTER REPORT)"
        report["MODE"] = current_mode
        report["FINAL_DECISION"] = decision_result["final_decision"]

        report["LIKELY_GAINERS"] = narrative_result["likely_gainers"]
        report["LIKELY_LOSERS"] = narrative_result["likely_losers"]

        report["WHY_DECISION"] = decision_result.get("why", decision_result.get("reasons", "No reason"))

        report["EVIDENCE_INTERNET"] = narrative_result["evidence"]

        report["SUMMARY"] = (
            "Decision is based on fundamentals, smart money, technicals, price action, "
            "global news, and internet narrative cross-verification."
        )

        report["SUGGESTION"] = {
            "BUY_OR_ACCUMULATE": narrative_result["suggestion"]["BUY_OR_ACCUMULATE"],
            "SELL_OR_AVOID": narrative_result["suggestion"]["SELL_OR_AVOID"],
            "RISK_NOTE": "If global risk rises, defensive sectors may outperform."
        }

        return report
