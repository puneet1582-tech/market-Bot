"""
Ultimate Brain — Crisis Capital Shield Engine
Detects extreme market stress and moves portfolio into capital protection mode.
"""

class CrisisCapitalShieldEngine:

    def detect_crisis(self, dashboard):
        linkage = dashboard.get("global_market_linkage", {})
        macro_signal = dashboard.get("global_master_signal", {})
        volatility_proxy = macro_signal.get("liquidity_score", 50)

        risk_bias = linkage.get("bias", "NEUTRAL")

        crisis = False
        if risk_bias == "RISK_OFF" and volatility_proxy < 25:
            crisis = True

        return crisis

    def apply_shield(self, dashboard):
        crisis = self.detect_crisis(dashboard)
        portfolio = dashboard.get("risk_governed_portfolio", {}).get("protected_portfolio", {})

        if not crisis:
            return {
                "crisis_mode": False,
                "shielded_portfolio": portfolio
            }

        # emergency reduction (move majority to cash-equivalent)
        shielded = {}
        for sym, w in portfolio.items():
            shielded[sym] = round(w * 0.4, 2)

        total = sum(shielded.values())
        if total > 0:
            for sym in shielded:
                shielded[sym] = round((shielded[sym] / total) * 100, 2)

        return {
            "crisis_mode": True,
            "shielded_portfolio": shielded
        }
