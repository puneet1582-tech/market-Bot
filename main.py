import os
import requests
import pandas as pd
from flask import Flask

app = Flask(__name__)

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

# ================= NSE DATA FETCH =================
def fetch_market_data():
    url = "https://www.nseindia.com/api/market-data-pre-open?key=NIFTY"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    data = r.json()

    stocks = []
    for item in data['data'][:5]:
        symbol = item['metadata']['symbol']
        price = item['metadata']['lastPrice']
        stocks.append(f"{symbol}: {price}")

    return "\n".join(stocks)

# ================= ALERT ENGINE =================
def run_market_alert():
    market_data = fetch_market_data()
    message = f"NSE Market Snapshot:\n{market_data}"
    send_telegram_message(message)

@app.route("/")
def home():
    return "Market Bot Running"

if __name__ == "__main__":
    mode = os.getenv("RUN_MODE", "ALERT")

    if mode == "SERVER":
        app.run(host="0.0.0.0", port=10000)
    else:
        run_market_alert()
