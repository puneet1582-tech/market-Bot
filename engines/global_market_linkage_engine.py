"""
Ultimate Brain — Global Market Linkage Engine
Maps global index movements to domestic sector bias signals
"""

class GlobalMarketLinkageEngine:

    def compute_linkage(self, global_indices):
        """
        global_indices example:
        {"SP500": 0.6, "NASDAQ": -0.3, "DOW": 0.2}
        """
        avg_move = sum(global_indices.values()) / max(len(global_indices), 1)

        if avg_move > 0.5:
            bias = "RISK_ON"
        elif avg_move < -0.5:
            bias = "RISK_OFF"
        else:
            bias = "NEUTRAL"

        return {"avg_move": round(avg_move, 3), "bias": bias}
