import os
import importlib
from pathlib import Path

print("\n===============================")
print("ULTIMATE BRAIN FULL SYSTEM AUDIT")
print("===============================\n")

health_score = 0
total_checks = 0


def check_folder(path):
    global health_score, total_checks
    total_checks += 1
    if Path(path).exists():
        print(f"[OK] Folder exists -> {path}")
        health_score += 1
    else:
        print(f"[MISSING] Folder -> {path}")


def check_file(path):
    global health_score, total_checks
    total_checks += 1
    if Path(path).exists():
        print(f"[OK] File exists -> {path}")
        health_score += 1
    else:
        print(f"[MISSING] File -> {path}")


print("\n--- CORE STRUCTURE CHECK ---\n")

check_folder("engines")
check_folder("data")
check_folder("logs")
check_folder("configs")

check_file("run.py")
check_file("brain_control.py")

print("\n--- ENGINE FILE CHECK ---\n")

if Path("engines").exists():
    for root, dirs, files in os.walk("engines"):
        for f in files:
            if f.endswith(".py"):
                total_checks += 1
                print(f"[ENGINE FOUND] {os.path.join(root, f)}")
                health_score += 1

print("\n--- DATA LAYER CHECK ---\n")

check_folder("data/prices")
check_folder("data/fundamentals")
check_folder("data/ownership")
check_folder("data/news")

print("\n--- NSE/BSE SYMBOL CHECK ---\n")

check_file("data/nse_symbols.csv")
check_file("data/bse_symbols.csv")

print("\n===============================")
print("FINAL SYSTEM HEALTH REPORT")
print("===============================\n")

if total_checks == 0:
    score = 0
else:
    score = (health_score / total_checks) * 100

print(f"Total Checks : {total_checks}")
print(f"Passed       : {health_score}")
print(f"Health Score : {round(score,2)} %")

if score > 90:
    print("\nSYSTEM STATUS : PRODUCTION READY")
elif score > 60:
    print("\nSYSTEM STATUS : PARTIALLY READY")
else:
    print("\nSYSTEM STATUS : CORE SYSTEM MISSING")

print("\n===============================\n")


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
