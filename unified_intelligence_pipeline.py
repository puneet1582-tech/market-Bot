import os
import subprocess
from datetime import datetime

PIPELINE_ENGINES = [
    "nse_universe_engine.py",
    "fundamentals_ingestion_engine.py",
    "core_master_runner.py"
]

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, "pipeline.log")

def log(msg):
    with open(log_file, "a") as f:
        f.write(f"{datetime.now()} - {msg}\n")

print("\n=== UNIFIED INTELLIGENCE PIPELINE START ===\n")
log("Pipeline execution started")

for engine in PIPELINE_ENGINES:
    if os.path.exists(engine):
        print(f"Running {engine}")
        log(f"Running {engine}")
        subprocess.run(["python3", engine], check=False)
    else:
        print(f"Missing engine: {engine}")
        log(f"Missing engine: {engine}")

print("\nPipeline completed:", datetime.now())
log("Pipeline execution completed")
