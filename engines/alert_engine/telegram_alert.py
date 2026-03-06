import os
import requests
from datetime import datetime, timezone
from engines.sector_report_engine import sector_report

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_message(text):

    if not BOT_TOKEN or not CHAT_ID:
        return

    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload={
        "chat_id":CHAT_ID,
        "text":text,
        "parse_mode":"Markdown"
    }

    requests.post(url,json=payload,timeout=10)


def send_market_report(result):

    mode=result.get("MARKET_SUMMARY",{}).get("mode","UNKNOWN")
    top=result.get("TOP_20",[])[:10]

    msg="Ultimate Brain Report\n"
    msg+=f"Time: {datetime.now(timezone.utc)}\n\n"

    msg+=f"Market Mode: {mode}\n\n"

    msg+="Sector Strength\n"
    msg+=sector_report()
    msg+="\n\n"

    msg+="Top Opportunities\n"

    for i,s in enumerate(top,1):
        msg+=f"{i}. {s['symbol']}  ({round(s['score'],2)})\n"

    send_message(msg)
