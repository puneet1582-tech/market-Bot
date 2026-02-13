from engines.final_report_engine import FinalReportEngine
import time
import threading
import requests
from flask import Flask

# ================= TELEGRAM CONFIG =================
BOT_TOKEN = "8441405404:AAEz_wneK8H0I7QoVr4mXc62vR-NiNm_NVA"
CHAT_ID = "1428062136"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=payload)

# ================= WEB SERVER =================
app = Flask(__name__)

@app.route("/")
def home():
    return "Market Bot Running"

# ================= BOT ENGINE =================
def run_bot():
    while True:
        engine = FinalReportEngine()
        report = engine.generate_report("RELIANCE", "Energy")

        message = ""
        for k, v in report.items():
            message += f"{k} : {v}\n"

        send_telegram_message(message)

        print("REPORT SENT TO TELEGRAM")

        # run once every 24 hours
        time.sleep(86400)

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
