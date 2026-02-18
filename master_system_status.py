import os

files = [
    "main.py",
    "brain_engine.py",
    "step2_full_data_engine.py",
    "logging_engine.py",
    "telegram_alert_engine.py",
    "requirements.txt"
]

print("\nSYSTEM STATUS\n")

for f in files:
    print(f"[FOUND] {f}" if os.path.exists(f) else f"[MISSING] {f}")

dirs = ["data", "logs", "output"]
for d in dirs:
    print(f"[DIR OK] {d}" if os.path.isdir(d) else f"[DIR MISSING] {d}")
