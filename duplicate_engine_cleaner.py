import os

REPORT = "duplicate_engine_report.txt"


def parse_report():

    duplicates = []

    with open(REPORT, "r") as f:
        lines = f.readlines()

    current = []

    for line in lines:

        if line.startswith("ENGINE:"):

            if current:
                duplicates.append(current)
                current = []

        elif line.strip().startswith("./"):

            current.append(line.strip())

    if current:
        duplicates.append(current)

    return duplicates


def delete_duplicates(groups):

    deleted = []

    for group in groups:

        # keep first file
        keep = group[0]

        for file in group[1:]:

            try:

                os.remove(file)

                deleted.append(file)

            except Exception as e:

                print("Error deleting:", file, e)

    return deleted


def main():

    print("Cleaning duplicate engines...\n")

    groups = parse_report()

    deleted = delete_duplicates(groups)

    print("\nDeleted files:")

    for f in deleted:
        print(f)

    print("\nCleanup complete.")


if __name__ == "__main__":
    main()
