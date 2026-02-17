"""
Ultimate Brain — Long-Term Opportunity Memory Engine
Stores multi-cycle opportunity signals for long-term compounding intelligence
"""

import json
import os
from datetime import datetime

MEMORY_FILE = "data/opportunity_memory.json"


class OpportunityMemoryEngine:

    def __init__(self):
        if not os.path.exists("data"):
            os.makedirs("data")

        if not os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "w") as f:
                json.dump({}, f)

    def update_memory(self, stocks):
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)

        for s in stocks:
            symbol = s.get("symbol")
            if not symbol:
                continue

            entry = {
                "timestamp": str(datetime.utcnow()),
                "probability": s.get("probability_score", 0),
                "adaptive_score": s.get("adaptive_score", 0)
            }

            memory.setdefault(symbol, []).append(entry)

        with open(MEMORY_FILE, "w") as f:
            json.dump(memory, f, indent=2)

        return memory
