import os
import subprocess
from datetime import datetime

print("\n==============================")
print(" ULTIMATE BRAIN MASTER STATUS ")
print("==============================\n")

required_files = [
    "main.py",
    "brain_engine.py",
    "step2_full_data_engine.py",
    "telegram_alert_engine.py",
    "logging_engine.py",
    "nse_universe_engine.py",
    "requirements.txt"
]

required_dirs = ["data", "logs", "output"]

print("FILE STATUS:\n")
for f in required_files:
    print(f"[FOUND]" if os.path.exists(f) else f"[MISSING] {f}")

print("\nDIRECTORY STATUS:\n")
for d in required_dirs:
    print(f"[OK]" if os.path.isdir(d) else f"[CREATE NEEDED] {d}")

print("\nGIT BRANCH:\n")
try:
    branch = subprocess.check_output(["git", "branch", "--show-current"]).decode().strip()
    print(branch)
except:
    print("Git branch not detected")

print("\nINGESTION OUTPUT CHECK:\n")
data_file = "data/nse_equity_universe.csv"
if os.path.exists(data_file):
    print("[OK] NSE universe data available")
else:
    print("[PENDING] NSE universe ingestion not executed")

print("\nPENDING CORE MODULES:")
print("- 10 Year Fundamentals Engine")
print("- Quarterly Comparison Engine")
print("- Global News Intelligence Engine")
print("- Top-20 Opportunity Detection Engine")
print("- Failure Recovery Engine")

print("\nAudit Time:", datetime.now())
print("\n==============================\n")
