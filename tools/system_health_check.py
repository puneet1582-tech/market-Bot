import os
import time
from datetime import datetime

FILES = [
    "run.py",
    "core/master_intelligence_controller.py",
    "engines/news_engine/global_news_collector.py",
    "engines/alert_engine/telegram_alert.py"
]

def check_files():
    missing = []
    for f in FILES:
        if not os.path.exists(f):
            missing.append(f)
    return missing

def main():
    print("ULTIMATE BRAIN HEALTH CHECK")
    print("Time:", datetime.utcnow())

    missing = check_files()

    if missing:
        print("Missing files:")
        for m in missing:
            print("-", m)
    else:
        print("All core files present")

if __name__ == "__main__":
    main()
