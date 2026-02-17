"""
Ultimate Brain — Global → Sector → Stock Opportunity Map Engine
Builds a hierarchical opportunity map from global macro signals
to sectors and finally to individual stocks.
"""

class GlobalSectorStockMapEngine:

    def build_map(self, dashboard):
        global_signal = dashboard.get("global_master_signal", {})
        sector_scores = dashboard.get("sector_scores", {})
        stocks = dashboard.get("probability_enriched_stocks", [])

        opportunity_map = {
            "macro_bias": global_signal.get("macro_bias", "NEUTRAL"),
            "sector_opportunities": {},
            "stock_opportunities": {}
        }

        # Sector opportunity ranking
        for sector, score in sector_scores.items():
            if score >= 70:
                opportunity_map["sector_opportunities"][sector] = "HIGH"
            elif score >= 50:
                opportunity_map["sector_opportunities"][sector] = "MEDIUM"
            else:
                opportunity_map["sector_opportunities"][sector] = "LOW"

        # Stock opportunity ranking
        for s in stocks:
            sym = s.get("symbol")
            prob = s.get("probability_score", 50)

            if prob >= 70:
                level = "HIGH"
            elif prob >= 50:
                level = "MEDIUM"
            else:
                level = "LOW"

            opportunity_map["stock_opportunities"][sym] = level

        return opportunity_map
