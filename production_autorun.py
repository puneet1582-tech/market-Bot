import subprocess
from datetime import datetime

print("\n=== ULTIMATE BRAIN PRODUCTION RUN ===\n")

print("Running Phase-11 Master Central Controller...")
subprocess.run(["python3", "phase11_master_controller_activation.py"], check=False)

print("\nTriggering Telegram Top-20 Delivery...")

try:
    from engines.telegram_top20_delivery_engine import send_top20
    result = send_top20()
    print("Telegram Delivery Status:", result)
except Exception as e:
    print("Telegram Automation Error:", e)

print("\nCompleted:", datetime.now())
