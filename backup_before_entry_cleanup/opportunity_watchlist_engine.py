# OPPORTUNITY WATCHLIST ENGINE
# Stores top opportunities for historical tracking

import json
from datetime import datetime

WATCHLIST_FILE = "opportunity_watchlist.json"

def update_watchlist(top_opportunities):
    try:
        entry = {
            "timestamp": str(datetime.now()),
            "top_opportunities": top_opportunities
        }

        try:
            with open(WATCHLIST_FILE, "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append(entry)

        with open(WATCHLIST_FILE, "w") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print("Watchlist update error:", e)
