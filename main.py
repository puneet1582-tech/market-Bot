import os
import requests
from flask import Flask

app = Flask(__name__)

BOT_TOKEN = "8441405404:AAEppNGjlfWjR4xzWNqfWpt8e53pnmQOZj8"
CHAT_ID = "1428062136"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

# ================= ALERT ENGINE =================
def run_market_alert():
    # यहां आपका original Ultimate Brain logic रहेगा
    send_telegram_message("Market Alert Bot Working")

# ================= WEB SERVER =================
@app.route("/")
def home():
    return "Market Bot Running"

# ================= MODE CONTROL =================
if __name__ == "__main__":
    mode = os.getenv("RUN_MODE", "ALERT")

    if mode == "SERVER":
        app.run(host="0.0.0.0", port=10000)
    else:
        run_market_alert()
