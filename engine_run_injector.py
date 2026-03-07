import os

ROOT = "core"


def fix_file(path):

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    if "def run(" in code:
        return False

    with open(path, "a") as f:
        f.write("\n\n")
        f.write("def run():\n")
        f.write("    print('Engine started:', __name__)\n")

    return True


def main():

    fixed = 0

    for root, dirs, files in os.walk(ROOT):

        for f in files:

            if f.endswith(".py"):

                path = os.path.join(root, f)

                if fix_file(path):
                    print("Added run() to:", path)
                    fixed += 1

    print("\nTotal engines fixed:", fixed)


if __name__ == "__main__":
    main()
