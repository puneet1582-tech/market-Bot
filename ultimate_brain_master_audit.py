#!/usr/bin/env python3

import os
import re
from datetime import datetime

PROJECT_ROOT = os.getcwd()

def line():
    print("-" * 70)

def scan_python_files():
    py_files = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files

def find_main_blocks(py_files):
    results = {}
    for file in py_files:
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            if 'if __name__ == "__main__"' in content:
                results[file] = True
            else:
                results[file] = False
    return results

def analyze_imports(file_path):
    imports = []
    if not os.path.isfile(file_path):
        return imports
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.strip().startswith("import") or line.strip().startswith("from"):
                imports.append(line.strip())
    return imports

def main():
    print("\n===== ULTIMATE BRAIN DEEP EXECUTION AUDIT =====")
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Timestamp   : {datetime.now()}")
    line()

    py_files = scan_python_files()
    print(f"Total Python Files Found: {len(py_files)}")
    line()

    main_blocks = find_main_blocks(py_files)

    print("\nENTRY POINT ANALYSIS ( __main__ blocks )")
    line()
    entry_count = 0
    for file, has_main in main_blocks.items():
        if has_main:
            print(f"ENTRY POINT FOUND: {file}")
            entry_count += 1

    print(f"\nTotal Entry Points: {entry_count}")
    line()

    print("\nMAIN.PY IMPORT ANALYSIS")
    line()
    main_py_path = os.path.join(PROJECT_ROOT, "main.py")
    main_imports = analyze_imports(main_py_path)
    if main_imports:
        for imp in main_imports:
            print(imp)
    else:
        print("No imports found or main.py missing.")

    line()

    print("\nMASTER_BRAIN IMPORT ANALYSIS")
    line()
    master_path = os.path.join(PROJECT_ROOT, "master_brain.py")
    master_imports = analyze_imports(master_path)
    if master_imports:
        for imp in master_imports:
            print(imp)
    else:
        print("master_brain.py missing or no imports.")

    line()

    print("\nARCHITECTURE INTEGRITY SUMMARY")
    line()
    if entry_count == 1:
        print("Single Entry Point Detected → GOOD (Institutional Standard)")
    elif entry_count > 1:
        print("Multiple Entry Points Detected → ARCHITECTURE RISK")
    else:
        print("No Entry Point Found → CRITICAL ERROR")

    print("\n===== DEEP AUDIT COMPLETE =====\n")

# DISABLED ENTRY POINT
# # DISABLED ENTRY POINT
    main()
