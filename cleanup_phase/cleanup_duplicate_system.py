import os
import shutil
from pathlib import Path

ROOT=Path(".")

backup_dir="backup_before_entry_cleanup"

removed=[]
kept=[]

for root,dirs,files in os.walk(ROOT):

    if backup_dir in root:
        continue

    for f in files:

        path=os.path.join(root,f)

        backup_path=os.path.join(ROOT,backup_dir,f)

        if os.path.exists(backup_path):

            kept.append(path)

for root,dirs,files in os.walk(backup_dir):

    for f in files:

        path=os.path.join(root,f)

        try:
            os.remove(path)
            removed.append(path)
        except:
            pass

print("REMOVED BACKUP FILES:",len(removed))

print("PRIMARY FILES KEPT:",len(kept))



if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
