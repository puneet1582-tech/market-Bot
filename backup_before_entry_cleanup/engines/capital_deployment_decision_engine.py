"""
Ultimate Brain — Institutional Capital Deployment Decision Engine
Generates final execution-ready capital deployment recommendations
based on strategic allocation and risk-governed portfolio.
"""

class CapitalDeploymentDecisionEngine:

    def generate_execution_plan(self, dashboard):
        allocation = dashboard.get("risk_governed_portfolio", {}).get("protected_portfolio", {})
        strategy = dashboard.get("strategic_decision", {})
        macro_bias = strategy.get("macro_bias", "NEUTRAL")

        execution_plan = {
            "macro_bias": macro_bias,
            "deployment_actions": []
        }

        for sym, weight in allocation.items():
            action = {
                "symbol": sym,
                "target_weight": weight,
                "execution_signal": "DEPLOY" if weight > 0 else "HOLD"
            }
            execution_plan["deployment_actions"].append(action)

        return execution_plan
