from flask import Flask
from brain_engine import BrainEngine
import threading
import time

app = Flask(__name__)

def background_data_runner():
    engine = BrainEngine()

    stock_list = [
        "RELIANCE.NS",
        "TCS.NS",
        "HDFCBANK.NS"
    ]

    while True:
        print("Starting Data Ingestion Cycle...")
        for stock in stock_list:
            output = engine.analyze_stock(stock)
            print("Loaded:", output)

        print("Cycle Completed. Sleeping 6 hours...")
        time.sleep(21600)

@app.route("/")
def home():
    return "Ultimate Brain Running Successfully"

if __name__ == "__main__":
    thread = threading.Thread(target=background_data_runner)
    thread.start()
    print("Ultimate Brain Started")

    app.run(host="0.0.0.0", port=10000)
