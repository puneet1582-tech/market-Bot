# ENGINE GUARD
# Automatically restarts engine if it stops

import subprocess
import time

def start_guard():
    while True:
        try:
            process = subprocess.Popen(["python", "main.py"])
            process.wait()
        except Exception as e:
            print("Engine crashed:", e)

        print("Restarting engine in 5 seconds...")
        time.sleep(5)
