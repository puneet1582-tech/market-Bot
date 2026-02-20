cat > master_system_audit.py
#!/usr/bin/env python3
import os
import sys
import importlib
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent

CRITICAL_FILES = [
    "main.py",
    "brain_engine.py",
    "step2_full_data_engine.py",
]

CRITICAL_DIRS = [
    "engines",
    "data",
    "logs",
    "config",
]

def header(title):
    print("\n" + "="*80)
    print(title)
    print("="*80)

def check_python_version():
    header("PYTHON ENVIRONMENT CHECK")
    print("Python Version:", sys.version)

def check_virtual_env():
    header("VIRTUAL ENV CHECK")
    print("Virtual Env Active:", hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

def check_files():
    header("CRITICAL FILE CHECK")
    for file in CRITICAL_FILES:
        path = PROJECT_ROOT / file
        print(f"{file:35} -> {'FOUND' if path.exists() else 'MISSING'}")

def check_directories():
    header("CRITICAL DIRECTORY CHECK")
    for d in CRITICAL_DIRS:
        path = PROJECT_ROOT / d
        print(f"{d:35} -> {'FOUND' if path.exists() else 'MISSING'}")

def scan_engines():
    header("ENGINE MODULE SCAN")
    engines_path = PROJECT_ROOT / "engines"
    count = 0
    if engines_path.exists():
        for file in engines_path.glob("*.py"):
            print("Engine:", file.name)
            count += 1
    print("Total Engines:", count)

def check_imports():
    header("IMPORT VALIDATION CHECK")
    failures = 0
    for file in PROJECT_ROOT.glob("*.py"):
        module_name = file.stem
        try:
            importlib.import_module(module_name)
        except Exception as e:
            print(f"IMPORT ERROR in {module_name}: {e}")
            failures += 1
    print("Total Import Failures:", failures)

def check_data_integrity():
    header("DATA DIRECTORY DEEP SCAN")
    data_path = PROJECT_ROOT / "data"
    total_files = 0
    total_size = 0
    if data_path.exists():
        for root, dirs, files in os.walk(data_path):
            for f in files:
                total_files += 1
                total_size += (Path(root) / f).stat().st_size
    print("Total Data Files:", total_files)
    print("Total Data Size (MB):", round(total_size / (1024*1024), 2))

def check_logs():
    header("LOG FILE CHECK")
    logs_path = PROJECT_ROOT / "logs"
    if logs_path.exists():
        files = list(logs_path.glob("*"))
        print("Log Files:", len(files))
    else:
        print("Logs Directory Missing")

def check_scheduler_presence():
    header("SCHEDULER DETECTION")
    detected = False
    for file in PROJECT_ROOT.glob("*.py"):
        content = file.read_text(errors="ignore").lower()
        if "schedule" in content or "cron" in content:
            detected = True
    print("Scheduler Detected:", detected)

def check_telegram_presence():
    header("TELEGRAM INTEGRATION DETECTION")
    detected = False
    for file in PROJECT_ROOT.glob("*.py"):
        content = file.read_text(errors="ignore").lower()
        if "telegram" in content or "bot_token" in content:
            detected = True
    print("Telegram Integration Detected:", detected)

def system_summary():
    header("SYSTEM SUMMARY")
    total_py = len(list(PROJECT_ROOT.glob("*.py")))
    total_dirs = len([d for d in PROJECT_ROOT.iterdir() if d.is_dir()])
    print("Total Python Files:", total_py)
    print("Total Directories:", total_dirs)
    print("Audit Timestamp:", datetime.now())

def main():
    header("ULTIMATE BRAIN - ULTRA DEEP SYSTEM AUDIT")
    check_python_version()
    check_virtual_env()
    check_files()
    check_directories()
    scan_engines()
    check_imports()
    check_data_integrity()
    check_logs()
    check_scheduler_presence()
    check_telegram_presence()
    system_summary()

# DISABLED ENTRY POINT
# if __name__ == "__main__":
    main()
