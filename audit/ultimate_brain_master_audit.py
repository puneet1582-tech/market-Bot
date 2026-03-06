import os
import sys
import importlib
from pathlib import Path

ROOT = Path(".")

print("\n===============================")
print("ULTIMATE BRAIN MASTER AUDIT")
print("===============================\n")

health_score = 0
total_checks = 0


def ok(msg):
    global health_score, total_checks
    total_checks += 1
    health_score += 1
    print("[OK]", msg)


def fail(msg):
    global total_checks
    total_checks += 1
    print("[MISSING]", msg)


def check_folder(path):
    if Path(path).exists():
        ok(f"Folder -> {path}")
    else:
        fail(f"Folder -> {path}")


def check_file(path):
    if Path(path).exists():
        ok(f"File -> {path}")
    else:
        fail(f"File -> {path}")


print("\n--- STRUCTURE CHECK ---\n")

check_folder("engines")
check_folder("data")
check_folder("logs")
check_folder("audit")

check_file("run.py")
check_file("brain_control.py")

print("\n--- ENGINE DISCOVERY ---\n")

engine_count = 0

for root, dirs, files in os.walk("engines"):
    for f in files:
        if f.endswith(".py"):
            engine_count += 1
            ok(os.path.join(root, f))

print("\nTotal Engines Found:", engine_count)

print("\n--- MODULE IMPORT AUDIT ---\n")

for root, dirs, files in os.walk("engines"):
    for f in files:
        if f.endswith(".py") and f != "__init__.py":
            module = os.path.join(root, f)
            module = module.replace("/", ".").replace(".py", "")
            try:
                importlib.import_module(module)
                ok(f"Import -> {module}")
            except Exception as e:
                fail(f"Import Error -> {module} : {e}")

print("\n--- DATA LAYER CHECK ---\n")

check_folder("data/prices")
check_folder("data/fundamentals")
check_folder("data/ownership")
check_folder("data/news")

print("\n--- NSE/BSE UNIVERSE CHECK ---\n")

check_file("data/nse_symbols.csv")
check_file("data/bse_symbols.csv")

print("\n--- TELEGRAM SYSTEM CHECK ---\n")

telegram_files = [
    "engines/telegram_alert_engine.py",
    "engines/telegram_top20_delivery_engine.py",
]

for f in telegram_files:
    if Path(f).exists():
        ok(f)
    else:
        fail(f)

print("\n--- ORCHESTRATION CHECK ---\n")

check_file("engines/master_orchestration_engine.py")
check_file("engines/master_brain_controller_engine.py")
check_file("engines/intelligence_orchestrator_engine.py")

print("\n--- AUTONOMOUS RUNNER CHECK ---\n")

check_file("engines/autonomous_daily_runner.py")
check_file("engines/daily_intelligence_pipeline_scheduler.py")

print("\n--- GLOBAL NEWS ENGINE CHECK ---\n")

check_file("engines/global_news_engine.py")
check_folder("engines/news_engine")

print("\n--- FUNDAMENTAL ENGINE CHECK ---\n")

check_file("engines/fundamentals_10y_engine.py")
check_file("engines/quarterly_fundamental_comparison_engine.py")

print("\n--- INSTITUTIONAL OWNERSHIP CHECK ---\n")

check_file("engines/institutional_ownership_engine.py")
check_file("engines/fii_dii_engine.py")
check_file("engines/promoter_engine.py")

print("\n===============================")
print("FINAL SYSTEM STATUS")
print("===============================\n")

score = (health_score / total_checks) * 100 if total_checks else 0

print("Total Checks :", total_checks)
print("Passed :", health_score)
print("Health Score :", round(score, 2), "%")

if score > 90:
    print("\nSYSTEM STATUS : ARCHITECTURE READY")
elif score > 70:
    print("\nSYSTEM STATUS : PARTIALLY READY")
else:
    print("\nSYSTEM STATUS : CORE SYSTEM MISSING")

print("\n===============================\n")
