import os
import subprocess
from datetime import datetime

print("\n=== ULTIMATE BRAIN PRODUCTION RUN ===\n")

ENGINES = [
    "nse_universe_engine.py",
    "fundamentals_ingestion_engine.py",
    "core_master_runner.py"
]

for engine in ENGINES:
    if os.path.exists(engine):
        print(f"Running {engine}")
        subprocess.run(["python3", engine], check=False)
    else:
        print(f"Missing: {engine}")

# -----------------------------------------
# PHASE-E3: TOP-20 + TELEGRAM AUTO DELIVERY
# -----------------------------------------

try:
    print("\nGenerating Daily Top-20 Opportunities...")
    from engines.daily_top20_opportunity_engine import generate_top20
    result = generate_top20()
    print("Top-20 Generated:", result)

    print("\nSending Top-20 via Telegram...")
    from engines.telegram_top20_delivery_engine import send_top20
    telegram_result = send_top20()
    print("Telegram Delivery Status:", telegram_result)

except Exception as e:
    print("Top-20 / Telegram Automation Error:", e)

print("\nCompleted:", datetime.now())
