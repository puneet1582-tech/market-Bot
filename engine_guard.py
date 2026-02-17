# ENGINE GUARD WITH UNIVERSE SCHEDULER

import subprocess
import time
import threading
from universe_scheduler_engine import run_universe_scheduler

def start_guard():
    # ---- Start Universe Scheduler Thread ----
    scheduler_thread = threading.Thread(target=run_universe_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    # ---- Engine Restart Guard Loop ----
    while True:
        try:
            process = subprocess.Popen(["python", "main.py"])
            process.wait()
        except Exception as e:
            print("Engine crashed:", e)

        print("Restarting engine in 5 seconds...")
        time.sleep(5)
