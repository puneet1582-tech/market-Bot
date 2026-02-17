"""
Ultimate Brain — Global Signal Fusion Engine
Combines global news impact, cross-market linkage, and liquidity
to produce a unified institutional macro signal.
"""

class GlobalSignalFusionEngine:

    def fuse(self, dashboard):
        linkage = dashboard.get("global_market_linkage", {})
        news_impact = dashboard.get("news_sector_impact", {})
        capital_flow = dashboard.get("capital_flow", {})

        bias = linkage.get("bias", "NEUTRAL")

        liquidity_score = 50
        if isinstance(capital_flow, dict):
            liquidity_score = sum(capital_flow.values()) if capital_flow else 50

        signal = {
            "macro_bias": bias,
            "liquidity_score": liquidity_score,
            "news_impact_sectors": list(news_impact.keys())[:10]
        }

        return signal
