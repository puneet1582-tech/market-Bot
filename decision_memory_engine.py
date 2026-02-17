# DECISION MEMORY ENGINE
# Stores opportunity decisions for historical tracking

import json
from datetime import datetime

MEMORY_FILE = "decision_memory.json"

def save_decision(report):
    try:
        entry = {
            "timestamp": str(datetime.now()),
            "report": report
        }

        try:
            with open(MEMORY_FILE, "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append(entry)

        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print("Memory save error:", e)
