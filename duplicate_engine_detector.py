import os
from collections import defaultdict

ROOT = "."
REPORT = "duplicate_engine_report.txt"


def collect_python_files():

    files = []

    for root, dirs, filenames in os.walk(ROOT):
        for f in filenames:
            if f.endswith(".py"):
                files.append(os.path.join(root, f))

    return files


def extract_engine_name(path):

    name = os.path.basename(path)

    name = name.replace(".py", "")

    return name


def detect_duplicates(files):

    engine_map = defaultdict(list)

    for f in files:

        engine = extract_engine_name(f)

        engine_map[engine].append(f)

    duplicates = {k: v for k, v in engine_map.items() if len(v) > 1}

    return duplicates


def save_report(duplicates):

    with open(REPORT, "w") as f:

        if not duplicates:
            f.write("No duplicate engines found\n")
            return

        for engine, paths in duplicates.items():

            f.write(f"\nENGINE: {engine}\n")

            for p in paths:
                f.write(f"  {p}\n")


def main():

    print("Scanning project for duplicate engines...\n")

    files = collect_python_files()

    duplicates = detect_duplicates(files)

    save_report(duplicates)

    print("Duplicate scan complete.")

    print("Report saved:", REPORT)


if __name__ == "__main__":
    main()
