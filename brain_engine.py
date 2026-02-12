import time
import datetime

def start_brain():
    print("Market Intelligence Brain Activated")
    while True:
        now = datetime.datetime.now()
        print("Brain Running:", now)
        time.sleep(60)

if __name__ == "__main__":
    start_brain()
