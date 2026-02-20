"""
Ultimate Brain — Adaptive Learning Intelligence Engine
Learns from historical performance and adjusts conviction weight
"""

class AdaptiveLearningEngine:

    def adjust_scores(self, stocks, performance_log):
        adjusted = []

        for s in stocks:
            symbol = s.get("symbol")
            past_perf = performance_log.get(symbol, 0)

            adj_factor = 1 + (past_perf * 0.05)
            s["adaptive_score"] = round(s.get("probability_score", 50) * adj_factor, 2)

            adjusted.append(s)

        return adjusted
