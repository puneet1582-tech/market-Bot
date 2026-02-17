import os
import requests
from dotenv import load_dotenv

# Load Telegram credentials from env file
load_dotenv("telegram_config.env")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_alert(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("Telegram credentials missing. Check telegram_config.env")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload)
    return response.json()


def test_alert():
    return send_telegram_alert("STEP-2 LIVE TEST: Telegram Alert Engine Working")
