"""
Ultimate Brain — Governance & Explainability Engine
Stores explanation trails for every generated investment decision.
"""

from datetime import datetime


def build_explanation(symbol, market_mode, classification, action):
    return {
        "symbol": symbol,
        "timestamp": str(datetime.utcnow()),
        "market_mode": market_mode,
        "classification": classification,
        "decision_action": action,
        "explanation": f"Decision derived from market mode {market_mode}, "
                       f"classification {classification}, resulting action {action}"
    }


def generate_explainability_report(decisions):
    report = []
    for d in decisions:
        report.append(
            build_explanation(
                d.get("symbol"),
                d.get("market_mode", "UNKNOWN"),
                d.get("classification", "UNKNOWN"),
                d.get("action", "HOLD")
            )
        )
    return report
