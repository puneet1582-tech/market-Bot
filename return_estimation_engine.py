# RETURN ESTIMATION ENGINE
# Estimates basic return movement from logged performance entries

import json

PERFORMANCE_FILE = "performance_log.json"

def estimate_returns():
    try:
        with open(PERFORMANCE_FILE, "r") as f:
            data = json.load(f)

        if not data:
            return {"estimated_return_score": 0}

        # Simple proxy scoring (placeholder until live historical comparison layer added)
        score = 0
        for entry in data[-50:]:
            if entry["decision_mode"] == "INVEST":
                score += 2
            elif entry["decision_mode"] == "TRADE":
                score += 1

        return {"estimated_return_score": score}

    except:
        return {"estimated_return_score": 0}
