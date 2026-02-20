"""
Ultimate Brain — Multi-Cycle Capital Allocation Optimization Engine
Optimizes long-term capital allocation using opportunity memory
and strategic decision signals.
"""

class MultiCycleCapitalAllocationEngine:

    def optimize(self, dashboard):
        memory = dashboard.get("opportunity_memory", {})
        strategy = dashboard.get("strategic_decision", {})
        base_portfolio = dashboard.get("optimized_portfolio_allocation", {})

        optimized = dict(base_portfolio)

        # simple reinforcement based on frequency in opportunity memory
        freq = {}
        for sym, records in memory.items():
            freq[sym] = len(records)

        if freq:
            max_freq = max(freq.values())
            for sym, count in freq.items():
                if sym in optimized:
                    optimized[sym] = optimized[sym] * (1 + (count / max_freq) * 0.10)

        # normalize to 100%
        total = sum(optimized.values())
        if total > 0:
            for sym in optimized:
                optimized[sym] = round((optimized[sym] / total) * 100, 2)

        return {
            "macro_bias": strategy.get("macro_bias", "NEUTRAL"),
            "allocation": optimized
        }
