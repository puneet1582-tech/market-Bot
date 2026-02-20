# OPPORTUNITY PERSISTENCE ENGINE
# Detects stocks that repeatedly appear in top opportunities

import json

WATCHLIST_FILE = "opportunity_watchlist.json"

def detect_persistent_opportunities(min_cycles=3):
    try:
        with open(WATCHLIST_FILE, "r") as f:
            history = json.load(f)

        counter = {}

        for entry in history:
            for op in entry.get("top_opportunities", []):
                symbol = op["symbol"]
                counter[symbol] = counter.get(symbol, 0) + 1

        persistent = [
            symbol for symbol, count in counter.items()
            if count >= min_cycles
        ]

        return persistent

    except:
        return []
