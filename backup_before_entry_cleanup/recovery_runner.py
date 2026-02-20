import subprocess
from datetime import datetime

PIPELINE = [
    "production_autorun.py",
    "intelligence_engine.py",
    "quarterly_comparison_engine.py"
]

print("\n=== FAILURE RECOVERY RUN ===\n")

for p in PIPELINE:
    try:
        subprocess.run(["python3", p], check=False)
    except Exception as e:
        print("Error:", e)

print("\nRecovery completed:", datetime.now())
