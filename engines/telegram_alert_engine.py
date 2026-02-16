import os
import requests

BOT_TOKEN = os.getenv("8441405404:AAEppNGjlfWjR4xzWNqfWpt8e53pnmQOZj8")
CHAT_ID = os.getenv("1428062136")

def send_telegram_alert(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram credentials not set")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        requests.post(url, data=payload, timeout=10)
        return True
    except Exception as e:
        print("Telegram error:", e)
        return False
