import os
import re

CORE_DIR = "core"

print("ULTIMATE BRAIN CORE ENGINE AUDIT\n")

engines = []

for root, dirs, files in os.walk(CORE_DIR):
    for f in files:
        if f.endswith(".py"):
            path = os.path.join(root, f)
            engines.append(path)

for file in sorted(engines):

    with open(file, "r", encoding="utf-8", errors="ignore") as fh:
        content = fh.read()

    classes = re.findall(r'class\s+([A-Za-z0-9_]+)', content)
    run_fn = "def run(" in content
    main_block = "__main__" in content

    print("FILE:", file)
    print("  classes:", classes if classes else "None")
    print("  has_run_function:", run_fn)
    print("  has_main_block:", main_block)
    print("-" * 40)

print("\nAUDIT COMPLETE")
