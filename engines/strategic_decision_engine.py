"""
Ultimate Brain — Strategic Decision Intelligence Engine
Generates long-term capital allocation strategy recommendations
based on macro bias, opportunity map, and portfolio intelligence.
"""

class StrategicDecisionEngine:

    def generate_strategy(self, dashboard):
        macro_bias = dashboard.get("global_master_signal", {}).get("macro_bias", "NEUTRAL")
        classification = dashboard.get("market_mode_classification", {})
        optimized_portfolio = dashboard.get("optimized_portfolio_allocation", {})

        strategy = {
            "macro_bias": macro_bias,
            "recommended_focus": [],
            "portfolio_guidance": optimized_portfolio
        }

        if macro_bias == "RISK_ON":
            strategy["recommended_focus"] = classification.get("INVEST", [])[:10]
        elif macro_bias == "NEUTRAL":
            strategy["recommended_focus"] = classification.get("TRADE", [])[:10]
        else:
            strategy["recommended_focus"] = classification.get("DEFENSIVE", [])[:10]

        return strategy
