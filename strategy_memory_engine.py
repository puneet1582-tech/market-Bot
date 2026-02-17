# STRATEGY MEMORY ENGINE
# Stores historical strategy decisions and regimes

import json
from datetime import datetime

STRATEGY_MEMORY_FILE = "strategy_memory.json"

def store_strategy_memory(market_mode, allocation):
    try:
        entry = {
            "timestamp": str(datetime.now()),
            "market_mode": market_mode,
            "portfolio": allocation
        }

        try:
            with open(STRATEGY_MEMORY_FILE, "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append(entry)

        with open(STRATEGY_MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print("Strategy memory error:", e)
