import time
from flask import Flask
import brain_engine
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "Ultimate Brain Live Engine Running"

def engine_runner():
    while True:
        print("ENGINE CYCLE START")
        try:
            brain_engine.run()
        except Exception as e:
            print("ENGINE ERROR:", e)
        print("ENGINE CYCLE END")
        time.sleep(60)  # 1 minute test interval

def start_engine():
    t = threading.Thread(target=engine_runner)
    t.daemon = False
    t.start()

if __name__ == "__main__":
    start_engine()
    app.run(host="0.0.0.0", port=10000)
