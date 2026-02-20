# PERFORMANCE TRACKER ENGINE
# Tracks historical opportunity performance

import json
from datetime import datetime

PERFORMANCE_FILE = "performance_log.json"

def log_performance(symbol, decision_mode, price):
    try:
        entry = {
            "timestamp": str(datetime.now()),
            "symbol": symbol,
            "decision_mode": decision_mode,
            "price": price
        }

        try:
            with open(PERFORMANCE_FILE, "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append(entry)

        with open(PERFORMANCE_FILE, "w") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print("Performance log error:", e)
