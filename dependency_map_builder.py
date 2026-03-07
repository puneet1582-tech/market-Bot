import os
import re

ROOT = "core"

imports = {}

for root, dirs, files in os.walk(ROOT):
    for f in files:
        if f.endswith(".py"):
            path = os.path.join(root, f)

            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()

            found = re.findall(r"from\s+([\w\.]+)\s+import\s+([\w]+)", content)

            imports[path] = found


for file, deps in imports.items():
    if deps:
        print("\n", file)
        for dep in deps:
            print("   ->", dep)
