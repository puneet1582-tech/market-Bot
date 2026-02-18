import os
from datetime import datetime

print("\n==============================")
print(" ULTIMATE BRAIN SYSTEM AUDIT ")
print("==============================\n")

project_files_required = [
    "main.py",
    "brain_engine.py",
    "step2_full_data_engine.py",
    "telegram_alert_engine.py",
    "logging_engine.py",
    "requirements.txt"
]

completed = []
missing = []

print("Checking required core files...\n")

for file in project_files_required:
    if os.path.exists(file):
        print(f"[FOUND]   {file}")
        completed.append(file)
    else:
        print(f"[MISSING] {file}")
        missing.append(file)

print("\n------------------------------")
print("SYSTEM STATUS SUMMARY")
print("------------------------------")

print(f"Completed Files: {len(completed)}")
for c in completed:
    print(f"  - {c}")

print(f"\nMissing Files: {len(missing)}")
for m in missing:
    print(f"  - {m}")

print("\n------------------------------")
print("NEXT CORE BUILD STATUS")
print("------------------------------")

print("Pending Critical Modules:")
print(" - NSE/BSE Universe Auto Ingestion")
print(" - 10 Year Fundamentals Auto Loader")
print(" - Quarterly Comparison Engine")
print(" - Global News Impact Engine")
print(" - Live Top-20 Opportunity Detector")
print(" - Production Failure Recovery Engine")

print("\nAudit completed at:", datetime.now())
print("\n==============================\n")
