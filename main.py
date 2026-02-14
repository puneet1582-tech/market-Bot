from engines.final_report_engine import FinalReportEngine
import threading
import requests
import time
from flask import Flask

# ================= TELEGRAM CONFIG =================
BOT_TOKEN = "8441405404:AAEppNGjlfWjR4xzWNqfWpt8e53pnmQOZj8"
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
    return "Market Intelligence Bot Running"

# ================= OPPORTUNITY DETECTION =================
def check_opportunity(report):
    """
    USER LOGIC PLACEHOLDER:
    यहाँ तुम define करोगे कि कब पैसा कमाने का मौका है.
    Example:
    return report["signal"] == "BUY"
    """
    return False   # अभी default False

# ================= BOT ENGINE =================
def run_bot():
    while True:
        try:
            engine = FinalReportEngine()
            report = engine.generate_report("RELIANCE", "Energy")

            if check_opportunity(report):
                message = "MARKET OPPORTUNITY ALERT\n\n"
                for k, v in report.items():
                    message += f"{k} : {v}\n"

                send_telegram_message(message)
                print("ALERT SENT")

        except Exception as e:
            print("Error:", e)

        # fast continuous monitoring (every 20 seconds)
        time.sleep(20)

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
