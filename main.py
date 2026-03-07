import time
import requests
from flask import Flask

app = Flask(__name__)

def fetch_stooq(symbol):
    try:
        url = f"https://stooq.com/q/l/?s={symbol}&f=sd2t2ohlcv&h&e=csv"
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            print("HTTP ERROR:", r.status_code)
            return None
        lines = r.text.split("\n")
        if len(lines) < 2:
            print("EMPTY CSV")
            return None
        parts = lines[1].split(",")
        if len(parts) < 7:
            print("INVALID CSV")
            return None
        return parts[6]  # close price
    except Exception as e:
        print("FETCH ERROR:", e)
        return None

def engine_loop():
    while True:
        print("===== ENGINE TICK =====")
        oil = fetch_stooq("cl.f")
        spx = fetch_stooq("^spx")
        reliance = fetch_stooq("reliance.ns")
        print("OIL:", oil)
        print("SPX:", spx)
        print("RELIANCE:", reliance)
        time.sleep(120)

@app.route("/")
def home():
    return "LEAN ENGINE RUNNING - STOOQ MODE"

# disabled_entry_point
    import threading
    t = threading.Thread(target=engine_loop)
    t.start()
    app.run(host="0.0.0.0", port=10000)


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print('Engine Error:', e)
