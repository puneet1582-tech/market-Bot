import os
import subprocess
from datetime import datetime

ENGINES = [
    "nse_universe_engine.py",
    "fundamentals_ingestion_engine.py",
    "core_master_runner.py"
]

print("\n=== ULTIMATE BRAIN PRODUCTION RUN ===\n")

for engine in ENGINES:
    if os.path.exists(engine):
        print(f"Running {engine}")
        subprocess.run(["python3", engine], check=False)
    else:
        print(f"Missing: {engine}")

print("\nCompleted:", datetime.now())
