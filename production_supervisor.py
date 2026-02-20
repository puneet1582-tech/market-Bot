import os
import subprocess
import time
from datetime import datetime

ENGINES = [
    "production_autorun.py",
    "intelligence_engine.py",
    "quarterly_comparison_engine.py"
]

LOG_FILE = "logs/supervisor.log"
os.makedirs("logs", exist_ok=True)

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {msg}\n")

def run_engine(engine):
    try:
        log(f"Starting {engine}")
        subprocess.run(["python3", engine], check=True)
        log(f"Completed {engine}")
    except Exception as e:
        log(f"Error in {engine}: {e}. Restarting...")
        time.sleep(5)
        run_engine(engine)

# DISABLED ENTRY POINT
# # DISABLED ENTRY POINT
    log("Supervisor started")
    while True:
        for engine in ENGINES:
            if os.path.exists(engine):
                run_engine(engine)
            else:
                log(f"Missing engine: {engine}")
        time.sleep(3600)
