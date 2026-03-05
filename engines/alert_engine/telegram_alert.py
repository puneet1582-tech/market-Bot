import requests
import json
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_alert(message):

    if not BOT_TOKEN or not CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass


def send_market_report(result):

    try:
        mode = result["MARKET_SUMMARY"]["mode"]
        top = result["TOP_20"][:10]
    except:
        return

    msg = "*Ultimate Brain Report*\n\n"
    msg += f"Market Mode: *{mode}*\n\n"
    msg += "Top Opportunities:\n"

    rank = 1
    for s in top:
        msg += f"{rank}. {s['symbol']} ({round(s['score'],3)})\n"
        rank += 1

    send_alert(msg)
