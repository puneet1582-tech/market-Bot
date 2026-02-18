"""
Ultimate Brain — Autonomous Continuous Intelligence Engine
Continuously records signal history and adapts intelligence over time.
"""

from datetime import datetime
import json
import os

MEMORY_FILE = "continuous_intelligence_memory.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []


def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)


def record_signal(signal_data):
    memory = load_memory()
    memory.append({
        "timestamp": str(datetime.utcnow()),
        "signal": signal_data
    })
    save_memory(memory)
    return True


def get_memory():
    return load_memory()
