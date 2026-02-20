"""
Ultimate Brain — Capital Allocation Priority Engine
Prioritizes capital deployment across long-term, swing, trade, and defensive buckets.
"""

from datetime import datetime


DEFAULT_PRIORITY = {
    "LONG_TERM": 0.50,
    "SWING": 0.25,
    "TRADE": 0.15,
    "DEFENSIVE": 0.10
}


def allocate_capital(classified_stocks, total_capital, priority_map=None):
    if priority_map is None:
        priority_map = DEFAULT_PRIORITY

    allocation = {}
    bucket_counts = {}

    # count stocks in each bucket
    for sym, cls in classified_stocks.items():
        bucket_counts.setdefault(cls, 0)
        bucket_counts[cls] += 1

    # distribute capital
    for sym, cls in classified_stocks.items():
        bucket_capital = total_capital * priority_map.get(cls, 0)
        per_stock = bucket_capital / max(bucket_counts.get(cls, 1), 1)
        allocation[sym] = round(per_stock, 2)

    return {
        "timestamp": str(datetime.utcnow()),
        "capital_allocation": allocation
    }
