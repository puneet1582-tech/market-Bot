cat > step2_full_data_engine.py << 'PY'
import yfinance as yf
from datetime import datetime

class FullDataEngine:
    def __init__(self):
        self.timestamp = datetime.now()

    def fetch_full_dataset(self, symbol):
        ticker = yf.Ticker(symbol)
        return {
            "symbol": symbol,
            "timestamp": str(self.timestamp),
            "price_data": ticker.history(period="1y")
        }
PY

cat > brain_engine.py << 'PY'
from step2_full_data_engine import FullDataEngine

class BrainEngine:
    def __init__(self):
        self.data_engine = FullDataEngine()

    def analyze_stock(self, symbol):
        data = self.data_engine.fetch_full_dataset(symbol)
        return {
            "symbol": data["symbol"],
            "records_price": len(data["price_data"]),
            "timestamp": data["timestamp"]
        }
PY

cat > main.py << 'PY'
from flask import Flask
import brain_engine
import threading
import time

app = Flask(__name__)

def run_engine():
    engine = brain_engine.BrainEngine()
    stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"]

    while True:
        for s in stocks:
            print(engine.analyze_stock(s))
        time.sleep(21600)

@app.route("/")
def home():
    return "Ultimate Brain Running"

if __name__ == "__main__":
    threading.Thread(target=run_engine).start()
    app.run(host="0.0.0.0", port=10000)
PY
