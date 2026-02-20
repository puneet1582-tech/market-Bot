import requests

BOT_TOKEN = "PASTE_TELEGRAM_TOKEN"
CHAT_ID = "PASTE_CHAT_ID"

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)
