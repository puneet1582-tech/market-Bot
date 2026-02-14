import time
import datetime
from step2_full_data_engine import start_step2_engine

def start_brain():
    print("Ultimate Brain Started")

    start_step2_engine()

    while True:
        print("Brain running:", datetime.datetime.now())
        time.sleep(60)
