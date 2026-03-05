import os
import requests
import logging
from datetime import datetime, timezone

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

logging.basicConfig(level=logging.INFO)

class TelegramAlertEngine:

    def __init__(self):
        if not BOT_TOKEN or not CHAT_ID:
            raise RuntimeError("Telegram credentials not set")

        self.url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    def send(self, text):

        payload = {
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        }

        r = requests.post(self.url, json=payload, timeout=10)

        if r.status_code != 200:
            raise RuntimeError(f"Telegram API error {r.text}")

    def send_market_report(self, result):

        mode = result.get("MARKET_SUMMARY", {}).get("mode", "UNKNOWN")
        top = result.get("TOP_20", [])[:10]

        msg = f"*Ultimate Brain Report*\n"
        msg += f"Time: {datetime.now(timezone.utc)}\n\n"
        msg += f"*Market Mode:* {mode}\n\n"
        msg += "*Top Opportunities*\n"

        for i,s in enumerate(top,1):
            msg += f"{i}. {s['symbol']}  ({round(s.get('score',0),3)})\n"

        self.send(msg)


def send_market_report(result):

    try:
        engine = TelegramAlertEngine()
        engine.send_market_report(result)
    except Exception as e:
        logging.error(f"Telegram error: {e}")
