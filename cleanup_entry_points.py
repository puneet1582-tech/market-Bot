import os
import glob

ALLOWED = {"run.py", "brain_control.py"}

for file in glob.glob("**/*.py", recursive=True):
    filename = os.path.basename(file)

    if filename in ALLOWED:
        continue

    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        if 'if __name__ == "__main__"' in content:
            print("Disabling entry in:", file)

            content = content.replace(
                '# DISABLED ENTRY POINT
# # DISABLED ENTRY POINT',
                '# DISABLED ENTRY POINT\n# # DISABLED ENTRY POINT
# # DISABLED ENTRY POINT'
            )

            with open(file, "w", encoding="utf-8") as f:
                f.write(content)

    except Exception as e:
        print("Error in:", file, e)

print("Entry cleanup complete.")
