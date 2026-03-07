import os
import re

ROOT = "."

def fix_file(file_path):

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    fixed_lines = []
    i = 0

    while i < len(lines):

        line = lines[i]
        fixed_lines.append(line)

        if re.match(r"\s*if .*:\s*$", line):
            pass

            if i + 1 >= len(lines) or re.match(r"\s*$", lines[i+1]):
                pass

                indent = len(line) - len(line.lstrip()) + 4
                fixed_lines.append(" " * indent + "pass\n")

        i += 1

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(fixed_lines)


def main():

    print("Fixing indentation errors...\n")

    for root, dirs, files in os.walk(ROOT):

        for f in files:

            if f.endswith(".py"):
                pass

                path = os.path.join(root, f)

                try:
                    fix_file(path)
                    print("Checked:", path)
                except:
                    pass

    print("\nFix complete.")


if __name__ == "__main__":
    main()
