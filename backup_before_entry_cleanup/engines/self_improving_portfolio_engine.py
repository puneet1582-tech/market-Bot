"""
Ultimate Brain — Self-Improving Portfolio Optimization Engine
Adjusts portfolio weights using adaptive and historical opportunity memory signals
"""

class SelfImprovingPortfolioEngine:

    def optimize(self, allocation, adaptive_stocks):
        # adaptive score lookup
        score_map = {s.get("symbol"): s.get("adaptive_score", 50) for s in adaptive_stocks}

        optimized = {}
        total_weight = 0.0

        for sym, weight in allocation.items():
            adj_factor = (score_map.get(sym, 50) / 50.0)
            new_weight = weight * adj_factor
            optimized[sym] = new_weight
            total_weight += new_weight

        # normalize weights
        if total_weight > 0:
            for sym in optimized:
                optimized[sym] = round((optimized[sym] / total_weight) * 100, 2)

        return optimized
