import subprocess
from datetime import datetime

PIPELINE = [
    "unified_intelligence_pipeline.py",
    "intelligence_engine.py"
]

print("\n=== DAILY AUTOPLAY RUN ===\n")

for script in PIPELINE:
    try:
        subprocess.run(["python3", script], check=False)
    except Exception as e:
        print(f"Error running {script}: {e}")

print("\nCompleted:", datetime.now())
