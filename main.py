import os
import requests

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

def fetch_market_data():
    try:
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
    except Exception as e:
        return f"Data error: {e}"

def run_market_alert():
    market_data = fetch_market_data()
    message = f"NSE Snapshot:\n{market_data}"
    send_telegram_message(message)

if __name__ == "__main__":
    run_market_alert()
