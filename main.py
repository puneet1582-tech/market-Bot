from engines.final_report_engine import FinalReportEngine
import time
import threading
import requests
from flask import Flask

BOT_TOKEN = "8441405404:AAEppNGjlfWjR4xzWNqfWpt8e53pnmQOZj8"
CHAT_ID = "1428062136"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=payload)

app = Flask(__name__)

@app.route("/")
def home():
    return "Market Bot Running"

def run_bot():
    while True:
        engine = FinalReportEngine()
        report = engine.generate_report("RELIANCE", "Energy")

        message = ""
        for k, v in report.items():
            message += f"{k} : {v}\n"

        send_telegram_message(message)
        print("REPORT SENT TO TELEGRAM")

        time.sleep(86400)

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
