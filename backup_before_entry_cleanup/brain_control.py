import os
import sys
import pandas as pd
import glob
from datetime import datetime

PROJECT_ROOT = os.getcwd()

PRICE_FILE = "data/nse_price_history_clean.csv"
SECTOR_FILE = "data/sector_final_authority.csv"

def section(title):
    print("\n" + "="*70)
    print(title)
    print("="*70)

def check_core_files():
    section("CORE FILE CHECK")
    required = [
        "main.py",
        "master_brain.py",
        "orchestrator.py",
        "run.py"
    ]
    score = 0
    for f in required:
        if os.path.exists(f):
            print(f"{f:30} : OK")
            score += 1
        else:
            print(f"{f:30} : MISSING")
    return score, len(required)

def check_entry_points():
    section("ENTRY POINT SCAN")
    entry_count = 0
    for file in glob.glob("**/*.py", recursive=True):
        try:
            with open(file, "r", encoding="utf-8") as f:
                if "__main__" in f.read():
                    print("ENTRY:", file)
                    entry_count += 1
        except:
            pass
    print("Total Entry Points:", entry_count)
    return entry_count

def validate_price_data():
    section("PRICE DATA VALIDATION")
    if not os.path.exists(PRICE_FILE):
        print("Clean price file missing.")
        return 0

    try:
        df = pd.read_csv(PRICE_FILE, nrows=5)
        required_cols = {"date","symbol","price"}
        if required_cols.issubset(df.columns):
            print("Schema OK")
            print("Columns:", list(df.columns))
            return 1
        else:
            print("Schema INVALID:", df.columns)
            return 0
    except Exception as e:
        print("Price file error:", e)
        return 0

def validate_sector_data():
    section("SECTOR DATA VALIDATION")
    if not os.path.exists(SECTOR_FILE):
        print("Sector file missing.")
        return 0
    try:
        df = pd.read_csv(SECTOR_FILE, nrows=5)
        if {"symbol","sector"}.issubset(df.columns):
            print("Sector schema OK")
            return 1
        else:
            print("Sector schema INVALID:", df.columns)
            return 0
    except Exception as e:
        print("Sector file error:", e)
        return 0

def detect_large_files():
    section("LARGE FILE RISK SCAN")
    risk = 0
    for root, dirs, files in os.walk("data"):
        for f in files:
            path = os.path.join(root, f)
            size_mb = os.path.getsize(path) / (1024*1024)
            if size_mb > 200:
                print(f"RISK: {f} is {size_mb:.2f} MB")
                risk += 1
    if risk == 0:
        print("No large file risk detected.")
    return risk

def health_summary(core_score, core_total, price_ok, sector_ok, entry_count):
    section("SYSTEM HEALTH SUMMARY")
    health = 0

    health += (core_score / core_total) * 30
    health += price_ok * 20
    health += sector_ok * 20

    if entry_count <= 5:
        health += 20
    else:
        health += 5

    print(f"Health Score: {health:.2f} / 100")

    if health > 80:
        print("STATUS: STABLE")
    elif health > 60:
        print("STATUS: MODERATE RISK")
    else:
        print("STATUS: HIGH RISK")

def run_full_check():
    print("\nULTIMATE BRAIN — CONTROL SYSTEM")
    print("Project Root:", PROJECT_ROOT)
    print("Timestamp:", datetime.now())

    core_score, core_total = check_core_files()
    entry_count = check_entry_points()
    price_ok = validate_price_data()
    sector_ok = validate_sector_data()
    detect_large_files()
    health_summary(core_score, core_total, price_ok, sector_ok, entry_count)

if __name__ == "__main__":
    if "--full-check" in sys.argv:
        run_full_check()
    else:
        print("Use: python brain_control.py --full-check")
