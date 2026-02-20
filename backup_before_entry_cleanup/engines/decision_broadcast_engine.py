"""
Ultimate Brain — Decision Broadcast Engine
Broadcasts final institutional decisions across multiple channels.
"""

from datetime import datetime
import json
import os


LOG_FILE = "decision_broadcast_log.json"


def _write_log(data):
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(data)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f)


def broadcast_decision(decision_data, telegram_func=None):
    record = {
        "timestamp": str(datetime.utcnow()),
        "decision": decision_data
    }

    # Telegram broadcast
    if telegram_func:
        try:
            telegram_func(str(decision_data))
        except Exception:
            pass

    # Local log storage
    _write_log(record)

    return True
