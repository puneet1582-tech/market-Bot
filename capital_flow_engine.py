# CAPITAL FLOW INTELLIGENCE ENGINE
# Detects relative capital movement between sectors

import json

SECTOR_HISTORY_FILE = "sector_rotation_history.json"

def detect_capital_flow():
    try:
        with open(SECTOR_HISTORY_FILE, "r") as f:
            history = json.load(f)

        if len(history) < 2:
            return {}

        latest = history[-1]["sector_scores"]
        previous = history[-2]["sector_scores"]

        flow = {}

        for sector in latest:
            flow[sector] = latest.get(sector, 0) - previous.get(sector, 0)

        return flow

    except:
        return {}
