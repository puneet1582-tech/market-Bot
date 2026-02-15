from flask import Flask
import brain_engine
import threading
import time

app = Flask(__name__)

def run_engine():
    engine = brain_engine.BrainEngine()
    stocks = ["RELIANCE.NS","TCS.NS","HDFCBANK.NS"]

    while True:
        for s in stocks:
            result = engine.analyze_stock(s)
            print("INGESTION:", result, flush=True)
        time.sleep(300)

@app.route("/")
def home():
    return "Ultimate Brain Running"

if __name__ == "__main__":
    threading.Thread(target=run_engine).start()
    app.run(host="0.0.0.0", port=10000)
