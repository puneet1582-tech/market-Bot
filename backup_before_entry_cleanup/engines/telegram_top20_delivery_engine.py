"""
Ultimate Brain — Telegram Top-20 Delivery Engine
Sends daily Top-20 institutional opportunities to Telegram.
"""

import os
import pandas as pd
from datetime import datetime
from telegram import Bot

INPUT_FILE = "data/daily_top20_opportunities.csv"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_top20():
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return {"status": "telegram_not_configured"}

    df = pd.read_csv(INPUT_FILE)
    if df.empty:
        return {"status": "no_data"}

    message = "📊 DAILY TOP-20 INSTITUTIONAL OPPORTUNITIES\n\n"
    for i, row in df.head(20).iterrows():
        message += f"{i+1}. {row['symbol']} — Score: {row['institutional_score']}\n"

    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

    return {
        "timestamp": str(datetime.utcnow()),
        "status": "sent"
    }


# DISABLED ENTRY POINT
# if __name__ == "__main__":
    print(send_top20())
