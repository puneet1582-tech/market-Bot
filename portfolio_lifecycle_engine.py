# PORTFOLIO LIFECYCLE TRACKING ENGINE
# Stores portfolio allocations over time

import json
from datetime import datetime

PORTFOLIO_HISTORY_FILE = "portfolio_lifecycle.json"

def track_portfolio(allocation):
    try:
        entry = {
            "timestamp": str(datetime.now()),
            "portfolio": allocation
        }

        try:
            with open(PORTFOLIO_HISTORY_FILE, "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append(entry)

        with open(PORTFOLIO_HISTORY_FILE, "w") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print("Portfolio lifecycle tracking error:", e)
