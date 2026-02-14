# ============================================================
# ULTIMATE BRAIN MAIN ENGINE
# Step-2 Auto Integration Enabled
# ============================================================

import time
import datetime
from step2_full_data_engine import start_step2_engine


def start_brain():
    print("Ultimate Brain Started")

    # STEP-2 ENGINE AUTO START
    start_step2_engine()

    while True:
        print("Brain Running:", datetime.datetime.now())
        time.sleep(60)


if __name__ == "__main__":
    start_brain()
