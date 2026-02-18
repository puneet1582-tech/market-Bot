"""
Ultimate Brain — Institutional Portfolio Optimization Engine
Improves next-cycle portfolio allocation using attribution intelligence.
"""

from datetime import datetime


def optimize_allocation(current_allocation, attribution_data):
    """
    current_allocation:
        dict {symbol: allocation_pct}

    attribution_data:
        dict containing 'stock_selection' and 'allocation_effect'
    """

    try:
        optimized = {}

        stock_effect = attribution_data.get("stock_selection", 0)
        alloc_effect = attribution_data.get("allocation_effect", 0)

        for sym, alloc in current_allocation.items():
            adjustment = 1.0

            if stock_effect > 0:
                adjustment += 0.05
            if alloc_effect < 0:
                adjustment -= 0.03

            optimized[sym] = round(alloc * adjustment, 4)

        return {
            "timestamp": str(datetime.utcnow()),
            "optimized_allocation": optimized
        }

    except Exception:
        return {
            "timestamp": str(datetime.utcnow()),
            "optimized_allocation": current_allocation
        }
