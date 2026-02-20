# SECTOR ROTATION ENGINE
# Tracks sector strength changes over time

import json
from datetime import datetime

SECTOR_HISTORY_FILE = "sector_rotation_history.json"

def update_sector_rotation(sector_scores):
    try:
        entry = {
            "timestamp": str(datetime.now()),
            "sector_scores": sector_scores
        }

        try:
            with open(SECTOR_HISTORY_FILE, "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append(entry)

        with open(SECTOR_HISTORY_FILE, "w") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print("Sector rotation update error:", e)
