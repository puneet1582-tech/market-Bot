import os
import subprocess
import re

PROJECT_ROOT = "."
PY_EXT = ".py"


def get_python_files():
    files = []
    for root, dirs, filenames in os.walk(PROJECT_ROOT):
        for f in filenames:
            if f.endswith(PY_EXT):
                files.append(os.path.join(root, f))
    return files


def fix_common_issues(file_path):

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    original = lines[:]
    new_lines = []
    entry_point_found = False

    for line in lines:

        if "DISABLED ENTRY POINT" in line:
            continue

        if re.match(r"\s*run\(\)", line):
            continue

        line = line.replace("\t", "    ")

        new_lines.append(line)

        if "__name__" in line and "__main__" in line:
            entry_point_found = True

    if not entry_point_found:
        new_lines.append("\n")
        new_lines.append("if __name__ == '__main__':\n")
        new_lines.append("    try:\n")
        new_lines.append("        run()\n")
        new_lines.append("    except Exception as e:\n")
        new_lines.append("        print('Engine Error:', e)\n")

    if new_lines != original:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        return True

    return False


def run_python_compile_check():

    print("\nRunning syntax check...\n")

    result = subprocess.run(
        ["python", "-m", "compileall", "."],
        capture_output=True,
        text=True
    )

    print(result.stdout)
    print(result.stderr)


def main():

    files = get_python_files()

    print(f"Scanning {len(files)} python files...\n")

    fixed = 0

    for f in files:
        try:
            if fix_common_issues(f):
                print("Fixed:", f)
                fixed += 1
        except Exception as e:
            print("Error processing:", f, e)

    print("\nTotal files fixed:", fixed)

    run_python_compile_check()

    print("\nSystem bug scan completed.")


if __name__ == "__main__":
    main()
