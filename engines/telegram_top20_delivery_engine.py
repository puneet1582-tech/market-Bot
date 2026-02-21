"""
Ultimate Brain — Telegram Top-20 Delivery Engine
Sends daily Top-20 institutional opportunities to Telegram.
"""

import os
import pandas as pd
from datetime import datetime
from telegram import Bot
from dotenv import load_dotenv

# Load environment
load_dotenv("telegram_config.env")

INPUT_FILE = "data/top20_institutional_opportunities.csv"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_top20():
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return {"status": "telegram_not_configured"}

    if not os.path.exists(INPUT_FILE):
        return {"status": "file_missing"}

    df = pd.read_csv(INPUT_FILE)
    if df.empty:
        return {"status": "no_data"}

    message = "📊 DAILY TOP-20 INSTITUTIONAL OPPORTUNITIES\n\n"

    for i, row in df.head(20).iterrows():
        symbol = row.get("symbol", "NA")
        score = row.get("institutional_score", "NA")
        message += f"{i+1}. {symbol} — Score: {score}\n"

    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

    return {
        "timestamp": str(datetime.utcnow()),
        "status": "sent"
    }
