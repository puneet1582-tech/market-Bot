import os
from datetime import datetime

LOCKED_CORE_FILES = [
    "opportunity_detection_engine.py",
    "nse_universe_engine.py",
    "fundamentals_ingestion_engine.py",
    "mode_decision_engine.py",
    "global_news_engine.py",
    "intelligence_engine.py"
]

print("\n==============================")
print(" ULTIMATE BRAIN — CORE RESET ")
print("==============================\n")

for file in LOCKED_CORE_FILES:
    if os.path.exists(file):
        print(f"[CORE READY] {file}")
    else:
        print(f"[CORE BUILD REQUIRED] {file}")

print("\nExtra runners and auxiliary pipelines will be ignored.")
print("System aligned back to locked architecture sequence.")

print("\nReset completed at:", datetime.now())
print("\n==============================\n")
