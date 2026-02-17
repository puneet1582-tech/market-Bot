"""
Ultimate Brain — Autonomous Risk Governance Engine
Controls exposure dynamically under extreme volatility or risk-off regimes.
"""

class RiskGovernanceEngine:

    def apply_risk_controls(self, dashboard):
        linkage = dashboard.get("global_market_linkage", {})
        volatility = dashboard.get("global_master_signal", {}).get("liquidity_score", 50)
        portfolio = dashboard.get("multicycle_capital_allocation", {}).get("allocation", {})

        risk_state = linkage.get("bias", "NEUTRAL")

        adjusted = dict(portfolio)

        if risk_state == "RISK_OFF" or volatility < 30:
            # defensive reduction
            for k in adjusted:
                adjusted[k] = round(adjusted[k] * 0.7, 2)

        total = sum(adjusted.values())
        if total > 0:
            for k in adjusted:
                adjusted[k] = round((adjusted[k] / total) * 100, 2)

        return {
            "risk_state": risk_state,
            "protected_portfolio": adjusted
        }
