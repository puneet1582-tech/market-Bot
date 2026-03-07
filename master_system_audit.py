import os
import subprocess
import ast

ROOT = "."
errors = []
python_files = []


def collect_files():
    for root, dirs, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".py"):
                python_files.append(os.path.join(root, f))


def check_syntax(file):
    try:
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()
        ast.parse(source)
    except Exception as e:
        errors.append((file, str(e)))


def check_missing_main(file):
    with open(file, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    if "def run(" in code and "__main__" not in code:
        with open(file, "a", encoding="utf-8") as f:
            f.write("\n\nif __name__ == '__main__':\n")
            f.write("    run()\n")


def compile_project():
    subprocess.run(["python", "-m", "compileall", "."])


def main():

    print("Scanning project...")

    collect_files()

    for file in python_files:
        check_syntax(file)
        check_missing_main(file)

    if errors:
        print("\nSyntax Errors Found:\n")
        for e in errors:
            print(e[0], ":", e[1])
    else:
        print("\nNo syntax errors detected")

    print("\nRunning compile test...\n")

    compile_project()

    print("\nAudit complete")


if __name__ == "__main__":
    main()
