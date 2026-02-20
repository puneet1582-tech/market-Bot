import os
import re
import glob

ALLOWED = {"run.py", "brain_control.py"}

pattern = re.compile(r'if\s*\(?\s*__name__\s*==\s*[\'"]__main__[\'"]\s*\)?\s*:')

for file in glob.glob("**/*.py", recursive=True):

    filename = os.path.basename(file)

    if "backup_before_entry_cleanup" in file:
        continue

    if filename in ALLOWED:
        continue

    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        if pattern.search(content):
            print("Hard disabling entry in:", file)

            new_content = pattern.sub(
                '# DISABLED ENTRY POINT',
                content
            )

            with open(file, "w", encoding="utf-8") as f:
                f.write(new_content)

    except Exception as e:
        print("Error:", file, e)

print("Hard cleanup completed.")
