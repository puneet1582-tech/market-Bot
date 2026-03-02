import requests
import time
from flask import Flask

app = Flask(__name__)

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_price(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
        r = requests.get(url, headers=HEADERS, timeout=10)
        data = r.json()
        result = data.get("quoteResponse", {}).get("result", [])
        if result:
            return result[0].get("regularMarketPrice")
        return None
    except Exception as e:
        print("PRICE ERROR:", e)
        return None

def engine_loop():
    while True:
        print("===== ENGINE TICK =====")
        oil = fetch_price("CL=F")
        spx = fetch_price("^GSPC")
        reliance = fetch_price("RELIANCE.NS")

        print("OIL:", oil)
        print("SPX:", spx)
        print("RELIANCE:", reliance)

        time.sleep(60)

@app.route("/")
def home():
    return "LEAN INTELLIGENCE ENGINE RUNNING"

if __name__ == "__main__":
    import threading
    t = threading.Thread(target=engine_loop)
    t.start()
    app.run(host="0.0.0.0", port=10000)
