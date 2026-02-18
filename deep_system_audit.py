import os
from datetime import datetime

CRITICAL_ENGINES = [
    "main.py",
    "brain_engine.py",
    "opportunity_detection_engine.py",
    "nse_universe_engine.py",
    "fundamentals_ingestion_engine.py",
    "mode_decision_engine.py",
    "global_news_engine.py",
    "intelligence_engine.py"
]

print("\n==============================")
print(" ULTIMATE BRAIN DEEP AUDIT ")
print("==============================\n")

print("FILE-BY-FILE ENGINE STATUS:\n")

for engine in CRITICAL_ENGINES:
    if os.path.exists(engine):
        with open(engine, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        print(f"[FOUND] {engine} | Lines: {len(lines)}")
    else:
        print(f"[MISSING] {engine}")

print("\nFULL PROJECT PYTHON FILE SCAN:\n")

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    line_count = len(f.readlines())
                print(f"{path} | {line_count} lines")
            except:
                pass

print("\nAudit completed at:", datetime.now())
print("\n==============================\n")
